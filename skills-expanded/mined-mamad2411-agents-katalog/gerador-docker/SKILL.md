---
name: gerador-docker
description: Gera ou corrige Dockerfile e docker-compose.yml seguindo regras específicas do projeto. Use esta skill sempre que o usuário pedir para criar, gerar, corrigir ou revisar um Dockerfile ou docker-compose — mesmo que não use esses termos exatos. Também use quando o usuário mencionar "containerizar", "subir com docker", "configurar docker", "preparar docker", "criar imagem", "montar compose", ou qualquer variação que indique configuração de ambiente Docker para o projeto.
---

## O que esta skill faz

Gera Dockerfile e/ou docker-compose.yml do zero, ou corrige arquivos existentes, aplicando as regras abaixo sem pedir confirmação. Ao final, exibe um resumo das decisões tomadas.

---

## Regras obrigatórias

### 1. Multi-stage build em Node.js

- **Node.js puro (sem compilação):** proibido usar multi-stage build. Um único stage é suficiente — multi-stage aqui só adiciona complexidade sem benefício.
- **Node.js com TypeScript, webpack, esbuild, vite ou qualquer bundler:** multi-stage é permitido e recomendado. Compile no primeiro stage, copie apenas o artefato final para o segundo.

**Como detectar o contexto:**  
Leia `package.json` (ou `src/package.json`). Se houver `typescript`, `ts-node`, `webpack`, `esbuild`, `vite`, `rollup`, `parcel` em `dependencies` ou `devDependencies`, é um projeto com compilação.

### 2. Tag de imagem

- **Proibido** usar `latest`. Sempre especifique uma versão explícita (ex: `node:18-alpine`, `postgres:15-alpine`).
- **Prefira imagens Alpine** (`-alpine`) por serem mais enxutas. Use como padrão para Node.js e serviços de infraestrutura (postgres, redis, nginx, etc.).

### 3. Volumes no docker-compose

- Volumes devem usar **bind mount** — nunca volumes nomeados.
- O diretório de destino do bind mount deve sempre ser `.docker/` na raiz do projeto (ex: `.docker/postgres`, `.docker/redis`).
- Adicione `.docker/` ao `.gitignore` se ainda não estiver lá.

---

## Processo de execução

1. **Identifique o escopo:** o usuário quer Dockerfile, docker-compose, ou ambos?
2. **Leia o projeto:** verifique `package.json` (ou `src/package.json`) para detectar linguagem e tipo de build.
3. **Verifique arquivos existentes:** se Dockerfile ou docker-compose.yml já existem, leia-os e identifique violações.
4. **Gere ou corrija:** crie do zero ou aplique as correções necessárias diretamente, sem pedir confirmação.
5. **Atualize `.gitignore`:** se criou volumes, garanta que `.docker/` está no `.gitignore`.
6. **Exiba o resumo:** ao final, mostre uma tabela com as decisões tomadas.

---

## Resumo final (sempre exibir)

Após gerar ou corrigir os arquivos, mostre:

```
## Decisões aplicadas

| Regra | Situação | Ação |
|---|---|---|
| Multi-stage build | [contexto detectado] | [o que foi feito] |
| Tag de imagem | [tags utilizadas] | [ok / corrigido] |
| Volumes | [bind mount em .docker/] | [ok / criado / corrigido] |
| .gitignore | [.docker/ presente?] | [ok / adicionado] |
```

Se nenhum arquivo existia antes, indique "gerado do zero" na coluna Situação.
