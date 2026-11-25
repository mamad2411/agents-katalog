---
name: hosting-deployment-indonesia
description: Use when deploying Laravel or Node.js to Indonesian VPS (IDCloudHost, Niagahoster, Rumahweb, Biznet Gio) or shared hosting with cPanel. Triggers on "deploy Laravel", "setup VPS", "Nginx reverse proxy", "Supervisor queue worker", "Let's Encrypt SSL", "database backup", "deploy ke IDCloudHost", "setup cPanel", "zero downtime deployment"
---

# Hosting & Deployment Indonesia

## Overview

Deploy aplikasi Laravel atau Node.js ke VPS Indonesia (IDCloudHost, Niagahoster,
Rumahweb, Biznet Gio) atau shared hosting cPanel. Skill ini menutup pain point
yang paling sering terlewat: config Supervisor, renewal SSL, Nginx reverse
proxy, dan backup database.

Dua jalur: **VPS** (kontrol penuh, Nginx + Supervisor) sebagai utama, dan
**shared hosting cPanel** sebagai alternatif.

## When to Use

- "deploy Laravel" atau "setup VPS" ke IDCloudHost/Niagahoster/Rumahweb/Biznet Gio
- "Nginx reverse proxy" untuk Node.js
- "Supervisor queue worker" untuk Laravel
- "Let's Encrypt SSL" + auto-renewal
- "database backup" automation dan restore
- "deploy ke IDCloudHost" / "setup cPanel"
- "zero downtime deployment"
- Butuh langkah server setup yang command/config-nya sering lupa

**Jangan pakai kalau:**

- Deploy ke cloud platform (AWS, GCP, Azure) — workflow berbeda.
- Docker/Kubernetes — tooling berbeda.
- Serverless — tidak ada server yang dikelola.

## Router

| Topik / tugas | Berkas |
| --- | --- |
| Setup awal VPS, hardening, firewall, SSH | `references/initial-server-setup.md` |
| Instalasi stack PHP 8.2 / Node.js + PM2 | `references/stack-installation.md` |
| Nginx: server block Laravel & reverse proxy Node.js | `references/nginx-reverse-proxy.md` |
| SSL Let's Encrypt, renewal, troubleshooting | `references/ssl-letsencrypt.md` |
| Deploy aplikasi Laravel/Node.js, `.env`, PM2 | `references/application-deployment.md` |
| Supervisor queue worker, multi-queue, Horizon | `references/supervisor-config.md` |
| Backup & restore database, rclone | `references/database-backup.md` |
| Zero-downtime, blue-green, rollback | `references/zero-downtime-deployment.md` |
| Shared hosting cPanel (Laravel & Node.js) | `references/cpanel-deployment.md` |

## Core Principles

1. **Otomatiskan deployment.** Langkah manual berulang cepat lupa satu; bungkus
   jadi script yang bisa diulang dan punya rollback.
2. **Pisahkan config per environment.** Nilai production ada di `.env`, bukan
   hardcoded di config atau repo.
3. **Jangan jalankan aplikasi sebagai root.** Pakai user khusus (mis. `deploy`).

   ```bash
   sudo -u deploy php artisan queue:work
   ```

4. **Backup dan SSL adalah bagian dari deploy**, bukan langkah opsional: cron
   backup + auto-renewal harus aktif sebelum aplikasi dianggap live.

## Workflow

1. Siapkan VPS: user non-root, SSH key, firewall, swap, timezone.
   → detail: `references/initial-server-setup.md`
2. Pasang stack sesuai runtime (PHP 8.2/Composer/MySQL/Redis atau Node.js/PM2).
   → detail: `references/stack-installation.md`
3. Konfigurasi Nginx: server block Laravel atau reverse proxy Node.js, lalu `nginx -t`.
   → detail: `references/nginx-reverse-proxy.md`
4. Pasang SSL Let's Encrypt, redirect HTTP→HTTPS, uji `certbot renew --dry-run`.
   → detail: `references/ssl-letsencrypt.md`
5. Deploy aplikasi: dependency, `.env`, migrate, cache, permission, PM2.
   → detail: `references/application-deployment.md`
6. Jalankan queue worker lewat Supervisor dan restart setelah tiap deploy.
   → detail: `references/supervisor-config.md`
7. Otomatiskan backup database + retention, lalu uji restore.
   → detail: `references/database-backup.md`
8. Ganti deploy manual dengan script zero-downtime (maintenance mode / PM2 reload).
   → detail: `references/zero-downtime-deployment.md`
9. Kalau targetnya shared hosting, ikuti jalur cPanel dan batasannya.
   → detail: `references/cpanel-deployment.md`

## Anti-Patterns

- Menjalankan app/queue sebagai root (`sudo php artisan queue:work`).
- Node.js tanpa process manager (`node app.js &`) — pakai PM2 + `pm2 save` + `pm2 startup`.
- Kredensial hardcoded di config/repo; `.env.example` harus berisi nilai kosong.
- Deploy tanpa backup database dan tanpa rencana rollback.
- `systemctl reload nginx` tanpa `nginx -t` lebih dulu.
- Memaksakan Node.js/WebSocket di shared hosting yang tidak mendukung.
- Deploy manual step-by-step tanpa script.

## Verification

- [ ] Initial server setup complete (non-root user, firewall, SSH hardened)
- [ ] Stack installed (PHP/Node.js, database, Nginx)
- [ ] Nginx configured dan tested (`sudo nginx -t`)
- [ ] SSL certificate obtained dan auto-renewal working
- [ ] Application deployed dan accessible
- [ ] Queue workers running (Laravel - check `sudo supervisorctl status`)
- [ ] Database backup automated (check cron, test restore)
- [ ] Deploy script created dan tested
- [ ] Logs accessible dan monitored
- [ ] DNS pointing to VPS dengan correct A record

## References

- `references/initial-server-setup.md` — hardening VPS: SSH, firewall, fail2ban, swap, timezone.
- `references/stack-installation.md` — instalasi PHP 8.2/Composer/MySQL/Redis dan Node.js/PM2.
- `references/nginx-reverse-proxy.md` — server block Laravel, reverse proxy Node.js, WebSocket, load balancing, tuning.
- `references/ssl-letsencrypt.md` — setup Certbot, auto-renewal, wildcard, renewal hooks, troubleshooting.
- `references/application-deployment.md` — deploy Laravel/Node.js, `ecosystem.config.js`, config `.env`.
- `references/supervisor-config.md` — config worker, multi-queue, Horizon, monitoring, tuning.
- `references/database-backup.md` — script backup MySQL/PostgreSQL, cron, restore, rclone.
- `references/zero-downtime-deployment.md` — deploy script, blue-green, migrasi aman, health check.
- `references/cpanel-deployment.md` — Git/FTP deploy, `.htaccess`, cron scheduler, AutoSSL, batasan vs VPS.

## Related Skills

- `security-and-hardening` - Untuk server security audit
- `observability-and-instrumentation` - Untuk monitoring & logging
- `ci-cd-and-automation` - Untuk automated deployment pipelines
