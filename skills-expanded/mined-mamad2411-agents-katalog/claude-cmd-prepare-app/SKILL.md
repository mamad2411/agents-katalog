# Prepare Application

Setup the application for the review or test.

## Variables

PORT: If `.ports.env` exists, read FRONTEND_PORT from it, otherwise default to 5173

## Setup

1. Check if `.ports.env` exists:
   - If it exists, source it and use `FRONTEND_PORT` for the PORT variable
   - If not, use default PORT: 5173

2. Reset the database:
   - Run `scripts/reset_db.sh`

3. Start the application:
   - IMPORTANT: Make sure the server and client are running on a background process using `nohup sh ./scripts/start.sh > /dev/null 2>&1 &`
   - The start.sh script will automatically use ports from `.ports.env` if it exists
   - Use `./scripts/stop_apps.sh` to stop the server and client

4. Verify the application is running:
   - The application should be accessible at http://localhost:PORT (where PORT is from `.ports.env` or default 5173)
   
Note: Read `scripts/` and `README.md` for more information on how to start, stop and reset the server and client.

