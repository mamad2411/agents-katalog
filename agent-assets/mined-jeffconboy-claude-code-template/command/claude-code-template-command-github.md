Perform GitHub operations using the connected GitHub MCP server:

**Available Actions:**
- Create issues from bug reports or feature requests
- Manage pull requests (create, review, merge)
- Repository management (clone, fork, create)
- Search repositories, issues, and code
- Manage releases and tags
- Organization and team management

**Usage Examples:**
- `/github create issue "Bug in login flow" with details from $ARGUMENTS`
- `/github create PR from current branch with summary`
- `/github search repositories related to $ARGUMENTS`
- `/github list my open issues`
- `/github merge PR #123 after review`

If $ARGUMENTS is provided, use it as the specific GitHub operation or search query.

The GitHub MCP server is pre-configured and ready to use!