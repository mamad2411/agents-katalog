---
name: local-validation
description: Use quando a tarefa exigir validação local no ecossistema Conn2Flow com Docker, tasks do workspace, token JWT, Phinx, MySQL ou leitura de logs.
---

# Validação local

Use esta skill quando a tarefa exigir sincronização do ambiente, execução de tasks, logs, migrações, token de teste ou checagens pontuais no banco.

## Ordem padrão

1. Escolha a menor validação capaz de falsificar a mudança.
2. Se a tarefa exigir ambiente atualizado, rode a task apropriada do workspace.
3. Se precisar autenticar no gestor, gere ou renove o token de teste.
4. Depois da edição, valide primeiro o slice tocado e só depois amplie escopo.
5. Use logs e consultas pontuais antes de partir para verificações maiores.

## Ajuste este arquivo por projeto

- Troque nomes de containers, tasks e paths pelo que existir no repositório real.
- Adicione aqui os comandos de sincronização, logs, banco e autenticação que o time usa todo dia.