---
name: sky-linux-server
description: >-
  VPS / Linux sunucu yönetimi: ilk kurulum ve sertleştirme (SSH anahtar, root girişi kapalı,
  ufw, fail2ban, otomatik güvenlik güncellemeleri), kullanıcı ve izinler, systemd servisleri
  ve zamanlayıcıları, Caddy/Nginx reverse proxy ve TLS, journalctl ve log rotasyonu, disk/
  bellek/süreç izleme, swap, yedekleme (restic), Coolify/Dokploy ile PaaS deneyimi ve sık
  sorunlar. Hetzner/DigitalOcean/Contabo vb. VPS'te bir şey kurarken kullan.
disable-model-invocation: true
---

# Sky · Linux Sunucu

## İlk 15 dakika (Ubuntu/Debian)

```bash
# 1) güncelle
apt update && apt full-upgrade -y
# 2) kullanıcı
adduser deploy && usermod -aG sudo deploy
mkdir -p /home/deploy/.ssh && cp ~/.ssh/authorized_keys /home/deploy/.ssh/ && chown -R deploy: /home/deploy/.ssh && chmod 700 /home/deploy/.ssh
# 3) SSH sertleştirme: /etc/ssh/sshd_config.d/hardening.conf
#    PermitRootLogin no
#    PasswordAuthentication no
#    KbdInteractiveAuthentication no
systemctl reload ssh            # ÖNCE yeni oturumda deploy ile girişi test et, sonra mevcut oturumu kapat
# 4) güvenlik duvarı
ufw allow OpenSSH && ufw allow 80,443/tcp && ufw enable
# 5) otomatik güvenlik güncellemeleri + kaba kuvvet koruması
apt install -y unattended-upgrades fail2ban && dpkg-reconfigure -plow unattended-upgrades
```
Saat dilimi: `timedatectl set-timezone Europe/Istanbul` (loglarda yerel saat istiyorsan; uygulamalar UTC saklamalı).
Küçük RAM'li sunucuda swap: `fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile` (+ fstab).

**Dikkat:** SSH ve güvenlik duvarı değişikliklerinde mevcut oturumu açık tut; kendini kilitlersen sağlayıcının web konsolu tek çıkış yolu.

## systemd servisi

```ini
# /etc/systemd/system/api.service
[Unit]
Description=Sky API
After=network-online.target
Wants=network-online.target

[Service]
User=deploy
WorkingDirectory=/srv/api
EnvironmentFile=/srv/api/.env
ExecStart=/srv/api/bin/api
Restart=on-failure
RestartSec=3
# sertleştirme
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/srv/api/data
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload && systemctl enable --now api
systemctl status api && journalctl -u api -f --since "10 min ago"
```
Cron yerine **systemd timer** (`api-backup.timer` + `.service`): log, hata durumu, kaçırılanları çalıştırma (`Persistent=true`).

## Reverse proxy

Caddy (otomatik HTTPS) en kolayı — örnek `sky-deploy`'da. Nginx tercih edilirse:
```nginx
server {
  server_name app.example.com;
  location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;       # WebSocket
    proxy_set_header Connection "upgrade";
  }
  client_max_body_size 20m;
}
```
+ `certbot --nginx -d app.example.com`. Uygulamalar yalnızca `127.0.0.1`'e bağlansın; dışarıya proxy açık.

## İzleme ve teşhis

```bash
df -h; du -sh /var/* | sort -h | tail       # disk (en sık kesinti sebebi: dolu disk)
free -h; htop                                 # bellek/CPU
ss -tlnp                                      # dinleyen portlar
journalctl --disk-usage; journalctl --vacuum-time=14d
docker system df; docker system prune         # Docker kullanıyorsan (önce ne silineceğine bak)
```
Uptime ve disk alarmı dışarıdan (bkz. `sky-observability`); Netdata / Beszel hafif sunucu panoları.

## Yedekleme

`restic` → S3/R2/B2: şifreli, artımlı, tekilleştirilmiş. Postgres için önce `pg_dump` (veya `pg_dumpall`), sonra restic; timer ile gece;
`restic check` ve **ayda bir geri yükleme denemesi**. Sağlayıcı snapshot'ları ek güvenlik, tek önlem değil.

## PaaS deneyimi kendi sunucunda

**Coolify** / **Dokploy**: Git push → build → deploy, SSL, veritabanları, yedekler, önizleme ortamları — VPS fiyatına Heroku hissi.
Tek sunucu tek hata noktasıdır: kritik üretimde yedekli kurulum veya yönetilen platform.

## Sık sorunlar

| Belirti | Bak |
|---|---|
| Site açılmıyor | `systemctl status`, `ss -tlnp`, `ufw status`, DNS |
| 502 Bad Gateway | uygulama ayakta mı, doğru porta mı proxy'leniyor |
| Disk doldu | loglar, Docker imajları, eski yedekler |
| Süreç ölüyor | `journalctl -u api`, `dmesg | grep -i oom` (OOM killer) |
| SSL yenilenmiyor | `certbot renew --dry-run`, 80 portu açık mı |
