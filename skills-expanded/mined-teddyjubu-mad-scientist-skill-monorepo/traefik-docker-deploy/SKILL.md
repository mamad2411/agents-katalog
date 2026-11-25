---
name: traefik-docker-deploy
category: devops
description: Deploy Docker apps behind Traefik reverse proxy on Charles's Hostinger server. Handles SSL, DNS, permissions, and firewall.
---

## What This Skill Does

This skill deploys Docker apps behind Traefik reverse proxy on Charles's Hostinger server. Handles SSL, DNS, permissions, and firewall.

## Environment

- **Server IP:** set `CHARLES_HOST_IP` in the environment before using IP-based commands.
- **Traefik config:** /docker/traefik/docker-compose.yml + /docker/traefik/traefik.yml
- **Traefik network:** traefik-net (bridge)
- **Traefik runs in:** host network mode
- **Firewall:** UFW active — ports 80, 443, 3000 already open
- **Let's Encrypt email:** realdealmeetup@gmail.com

## Deployment Steps

1. **Check Docker is available:**
   `docker --version`

2. **Stop/remove any previous version of the container:**
   `docker rm -f <container_name> 2>/dev/null || true`

3. **Verify the domain has DNS:**
   `dig +short <domain>` or `host <domain> 8.8.8.8`
   If no DNS record exists, use sslip.io as fallback:
   - Format: `http://IP-WITH-DASHES.sslip.io` (derive it from `$CHARLES_HOST_IP`)
   - **CAUTION:** sslip.io CAN get Let's Encrypt certs, but rate limits from prior failed attempts or DNS quirks can cause temporary failures. If HTTPS is flaky, fall back to plain HTTP immediately.

4. **Create data directory with correct permissions:**
   `mkdir -p /root/<app_name>/data`
   `chown -R 1000:1000 /root/<app_name>`  (common for apps that run as non-root)

5. **Launch behind Traefik:**
   ```bash
   docker run -d \
     --name <container_name> \
     --restart unless-stopped \
     --network traefik-net \
     -e APPLICATION_URL=https://<domain> \
     --label "traefik.enable=true" \
     --label "traefik.http.routers.<name>.rule=Host(\`<domain>\`)" \
     --label "traefik.http.routers.<name>.entrypoints=websecure" \
     --label "traefik.http.routers.<name>.tls.certresolver=letsencrypt" \
     --label "traefik.http.services.<name>.loadbalancer.server.port=<internal_port>" \
     -v /root/<app_name>/data:/app/data \
     <image_name>
   ```

   For HTTP-only (no TLS), also add:
   ```
   --label "traefik.http.routers.<name>-insecure.rule=Host(\`<domain>\`)" \
   --label "traefik.http.routers.<name>-insecure.entrypoints=web" \
   ```

6. **Verify the container is healthy:**
   `docker ps --filter name=<container_name> --format '{{.Status}}'`
   Should show "Up X seconds" (not "Restarting")

7. **Check Traefik logs for SSL certificate issuance:**
   `docker logs traefik 2>&1 | grep -i <domain> | tail -5`
   Wait up to 60 seconds for the certificate to be obtained.

8. **Test from the server:**
   `curl -sk https://<domain> | head -5`
   `curl -sL http://<domain> | head -5`

## Troubleshooting

### Container is restart-looping
- **Wrong UID:** Many apps run as non-root (UID 1000). Check: `docker run --rm <image> id`. Fix perms: `chown -R 1000:1000 /root/<app>`.
- **Missing dirs/files:** Some apps need specific subdirectories pre-created (e.g., log dirs). Check `docker logs <container>` for error messages.
- **Stale config files:** Remove old config files from previous attempts that may override the database.

### SSL certificate fails (400 DNS error)
- Domain has no DNS A record pointing to `$CHARLES_HOST_IP`.
- Fix: add DNS record at registrar, or use sslip.io: `IP-WITH-DASHES.sslip.io`
- Note: if Let's Encrypt failed recently, it may rate-limit retries. HTTP fallback works immediately.
- **here.now is NOT an option for HTTPS** — it only hosts static files (HTML/CSS/JS), not running server applications.

### Port not accessible from outside
- Traefik handles all external traffic via ports 80/443 — apps behind Traefik do NOT need host port mapping (`-p`).
- Do NOT use `-p <port>:<port>` when connected to traefik-net.
- If you MUST use raw port, check UFW: `sudo ufw status` and add rule: `sudo ufw allow <port>/tcp`.
- **ALREADY OPEN ports** on this server (no need to add UFW rules): 22, 7000, 80, 443, 3000, 3001, 3005, 3210, 46736, 49248, 50183.
- **SIMPLEST APPROACH when Traefik/DNS is problematic:** Use an already-open port (7000 is preferred) with direct IP access, e.g. `http://$CHARLES_HOST_IP:7000`. This bypasses all DNS/SSL complexity.
- **HTTPS tunnel fallback:** If you need HTTPS without DNS, use localtunnel:
  `npm install -g localtunnel`
  `lt --port <app_port> --local-host localhost --subdomain <unique-name>`
  This gives you `https://<unique-name>.loca.lt` — user may need to click through a "waiting for accept" page on first visit.

### Verify Traefik is routing correctly
- `docker network inspect traefik-net --format '{{range .Containers}}{{.Name}} {{end}}'` — confirms container is on the right network.
- Test from Inside Traefik: `docker exec traefik wget -qO- http://<container_name>:<port> | head -5`
  Note: hostname-based DNS won't work from Traefik container. Use container name only if on same Docker network, or use `curl -H "Host: <domain>" http://<container_ip>:<port>`.

### Filebrowser-specific: password "admin" rejected
- The `filebrowser/filebrowser` image rejects short/easy passwords with "password is too short" (min 12) or "password is too easy".
- **Solution:** Use the quick-setup flags which bypass the policy:
  `docker run --rm -v /root/filebrowser/data:/database filebrowser/filebrowser:latest --database /database/filebrowser.db --root /srv --port 8080 --address 0.0.0.0 --username admin --password admin`
  This creates the database with admin/admin credentials in one step.
- **Do NOT** run `config init` followed by `config set` separately — the init sets a minimumPasswordLength of 12 that later blocks short passwords even for existing users.
- After creating the DB, ensure correct ownership: `chown 1000:1000 /root/filebrowser/data/filebrowser.db`
- No need for a separate config JSON file — the database has all the settings.
