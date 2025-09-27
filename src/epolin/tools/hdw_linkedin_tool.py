"""Tools dedicated to the HDW MCP LinkedIn scraping service."""

from __future__ import annotations

import json
import os
import shlex
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Iterable

import anyio
from crewai.tools import BaseTool
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import CallToolResult
from pydantic import BaseModel, Field, HttpUrl


class HdwLinkedinToolInput(BaseModel):
    """Input schema for the HDW LinkedIn scraping tool."""

    profile_url: HttpUrl = Field(
        ..., description="URL du profil LinkedIn à scraper via le service MCP HDW."
    )


@dataclass(slots=True)
class _TransportConfig:
    """Configuration interne décrivant comment contacter le serveur MCP."""

    mode: str
    server_url: str | None
    headers: Dict[str, str]
    timeout: float
    read_timeout: float | None
    command: str | None
    command_args: list[str]
    command_env: Dict[str, str] | None


class HdwLinkedinTool(BaseTool):
    """Tool calling the HDW MCP server to retrieve LinkedIn public data."""

    name: str = "hdw_linkedin_scraper"
    description: str = (
        "Interroge le service MCP HDW pour extraire les données publiques d'un profil "
        "LinkedIn. Fournir une URL complète de profil."
    )
    args_schema = HdwLinkedinToolInput

    def __init__(
        self,
        *,
        server_url: str | None = None,
        transport: str | None = None,
        tool_name: str | None = None,
        api_key: str | None = None,
        headers: Dict[str, str] | None = None,
        command: str | None = None,
        command_args: Iterable[str] | None = None,
        command_env: Dict[str, str] | None = None,
        timeout: float = 120.0,
        read_timeout: float | None = None,
    ) -> None:
        super().__init__()
        self._tool_name = tool_name or os.getenv(
            "MCP_HDW_TOOL_NAME", "scrape_linkedin_profile"
        )
        self._transport = self._build_transport_config(
            server_url=server_url,
            transport=transport,
            api_key=api_key,
            headers=headers,
            command=command,
            command_args=command_args,
            command_env=command_env,
            timeout=timeout,
            read_timeout=read_timeout,
        )

    def _build_transport_config(
        self,
        *,
        server_url: str | None,
        transport: str | None,
        api_key: str | None,
        headers: Dict[str, str] | None,
        command: str | None,
        command_args: Iterable[str] | None,
        command_env: Dict[str, str] | None,
        timeout: float,
        read_timeout: float | None,
    ) -> _TransportConfig:
        """Prepare transport related information by merging defaults with overrides."""

        resolved_transport = (transport or os.getenv("MCP_HDW_TRANSPORT", "http")).lower()
        resolved_headers: Dict[str, str] = dict(headers or {})

        if api_key is None:
            api_key = os.getenv("MCP_HDW_API_KEY")
        if api_key:
            resolved_headers.setdefault("Authorization", f"Bearer {api_key}")

        resolved_server_url = server_url or os.getenv("MCP_HDW_SERVER_URL")

        if command is None:
            command = os.getenv("MCP_HDW_COMMAND")
        if command_args is None:
            raw_args = os.getenv("MCP_HDW_COMMAND_ARGS")
            command_args = shlex.split(raw_args) if raw_args else []
        else:
            command_args = list(command_args)

        if command_env is None:
            env_json = os.getenv("MCP_HDW_COMMAND_ENV")
            if env_json:
                try:
                    command_env = json.loads(env_json)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        "MCP_HDW_COMMAND_ENV doit contenir un dictionnaire JSON valide."
                    ) from exc
        if read_timeout is None:
            read_timeout_env = os.getenv("MCP_HDW_READ_TIMEOUT")
            if read_timeout_env:
                try:
                    read_timeout = float(read_timeout_env)
                except ValueError as exc:
                    raise ValueError(
                        "MCP_HDW_READ_TIMEOUT doit être un nombre flottant."
                    ) from exc

        timeout_env = os.getenv("MCP_HDW_TIMEOUT")
        if timeout_env:
            try:
                timeout = float(timeout_env)
            except ValueError as exc:
                raise ValueError("MCP_HDW_TIMEOUT doit être un nombre flottant.") from exc

        return _TransportConfig(
            mode=resolved_transport,
            server_url=resolved_server_url,
            headers=resolved_headers,
            timeout=timeout,
            read_timeout=read_timeout,
            command=command,
            command_args=command_args,
            command_env=command_env,
        )

    def _run(self, profile_url: str) -> str:
        return anyio.run(self._call_async, str(profile_url))

    async def _arun(self, profile_url: str) -> str:
        return await self._call_async(str(profile_url))

    async def _call_async(self, profile_url: str) -> str:
        result = await self._call_hdw(profile_url)
        return self._format_result(result)

    async def _call_hdw(self, profile_url: str) -> CallToolResult:
        payload = {"profile_url": profile_url}
        read_timeout = (
            timedelta(seconds=self._transport.read_timeout)
            if self._transport.read_timeout is not None
            else None
        )

        if self._transport.mode == "http":
            if not self._transport.server_url:
                raise RuntimeError(
                    "Aucune URL MCP HDW n'est configurée (MCP_HDW_SERVER_URL manquant)."
                )
            async with streamablehttp_client(
                self._transport.server_url,
                headers=self._transport.headers,
                timeout=self._transport.timeout,
            ) as (read_stream, write_stream, _):
                async with ClientSession(
                    read_stream,
                    write_stream,
                    read_timeout_seconds=read_timeout,
                ) as session:
                    await session.initialize()
                    return await session.call_tool(self._tool_name, payload)

        if self._transport.mode == "stdio":
            if not self._transport.command:
                raise RuntimeError(
                    "Aucune commande MCP HDW n'est configurée (MCP_HDW_COMMAND manquant)."
                )
            server = StdioServerParameters(
                command=self._transport.command,
                args=list(self._transport.command_args),
                env=self._transport.command_env,
            )
            async with stdio_client(server) as (read_stream, write_stream):
                async with ClientSession(
                    read_stream,
                    write_stream,
                    read_timeout_seconds=read_timeout,
                ) as session:
                    await session.initialize()
                    return await session.call_tool(self._tool_name, payload)

        raise RuntimeError(
            "Mode de transport MCP HDW inconnu. Utiliser 'http' ou 'stdio'."
        )

    def _format_result(self, result: CallToolResult) -> str:
        if result.isError:
            raise RuntimeError(f"Erreur renvoyée par HDW: {result.model_dump()}")

        fragments: list[str] = []
        for block in result.content:
            data = block.model_dump()
            block_type = data.get("type")
            if block_type == "text" and "text" in data:
                fragments.append(data["text"])
            elif block_type == "resource" and "resource" in data:
                fragments.append(json.dumps(data["resource"], ensure_ascii=False))
            else:
                fragments.append(json.dumps(data, ensure_ascii=False))

        if result.structuredContent:
            fragments.append(json.dumps(result.structuredContent, ensure_ascii=False))

        output = "\n".join(part for part in fragments if part).strip()
        return output or json.dumps(result.model_dump(), ensure_ascii=False)
