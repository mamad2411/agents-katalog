---
name: "PocketBase Deploy"
description: "Deploy em produção para PocketBase. Use ao fazer deploy do PocketBase em um servidor, configurar Docker, systemd, reverse proxy (nginx/Caddy), TLS, SMTP, backups, armazenamento S3, rate limiting ou hardening para produção. Fornece configs prontas para usar."
---

# Deploy em Produção do PocketBase

## Deploy com Binary Único

PocketBase é um único binary. Sem dependências de runtime.

```bash
# Download
wget https://github.com/pocketbase/pocketbase/releases/download/v0.X.X/pocketbase_0.X.X_linux_amd64.zip
unzip pocketbase_*.zip
chmod +x pocketbase

# Executar
./pocketbase serve --http="0.0.0.0:8090"
```

Dados armazenados em `pb_data/` (banco SQLite, arquivos enviados, logs).

## Serviço systemd

```ini
# /etc/systemd/system/pocketbase.service
[Unit]
Description=PocketBase
After=network.target

[Service]
Type=simple
User=pocketbase
Group=pocketbase
LimitNOFILE=4096
Restart=always
RestartSec=5s
WorkingDirectory=/opt/pocketbase
ExecStart=/opt/pocketbase/pocketbase serve --http="127.0.0.1:8090"

# Hardening de segurança
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/pocketbase/pb_data /opt/pocketbase/pb_hooks /opt/pocketbase/pb_migrations
PrivateTmp=true

# Limite de memória (ajuste ao seu servidor)
# MemoryMax=512M

[Install]
WantedBy=multi-user.target
```

```bash
# Setup
sudo useradd --system --no-create-home pocketbase
sudo mkdir -p /opt/pocketbase
sudo cp pocketbase /opt/pocketbase/
sudo chown -R pocketbase:pocketbase /opt/pocketbase

# Ativar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable pocketbase
sudo systemctl start pocketbase
sudo systemctl status pocketbase

# Logs
sudo journalctl -u pocketbase -f
```

### Limite de descritores de arquivo

Para deployments com alto tráfego, aumente o limite:

```ini
# Na seção [Service]:
LimitNOFILE=65535
```

Também defina no sistema em `/etc/security/limits.conf`:
```
pocketbase soft nofile 65535
pocketbase hard nofile 65535
```

### Limite de memória Go

Para ambientes com recursos restritos:

```ini
Environment=GOMEMLIMIT=400MiB
```

## Docker

### Dockerfile

```dockerfile
FROM alpine:latest

ARG PB_VERSION=0.25.0

RUN apk add --no-cache \
    unzip \
    ca-certificates

# Download e instale PocketBase
# NOTA: verifique o checksum em produção — veja https://github.com/pocketbase/pocketbase/releases
ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/ && rm /tmp/pb.zip

# Copie hooks e migrações
COPY ./pb_hooks /pb/pb_hooks
COPY ./pb_migrations /pb/pb_migrations

EXPOSE 8090

CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8090"]
```

### docker-compose.yml

```yaml
services:
  pocketbase:
    build: .
    ports:
      - "127.0.0.1:8090:8090"  # vinculado apenas a localhost — expor via reverse proxy
    volumes:
      - pb_data:/pb/pb_data
      - ./pb_hooks:/pb/pb_hooks
      - ./pb_migrations:/pb/pb_migrations
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8090/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  pb_data:
```

## Reverse Proxy

### Caddy (recomendado — TLS automático)

```
# /etc/caddy/Caddyfile
myapp.com {
    reverse_proxy localhost:8090
}
```

Pronto. Caddy gerencia certificados TLS automaticamente via Let's Encrypt.

### nginx

```nginx
# /etc/nginx/sites-available/pocketbase
server {
    listen 80;
    server_name myapp.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 50M;

    # Bloqueie acesso público ao painel de administração
    location /_/ {
        return 403;
    }

    location / {
        proxy_pass http://127.0.0.1:8090;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Suporte a SSE para realtime
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
    }
}
```

**Crítico para realtime**: `proxy_buffering off` e `proxy_read_timeout` devem estar configurados para que subscrições SSE funcionem.

```bash
# Let's Encrypt com nginx
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d myapp.com
```

## Configuração SMTP

Configure no Painel > Configurações > Configurações de email, ou via hooks:

```js
// pb_hooks/settings.pb.js
onBootstrap(function(e) {
    var settings = e.app.settings()
    settings.smtp.enabled = true
    settings.smtp.host = $os.getenv("SMTP_HOST")
    settings.smtp.port = parseInt($os.getenv("SMTP_PORT") || "587")
    settings.smtp.username = $os.getenv("SMTP_USER")
    settings.smtp.password = $os.getenv("SMTP_PASS")
    settings.smtp.tls = true  // STARTTLS
    // settings.smtp.authMethod = "PLAIN"  // ou "LOGIN"
    settings.meta.senderName = "My App"
    settings.meta.senderAddress = "noreply@myapp.com"
    e.app.save(settings)
    return e.next()
})
```

## Hardening de Segurança

### MFA para superusuário

Sempre ative MFA para contas de superusuário em produção:
Painel > Superusers > Opções de autenticação > MFA > Ativar

### Chave de criptografia de configurações

Criptografe configurações sensíveis (senhas SMTP, chaves S3) em repouso:

```bash
./pocketbase serve --encryptionEnv=PB_ENCRYPTION_KEY
```

Configure a variável de ambiente `PB_ENCRYPTION_KEY` com uma string aleatória de 32+ caracteres. Uma vez configurada, as configurações são criptografadas no banco de dados. **Não perca esta chave** — você não conseguirá descriptografar as configurações sem ela.

### Rate limiting

Limitador de taxa integrado (ativado por padrão). Configure no Painel > Configurações > Limites de taxa, ou:

```js
settings.rateLimits.enabled = true
settings.rateLimits.rules = [
    { label: "*:auth*", maxRequests: 10, duration: 300 },  // 10 tentativas de autenticação por 5 min
    { label: "POST:/api/collections/*/records", maxRequests: 50, duration: 60 },
]
```

### Oculte o painel em produção

```bash
./pocketbase serve --http="127.0.0.1:8090"  # vinculado apenas a localhost
```

Acesse o painel apenas via túnel SSH:
```bash
ssh -L 8090:127.0.0.1:8090 user@server
```

## Armazenamento S3

Para uploads de arquivos, transfira para armazenamento compatível com S3:

Painel > Configurações > Armazenamento de arquivos > S3

```js
// Ou via hooks:
onBootstrap(function(e) {
    var settings = e.app.settings()
    settings.s3.enabled = true
    settings.s3.bucket = $os.getenv("S3_BUCKET")
    settings.s3.region = $os.getenv("S3_REGION")
    settings.s3.endpoint = $os.getenv("S3_ENDPOINT")
    settings.s3.accessKey = $os.getenv("S3_ACCESS_KEY")
    settings.s3.secret = $os.getenv("S3_SECRET")
    settings.s3.forcePathStyle = true  // para MinIO/Backblaze
    e.app.save(settings)
    return e.next()
})
```

Provedores compatíveis: AWS S3, Backblaze B2, Cloudflare R2, MinIO, DigitalOcean Spaces, Wasabi.

## Backups

### Bancos pequenos (< 1GB)

Use o recurso de backup integrado:
- Painel > Configurações > Backups
- Ou via API: `POST /api/backups`
- Agendamento automático: configure cron no Painel

### Bancos grandes

O backup do Painel usa a API de backup online do SQLite (trava o banco brevemente). Para bancos grandes, use:

```bash
# Comando sqlite3 .backup (backup quente, travamento mínimo)
sqlite3 /opt/pocketbase/pb_data/data.db ".backup '/tmp/backup.db'"

# Depois rsync para servidor remoto
rsync -avz /tmp/backup.db backup-server:/backups/pocketbase/data-$(date +%Y%m%d).db
```

**Nunca copie o arquivo `.db` diretamente** enquanto PocketBase está em execução — pode estar em estado inconsistente.

### Script de backup

```bash
#!/bin/bash
# /opt/pocketbase/backup.sh
set -euo pipefail

BACKUP_DIR="/backups/pocketbase"
DB_PATH="/opt/pocketbase/pb_data/data.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup quente
sqlite3 "$DB_PATH" ".backup '${BACKUP_DIR}/data_${DATE}.db'"

# Também faça backup dos arquivos pb_data (uploads, se não usar S3)
tar -czf "${BACKUP_DIR}/pb_data_${DATE}.tar.gz" -C /opt/pocketbase pb_data --exclude='pb_data/data.db*'

# Retenha os últimos 30 dias
find "$BACKUP_DIR" -name "data_*.db" -mtime +30 -delete
find "$BACKUP_DIR" -name "pb_data_*.tar.gz" -mtime +30 -delete
```

```bash
# Crontab: diariamente às 2 AM
0 2 * * * /opt/pocketbase/backup.sh >> /var/log/pocketbase-backup.log 2>&1
```

## Health Check

```bash
curl http://localhost:8090/api/health
# {"code":200,"message":"API is healthy."}
```

## Checklist de Deploy

1. **Binary**: arquitetura correta (linux_amd64 / linux_arm64)
2. **systemd**: serviço ativado, LimitNOFILE configurado
3. **Reverse proxy**: Caddy ou nginx com TLS, proxy_buffering off para SSE
4. **SMTP**: configurado e testado (envie um email de verificação de teste)
5. **Superusuário**: senha forte + MFA ativado
6. **Chave de criptografia**: `--encryptionEnv` configurado para configurações sensíveis
7. **Backups**: automatizados diariamente, procedimento de restauração testado
8. **Rate limiting**: ativado com padrões sensatos
9. **Armazenamento de arquivos**: S3 configurado se esperar muitos uploads
10. **Monitoramento**: endpoint de health check monitorado, logs de journalctl revisados
11. **Firewall**: apenas 80/443 expostos, 8090 vinculado a localhost
12. **GOMEMLIMIT**: configurado se em VPS com recursos restritos