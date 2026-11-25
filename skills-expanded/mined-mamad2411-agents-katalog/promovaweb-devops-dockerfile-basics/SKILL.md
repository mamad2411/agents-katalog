---
name: promovaweb-devops-dockerfile-basics
description: Aprenda os fundamentos do Dockerfile e as melhores práticas para criar imagens de container prontas para produção
license: MIT
metadata:
  author: promovaweb
  version: "1.1"
---

# Skill de Fundamentos de Dockerfile

Domine os fundamentos do Dockerfile e as melhores práticas de 2024-2025 para criar imagens de container seguras e otimizadas.

## Propósito

Fornecer orientação abrangente sobre a sintaxe do Dockerfile, ordenação de instruções, otimização de camadas (layers) e melhores práticas de segurança.

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|---------|-------------|
| base_image | string | Não | - | Imagem base a ser utilizada |
| language | string | Não | - | Linguagem de programação (node/python/go/java) |
| optimize | boolean | Não | true | Aplicar recomendações de otimização |

## Instruções Principais

### Referência de Instruções

| Instrução | Propósito | Exemplo |
|-------------|---------|---------|
| FROM | Imagem base | `FROM node:20-alpine` |
| WORKDIR | Define o diretório de trabalho | `WORKDIR /app` |
| COPY | Copia arquivos | `COPY package*.json ./` |
| RUN | Executa um comando | `RUN npm ci` |
| ENV | Define variáveis de ambiente | `ENV NODE_ENV=production` |
| EXPOSE | Documenta a porta | `EXPOSE 3000` |
| USER | Define o usuário | `USER appuser` |
| CMD | Comando padrão | `CMD ["node", "app.js"]` |
| ENTRYPOINT | Comando fixo | `ENTRYPOINT ["./start.sh"]` |
| HEALTHCHECK | Verificação de integridade | `HEALTHCHECK CMD curl -f http://localhost/` |

### Ordem de Otimização de Camadas (Layers)

```dockerfile
# 1. Imagem base (mais estável)
FROM node:20-alpine

# 2. Dependências do sistema
RUN apk add --no-cache curl

# 3. Criar usuário (segurança)
RUN addgroup -g 1001 app && adduser -u 1001 -G app -D app

# 4. Definir diretório de trabalho
WORKDIR /app

# 5. Copiar arquivos de dependência (camada de cache)
COPY package*.json ./

# 6. Instalar dependências
RUN npm ci --only=production

# 7. Copiar código da aplicação (mais volátil)
COPY --chown=app:app . .

# 8. Mudar para usuário não-root
USER app

# 9. Health check
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:3000/health || exit 1

# 10. Comando padrão
CMD ["node", "server.js"]
```

## Melhores Práticas (2024-2025)

### Essenciais de Segurança

```dockerfile
# Sempre use tags de versão específicas
FROM node:20.10-alpine  # Bom
# FROM node:latest      # Ruim

# Executar como usuário não-root
USER nonroot

# Usar multi-stage builds
FROM node:20 AS builder
# ... passos de build ...
FROM node:20-alpine AS runtime
COPY --from=builder /app/dist ./
```

### Técnicas de Otimização

```dockerfile
# Combinar comandos RUN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Usar .dockerignore
# node_modules, .git, *.md, etc.

# Aproveitar BuildKit cache mounts
RUN --mount=type=cache,target=/root/.npm npm ci
```

## Tratamento de Erros

### Erros Comuns

| Erro | Causa | Solução |
|-------|-------|----------|
| `COPY failed: file not found` | Arquivo fora do contexto | Verifique o .dockerignore |
| `returned non-zero code: 127` | Comando não encontrado | Instale o pacote primeiro |
| `permission denied` | Executando como não-root | Use COPY --chown |

### Comandos de Validação

```bash
# Lint do Dockerfile
hadolint Dockerfile

# Build sem cache
docker build --no-cache -t app:test .

# Inspecionar camadas (layers)
docker history app:test
```

## Solução de Problemas (Troubleshooting)

### Checklist de Depuração

- [ ] O .dockerignore exclui arquivos desnecessários?
- [ ] A tag da imagem base é específica (não :latest)?
- [ ] As dependências foram copiadas antes do código-fonte?
- [ ] O usuário não-root está configurado?
- [ ] HEALTHCHECK está definido?

### Problemas Comuns

| Sintoma | Causa | Correção |
|---------|-------|-----|
| Tamanho grande da imagem | Sem multi-stage | Adicione um estágio de build |
| Builds lentos | Ordem de camadas ruim | Mova o COPY para depois das dependências |
| Avisos de segurança | Usuário root | Adicione a instrução USER |

## Uso

```
Skill("dockerfile-basics")
```

## Skills Relacionadas

- docker-multi-stage
- docker-optimization
- docker-security
