---
name: mcp-file-systems-code-execution
description: 68 MCP servers for file systems, code execution, and command-line — FileSystem, E2B, Microsandbox, Docker, Shell, and more.
---

# MCP File Systems, Code Execution & CLI (68 servers)

File operations, sandboxed execution, and system command access.

## File Systems (47 servers)

| Server | Capability | Source |
|--------|-----------|--------|
| **FileSystem MCP (official)** | Local file system access | modelcontextprotocol/servers/src/filesystem |
| **FileSystem MCP (Go)** | Golang implementation | github.com/mark3labs/mcp-filesystem-server |
| **FileStash MCP** | Remote storage (SFTP, S3, FTP, SMB, WebDAV) | github.com/mickael-kerjean/filestash |
| **Backup MCP** | File/folder backup & restore | github.com/hexitex/MCP-Backup-Server |
| **Everything Search MCP** | Windows file search (Everything SDK) | github.com/mamertofabian/mcp-everything-search |
| **Fast Filesystem MCP** | Large file handling, streaming | github.com/efforthye/fast-filesystem-mcp |
| **llm-context MCP** | Share code context with LLMs | github.com/cyberchitta/llm-context.py |

## Code Execution (21 servers)

| Server | Capability | Source |
|--------|-----------|--------|
| **E2B MCP** | Secure cloud dev environments | github.com/e2b-dev/mcp-server |
| **Microsandbox MCP** | Self-hosted secure code execution | github.com/microsandbox/microsandbox |
| **Docker MCP** | Container & compose management | github.com/QuantGeekDev/docker-mcp |
| **Code Execution MCP** | Run code snippets | Various implementations |

## Command Line & OS Automation (39 servers)

| Server | Capability | Source |
|--------|-----------|--------|
| **Shell MCP (wcgw)** | Autonomous shell execution (Mac) | github.com/rusiaaman/wcgw |
| **Windows CLI MCP** | PowerShell, CMD, Git Bash | github.com/SimonB97/win-cli-mcp-server |
| **Windows Control MCP** | Mouse, keyboard, screen (NutJS) | github.com/Cheffromspace/nutjs-windows-control |
| **Command Line MCP** | Any command execution | github.com/phialsbasement/cmd-mcp-server |
| **Apple Shortcuts MCP** | Apple Shortcuts integration | github.com/recursechat/mcp-server-apple-shortcuts |

## Capabilities
- File read/write/search across local and remote systems
- Backup and recovery
- Sandboxed code execution (E2B, Microsandbox)
- Container management (Docker)
- Shell command execution
- OS-level automation (mouse, keyboard, screen)
- Apple Shortcuts integration
- Remote storage protocol support (SFTP, S3, FTP, SMB, NFS, WebDAV)
