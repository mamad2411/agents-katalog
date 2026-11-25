---
name: using-neon
description: Guias e melhores práticas para trabalhar com Neon Serverless Postgres. Cobre introdução, desenvolvimento local com Neon, escolha de método de conexão, recursos do Neon, autenticação (@neondatabase/auth), API de dados estilo PostgREST (@neondatabase/neon-js), Neon CLI e Platform API/SDKs do Neon. Use para qualquer pergunta relacionada a Neon.
---

# Neon Serverless Postgres

Neon é uma plataforma Postgres serverless que separa compute e storage para oferecer autoscaling, branching, instant restore e scale-to-zero. É totalmente compatível com Postgres e funciona com qualquer linguagem, framework ou ORM que suporte Postgres.

## Documentação do Neon

Sempre consulte a documentação do Neon antes de fazer afirmações relacionadas ao Neon. A documentação é a fonte única de verdade para todas as informações relacionadas ao Neon.

Abaixo você encontrará uma lista de recursos organizados por área de interesse. Isso foi criado para ajudar você a encontrar as páginas de documentação corretas e adicionar um pouco de contexto adicional.

Você pode usar os comandos `curl` para buscar a página de documentação como markdown:

**Documentação:**

```bash
# Obter lista de todos os documentos do Neon
curl https://neon.tech/llms.txt

# Buscar qualquer página de documentação como markdown
curl -H "Accept: text/markdown" https://neon.tech/docs/<path>
```

Não adivinhe páginas de documentação. Use o índice `llms.txt` para encontrar a URL relevante ou siga os links nos recursos abaixo.

## Visão Geral dos Recursos

Consulte o arquivo de recurso apropriado com base nas necessidades do usuário:

### Guias Principais

| Área               | Recurso                            | Quando Usar                                               |
| ------------------ | ---------------------------------- | --------------------------------------------------------- |
| O que é Neon       | `references/what-is-neon.md`       | Entender conceitos, arquitetura e recursos principais do Neon |
| Consultando Docs   | `references/referencing-docs.md`   | Procurar documentação oficial, verificar informações      |
| Recursos           | `references/features.md`           | Branching, autoscaling, scale-to-zero, instant restore   |
| Introdução         | `references/getting-started.md`    | Configurar um projeto, connection strings, dependências, schema |
| Métodos de Conexão | `references/connection-methods.md` | Escolher drivers com base na plataforma e runtime         |
| Ferramentas para Desenvolvedor | `references/devtools.md`           | Extensão VSCode, servidor MCP, Neon CLI (`neon init`)    |

### Drivers de Banco de Dados & ORMs

Queries HTTP/WebSocket para funções serverless/edge.

| Área               | Recurso                        | Quando Usar                                     |
| ------------------ | ------------------------------ | ----------------------------------------------- |
| Serverless Driver  | `references/neon-serverless.md` | `@neondatabase/serverless` - queries HTTP/WebSocket |
| Drizzle ORM        | `references/neon-drizzle.md`    | Integração Drizzle ORM com Neon                 |

### Auth & Data API SDKs

Autenticação e API de dados estilo PostgREST para Neon.

| Área         | Recurso                   | Quando Usar                                                    |
| ------------ | ------------------------- | -------------------------------------------------------------- |
| Neon Auth    | `references/neon-auth.md` | `@neondatabase/auth` - Autenticação apenas                     |
| Neon JS SDK  | `references/neon-js.md`   | `@neondatabase/neon-js` - Auth + Data API (queries estilo PostgREST) |

### Neon Platform API & CLI

Gerenciar recursos do Neon programaticamente via REST API, SDKs ou CLI.

| Área                  | Recurso                            | Quando Usar                                     |
| --------------------- | ---------------------------------- | ----------------------------------------------- |
| Visão Geral Platform API | `references/neon-platform-api.md`   | Gerenciar recursos do Neon via REST API         |
| Neon CLI              | `references/neon-cli.md`            | Workflows no terminal, scripts, pipelines CI/CD |
| TypeScript SDK        | `references/neon-typescript-sdk.md` | `@neondatabase/api-client`                      |
| Python SDK            | `references/neon-python-sdk.md`     | Pacote `neon-api`                               |