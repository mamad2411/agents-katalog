# Prepare Application

Setup the application for review or test.

## Variables

PORT: from `.ports.env` (FRONTEND_PORT) if it exists, otherwise 5173

## Setup

- Check if `.ports.env` exists in the project root. If it does, read `FRONTEND_PORT` from it and use that as the PORT. Otherwise use 5173.
- IMPORTANT: Start the SvelteKit dev server in the background: `nohup bun run dev --port $PORT > /dev/null 2>&1 &`
- Wait a few seconds for the dev server to start, then verify it's running by checking `curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT`
- Note: This project uses Convex (hosted backend) — no local database setup is needed.
- The application URL will be `http://localhost:$PORT`
- Check if `DEV_TUNNEL_URL` is set in `.env.local`. If it is, the **external URL** (for cloud tools like Firecrawl that cannot reach localhost) is `$DEV_TUNNEL_URL`. This URL is provided by Cloudflare Tunnel (`cloudflared tunnel run babylon-dev`). If not set, external URL is the same as the application URL.
- IMPORTANT: When using Firecrawl or any cloud-hosted browser/scraping tool, ALWAYS use the external URL, never localhost.