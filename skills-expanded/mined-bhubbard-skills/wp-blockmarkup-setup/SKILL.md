---
name: wp-blockmarkup-setup
description: "Guidelines for installing and configuring the wp-blockmarkup-mcp server to index Gutenberg and third-party block schemas."
---

# WP BlockMarkup MCP Setup

The `wp-blockmarkup-mcp` is a powerful local MCP server that gives AI assistants a verified database of block schemas, attributes, and validated markup examples, eliminating AI "hallucinations" of Gutenberg markup.

## Installation & Configuration

1. **Install Globally or via npx:** 
   You can run `npx wp-blockmarkup-mcp` to use the server without a global install. To pin the version, configure your MCP client with `args: ["-y", "wp-blockmarkup-mcp@1.1.1"]`.
   
2. **Indexing Sources:**
   Before the server is useful, you must index your block sources. Run the CLI binary provided by `wp-blockmarkup-mcp` to clone and index repositories:
   *   **Gutenberg Core:** `npx -y --package=wp-blockmarkup-mcp@1.1.1 wp-blocks source:add --name gutenberg --type github-public --repo https://github.com/WordPress/gutenberg --branch trunk`
   *   **WooCommerce:** `npx -y --package=wp-blockmarkup-mcp@1.1.1 wp-blocks source:add --name woocommerce-blocks --type github-public --repo https://github.com/woocommerce/woocommerce --subfolder plugins/woocommerce-blocks --branch trunk`
   *   **Local Plugins:** `npx -y --package=wp-blockmarkup-mcp@1.1.1 wp-blocks source:add --name my-local-blocks --type local-folder --path /path/to/wp-content/plugins/my-blocks`

3. **Incremental Updates:**
   Use `npx -y --package=wp-blockmarkup-mcp@1.1.1 wp-blocks index --source gutenberg` to re-fetch and incrementally update the SQLite database cache in `~/.wp-blockmarkup-mcp/`.
