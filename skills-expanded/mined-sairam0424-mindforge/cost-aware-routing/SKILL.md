---
name: cost-aware-routing
version: 1.0.0
min_mindforge_version: 10.0.3
status: stable
triggers: token budget, model routing, cost optimization, model selection, Haiku, Flash, cheap model, expensive model, cost per token, budget, spend, token usage
---

# Skill — Cost-Aware Routing

## When this skill activates
When making model selection decisions, monitoring token spend, optimizing
for cost-performance tradeoffs, or when budget limits are approaching.

## Mandatory actions when this skill is active

### Model Tier Reference

| Tier | Model | Input/Output per 1M | Best For |
|------|-------|--------------------:|----------|
| simple | claude-haiku-4-5 | $0.25 / $1.25 | File reads, simple edits, formatting |
| standard | claude-sonnet-4-6 | $3 / $15 | Multi-file work, code review, daily tasks |
| complex | claude-opus-4-7 | $15 / $75 | Architecture, security, hard debugging |
| research | gemini-2.5-pro | $1.25 / $10 | Web research, long context, synthesis |
| consult | gpt-4o | $2.50 / $10 | Second opinions, alternative perspectives |

### Routing Rules

**Match task complexity to model tier:**
- Difficulty 1-3 (single file, obvious change): **simple**
- Difficulty 3-6 (multi-file, some judgment): **standard**
- Difficulty 6-8 (cross-system, complex logic): **complex**
- Difficulty 8-10 (architectural, novel problems): **complex**

**Override rules (always apply):**
- Security tasks: minimum **standard** (never use simple for auth/payment)
- Architecture decisions: minimum **complex**
- File exploration/reading: always **simple**
- Research requiring web access: **research**

### Cost Optimization Patterns

1. **Start cheap, escalate if needed:**
   - Try simple tier first for uncertain-complexity tasks
   - If result quality is insufficient: escalate to next tier
   - Log escalation with reason

2. **Batch similar tasks:**
   - 5 simple edits in one call < 5 separate calls
   - Group related file reads into single exploration

3. **Cache aggressively:**
   - Prompt caching reduces input costs ~90%
   - Structure prompts with static context first (cacheable)
   - Dynamic content last (not cached, but small)

4. **Avoid token waste:**
   - Don't re-read files already in context
   - Don't repeat instructions the model already has
   - Use compaction when context grows large

### Budget Monitoring

Check budget status regularly:
- Session budget remaining: from token-usage.jsonl
- Warning threshold: `[COST_WARN_USD]` from config
- Hard limit: `[COST_HARD_LIMIT_USD]` from config

**When budget is tight:**
- Downgrade all tasks one tier (complex→standard, standard→simple)
- Warn user: "Budget at X% — operating in economy mode"
- Never exceed hard limit without explicit user approval

### After any task
- Log actual model used + tokens consumed to token-usage.jsonl
- Compare actual vs optimal tier (for future routing accuracy)
- Report cost in session summary

## Self-check before task completion
- [ ] Did I log the model routing decision with rationale?
- [ ] Did I record actual token usage in token-usage.jsonl?
- [ ] Did I check remaining budget against session/project limits?
- [ ] Did I flag any tasks where a cheaper model could have been used?
