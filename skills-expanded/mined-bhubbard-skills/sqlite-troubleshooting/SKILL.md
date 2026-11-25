---
name: sqlite-troubleshooting
description: Debug query compatibility issues with the SQLite plugin.
---

# SQLite Troubleshooting

This skill helps debug issues when running WordPress on SQLite.

## Instructions
1. Check if complex MySQL-specific functions (like CONVERT()) are properly polyfilled.
2. Verify table locks or specific row-level locking clauses.
3. Review the WordPress debug log for translation errors from MySQL to SQLite.
