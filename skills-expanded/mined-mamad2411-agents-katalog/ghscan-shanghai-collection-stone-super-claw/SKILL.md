# FRP Project

Use this skill when the user asks to expose a generated code project publicly through FRP, inspect FRP endpoints, or prepare a project for PM2-managed external mapping.

Rules:

- All generated projects must live under the bound workspace `code/` directory.
- Projects must be Node.js projects with a `package.json`.
- Projects must be managed by PM2. Add or update an `ecosystem.config.cjs` entry and use PM2 process names that include the project directory name.
- Keep local app ports explicit in `.env` or the PM2 ecosystem file.
- Store generated artifacts outside code in the correct workspace directories: `images/`, `video/`, `file/`, or `pdf/`. PDF files must go under `pdf/`; generic non-PDF files must go under `file/`.
- Query FRP endpoint state through the gateway endpoint `GET /api/frp/endpoints` or the persistent `services/frp-manager.mjs` PM2 service.
- When an endpoint is configured in env, prefer that configured public URL instead of inventing one.

Supported env hints:

```text
FRP_ENDPOINTS=[{"id":"demo","name":"Demo","localUrl":"http://127.0.0.1:3000","publicUrl":"https://demo.example.com","pm2Name":"demo"}]
FRP_MANAGER_PORT=5188
GATEWAY_PUBLIC_BASE_URL=https://gateway.example.com
```

Useful commands:

```bash
npm --prefix C:\project\super-claw run frp:manager
npm --prefix C:\project\super-claw run pm2:start
npm --prefix C:\project\super-claw run pm2:status
```
