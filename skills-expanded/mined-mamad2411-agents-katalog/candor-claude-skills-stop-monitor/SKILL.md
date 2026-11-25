# /stop-monitor — Stop Monitoring and Summarize

Stop the running Signal app and capture all logs and browser state for review.

## Steps

1. Read all server logs from the background uvicorn task using `TaskOutput`
2. Capture the current browser state from the monitored tab:
   - Page content via `mcp__claude-in-chrome__read_page` or `mcp__claude-in-chrome__get_page_text`
   - Console messages via `mcp__claude-in-chrome__read_console_messages`
   - Network requests via `mcp__claude-in-chrome__read_network_requests`
3. Stop the background uvicorn process using `TaskStop`
4. Present a summary to the user covering:
   - **Server logs**: HTTP requests served, any errors or tracebacks
   - **Browser console**: JavaScript errors, warnings, or notable log messages
   - **Network requests**: Failed requests, slow responses, or error status codes
   - **Overall status**: Whether the session was clean or had issues
5. Keep all captured context in the conversation so the user can ask follow-up questions

## Important

- If no background task ID is available from a previous `/monitor-app`, tell the user no monitoring session is active
- If the browser tab is no longer available, skip browser capture and note it in the summary
- Always stop the server process to avoid orphaned background tasks
