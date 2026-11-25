---
name: wp-blockmarkup-usage
description: "Guidelines for querying the wp-blockmarkup-mcp server to correctly generate, query, and validate Gutenberg blocks."
---

# WP BlockMarkup MCP Usage

When connected to the `wp-blockmarkup-mcp` server, use the available MCP tools to ensure your generated Gutenberg markup never throws an "Attempt Block Recovery" error in the WordPress editor.

## Tools Overview

1.  **`search_blocks`**: Use this to find correct block names based on the user's intent.
2.  **`get_block_schema`**: Retrieve the full attribute table, types, defaults, and the structure for a block. *Always call this before guessing a block's structure.*
3.  **`validate_markup`**: Accepts raw block markup and validates it structurally and functionally against the official WordPress parser and the block's `save()` AST.

## Theme-Aware Generation Workflow

`wp-blockmarkup-mcp` provides structural validation, but it **does not** know the site's theme variables (like color slugs or font-sizes). When generating content for a specific site:

1. Use a standard WordPress MCP (or site context) to retrieve the active theme's `theme.json` configuration to find valid color slugs (e.g., `primary`, `accent`).
2. Use `get_block_schema` to identify exactly how those theme colors should be applied to the block (e.g., which attributes to set).
3. Generate the markup using the valid theme slugs and the verified block attributes.
4. Pass the result to `validate_markup`. The validator is slug-agnostic—it checks that if you declare `"backgroundColor":"primary"`, the HTML contains `has-primary-background-color` and `has-background`.

## Dynamic vs Static Blocks

*   **Static Blocks**: Fully validated.
*   **Dynamic Blocks** (e.g., core/latest-posts): The server will instruct you to output the comment-only self-closing markup (e.g. `<!-- wp:latest-posts {"postsToShow":5} /-->`). The validation status will return `attributes_only`. Do not attempt to generate the inner HTML for dynamic blocks; WordPress renders them natively server-side.
