---
name: freepbx-docker
description: Deploy FreePBX 17 in Docker with Asterisk 21, MariaDB, custom SIP/RTP ports, and full persistence
version: 1.0
author: hermes
tags: [freepbx, asterisk, voip, sip, docker, pbx]
---

# FreePBX 17 Docker Deployment

Deploy a production-ready FreePBX 17 PBX system in Docker with custom SIP trunking ports.

## Architecture

- **FreePBX container**: `escomputers/freepbx:17-nofail2ban` (Debian bookworm, Asterisk 21, PHP 8.2)
- **MariaDB container**: `mariadb:11` (separate — NOT included in FreePBX image)
- **Network**: Host mode (avoids port mapping issues with large RTP ranges)

## GitHub Repos

| Repo | Stars | Notes |
|------|-------|-------|
| `escomputers/freepbx-docker` | 105 | **Recommended**. FreePBX 17, Asterisk 21, PHP 8.2. Uses `var_data:/var` + `etc_data:/etc` volumes. Bridge network with iptables DNAT for RTP. Install via `run.sh --install-freepbx`. |
| `tiredofit/docker-freepbx` | 536 | Popular but older (FreePBX 15, Asterisk 17). All-in-one with MariaDB inside. Less flexible. |
| `scorpionukr/Docker-FreePBX` | 8 | FreePBX 17 clean build, good reference Dockerfile. |

## Port Layout (Custom)

| Service | Port | Protocol |
|---------|------|----------|
| Web Admin | 2101 | TCP |
| SIP Signaling | 2000 | UDP + TCP |
| SIP TLS | 2001 | TCP |
| RTP Media | 2003-2100 | UDP |
| AMI Manager | 5038 | TCP |

## Step-by-Step Deployment

### 1. Start MariaDB

```bash
docker run -d \
  --name freepbx-mariadb \
  --restart unless-stopped \
  --network host \
  -e MYSQL_ROOT_PASSWORD=<rootpass> \
  -e MYSQL_DATABASE=asterisk \
  -e MYSQL_USER=asterisk \
  -e MYSQL_PASSWORD=<dbpass> \
  -v freepbx_db_data:/var/lib/mysql \
  mariadb:11
```

Wait for healthy:
```bash
for i in $(seq 1 20); do
  docker exec freepbx-mariadb healthcheck.sh --connect --innodb_initialized 2>/dev/null && break
  sleep 3
done
```

Create CDR database:
```bash
docker exec freepbx-mariadb mariadb -u root -p<rootpass> -e \
  "CREATE DATABASE IF NOT EXISTS asteriskcdrdb; GRANT ALL ON asteriskcdrdb.* TO 'asterisk'@'%'; FLUSH PRIVILEGES;"
```

### 2. Start FreePBX Container

```bash
docker run -d \
  --name freepbx \
  --restart unless-stopped \
  --network host \
  -v freepbx_var_data:/var \
  -v freepbx_etc_data:/etc \
  escomputers/freepbx:17-nofail2ban
```

**IMPORTANT**: The escomputers repo uses `var_data:/var` and `etc_data:/etc` as volumes — this persists EVERYTHING including freepbx.conf, asterisk configs, and web files. This prevents the config-loss issue.

### 3. Install FreePBX (First Run Only)

```bash
docker exec -it freepbx bash -c '
  cd /usr/local/src/freepbx
  ./start_asterisk start
  php install -n --dbuser=asterisk --dbpass=<dbpass> --dbhost=127.0.0.1
'
```

### 4. Fix Missing #include Files (CRITICAL)

The FreePBX `pjsip.conf` includes custom files that DON'T exist after a fresh volume mount. Without them, PJSIP silently fails — **no transports load, no SIP works**.

```bash
docker exec freepbx bash -c '
for f in pjsip_custom.conf pjsip_custom_post.conf \
         pjsip.aor_custom.conf pjsip.aor_custom_post.conf \
         pjsip.auth_custom.conf pjsip.auth_custom_post.conf \
         pjsip.endpoint_custom.conf pjsip.endpoint_custom_post.conf \
         pjsip.registration_custom.conf pjsip.registration_custom_post.conf \
         pjsip.identify_custom.conf pjsip.identify_custom_post.conf \
         pjsip.transports_custom_post.conf; do
  touch /etc/asterisk/$f
done'
```

**Verification**: `docker exec freepbx asterisk -rx "pjsip show transports"` — must show transport objects, NOT "No objects found."

### 5. Change SIP Port to 2000

FreePBX's `SIPPORT` DB setting only affects chan_sip (not loaded by default in FPBX 17). PJSIP transport port must be changed in the generated config:

```bash
docker exec freepbx sed -i 's/bind=0.0.0.0:5060/bind=0.0.0.0:2000/' /etc/asterisk/pjsip.transports.conf
```

Add TCP/TLS transports in `pjsip.transports_custom.conf`:
```ini
[0.0.0.0-tcp]
type=transport
protocol=tcp
bind=0.0.0.0:2000
external_media_address=<PUBLIC_IP>
external_signaling_address=<PUBLIC_IP>

[0.0.0.0-tls]
type=transport
protocol=tls
bind=0.0.0.0:2001
external_media_address=<PUBLIC_IP>
external_signaling_address=<PUBLIC_IP>
```

### 6. Change RTP Range

```bash
docker exec freepbx sed -i 's/^rtpstart=.*/rtpstart=2003/' /etc/asterisk/rtp.conf
docker exec freepbx sed -i 's/^rtpend=.*/rtpend=2100/' /etc/asterisk/rtp.conf
```

Also update in FreePBX DB:
```bash
docker exec freepbx-mariadb mariadb -u root -p<rootpass> asterisk -e \
  "INSERT INTO freepbx_settings (keyword, value, module, type) VALUES ('RTPSTART','2003','core','text') ON DUPLICATE KEY UPDATE value='2003';"
docker exec freepbx-mariadb mariadb -u root -p<rootpass> asterisk -e \
  "INSERT INTO freepbx_settings (keyword, value, module, type) VALUES ('RPEND','2100','core','text') ON DUPLICATE KEY UPDATE value='2100';"
```

### 7. Change Apache Web Admin Port to 2101

```bash
docker exec freepbx sed -i 's/Listen 80/Listen 2101/' /etc/apache2/ports.conf
docker exec freepbx sed -i 's/<VirtualHost \*:80>/<VirtualHost *:2101>/' /etc/apache2/sites-enabled/000-default.conf
docker exec -d freepbx apachectl restart
```

### 8. Restart Asterisk to Apply SIP/RTP Changes

PJSIP transports require a full Asterisk restart (reload won't re-bind ports):

```bash
docker exec freepbx bash -c '
  asterisk -rx "core stop now"
  sleep 3
  /usr/sbin/safe_asterisk -U asterisk -G asterisk &
  sleep 5
  asterisk -rx "pjsip show transports"
'
```

### 9. Fix Permissions (CRITICAL)

Apache in this image runs as **`asterisk`** user, NOT `www-data`. All web files must be owned by `asterisk`:

```bash
docker exec freepbx chown -R asterisk:asterisk /var/www/html
docker exec freepbx chown -R asterisk:asterisk /var/lib/php/sessions
```

**Symptom if wrong**: "Less.php cache directory isn't writable: /var/www/html/admin/assets/less/cache/"

### 10. Install Missing Modules

After first install, some modules may be missing (e.g., pm2):

```bash
docker exec freepbx bash -c '
  export PATH=$PATH:/var/lib/asterisk/bin
  fwconsole ma install pm2
  fwconsole reload
'
```

## Critical Pitfalls

1. **No MariaDB in image** — Must run separate MariaDB container on same network
2. **Missing #include files** — `pjsip_custom.conf` etc. must be `touch`'d or PJSIP silently fails with "No objects found"
3. **Apache runs as `asterisk`** — NOT `www-data`. All /var/www/html must be owned by asterisk
4. **`/etc/freepbx.conf` is ephemeral** — If not in a volume, it's lost on container recreation. Use `etc_data:/etc` volume mount
5. **`SIPPORT` DB setting is chan_sip only** — Does NOT affect PJSIP. Edit `pjsip.transports.conf` directly
6. **PJSIP transport port changes need full restart** — `core reload` won't re-bind transport ports
7. **`fwconsole` path** — Not in default PATH. Use `export PATH=$PATH:/var/lib/asterisk/bin`
8. **Docker compose plugin unavailable** — Use manual `docker run` or install `docker-compose` standalone
9. **RTP port range** — Large ranges (e.g. 16384-32767) exhaust Docker's port mapping. Use iptables DNAT or host networking instead
10. **`freepbx.conf` credentials** — Must match what's in the DB. Check `freepbx_settings` table for `AMPMGRUSER`/`AMPMGRPASS`

## Recreating freepbx.conf (if lost)

```bash
# First get actual credentials from DB:
docker exec freepbx-mariadb mariadb -u root -p<rootpass> asterisk -e \
  "SELECT keyword, value FROM freepbx_settings WHERE keyword IN ('AMPMGRUSER','AMPMGRPASS');"

# Then create the file:
docker exec freepbx bash -c 'cat > /etc/freepbx.conf << "EOF"
<?php
$amppath[0] = "/var/www/html";
$amp_conf["AMPDBENGINE"] = "mysql";
$amp_conf["AMPDBHOST"] = "127.0.0.1";
$amp_conf["AMPDBUSER"] = "asterisk";
$amp_conf["AMPDBPASS"] = "<dbpass>";
$amp_conf["AMPDBNAME"] = "asterisk";
$amp_conf["AMPDBPORT"] = "3306";
$amp_conf["AMPENGINE"] = "asterisk";
$amp_conf["AMPMGRUSER"] = "<from_db>";
$amp_conf["AMPMGRPASS"] = "<from_db>";
require_once("/var/www/html/admin/bootstrap.php");
EOF'
```

## References

- `references/escomputers-docker-compose.yaml` — Official docker-compose from escomputers/freepbx-docker (bridge network + iptables DNAT approach)
- `references/escomputers-run.sh` — Official run.sh script with RTP iptables rules and install command

## GitHub Repo

Skill maintained in: `icemellow-me/cybersecurity-skills` → `freepbx-docker/`

## Verification Checklist

- [ ] MariaDB healthy: `docker exec freepbx-mariadb healthcheck.sh`
- [ ] Asterisk running: `docker exec freepbx asterisk -rx "core show uptime"`
- [ ] PJSIP transports loaded: `docker exec freepbx asterisk -rx "pjsip show transports"`
- [ ] SIP on port 2000: Verify UDP listener
- [ ] Web admin accessible: `curl -s -o /dev/null -w "%{http_code}" http://<IP>:2101/admin/`
- [ ] Less cache writable: No "cache directory isn't writable" error
- [ ] RTP range set: `grep -E "^rtpstart|^rtpend" /etc/asterisk/rtp.conf`
