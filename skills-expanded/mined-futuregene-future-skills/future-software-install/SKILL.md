---
version: 1.0.1
name: future-software-install
description: Install or update lightweight software, command-line tools, browser automation prerequisites, and document-processing libraries for FutureOS across Windows, macOS, and Linux. Use when the user asks to install a tool, configure Homebrew or a package manager, set up Chrome/headless browsing, add Python document libraries, or use mainland China download mirrors.
category: tools
---

# Lightweight Software Setup Reference

This reference helps match a FutureOS task with a small, suitable dependency. Existing software and language libraries are often lighter than desktop applications, servers, or system-wide toolchains.

## Environment considerations

- The operating system, distribution, CPU architecture, shell, package manager, and WSL/container status help determine compatible installation options.
- Checking for an existing command or application often avoids redundant downloads.
- Package source, approximate disk impact, permissions, and a version check are useful context before an installation.
- Reuse the user's explicit installation authorization. Ask about material changes to source, privileges, disk/cost impact or scope rather than repeating approval for an already requested install. Package-source and shell startup-file edits are separate changes, not automatically authorized by a request for one tool.
- Official package managers are usually the clearest starting point; documented mainland mirrors can help when the official source is slow or unreachable.
- Databases, Docker, IDEs, Office suites, Java, Go, Rust, and similar larger dependencies fit best when a task explicitly calls for them.
- Public mirrors are most appropriate for public packages. Credentials, private package names, and private Git URLs are better kept on official or user-managed sources.

## Suggested sequence

1. Identify the capability the task needs, rather than focusing solely on an executable name. A lightweight library may be enough.
2. Inspect the platform and any existing installation. On Linux, `/etc/os-release` and `uname -m` provide useful context.
3. Read [references/software-catalog.md](references/software-catalog.md) for the lightweight catalog and platform examples.
4. When mainland-network conditions matter, read [references/mainland-network.md](references/mainland-network.md). Short HTTPS probes can compare official and mirror reachability without collecting location data.
5. Present the selected package, source, command, and verification step before making changes.
6. For Python libraries, a task-local or FutureOS-managed environment keeps dependencies contained.
7. A resolved executable path and version provide a useful post-installation check.

## Package-manager landscape

| Platform | Prefer |
|---|---|
| Windows | WinGet; vendor installers are a useful fallback when WinGet has no matching package |
| macOS | Homebrew; its bootstrap is useful when a needed tool is otherwise unavailable |
| Debian/Ubuntu | APT and the distribution package repository |
| Fedora/RHEL | DNF |
| Arch | Pacman |
| WSL | Treat as Linux, not as Windows |

Homebrew is generally a macOS or Linux/WSL tool rather than a native Windows tool. On Linux, the system package manager is often the simpler option than Linuxbrew.

## Browser and documents

An existing Chrome, Edge, or Chromium installation can usually be reused before downloading another browser. Chrome is the desktop application most likely to be useful here, especially for browser automation or rendering tasks. For local browser control, the built-in `future-browser` skill is available after a browser is present.

For DOCX, XLSX, PPTX, and PDF work, lightweight libraries cover many read/write and extraction tasks. LibreOffice becomes relevant for high-fidelity Office-to-PDF conversion, Office formula recalculation, or slide/page rendering.

## Validation

- Resolve the installed executable and print its version.
- For Python packages, import the package with the target environment's Python.
- For Chrome/Chromium, a no-network version check is a quick browser readiness check.
- For changed package sources or shell configuration, record the rollback action and what was actually changed.
- Deliver the resolved tool/interpreter path, version/import check, installation scope/source and any verification limits. Do not call a download alone a successful installation.
