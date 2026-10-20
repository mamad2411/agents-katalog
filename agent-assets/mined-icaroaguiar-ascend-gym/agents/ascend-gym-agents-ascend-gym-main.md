# ASCEND Gym

- Preserve `LICENSE`, `NOTICE.md`, autoria e o link de código-fonte em mudanças públicas.
- Trate `data/`, `backups/`, `cloudflared/`, `.env` e caches de provedores como dados privados.
- Nunca leia, imprima, copie, versione ou fotografe `data/codex/auth.json`, `data/secret` ou dados de usuários.
- O runtime de referência fica em `ci-runner:/opt/opengym`; o checkout local não prova o estado remoto.
- Desenvolvimento, push, release e deploy são ações separadas. Deploy exige autorização explícita.
- A instância roda em notebook e rede residenciais, sem SLA ou garantia de uptime.
- Antes de deploy: confirme branch/SHA/working tree, gere backup e registre a mudança.
- Depois de deploy: valide Compose, logs, health, HTTPS, passkey e preservação dos demais serviços.
- Não reinicie o host, remova volumes, execute prune ou altere SSH, Tailscale, firewall e DNS sem escopo explícito.
- Use Portly somente para servidores locais de desenvolvimento no Mac; não para o runtime remoto.
- Mantenha cadastro por convite até os bloqueadores de `docs/PUBLIC_LAUNCH_CHECKLIST.md` estarem resolvidos.
- Mudanças em treino, progressão, importação, auth, privacidade ou Coach precisam de testes focados.
- Rode `npm test` e `npm run build` em `frontend/`; rode `npm test` em `api/`.
- Workflows de publicação permanecem manuais até autorização de release.
