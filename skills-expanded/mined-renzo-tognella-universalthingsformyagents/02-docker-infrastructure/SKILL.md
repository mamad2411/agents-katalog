---
name: Docker & Infrastructure
description: Configuração de containers Docker para Neo4j e Qdrant, healthchecks, volumes persistentes, e troubleshooting de infraestrutura local.
---

# Docker & Infrastructure

## Quando Usar

- Ao subir/derrubar serviços de infraestrutura
- Ao debugar problemas de conexão com Neo4j ou Qdrant
- Ao configurar novo ambiente de desenvolvimento

## Docker Compose de Referência

```yaml
version: "3.9"
services:
  neo4j:
    image: neo4j:5.26-community
    container_name: memory-neo4j
    ports:
      - "7474:7474"   # Browser UI
      - "7687:7687"   # Bolt protocol
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_dbms_security_procedures_unrestricted: apoc.*
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  qdrant:
    image: qdrant/qdrant:v1.13.2
    container_name: memory-qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "bash -lc \"exec 3<>/dev/tcp/127.0.0.1/6333 && printf 'GET /healthz HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n' >&3 && grep -q 'healthz check passed' <&3\"",
        ]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  neo4j_data:
  qdrant_data:
```

## Comandos Essenciais

```bash
# Subir serviços
docker compose up -d

# Verificar status
docker compose ps

# Ver logs
docker compose logs neo4j
docker compose logs qdrant

# Reiniciar serviço específico
docker compose restart neo4j

# Derrubar tudo (preserva dados)
docker compose down

# Derrubar tudo E apagar dados
docker compose down -v

# Verificar saúde
docker inspect --format='{{.State.Health.Status}}' memory-neo4j
docker inspect --format='{{.State.Health.Status}}' memory-qdrant
```

## Verificação de Conectividade

```bash
# Neo4j Browser
open http://localhost:7474
# Login: neo4j / password
# Rodar: RETURN 1 AS test

# Qdrant Dashboard
open http://localhost:6333/dashboard

# Qdrant healthcheck
curl http://localhost:6333/healthz
```

## Troubleshooting

| Problema | Causa Provável | Solução |
|----------|---------------|---------|
| Neo4j não inicia | Porta 7474/7687 em uso | `lsof -i :7474` → kill processo |
| Qdrant não inicia | Porta 6333 em uso | `lsof -i :6333` → kill processo |
| APOC não disponível | Plugin não carregou | Verificar `NEO4J_PLUGINS` no compose |
| Dados perdidos | Volumes não persistidos | Verificar `volumes:` no compose |
| "Connection refused" | Container não healthy | `docker compose logs <service>` |

## Regras

- Sempre usar `healthcheck` em todos os serviços
- Sempre usar volumes nomeados para persistência
- Nunca expor portas de produção em desenvolvimento sem necessidade
- APOC é obrigatório para `jaroWinklerDistance` na consolidação
