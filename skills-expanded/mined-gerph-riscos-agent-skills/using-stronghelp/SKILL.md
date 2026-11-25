---
name: using-stronghelp
description: Development and maintenance of StrongHelp manuals for RISC OS. Use when the agent needs to create, edit, or build StrongHelp manuals, or when processing help pages in the StrongHelp format.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-shextract:*) Bash(riscos-strongcopy:*)
---

# StrongHelp Development

This skill provides guidance for developing StrongHelp manuals, which are the standard hypertext help format for RISC OS.

## Quick Start

1.  **List the container contents first**: `riscos-shextract --list <manual_file,3d6>`
2.  **Extract a manual for inspection or editing**: `riscos-shextract --extract-dir <dirname> <manual_file,3d6>`
3.  **Read the extracted page files, not the packed `,3d6` bytes directly**.
4.  **Build a manual**: `riscos-strongcopy -o <manual_file,3d6> <directory>`

## Developing Pages

Every StrongHelp page is a text file where the first line is the title. Use `#Parent` on every page to ensure navigation works correctly.

### Workflow

1.  **List the manual**: Use `riscos-shextract --list` to see the real page names and directories before making assumptions about the structure.
2.  **Extract the manual**: Use `riscos-shextract --extract-dir` and inspect the extracted files in the filesystem.
3.  **Identify the target page**: Find the existing page or determine the filename for a new one.
4.  **Apply Syntax**: Use the syntax guide in [references/syntax.md](references/syntax.md) for formatting and links.
5.  **Organize Structure**: Use the structure guide in [references/structure.md](references/structure.md) for directory organization and special files.
6.  **Verify Links**: Ensure all links point to valid page names or files.
7.  **Build**: Use `riscos-strongcopy` to package the directory into a `.3d6` manual file.

## Tools

-   **riscos-shextract**: Extracts contents from a StrongHelp `.3d6` container.
-   **riscos-strongcopy**: Packages a directory into a StrongHelp `.3d6` container.

## Best Practices

-   **Inspection**: Do not treat a packed `,3d6` manual as plain text and do not run unrelated decoders over it. Extract it first, then read the extracted page files.
-   **Navigation**: Include `#Parent !Root` (or the appropriate parent) on every page.
-   **Columns**: Use `TAB` for alignment instead of spaces to ensure correct rendering.
-   **Formatting**: Use `#fCode` for examples and `#H1` for main headers.
-   **Organization**: For manuals with many pages, use prefix directories (e.g., `Wimp_`) or first-letter ranges (e.g., `[a-z]`).
-   **Filenames**: Remember that StrongHelp uses special filenames for redirection (e.g., `OLD>NEW`).
