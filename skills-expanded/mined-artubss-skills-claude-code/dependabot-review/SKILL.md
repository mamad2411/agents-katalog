---
name: dependabot-review
description: Analise e gerencie PRs do Dependabot. Categoriza por risco, verifica status de CI, mescla automaticamente atualizações seguras e relata problemas. Use quando o usuário disser "revisar dependabot", "mesclar dependabot", "PRs dependabot" ou "atualizar dependências".
license: MIT
metadata:
  author: claude-code-templates
  version: "1.0.0"
---

# Análise de PR do Dependabot

Você é um especialista em gerenciamento de dependências. Seu trabalho é revisar todos os PRs abertos do Dependabot, avaliar riscos e tomar ações.

## Fluxo de Trabalho

### Etapa 1: Descoberta

Liste todos os PRs abertos do Dependabot:

```bash
gh pr list --author "dependabot[bot]" --state open --json number,title,labels,createdAt,headRefName --limit 50
```

Se nenhum PR for encontrado, informe o usuário e pare.

### Etapa 2: Classificação

Para cada PR, classifique-o em um nível de risco com base no nome da branch e no título:

| Nível | Critérios | Ação |
|-------|-----------|------|
| **Seguro** | Atualizações do GitHub Actions (`dependabot/github_actions/`), patches (`1.2.3` -> `1.2.4`) | Mesclar automaticamente |
| **Baixo Risco** | Bumps menores (`1.2.0` -> `1.3.0`) para bibliotecas bem conhecidas | Mesclar automaticamente após verificação de CI |
| **Requer Revisão** | Bumps maiores (`1.x` -> `2.x`), bibliotecas desconhecidas, PRs com tag de segurança | Relatar ao usuário |

Para determinar o tipo de bump, analise o título do PR. Os títulos do Dependabot seguem padrões como:
- `Bump X from 1.2.3 to 1.2.4` (patch)
- `Bump X from 1.2.0 to 1.3.0` (minor)
- `Bump X from 1.0.0 to 2.0.0` (major)

### Etapa 3: Verificação de CI

Para cada PR que você planeja mesclar, verifique o status de CI:

```bash
gh pr checks <number> --json name,state,bucket
```

- Se todos os testes **passarem**: prossiga com a mesclagem
- Se os testes estiverem **pendentes**: aguarde até 2 minutos (pesquise a cada 30s). Se ainda estiverem pendentes, ignore e relate como "CI pendente"
- Se algum teste **falhar**: ignore e relate ao usuário

### Etapa 4: Mesclar PRs Seguros

Para PRs classificados como Seguro ou Baixo Risco com CI aprovado:

```bash
gh pr merge <number> --merge --delete-branch
```

**Regras importantes:**
- Nunca force-merge
- Nunca mescle PRs com CI falhando
- Nunca mescle bumps de versão maior sem confirmação do usuário
- Mescle um por vez para evitar conflitos

### Etapa 5: Relatório

Após processar, apresente uma tabela de resumo ao usuário:

```
## Resumo de Análise do Dependabot

### Mesclados (X PRs)
| PR | Atualização | Tipo |
|----|-------------|------|
| #123 | actions/checkout v4 -> v6 | GitHub Actions |

### Requer Revisão (X PRs)
| PR | Atualização | Risco | Motivo |
|----|-------------|-------|--------|
| #456 | jest 29 -> 30 | Major | Mudanças importantes possíveis |

### Ignorados (X PRs)
| PR | Atualização | Motivo |
|----|-------------|--------|
| #789 | chalk 5.5 -> 5.6 | CI falhando |
```

## Proteções

- **Sempre verifique CI antes de mesclar** — nunca mescle PRs com falhas
- **Bumps maiores precisam de aprovação do usuário** — apresente o changelog e pergunte
- **Limire a taxa de mesclagens** — se houver mais de 10 PRs, processe em lotes de 5 e pergunte ao usuário antes de continuar
- **Tratamento de conflitos** — se uma mesclagem falhar por conflitos, ignore e relate. Não tente resolver conflitos
- **PRs de segurança** — se um PR tiver a label `security` ou mencionar um CVE, sempre sinalize para o usuário mesmo que seja um patch, para que ele fique ciente
- **Cascatas de rebase** — após mesclar vários PRs, os restantes podem precisar de rebase. Execute `gh pr list --author "dependabot[bot]"` novamente após cada lote para ver o status atualizado

## Padrões Comuns

**Mesclagem segura rápida (apenas GitHub Actions):**
O usuário diz "mesclar os PRs de actions" — filtre apenas branches `dependabot/github_actions/`.

**Revisão completa:**
O usuário diz "revisar dependabot" — execute o fluxo de trabalho completo acima.

**Execução de teste:**
O usuário diz "verificar dependabot" ou "mostrar PRs dependabot" — execute apenas as Etapas 1-2, relate a classificação sem mesclar.