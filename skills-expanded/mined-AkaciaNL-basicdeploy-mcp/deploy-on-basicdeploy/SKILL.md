---
name: deploy-on-basicdeploy
description: Deploy and host a web app, API, or site on BasicDeploy and get a live HTTPS URL. Trigger when the user asks to deploy, host, ship, or "put online" an app on BasicDeploy (with the BasicDeploy connector available). Covers creating a container, deploying code over the chat connector, the REQUIRED 0.0.0.0:8080 port, the preset DATABASE_URL / S3 / KAFKA env vars, logs, Kafka topics, and always-on. Do not use for other hosting providers.
---

# Deploy on BasicDeploy

BasicDeploy gives each app a live container with a PostgreSQL database, S3-compatible
object storage, a Kafka broker, and a public HTTPS URL, all wired in. Follow these steps to deploy reliably.

## The one rule that breaks deploys
The container's public URL is **always routed to port 8080**. Your app **MUST listen on
`0.0.0.0:8080`**, not `localhost`/`127.0.0.1`, and not 3000/5000/8000. Any other port, or a
loopback bind, returns HTTP 503 at the public URL even though the process is running. If the
framework reads a `PORT` env var, set it to 8080.

## Steps
1. **(Optional) Check the account:** call `get_account` for plan limits and selectable memory sizes.
2. **Create a container:** call `create_container` (optionally `memoryMb`). It returns the
   container id + public URL and auto-provisions a Postgres database and an S3 bucket.
3. **Put the app in the container, two ways:**
   - **Chat / remote connector (ChatGPT, Claude, Gemini): use `exec_command`.** There is no
     shared filesystem, so `deploy_app`'s tarball path will NOT work here. Write the app files
     into the container with `exec_command` (heredoc/echo, or `git clone`), install deps, then
     start the server bound to `0.0.0.0:8080`.
   - **Local stdio server: use `deploy_app`** with a tarball path on your own machine
     (Dockerfile / package.json / requirements.txt / go.mod at the archive root).
4. **Use the preset env vars, do not hardcode:** `DATABASE_URL` (Postgres),
   `S3_ENDPOINT` / `S3_ACCESS_KEY` / `S3_SECRET_KEY` / `S3_BUCKET`, and `KAFKA_BOOTSTRAP` /
   `KAFKA_USERNAME` / `KAFKA_PASSWORD` / `KAFKA_GROUP_PREFIX` are already set in the container
   environment. Read them from the environment. Kafka consumer-group ids MUST start with
   `KAFKA_GROUP_PREFIX`; create topics via the Connect tab, `POST /api/kafka/topics`, or the
   `create_topic` tool (auto-create is off).
5. **Keep it running:** there is no init/supervisor, a process started via `exec_command`
   runs only until the container sleeps or restarts and is NOT relaunched. For a long-running
   web server, run it as the container's main process and enable always-on with `set_always_on`
   (free on Pro/Scale; a paid add-on on Free). For a one-shot job, re-run the start command after each wake.
6. **Verify:** open the public URL from step 2. A 503 means the app is on the wrong port or bound
   to localhost, fix it to `0.0.0.0:8080`. Use `get_logs` to debug.

## Notes
- `get_logs` shows the container's **main process** output. A process started as a child of
  `exec_command` won't appear there, run the app as the main process to get logs.
- `S3_ENDPOINT` and `DATABASE_URL` are cluster-internal, reachable only from inside the container.
  To serve user-uploaded media, read it from S3 in your backend and stream it to the client, do
  NOT hand browsers direct S3 or presigned URLs.
- Optional: add hosted sign-up/login to the app you build via BasicDeploy's auth-as-a-service
  (standard OpenID Connect), see the docs.
- Pricing is flat: database, storage, bandwidth and URL are included; no usage bills.
- Full documentation: call the `get_docs` tool, or see https://basicdeploy.com/docs.
