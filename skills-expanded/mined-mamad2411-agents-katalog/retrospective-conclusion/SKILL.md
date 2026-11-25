# Retrospective Conclusion

## Purpose
Finalises retrospective summary and converts improvement actions into properly structured backlog items.

## Role
Product Owner

## Phase
Retrospective

## Triggered By
PM `retrospective-facilitation` completes Stage 5.

## Inputs
- Improvement actions from the retro session

## CRITICAL RULE
Improvement actions ALWAYS go to Backlog. Next sprint assignment ONLY happens when Edward runs `/start`.

## Process
1. Review all improvement actions from retro session.
2. Write retrospective conclusion summary:
   - What went well (data-backed, reference metrics)
   - Pain points (data-backed, reference metrics)
   - Key decisions made this sprint
   - Top 3 improvement actions for next sprint
3. For each improvement action, create kanban card:
   - type: `story` or `task` (depending on scope)
   - title: `[Improvement] {specific action}`
   - body: problem identified, root cause, action, measure of success
   - priority: Must Ship / Should Ship / Can Hold
   - status: Backlog
4. Link all improvement cards to retro kanban card.
5. Signal PM: conclusion complete, backlog updated.

## Outputs
Retro conclusion summary, improvement kanban cards in Backlog.

## Quality Gates
- [ ] All improvement actions have kanban cards
- [ ] All cards set to Backlog status (never sprint)
- [ ] Cards linked to retro kanban card
- [ ] PM signalled

## References
- `.claude/skills/pm/retrospective-facilitation/SKILL.md`
- `.claude/skills/pm/release-scope-management/SKILL.md`
