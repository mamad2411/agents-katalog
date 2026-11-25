---
name: gh-fix-ci
description: Inspecione verificações de PR no GitHub com gh, puxe logs com falha do GitHub Actions, resuma o contexto da falha e crie um plano de correção e implemente após aprovação do usuário. Use quando um usuário pedir para depurar ou corrigir verificações com falha de CI/CD em GitHub Actions e deseja um plano + mudanças de código; para verificações externas (ex: Buildkite), apenas informe a URL de detalhes e marque-as como fora do escopo.
metadata:
  short-description: Corrigir ações de CI do Github com falha
---

# Plano de Correção de Verificações de PR do GitHub

## Visão geral

Use gh para localizar verificações com falha no PR, busque logs do GitHub Actions para falhas acionáveis, resuma o snippet da falha e então proponha um plano de correção e implemente após aprovação explícita.
- Depende da skill `plan` para elaborar e aprovar o plano de correção.

Pré-requisito: certifique-se de que `gh` está autenticado (por exemplo, execute `gh auth login` uma vez) e depois execute `gh auth status` com permissões escaladas (inclua scopes de workflow/repo) para que os comandos `gh` funcionem. Se o sandboxing bloquear `gh auth status`, execute-o novamente com `sandbox_permissions=require_escalated`. Se o sandboxing bloquear `gh auth status`, execute-o novamente com `sandbox_permissions=require_escalated`.

## Entradas

- `repo`: caminho dentro do repositório (padrão `.`)
- `pr`: número ou URL do PR (opcional; assume o PR da branch atual)
- autenticação `gh` para o host do repositório

## Início rápido

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Adicione `--json` se desejar saída amigável para máquinas para resumo.

## Fluxo de trabalho

1. Verifique a autenticação do gh.
   - Execute `gh auth status` no repositório com scopes escalados (workflow/repo) após executar `gh auth login`.
   - Se o status de autenticação em sandbox falhar, reexecute o comando com `sandbox_permissions=require_escalated` para permitir acesso à rede/keyring.
   - Se não autenticado, peça ao usuário para fazer login antes de prosseguir.
2. Resolva o PR.
   - Prefira o PR da branch atual: `gh pr view --json number,url`.
   - Se o usuário fornecer um número ou URL do PR, use-o diretamente.
3. Inspecione verificações com falha (apenas GitHub Actions).
   - Preferido: execute o script incluído (lida com mudanças de campo gh e fallbacks de log de job):
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Adicione `--json` para saída amigável para máquinas.
   - Fallback manual:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - Se um campo for rejeitado, reexecute com os campos disponíveis informados por `gh`.
     - Para cada verificação com falha, extraia o id da execução de `detailsUrl` e execute:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - Se o log da execução disser que ainda está em andamento, busque logs de job diretamente:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. Defina o escopo de verificações não-GitHub Actions.
   - Se `detailsUrl` não for uma execução do GitHub Actions, rotule como externa e apenas informe a URL.
   - Não tente Buildkite ou outros provedores; mantenha o fluxo de trabalho enxuto.
5. Resuma as falhas para o usuário.
   - Forneça o nome da verificação com falha, URL da execução (se houver) e um snippet de log conciso.
   - Destaque logs ausentes explicitamente.
6. Crie um plano.
   - Use a skill `plan` para elaborar um plano conciso e solicitar aprovação.
7. Implemente após aprovação.
   - Aplique o plano aprovado, resuma diffs/testes e pergunte sobre abrir um PR.
8. Recheck status.
   - Após mudanças, sugira reexecutar os testes relevantes e `gh pr checks` para confirmar.

## Recursos Inclusos

### scripts/inspect_pr_checks.py

Busque verificações com falha no PR, puxe logs do GitHub Actions e extraia um snippet de falha. Sai com código diferente de zero quando falhas permanecem para que possa ser usado em automação.

Exemplos de uso:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`