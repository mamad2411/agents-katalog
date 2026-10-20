---
alwaysApply: true
description: "Docker-only Deployment-Vorgaben"
---

# Deployment

- Docker-only. Kein lokales Setup, kein bare-metal.
- VPS mit Nginx Reverse Proxy.
- Nur neueste stabile Software/Bibliotheken, keine Betas.
- docker-compose.yml für alle Services.
- .env definiert das Security-Niveau — NIE editieren, NIE in Code einbetten.
