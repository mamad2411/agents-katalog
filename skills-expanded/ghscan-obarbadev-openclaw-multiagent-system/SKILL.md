---
name: "daily_standup"
description: "Compila o progresso diário da squad para o canal do Discord."
---

# SKILL: DAILY_STANDUP

**Responsável:** Lead Agent
**Permissão:** role=lead
**Trigger:** cron diário às 23h00

---

## Protocolo

### 1. Coletar dados do GitHub

```bash
# Issues concluídas hoje
gh issue list --repo {repo} --state closed \
  --search "closed:$(date +%Y-%m-%d)" \
  --json number,title,closedAt,assignees

# Issues em progresso
gh issue list --repo {repo} --state open \
  --label "in_progress" \
  --json number,title,assignees,updatedAt

# Issues em review
gh issue list --repo {repo} --state open \
  --label "review" \
  --json number,title,assignees,updatedAt

# Issues bloqueadas
gh issue list --repo {repo} --state open \
  --label "blocked" \
  --json number,title,assignees,updatedAt

# PRs abertas (verificar paradas > 24h)
gh pr list --repo {repo} --state open \
  --json number,title,author,reviewDecision,updatedAt
```

### 2. Coletar dados do state.json

```bash
cat $HOME/.openclaw/workspace/projects/{project}/state.json | jq '{
  version,
  updated_at,
  agents: (.agents | to_entries | map({
    name: .key,
    role: .value.role,
    load: (.value.active_issues | length),
    capacity: .value.capacity
  })),
  issues_by_status: (.issues | to_entries | group_by(.value.status) |
    map({ status: .[0].value.status, count: length }))
}'
```

Verificar também bloqueios ativos via state.json com este detalhamento:

```bash
cat $HOME/.openclaw/workspace/projects/{project}/state.json | jq -r '.issues | to_entries[] | select(.value.status == "blocked") | .key'
```

### 3. Resolver Anomalias Notáveis (Opcional)

1. **Se encontrar Issue bloqueada ou PR travada > 24h**:
   a. Se bloqueio conversacional for resolúvel → disparar:
   `bash $HOME/.openclaw/workspace/scripts/state_engine.sh {project} {repo} {N} unblocked`
   b. Se crítico, escalar com alerta no Discord antes do relatório geral: `⚠️ Bloqueio: Issue #N parada há <tempo> — <motivo>`

### 4. Gerar relatório e postar no Discord

Monte o relatório e poste via `openclaw message send`:

```bash
LEAD_THREAD=$(jq -r '.discord.threads.lead // empty' ~/.openclaw/workspace/projects/{project}/state.json)
openclaw message send \
  --channel discord \
  --target "thread:$LEAD_THREAD" \
  --message "$(cat <<'MSG'
📊 DAILY STANDUP — {projeto} — {data}

✅ Concluído hoje ({N})
  • #{numero} Título da issue

🔄 Em desenvolvimento ({N})
  • #{numero} Título → developer-X (atualizado há Xh)

👀 Em revisão ({N})
  • #{numero} Título → reviewer (há Xh)

🚨 Bloqueado ({N})
  • #{numero} Título — motivo

📈 Capacidade da squad
  • developer-1: X/1 issues

🔮 Backlog estimado: X issues pendentes
MSG
)"
```

### 5. Atualizar WORKING_LEAD.md e DAILY_LOG.md

Persistir o relatório em:

```bash
echo "[{data}] ..." >> $HOME/.openclaw/workspace/projects/{project}/memory/DAILY_LOG.md
```

### 6. Verificar saúde do sistema

```bash
$HOME/.openclaw/workspace/scripts/health_check.sh {project}
```

Se houver warnings críticos, postar alerta adicional no Discord.

---

## Regras

- Sempre baseado em dados reais do GitHub + state.json
- Nunca inventar status
- Se health-check retornar erro, escalar imediatamente
