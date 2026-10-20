---
description: Segurança, licença e operação do ASCEND Gym
alwaysApply: true
---

# ASCEND Gym

- Preserve a AGPL, os avisos de autoria e o link para o código correspondente.
- Nunca exponha arquivos de `data/`, `backups/`, `cloudflared/`, `.env` ou credenciais de IA.
- Trate desenvolvimento, push, release e deploy como ações independentes.
- A instância em `ci-runner:/opt/opengym` é best-effort e exige autorização explícita para deploy.
- Antes de alterar o runtime, faça backup e confirme branch, SHA, working tree e serviços existentes.
- Depois de um deploy autorizado, valide health, HTTPS, passkeys, logs e os demais serviços do host.
- Mantenha a beta por convite até concluir `docs/PUBLIC_LAUNCH_CHECKLIST.md`.
- Execute os testes focados e o build do frontend antes de afirmar prontidão.
