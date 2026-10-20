---
name: cloudflare-ness
description: Convencoes de Cloudflare do ambiente — tunnel em vez de porta exposta, R2 para backup e artefato grande, nomenclatura de subdominio e escopo minimo de token. Use ao expor servico, criar bucket, emitir token ou mexer em DNS.
---

# cloudflare-ness

## Exposicao de servico

Tunnel, sempre. **Nenhuma porta publica** — a politica de entrada do UFW e `deny`, inclusive para a 22.
Servico novo entra como ingress no tunnel existente, nao como porta aberta e nao como segundo tunnel.

Todo hostname fica atras de Zero Trust Access com a politica de e-mail. Excecao (algo publico de fato)
e decisao do Ricardo, registrada — nao inferida por conveniencia de teste.

## Nomenclatura de subdominio

Zona `esper.ws`, um subdominio por projeto, sem sufixo de ambiente:

| Uso | Forma | Exemplo |
|---|---|---|
| Acesso administrativo | `<funcao>.esper.ws` | `ssh.esper.ws`, `painel.esper.ws` |
| Preview de aplicacao | `<projeto>.esper.ws` | `niso.esper.ws` |
| Preview de branch | `<branch>.<projeto>.esper.ws` | `feat-login.niso.esper.ws` |

Producao de cliente nao mora aqui — `esper.ws` e ambiente de desenvolvimento.

## R2

Backup do restic e artefato grande (evidencia, midia, dataset) vao para R2, nunca para o repositorio
nem para `data/` esperando backup manual. Um bucket por proposito, nome em `kebab-case` com o projeto
na frente (`niso-evidence`, `bekaa-storage`).

## Token

- **Nunca** Global API Key. Sempre token com escopo minimo e recursos restritos a conta e a zona que precisam.
- Um token por proposito. Token de automacao de tunnel nao serve para mexer em DNS de producao.
- Escopo tipico deste ambiente: `Cloudflare Tunnel: Edit`, `Access: Apps and Policies: Edit`,
  `Workers R2 Storage: Edit` na conta, e `DNS: Edit` restrito a `esper.ws`.
- Token vive em `/srv/dev/secrets/.env`, modo 600. Chamada de API roda **na VPS**, lendo dali —
  assim o valor nao transita por maquina local nem por transcript de agente.
- Token que apareceu em chat, log ou captura de tela e token rotacionado, nao token apagado.
