# Web Clipper

Extracts readable content from any URL and saves it as clean Markdown in `memory/clippings/`.
Useful for research, documentation, and archiving.

## Usage

```bash
node skills/web-clipper/index.js <url>
```

Example:
```bash
node skills/web-clipper/index.js https://example.com/article
```

## Features

- **Readability**: Removes ads, sidebars, and clutter.
- **Markdown**: Converts HTML to clean Markdown.
- **Metadata**: Saves title, author, date, and source URL in frontmatter.
- **Persistence**: Stores clippings in `memory/clippings/` for future reference.

## Installation

This skill requires `axios`, `jsdom`, `@mozilla/readability`, and `turndown`.
Dependencies are managed via `package.json`.
Run `npm install` in this directory to install them.
