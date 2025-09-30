## Overview

The Stdio (Standard Input/Output) transport is designed for connecting `MCPServerAdapter` to local MCP servers that communicate over their standard input and output streams. This is typically used when the MCP server is a script or executable running on the same machine as your CrewAI application.

## Key Concepts

-   **Local Execution**: Stdio transport manages a locally running process for the MCP server.
-   **`StdioServerParameters`**: This class from the `mcp` library is used to configure the command, arguments, and environment variables for launching the Stdio server.

## Connecting via Stdio

You can connect to an Stdio-based MCP server using two main approaches for managing the connection lifecycle:

### 1\. Fully Managed Connection (Recommended)

Using a Python context manager (`with` statement) is the recommended approach. It automatically handles starting the MCP server process and stopping it when the context is exited.

```
<span><span>from</span><span> crewai </span><span>import</span><span> Agent, Task, Crew, Process</span></span>
<span><span>from</span><span> crewai_tools </span><span>import</span><span> MCPServerAdapter</span></span>
<span><span>from</span><span> mcp </span><span>import</span><span> StdioServerParameters</span></span>
<span><span>import</span><span> os</span></span>
<span></span>
<span><span># Create a StdioServerParameters object</span></span>
<span><span>server_params</span><span>=</span><span>StdioServerParameters(</span></span>
<span><span>    command</span><span>=</span><span>"python3"</span><span>, </span></span>
<span><span>    args</span><span>=</span><span>[</span><span>"servers/your_stdio_server.py"</span><span>],</span></span>
<span><span>    env</span><span>=</span><span>{</span><span>"UV_PYTHON"</span><span>: </span><span>"3.12"</span><span>, </span><span>**</span><span>os.environ},</span></span>
<span><span>)</span></span>
<span></span>
<span><span>with</span><span> MCPServerAdapter(server_params) </span><span>as</span><span> tools:</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"Available tools from Stdio MCP server: </span><span>{</span><span>[tool.name </span><span>for</span><span> tool </span><span>in</span><span> tools]</span><span>}</span><span>"</span><span>)</span></span>
<span></span>
<span><span>    # Example: Using the tools from the Stdio MCP server in a CrewAI Agent</span></span>
<span><span>    research_agent </span><span>=</span><span> Agent(</span></span>
<span><span>        role</span><span>=</span><span>"Local Data Processor"</span><span>,</span></span>
<span><span>        goal</span><span>=</span><span>"Process data using a local Stdio-based tool."</span><span>,</span></span>
<span><span>        backstory</span><span>=</span><span>"An AI that leverages local scripts via MCP for specialized tasks."</span><span>,</span></span>
<span><span>        tools</span><span>=</span><span>tools,</span></span>
<span><span>        reasoning</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        verbose</span><span>=</span><span>True</span><span>,</span></span>
<span><span>    )</span></span>
<span><span>    </span></span>
<span><span>    processing_task </span><span>=</span><span> Task(</span></span>
<span><span>        description</span><span>=</span><span>"Process the input data file 'data.txt' and summarize its contents."</span><span>,</span></span>
<span><span>        expected_output</span><span>=</span><span>"A summary of the processed data."</span><span>,</span></span>
<span><span>        agent</span><span>=</span><span>research_agent,</span></span>
<span><span>        markdown</span><span>=</span><span>True</span></span>
<span><span>    )</span></span>
<span><span>    </span></span>
<span><span>    data_crew </span><span>=</span><span> Crew(</span></span>
<span><span>        agents</span><span>=</span><span>[research_agent],</span></span>
<span><span>        tasks</span><span>=</span><span>[processing_task],</span></span>
<span><span>        verbose</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        process</span><span>=</span><span>Process.sequential </span></span>
<span><span>    )</span></span>
<span><span>   </span></span>
<span><span>    result </span><span>=</span><span> data_crew.kickoff()</span></span>
<span><span>    print</span><span>(</span><span>"</span><span>\n</span><span>Crew Task Result (Stdio - Managed):</span><span>\n</span><span>"</span><span>, result)</span></span>
<span></span>
```

### 2\. Manual Connection Lifecycle

If you need finer-grained control over when the Stdio MCP server process is started and stopped, you can manage the `MCPServerAdapter` lifecycle manually.

```
<span><span>from</span><span> crewai </span><span>import</span><span> Agent, Task, Crew, Process</span></span>
<span><span>from</span><span> crewai_tools </span><span>import</span><span> MCPServerAdapter</span></span>
<span><span>from</span><span> mcp </span><span>import</span><span> StdioServerParameters</span></span>
<span><span>import</span><span> os</span></span>
<span></span>
<span><span># Create a StdioServerParameters object</span></span>
<span><span>stdio_params</span><span>=</span><span>StdioServerParameters(</span></span>
<span><span>    command</span><span>=</span><span>"python3"</span><span>, </span></span>
<span><span>    args</span><span>=</span><span>[</span><span>"servers/your_stdio_server.py"</span><span>],</span></span>
<span><span>    env</span><span>=</span><span>{</span><span>"UV_PYTHON"</span><span>: </span><span>"3.12"</span><span>, </span><span>**</span><span>os.environ},</span></span>
<span><span>)</span></span>
<span></span>
<span><span>mcp_server_adapter </span><span>=</span><span> MCPServerAdapter(</span><span>server_params</span><span>=</span><span>stdio_params)</span></span>
<span><span>try</span><span>:</span></span>
<span><span>    mcp_server_adapter.start()  </span><span># Manually start the connection and server process</span></span>
<span><span>    tools </span><span>=</span><span> mcp_server_adapter.tools</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"Available tools (manual Stdio): </span><span>{</span><span>[tool.name </span><span>for</span><span> tool </span><span>in</span><span> tools]</span><span>}</span><span>"</span><span>)</span></span>
<span></span>
<span><span>    # Example: Using the tools with your Agent, Task, Crew setup</span></span>
<span><span>    manual_agent </span><span>=</span><span> Agent(</span></span>
<span><span>        role</span><span>=</span><span>"Local Task Executor"</span><span>,</span></span>
<span><span>        goal</span><span>=</span><span>"Execute a specific local task using a manually managed Stdio tool."</span><span>,</span></span>
<span><span>        backstory</span><span>=</span><span>"An AI proficient in controlling local processes via MCP."</span><span>,</span></span>
<span><span>        tools</span><span>=</span><span>tools,</span></span>
<span><span>        verbose</span><span>=</span><span>True</span></span>
<span><span>    )</span></span>
<span><span>    </span></span>
<span><span>    manual_task </span><span>=</span><span> Task(</span></span>
<span><span>        description</span><span>=</span><span>"Execute the 'perform_analysis' command via the Stdio tool."</span><span>,</span></span>
<span><span>        expected_output</span><span>=</span><span>"Results of the analysis."</span><span>,</span></span>
<span><span>        agent</span><span>=</span><span>manual_agent</span></span>
<span><span>    )</span></span>
<span><span>    </span></span>
<span><span>    manual_crew </span><span>=</span><span> Crew(</span></span>
<span><span>        agents</span><span>=</span><span>[manual_agent],</span></span>
<span><span>        tasks</span><span>=</span><span>[manual_task],</span></span>
<span><span>        verbose</span><span>=</span><span>True</span><span>,</span></span>
<span><span>        process</span><span>=</span><span>Process.sequential</span></span>
<span><span>    )</span></span>
<span><span>        </span></span>
<span><span>       </span></span>
<span><span>    result </span><span>=</span><span> manual_crew.kickoff() </span><span># Actual inputs depend on your tool</span></span>
<span><span>    print</span><span>(</span><span>"</span><span>\n</span><span>Crew Task Result (Stdio - Manual):</span><span>\n</span><span>"</span><span>, result)</span></span>
<span><span>            </span></span>
<span><span>except</span><span> Exception</span><span> as</span><span> e:</span></span>
<span><span>    print</span><span>(</span><span>f</span><span>"An error occurred during manual Stdio MCP integration: </span><span>{</span><span>e</span><span>}</span><span>"</span><span>)</span></span>
<span><span>finally</span><span>:</span></span>
<span><span>    if</span><span> mcp_server_adapter </span><span>and</span><span> mcp_server_adapter.is_connected: </span><span># Check if connected before stopping</span></span>
<span><span>        print</span><span>(</span><span>"Stopping Stdio MCP server connection (manual)..."</span><span>)</span></span>
<span><span>        mcp_server_adapter.stop()  </span><span># **Crucial: Ensure stop is called**</span></span>
<span><span>    elif</span><span> mcp_server_adapter: </span><span># If adapter exists but not connected (e.g. start failed)</span></span>
<span><span>        print</span><span>(</span><span>"Stdio MCP server adapter was not connected. No stop needed or start failed."</span><span>)</span></span>
<span></span>
```

Remember to replace placeholder paths and commands with your actual Stdio server details. The `env` parameter in `StdioServerParameters` can be used to set environment variables for the server process, which can be useful for configuring its behavior or providing necessary paths (like `PYTHONPATH`).