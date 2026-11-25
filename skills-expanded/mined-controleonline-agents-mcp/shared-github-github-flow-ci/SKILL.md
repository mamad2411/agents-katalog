# GitHub Flow — CI

Este arquivo e apenas um complemento historico de CI. Ele **nao substitui** o
rito de Release Candidate definido em `shared-github-github-flow/SKILL.md` e
`shared-github-release-candidate/SKILL.md`.

## Regra atual

- `dev` recebe merges por task a partir de `task-{id}`.
- `staging` recebe somente RC congelada `rc/X.Y.Z-rc.N`.
- `master` recebe somente a mesma RC homologada em `Deploy`.
- `Security` e o gate ativo antes da revalidacao do Manager.
- `QA`, `Security`, `Design` e `UX` estao ativos: RC exige o quarteto `agent:qa:accepted` + `agent:security:accepted` + `agent:design:accepted` + `agent:ux:accepted`.
- Hotfix tambem precisa de RC congelada antes de master.
