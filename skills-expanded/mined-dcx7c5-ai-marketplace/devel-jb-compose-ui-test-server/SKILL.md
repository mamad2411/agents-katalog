---
name: devel-jb-compose-ui-test-server
description: "-| | `GET /health` | Health check | | `GET /onNodeWithTag/{tag}/performClick` | Click element by test tag | | `GET /onNodeWithTag/{tag}/performTextInput?"
domain: cybersecurity
---

-|
| `GET /health` | Health check |
| `GET /onNodeWithTag/{tag}/performClick` | Click element by test tag |
| `GET /onNodeWithTag/{tag}/performTextInput?text=...` | Enter text (URL-encode the text!) |
| `GET /onNodeWithText/{text}/performClick` | Click element by display text |
| `GET /waitUntilExactlyOneExists/tag/{tag}?timeout=5000` | Wait for element by tag |
| `GET /waitUntilExactlyOneExists/text/{text}?exact=true&timeout=5000` | Wait for element by text |
| `GET /waitForIdle` | Wait for UI to stabilize |
| `GET /captureScreenshot?path=screenshot.png` | Capture screenshot |

## Workflow Pattern

Follow this sequence for reliable interactions:

```bash
# 1. Verify server is running
curl http://localhost:54345/health

# 2. Wait for UI to be ready
curl http://localhost:54345/waitForIdle

# 3. Perform action
curl "http://localhost:54345/onNodeWithTag/username/performTextInput?text=myuser"

# 4. Wait for UI to settle
curl http://localhost:54345/waitForIdle

# 5. Perform next action
curl http://localhost:54345/onNodeWithTag/login_button/performClick

# 6. Wait for result
curl "http://localhost:54345/waitUntilExactlyOneExists/tag/dashboard?timeout=10000"

# 7. Capture screenshot to verify
curl "http://localhost:54345/captureScreenshot?path=result.png"
```

## Finding Test Tags

Search the codebase for existing test tags:

```bash
grep -r "testTag\|Modifier.testTag" --include="*.kt" .
```

Also check:
- `CLAUDE.md` for documented test tags
- Test files in `src/*Test/` directories

## Important Notes

- **Always URL-encode** special characters in text: space→`%20`, `@`→`%40`, `&`→`%26`
- **Use `waitForIdle`** between operations for stability
- **Check HTTP status codes**: 200=success, 400=bad request, 500=error
- **Use appropriate timeouts** for waits (default 5000ms may be too short)
- Screenshots require absolute paths

## Error Handling

If an endpoint returns an error:
1. Check the element exists (search for its test tag in code)
2. Ensure UI has finished loading (`waitForIdle`)
3. Verify the server is still running (`/health`)
4. Try with a longer timeout for wait operations
