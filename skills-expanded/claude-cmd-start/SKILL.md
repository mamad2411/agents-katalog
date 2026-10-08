# Start the application

## Variables

PORT: If `.ports.env` exists, read FRONTEND_PORT from it, otherwise default to 5173

## Workflow

1. Check if `.ports.env` exists:
   - If it exists, source it and use `FRONTEND_PORT` for the PORT variable
   - If not, use default PORT: 5173

2. Check to see if a process is already running on port PORT.

3. If it is just open it in the browser with `open http://localhost:PORT`.

4. If there is no process running on port PORT, run these commands:
   - Run `nohup sh ./scripts/start.sh > /dev/null 2>&1 &`
   - Note: start.sh automatically reads `.ports.env` if it exists
   - Run `sleep 3`
   - Run `open http://localhost:PORT`

5. Let the user know that the application is running on port PORT and the browser is open.