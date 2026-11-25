---
name: minimax-coding-plan
description: MiniMax Coding Plan MCP - Web search and image understanding tools for developers
version: 1.0.0
---

# MiniMax Skill

MiniMax Coding Plan MCP provides two specialized tools: **web_search** and **understand_image**, to help developers quickly retrieve information and understand image content during coding.

## Environment Variables

**Required:**
- `MINIMAX_API_KEY`: MiniMax API Key (get from https://platform.minimaxi.com/subscribe/coding-plan)

**Optional:**
- `MINIMAX_API_HOST`: API host URL, defaults to `https://api.minimaxi.com`
- `MINIMAX_MCP_BASE_PATH`: Local output directory path
- `MINIMAX_API_RESOURCE_MODE`: Resource mode (`url` or `local`), defaults to `url`

## Available Tools

### web_search

Performs web search based on a query and returns search results with related suggestions.

**Args:**
- `query` (str, required): Search query. Use 3-5 keywords for best results. For time-sensitive topics, include the current date (e.g., `latest iPhone 2025`).

**Returns:** JSON object containing search results:
```json
{
    "organic": [
        {
            "title": "Search result title",
            "link": "Result URL",
            "snippet": "Brief description or excerpt",
            "date": "Result date"
        }
    ],
    "related_searches": [{"query": "Related search suggestion"}],
    "base_resp": {"status_code": status_code, "status_msg": "Status message"}
}
```

**Search Strategy:**
- If no useful results are returned, try rephrasing your query with different keywords.

### understand_image

Analyzes and interprets image content from local files or URLs based on instructions.

**Args:**
- `prompt` (str, required): A text prompt describing what to analyze or extract from the image.
- `image_source` (str, required): Image source URL or file path.
    - URL: `https://example.com/image.jpg`
    - Relative path: `images/photo.png`
    - Absolute path: `/Users/username/Documents/image.jpg`
    - **Note**: If the file path starts with `@`, remove the `@` prefix.

**Supported formats:** JPEG, PNG, WebP (max 20MB)

**Returns:** Text description of the image analysis result.

## Usage

### Execute Tools

```bash
$SKILL_DIR/scripts/exec-with-env.sh $SKILL_DIR/mcp-config.json <tool_name> '<arguments_json>'
```

### Examples

**Web Search:**
```bash
$SKILL_DIR/scripts/exec-with-env.sh $SKILL_DIR/mcp-config.json web_search '{"query": "latest react features 2025"}'
```

**Image Understanding:**
```bash
$SKILL_DIR/scripts/exec-with-env.sh $SKILL_DIR/mcp-config.json understand_image '{"prompt": "Describe this image", "image_source": "https://example.com/image.jpg"}'
```

## Execution Strategy

**Important: Execute directly, don't ask beforehand**

When using this skill, **execute commands directly** without asking users to confirm environment variables are set.

- Environment variable status is determined at execution time
- If execution fails, the error message will clearly indicate missing configuration
- Only then inform the user what needs to be configured
- Follow "fail fast" principle to avoid unnecessary interactions

**Don't do this:**
- "Please confirm you have set the MINIMAX_API_KEY environment variable"
- "Before executing, please ensure you have configured..."

**Do this:**
- Execute the command directly
- If it fails, inform the user based on the error message

## Use Cases

- Need to search for real-time or external information → **Use web_search**
- Need to analyze, describe, or extract information from an image → **Use understand_image**
- User provides an image that needs understanding → **Use understand_image**

## Error Handling

If execution returns an error:
- Check the tool name is correct
- Verify required arguments are provided (marked with `*` in signatures above)
- Ensure `MINIMAX_API_KEY` environment variable is set
- Check the MCP server is accessible

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: [mcp-to-skill](https://github.com/larkinwc/ts-mcp-to-skill)*

## References

- [MiniMax Coding Plan MCP Official Documentation](https://platform.minimaxi.com/docs/guides/coding-plan-mcp-guide)
