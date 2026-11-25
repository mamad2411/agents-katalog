---
name: "security-ownership-map"
description: "Analise repositórios git para construir uma topologia de propriedade de segurança (pessoas-para-arquivo), calcule fator de bus e propriedade de código sensível, e exporte CSV/JSON para bancos de dados de grafos e visualização. Ative apenas quando o usuário explicitamente quer uma análise de propriedade ou fator de bus orientada à segurança baseada no histórico de git (por exemplo: código sensível órfão, mantenedores de segurança, verificações de realidade do CODEOWNERS para risco, pontos críticos de sensibilidade, ou clusters de propriedade). Não ative para listas gerais de mantenedores ou questões de propriedade não relacionadas à segurança."
author: openai
---

# Mapa de Propriedade de Segurança

## Visão geral

Construa um grafo bipartido de pessoas e arquivos a partir do histórico de git, depois calcule risco de propriedade e exporte artefatos de grafo para Neo4j/Gephi. Também construa um grafo de co-mudança de arquivos (similaridade Jaccard em commits compartilhados) para agrupar arquivos por como se movem juntos enquanto ignora commits grandes e ruidosos.

## Requisitos

- Python 3
- `networkx` (obrigatório; detecção de comunidade está ativada por padrão)

Instale com:

```bash
pip install networkx
```

## Fluxo de trabalho

1. Defina o escopo do repositório e janela de tempo (opcional `--since/--until`).
2. Decida as regras de sensibilidade (use padrões ou forneça uma configuração CSV).
3. Construa o mapa de propriedade com `scripts/run_ownership_map.py` (grafo de co-mudança está ativo por padrão; use `--cochange-max-files` para ignorar commits de supernó).
4. Comunidades são computadas por padrão; saída graphml é opcional (`--graphml`).
5. Consulte as saídas com `scripts/query_ownership.py` para fatias JSON limitadas.
6. Persista e visualize (veja `references/neo4j-import.md`).

Por padrão, o grafo de co-mudança ignora arquivos comuns de "cola" (lockfiles, `.github/*`, configuração de editor) para que clusters reflitam movimento de código real em vez de edições de infra compartilhadas. Sobrescreva com `--cochange-exclude` ou `--no-default-cochange-excludes`. Commits do Dependabot são excluídos por padrão; sobrescreva com `--no-default-author-excludes` ou adicione padrões via `--author-exclude-regex`.

Se você quer excluir cola de compilação Linux como `Kbuild` do clustering de co-mudança, passe:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo /path/to/linux \
  --out ownership-map-out \
  --cochange-exclude "**/Kbuild"
```

## Início rápido

Execute a partir da raiz do repositório:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

Padrões: identidade de autor, data de autor e commits de merge excluídos. Use `--identity committer`, `--date-field committer` ou `--include-merges` se necessário.

Exemplo (sobrescrever exclusões de co-mudança):

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --cochange-exclude "**/Cargo.lock" \
  --cochange-exclude "**/.github/**" \
  --no-default-cochange-excludes
```

Comunidades são computadas por padrão. Para desativar:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --no-communities
```

## Regras de sensibilidade

Por padrão, o script marca caminhos comuns de auth/crypto/secret. Sobrescreva fornecendo um arquivo CSV:

```
# pattern,tag,weight
**/auth/**,auth,1.0
**/crypto/**,crypto,1.0
**/*.pem,secrets,1.0
```

Use com `--sensitive-config path/to/sensitive.csv`.

## Artefatos de saída

`ownership-map-out/` contém:

- `people.csv` (nós: pessoas)
- `files.csv` (nós: arquivos)
- `edges.csv` (arestas: toques)
- `cochange_edges.csv` (arestas de co-mudança arquivo-para-arquivo com peso Jaccard; omitido com `--no-cochange`)
- `summary.json` (achados de propriedade de segurança)
- `commits.jsonl` (opcional, se `--emit-commits`)
- `communities.json` (computado por padrão a partir de arestas de co-mudança quando disponível; inclui `maintainers` por comunidade; desative com `--no-communities`)
- `cochange.graph.json` (NetworkX node-link JSON com `community_id` + `community_maintainers`; retorna a `ownership.graph.json` se não houver arestas de co-mudança)
- `ownership.graphml` / `cochange.graphml` (opcional, se `--graphml`)

`people.csv` inclui detecção de fuso horário baseada em offsets de commit de autor: `primary_tz_offset`, `primary_tz_minutes` e `timezone_offsets`.

## Helper de consulta LLM

Use `scripts/query_ownership.py` para retornar fatias pequenas e limitadas em JSON sem carregar o grafo completo no contexto.

Exemplos:

```bash
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out person --person alice@corp --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out file --file crypto/tls
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file crypto/tls --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3
```

Use `--community-top-owners 5` (padrão) para controlar quantos mantenedores são armazenados por comunidade.

## Consultas básicas de segurança

Execute essas para responder questões comuns de propriedade de segurança com saída limitada:

```bash
# Código sensível órfão (obsoleto + baixo fator de bus)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code

# Proprietários ocultos para tags sensíveis
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section hidden_owners

# Pontos críticos sensíveis com baixo fator de bus
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section bus_factor_hotspots

# Arquivos auth/crypto com fator de bus <= 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag crypto --bus-factor-max 1

# Quem está tocando código sensível mais frequentemente
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --sort sensitive_touches --limit 10

# Vizinhos de co-mudança (dicas de cluster para deriva de propriedade)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file path/to/file --min-jaccard 0.05 --limit 20

# Mantenedores da comunidade (para um cluster)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3

# Mantenedores mensais para a comunidade contendo um arquivo
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --top 5

# Buckets trimestrais em vez de mensais
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --bucket quarter \
  --top 5
```

Notas:
- Toques padrão para um commit autenticado (não por arquivo). Use `--touch-mode file` para contar toques por arquivo.
- Use `--window-days 90` ou `--weight recency --half-life-days 180` para suavizar churn.
- Filtre bots com `--ignore-author-regex '(bot|dependabot)'`.
- Use `--min-share 0.1` para mostrar apenas mantenedores estáveis.
- Use `--bucket quarter` para agrupamentos de trimestre de calendário.
- Use `--identity committer` ou `--date-field committer` para alternar de atribuição de autor.
- Use `--include-merges` para incluir commits de merge (excluídos por padrão).

### Formato de resumo (padrão)

Use esta estrutura, adicione campos se necessário:

```json
{
  "orphaned_sensitive_code": [
    {
      "path": "crypto/tls/handshake.rs",
      "last_security_touch": "2023-03-12T18:10:04+00:00",
      "bus_factor": 1
    }
  ],
  "hidden_owners": [
    {
      "person": "alice@corp",
      "controls": "63% of auth code"
    }
  ]
}
```

## Persistência de grafo

Use `references/neo4j-import.md` quando você precisar carregar os CSVs em Neo4j. Inclui constraints, import Cypher e dicas de visualização.

## Notas

- `bus_factor_hotspots` em `summary.json` lista arquivos sensíveis com baixo fator de bus; `orphaned_sensitive_code` é o subconjunto obsoleto.
- Se `git log` é muito grande, restrinja com `--since` ou `--until`.
- Compare `summary.json` contra CODEOWNERS para destacar deriva de propriedade.