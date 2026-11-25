---

name: filebrowser-deploy
description: Deploy filebrowser (web-based file manager) with HTTPS via Cloudflare tunnel on Charles' server
tags: [docker, filebrowser, https, cloudflare, web-service]

---
## What This Skill Does

This skill Deploy filebrowser (web-based file manager) with HTTPS via Cloudflare tunnel on Charles' server.

## Trigger
When the user needs to deploy filebrowser (web-based file manager) with HTTPS access on Charles' server.

## Steps

### 1. Pull the image
```bash
docker pull filebrowser/filebrowser:latest
```

### 2. Create config with low password requirements
```bash
mkdir -p /root/filebrowser
cat > /root/filebrowser/settings.json << 'EOF'
{
  "port": 80,
  "baseURL": "",
  "address": "0.0.0.0",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
EOF
```

### 3. Initialize database and create admin user
The Docker image has a built-in `/config/settings.json` with `minimumPasswordLength: 12` that cannot be removed. You MUST:
1. Run `config init` to create the DB
2. Run `config set --minimumPasswordLength 4` to allow shorter passwords
3. Run `users add` with a password that also passes the **dictionary check** -- `admin` is banned. Use `Admin123456` or similar.

```bash
docker volume create fb-data

# Init the database (mounts our settings.json as /config/settings.json)
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json filebrowser/filebrowser:latest config init --config /config/settings.json --database /database/filebrowser.db

# Lower minimum password length to 4
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json filebrowser/filebrowser:latest config set --config /config/settings.json --database /database/filebrowser.db --minimumPasswordLength 4

# Create admin user (password must NOT be a dictionary word)
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json filebrowser/filebrowser:latest users add admin Admin123456 --config /config/settings.json --database /database/filebrowser.db --perm.admin
```

### 4. Launch container
```bash
docker rm -f filebrowser 2>/dev/null || true
docker run -d \
  --name filebrowser \
  --restart unless-stopped \
  -p 7000:80 \
  -v fb-data:/database \
  -v /:/srv \
  filebrowser/filebrowser:latest
```

### 5. Verify login
```bash
curl -s -X POST http://localhost:7000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123456"}'
# Should return a JWT token on success, or "403 Forbidden" on failure
```

### 6. Set up HTTPS via Cloudflare quick tunnel
```bash
# Install cloudflared if needed
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# Start tunnel in background
nohup cloudflared tunnel --url http://localhost:7000 > /tmp/cloudflared.log 2>&1 &
sleep 6

# Extract the URL from logs
grep "https://" /tmp/cloudflared.log | head -1
```

## Password Reset / User Management (post-deploy)

If you need to change a user's password after the container is already running:

### Method 1: Stop container, run command with volumes (reliable)
```bash
docker stop filebrowser
mkdir -p /root/filebrowser
# Ensure settings.json exists with port/root/db config
cat > /root/filebrowser/settings.json << 'EOF'
{
  "port": 80,
  "baseURL": "",
  "address": "0.0.0.0",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
EOF

docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json filebrowser/filebrowser:latest users update admin --config /config/settings.json --database /database/filebrowser.db --password "NewPassword123!"
docker start filebrowser
```

### Method 2: docker exec with --config flag
```bash
docker exec filebrowser filebrowser users update admin --config /config/settings.json --database /database/filebrowser.db --password "NewPassword123!"
```

### Key requirement
You **must** pass both `--config` and `--database` flags. The `--database` flag alone causes a silent timeout. If `--config` is missing the binary can't find the database connection info even with `--database` explicitly provided. Passwords must pass the dictionary check (no "admin", "password", etc.).

## Resetting the admin password
The `filebrowser users update` CLI command **times out** if the filebrowser container is running. You MUST stop it first:

```bash
docker stop filebrowser
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json filebrowser/filebrowser:latest users update admin --config /config/settings.json --database /database/filebrowser.db --password "NewPass123!"
docker start filebrowser
```

## Pitfalls
- `minimumPasswordLength` is 12 by default and baked into the container's `/config/settings.json` -- you must mount your own config to override it
- The quick setup flags (`--username admin --password admin`) silently create the user but the password hash is wrong due to config conflicts -- use the 3-step `config init` -> `config set` -> `users add` flow instead
- "admin" as a password passes the length check but fails the **dictionary check** ("password is too easy") -- use `Admin123456` or similar
- The `gtsteffaniak/filebrowser` Docker image does NOT exist on Docker Hub -- the official image is `filebrowser/filebrowser`
- The gtsteffaniak fork binary has a completely different CLI (`set -u`, `-a`) -- don't mix the two
- Named volumes (`fb-data`) avoid bind-mount permission issues that corrupt the SQLite database
- Localtunnel (`lt`) is unreliable on this server -- use `cloudflared` instead
- Cloudflare quick tunnels get a random URL each time -- ask the user if they need a permanent named tunnel tied to a custom domain
