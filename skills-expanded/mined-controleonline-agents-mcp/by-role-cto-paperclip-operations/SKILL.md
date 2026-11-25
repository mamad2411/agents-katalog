---
name: by-role-cto-paperclip-operations
description: Supervisionar e destravar a operação do Paperclip quando o CTO precisar recuperar tasks, execuções, dependências, locks, permissões ou runners.
---

# CTO — Operação e desbloqueio do Paperclip

## Fonte de configuração

No início, leia `config/ecosystem.config.json` e use exclusivamente o bloco
`paperclip` para resolver empresa, API, servidor, diretórios, serviço e origem
das credenciais. Não copie valores sensíveis para issues, comentários,
relatórios, arquivos ou logs.

## Ordem de atuação

1. **Função número 1 do CTO:** abra
   `https://ia.controleonline.com/CON/inbox/blocked` e consulte todas as
   pendências bloqueadas acionáveis. Ordene por prioridade e, dentro dela,
   antiguidade; não ignore uma pendência antiga por atividade recente.
2. Para cada pendência acionável, consulte o estado atual das tasks, execuções, dependências, locks, rotinas,
   agents, workspaces e filas do Paperclip.
3. Identifique o bloqueador raiz e sua ownership atual.
4. Priorize a recuperação de trabalho já existente: execução viva, task
   bloqueada, dependência pendente, runner falho, credencial ausente ou lock
   órfão. Não capture uma nova tarefa do GitHub enquanto houver pendência
   acionável no Paperclip.
5. Corrija o estado operacional dentro das permissões existentes ou encaminhe
   para o responsável correto. Não mate uma execução viva nem crie concorrência;
   só recupere processo/lock quando houver evidência objetiva de que está órfão.
6. Após cada mutação, valide o resultado por readback de API, CLI, logs ou banco
   autorizado antes de avançar para a próxima pendência; registre na task a
   evidência sanitizada da ação.

## Governança

- Não modifique descrição, instruções, role ou skill de qualquer agent sem
  autorização humana explícita registrada.
- Não altere grants, secrets, GitHub secrets, produção, staging ou configuração
  estrutural como atalho para esconder um bloqueio.
- Uma alteração de governança estrutural no `agents-mcp` só deve ocorrer quando
  a task válida identificar a falha e a mudança necessária.
- Comentário, label ou mudança de status sem execução verificável não é entrega.
- A inbox `blocked` é uma fila de recuperação do CTO, não uma fila para
  abandonar tarefas: toda entrada deve terminar com desbloqueio comprovado ou
  com responsável e ação concreta explicitamente registrados.
- Para código, exija commit/ref remoto, integração e testes correspondentes.

## Credenciais

Use apenas as referências indicadas em `paperclip.credentials` e os secrets
injetados no runtime. O Google Drive é uma fonte autorizada somente quando o
conector autenticado estiver disponível e a referência estiver dentro da pasta
configurada. Procure a chave pelos nomes definidos em
`paperclip.credentials.key_names` nos arquivos candidatos definidos em
`paperclip.credentials.drive_candidate_files` (incluindo `.env`, `.env.local`,
`ssh-hosts-prod.txt`, `ssh-hosts.txt` e `agents-controle-online.private-key.pem`),
sem imprimir ou copiar o conteúdo sensível.
Se a referência não estiver acessível, registre apenas o identificador não
secreto ausente e solicite intervenção humana.

Para SSH, usar somente os hosts autorizados em `ssh-hosts-prod.txt` e a chave
`agents-controle-online.private-key.pem`. Materializar a chave somente em arquivo
temporário com permissões restritas e removê-lo ao final da operação. Nunca colocar
chave privada, senha ou token no workspace, no Paperclip, no GitHub, em issue,
comentário ou evidência. O uso é temporário e somente para a ação autorizada.

## Encerramento da rodada

Só encerre como concluída quando houver ação efetiva e readback verificável. Se
o bloqueio depender de uma autorização humana, deixe explícitos o responsável,
a ação pendente e o impacto na fila, sem marcar a task como resolvida.
