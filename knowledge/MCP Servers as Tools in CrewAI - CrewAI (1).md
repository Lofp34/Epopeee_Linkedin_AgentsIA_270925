## Overview

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) provides a standardized way for AI agents to provide context to LLMs by communicating with external services, known as MCP Servers. The `crewai-tools` library extends CrewAI’s capabilities by allowing you to seamlessly integrate tools from these MCP servers into your agents. This gives your crews access to a vast ecosystem of functionalities. We currently support the following transport mechanisms:

-   **Stdio**: for local servers (communication via standard input/output between processes on the same machine)
-   **Server-Sent Events (SSE)**: for remote servers (unidirectional, real-time data streaming from server to client over HTTP)
-   **Streamable HTTP**: for remote servers (flexible, potentially bi-directional communication over HTTP, often utilizing SSE for server-to-client streams)

## Video Tutorial

Watch this video tutorial for a comprehensive guide on MCP integration with CrewAI:

<iframe width="100%" height="400" src="https://www.youtube.com/embed/TpQ45lAZh48" title="CrewAI MCP Integration Guide" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" data-dashlane-frameid="3660"></iframe>

## Installation

Before you start using MCP with `crewai-tools`, you need to install the `mcp` extra `crewai-tools` dependency with the following command:

```
<span><span>uv</span><span> pip</span><span> install</span><span> 'crewai-tools[mcp]'</span></span>
```

## Key Concepts & Getting Started

The `MCPServerAdapter` class from `crewai-tools` is the primary way to connect to an MCP server and make its tools available to your CrewAI agents. It supports different transport mechanisms and simplifies connection management. Using a Python context manager (`with` statement) is the **recommended approach** for `MCPServerAdapter`. It automatically handles starting and stopping the connection to the MCP server.

## Connection Configuration

The `MCPServerAdapter` supports several configuration options to customize the connection behavior:

-   **`connect_timeout`** (optional): Maximum time in seconds to wait for establishing a connection to the MCP server. Defaults to 30 seconds if not specified. This is particularly useful for remote servers that may have variable response times.

```
<span><span># Example with custom connection timeout</span></span>
<span><span>with</span><span> MCPServerAdapter(server_params, </span><span>connect_timeout</span><span>=</span><span>60</span><span>) </span><span>as</span><span> tools:</span></span>
<span><span>    # Connection will timeout after 60 seconds if not established</span></span>
<span><span>    pass</span></span>
```

```
<span><span>from</span><span> crewai </span><span>import</span><span> Agent</span></span>
<span><span>from</span><span> crewai_tools </span><span>import</span><span> MCPServerAdapter</span></span>
<span><span>from</span><span> mcp </span><span>import</span><span> StdioServerParameters </span><span># For Stdio Server</span></span>
<span></span>
<span><span># Example server_params (choose one based on your server type):</span></span>
<span><span># 1. Stdio Server:</span></span>
<span><span>server_params</span><span>=</span><span>StdioServerParameters(</span></span>
<span><span>    command</span><span>=</span><span>"python3"</span><span>,</span></span>
<span><span>    args</span><span>=</span><span>[</span><span>"servers/your_server.py"</span><span>],</span></span>
<span><span>    env</span><span>=</span><span>{</span><span>"UV_PYTHON"</span><span>: </span><span>"3.12"</span><span>, </span><span>**</span><span>os.environ},</span></span>
<span><span>)</span></span>
<span></span>
<span><span># 2. SSE Server:</span></span>
<span><span>server_params </span><span>=</span><span> {</span></span>
<span><span>    "url"</span><span>: </span><span>"http://localhost:8000/sse"</span><span>,</span></span>
<span><span>    "transport"</span><span>: </span><span>"sse"</span></span>
<span><span>}</span></span>
<span></span>
<span><span># 3. Streamable HTTP Server:</span></span>
<span><span>server_params </span><span>=</span><span> {</span></span>
<span><span>    "url"</span><span>: </span><span>"http://localhost:8001/mcp"</span><span>,</span></span>
<span><span>    "transport"</span><span>: </span><span>"streamable-http"</span></span>
<span><span>}</span></span>
<span></span>
<span><span># Example usage (uncomment and adapt once server_params is set):</span></span>
<span><span>with</span><span> MCPServerAdapter(server_params, </span><span>connect_timeout</span><span>=</span><span>60</span><span>) </span><span>as</span><span> mcp_tools:</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[tool.name </span><span>for</span><span> tool </span><span>in</span><span> mcp_tools]</span><span>}</span><span>"</span><span>)</span></span>
<span></span>
<span><span>    my_agent </span><span>=</span><span> Agent(</span></span>
<span><span>        role</span><span>=</span><span>"MCP Tool User"</span><span>,</span></span>
<span><span>        goal</span><span>=</span><span>"Utilize tools from an MCP server."</span><span>,</span></span>
<span><span>        backstory</span><span>=</span><span>"I can connect to MCP servers and use their tools."</span><span>,</span></span>
<span><span>        tools</span><span>=</span><span>mcp_tools, </span><span># Pass the loaded tools to your agent</span></span>
<span><span>        reasoning</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        verbose</span><span>=</span><span>True</span></span>
<span><span>    )</span></span>
<span><span>    # ... rest of your crew setup ...</span></span>
```

This general pattern shows how to integrate tools. For specific examples tailored to each transport, refer to the detailed guides below.

There are two ways to filter tools:

1.  Accessing a specific tool using dictionary-style indexing.
2.  Pass a list of tool names to the `MCPServerAdapter` constructor.

### Accessing a specific tool using dictionary-style indexing.

```
<span><span>with</span><span> MCPServerAdapter(server_params, </span><span>connect_timeout</span><span>=</span><span>60</span><span>) </span><span>as</span><span> mcp_tools:</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[tool.name </span><span>for</span><span> tool </span><span>in</span><span> mcp_tools]</span><span>}</span><span>"</span><span>)</span></span>
<span></span>
<span><span>    my_agent </span><span>=</span><span> Agent(</span></span>
<span><span>        role</span><span>=</span><span>"MCP Tool User"</span><span>,</span></span>
<span><span>        goal</span><span>=</span><span>"Utilize tools from an MCP server."</span><span>,</span></span>
<span><span>        backstory</span><span>=</span><span>"I can connect to MCP servers and use their tools."</span><span>,</span></span>
<span><span>        tools</span><span>=</span><span>[mcp_tools[</span><span>"tool_name"</span><span>]], </span><span># Pass the loaded tools to your agent</span></span>
<span><span>        reasoning</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        verbose</span><span>=</span><span>True</span></span>
<span><span>    )</span></span>
<span><span>    # ... rest of your crew setup ...</span></span>
```

### Pass a list of tool names to the `MCPServerAdapter` constructor.

```
<span><span>with</span><span> MCPServerAdapter(server_params, </span><span>"tool_name"</span><span>, </span><span>connect_timeout</span><span>=</span><span>60</span><span>) </span><span>as</span><span> mcp_tools:</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[tool.name </span><span>for</span><span> tool </span><span>in</span><span> mcp_tools]</span><span>}</span><span>"</span><span>)</span></span>
<span></span>
<span><span>    my_agent </span><span>=</span><span> Agent(</span></span>
<span><span>        role</span><span>=</span><span>"MCP Tool User"</span><span>,</span></span>
<span><span>        goal</span><span>=</span><span>"Utilize tools from an MCP server."</span><span>,</span></span>
<span><span>        backstory</span><span>=</span><span>"I can connect to MCP servers and use their tools."</span><span>,</span></span>
<span><span>        tools</span><span>=</span><span>mcp_tools, </span><span># Pass the loaded tools to your agent</span></span>
<span><span>        reasoning</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        verbose</span><span>=</span><span>True</span></span>
<span><span>    )</span></span>
<span><span>    # ... rest of your crew setup ...</span></span>
```

## Using with CrewBase

To use MCPServer tools within a CrewBase class, use the `get_mcp_tools` method. Server configurations should be provided via the `mcp_server_params` attribute. You can pass either a single configuration or a list of multiple server configurations.

```
<span><span>@CrewBase</span></span>
<span><span>class</span><span> CrewWithMCP</span><span>:</span></span>
<span><span>  # ... define your agents and tasks config file ...</span></span>
<span></span>
<span><span>  mcp_server_params </span><span>=</span><span> [</span></span>
<span><span>    # Streamable HTTP Server</span></span>
<span><span>    {</span></span>
<span><span>        "url"</span><span>: </span><span>"http://localhost:8001/mcp"</span><span>,</span></span>
<span><span>        "transport"</span><span>: </span><span>"streamable-http"</span></span>
<span><span>    },</span></span>
<span><span>    # SSE Server</span></span>
<span><span>    {</span></span>
<span><span>        "url"</span><span>: </span><span>"http://localhost:8000/sse"</span><span>,</span></span>
<span><span>        "transport"</span><span>: </span><span>"sse"</span></span>
<span><span>    },</span></span>
<span><span>    # StdIO Server</span></span>
<span><span>    StdioServerParameters(</span></span>
<span><span>        command</span><span>=</span><span>"python3"</span><span>,</span></span>
<span><span>        args</span><span>=</span><span>[</span><span>"servers/your_stdio_server.py"</span><span>],</span></span>
<span><span>        env</span><span>=</span><span>{</span><span>"UV_PYTHON"</span><span>: </span><span>"3.12"</span><span>, </span><span>**</span><span>os.environ},</span></span>
<span><span>    )</span></span>
<span><span>  ]</span></span>
<span></span>
<span><span>  @agent</span></span>
<span><span>  def</span><span> your_agent</span><span>(</span><span>self</span><span>):</span></span>
<span><span>      return</span><span> Agent(</span><span>config</span><span>=</span><span>self</span><span>.agents_config[</span><span>"your_agent"</span><span>], </span><span>tools</span><span>=</span><span>self</span><span>.get_mcp_tools()) </span><span># get all available tools</span></span>
<span></span>
<span><span>    # ... rest of your crew setup ...</span></span>
```

### Connection Timeout Configuration

You can configure the connection timeout for MCP servers by setting the `mcp_connect_timeout` class attribute. If no timeout is specified, it defaults to 30 seconds.

```
<span><span>@CrewBase</span></span>
<span><span>class</span><span> CrewWithMCP</span><span>:</span></span>
<span><span>  mcp_server_params </span><span>=</span><span> [</span><span>...</span><span>]</span></span>
<span><span>  mcp_connect_timeout </span><span>=</span><span> 60</span><span>  # 60 seconds timeout for all MCP connections</span></span>
<span></span>
<span><span>  @agent</span></span>
<span><span>  def</span><span> your_agent</span><span>(</span><span>self</span><span>):</span></span>
<span><span>      return</span><span> Agent(</span><span>config</span><span>=</span><span>self</span><span>.agents_config[</span><span>"your_agent"</span><span>], </span><span>tools</span><span>=</span><span>self</span><span>.get_mcp_tools())</span></span>
```

```
<span><span>@CrewBase</span></span>
<span><span>class</span><span> CrewWithDefaultTimeout</span><span>:</span></span>
<span><span>  mcp_server_params </span><span>=</span><span> [</span><span>...</span><span>]</span></span>
<span><span>  # No mcp_connect_timeout specified - uses default 30 seconds</span></span>
<span></span>
<span><span>  @agent</span></span>
<span><span>  def</span><span> your_agent</span><span>(</span><span>self</span><span>):</span></span>
<span><span>      return</span><span> Agent(</span><span>config</span><span>=</span><span>self</span><span>.agents_config[</span><span>"your_agent"</span><span>], </span><span>tools</span><span>=</span><span>self</span><span>.get_mcp_tools())</span></span>
```

### Filtering Tools

You can filter which tools are available to your agent by passing a list of tool names to the `get_mcp_tools` method.

```
<span><span>@agent</span></span>
<span><span>def</span><span> another_agent</span><span>(</span><span>self</span><span>):</span></span>
<span><span>    return</span><span> Agent(</span></span>
<span><span>      config</span><span>=</span><span>self</span><span>.agents_config[</span><span>"your_agent"</span><span>],</span></span>
<span><span>      tools</span><span>=</span><span>self</span><span>.get_mcp_tools(</span><span>"tool_1"</span><span>, </span><span>"tool_2"</span><span>) </span><span># get specific tools</span></span>
<span><span>    )</span></span>
```

The timeout configuration applies to all MCP tool calls within the crew:

```
<span><span>@CrewBase</span></span>
<span><span>class</span><span> CrewWithCustomTimeout</span><span>:</span></span>
<span><span>  mcp_server_params </span><span>=</span><span> [</span><span>...</span><span>]</span></span>
<span><span>  mcp_connect_timeout </span><span>=</span><span> 90</span><span>  # 90 seconds timeout for all MCP connections</span></span>
<span></span>
<span><span>  @agent</span></span>
<span><span>  def</span><span> filtered_agent</span><span>(</span><span>self</span><span>):</span></span>
<span><span>      return</span><span> Agent(</span></span>
<span><span>        config</span><span>=</span><span>self</span><span>.agents_config[</span><span>"your_agent"</span><span>],</span></span>
<span><span>        tools</span><span>=</span><span>self</span><span>.get_mcp_tools(</span><span>"tool_1"</span><span>, </span><span>"tool_2"</span><span>) </span><span># specific tools with custom timeout</span></span>
<span><span>      )</span></span>
```

## Explore MCP Integrations

Checkout this repository for full demos and examples of MCP integration with CrewAI! 👇

[

## GitHub Repository

CrewAI MCP Demo



](https://github.com/tonykipkemboi/crewai-mcp-demo)

## Staying Safe with MCP

#### Security Warning: DNS Rebinding Attacks

SSE transports can be vulnerable to DNS rebinding attacks if not properly secured. To prevent this:

1.  **Always validate Origin headers** on incoming SSE connections to ensure they come from expected sources
2.  **Avoid binding servers to all network interfaces** (0.0.0.0) when running locally - bind only to localhost (127.0.0.1) instead
3.  **Implement proper authentication** for all SSE connections

Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites. For more details, see the [Anthropic’s MCP Transport Security docs](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

### Limitations

-   **Supported Primitives**: Currently, `MCPServerAdapter` primarily supports adapting MCP `tools`. Other MCP primitives like `prompts` or `resources` are not directly integrated as CrewAI components through this adapter at this time.
-   **Output Handling**: The adapter typically processes the primary text output from an MCP tool (e.g., `.content[0].text`). Complex or multi-modal outputs might require custom handling if not fitting this pattern.