# CLAUDE.md - STJ Dados Abertos

API para consulta de dados do STJ.

---

## Endpoints
- GET /api/stj/processos
- GET /api/stj/processo/{numero}

## Dependencias
- httpx para requests
- Redis para cache (opcional)

## NUNCA
- Fazer requests ao STJ sem cache check
- Ignorar rate limits da API do STJ

---

*Herdado de: ferramentas/CLAUDE.md*
