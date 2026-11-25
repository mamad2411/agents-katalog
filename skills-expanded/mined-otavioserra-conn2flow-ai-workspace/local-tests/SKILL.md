---
name: local-tests
description: Use quando a tarefa exigir testes locais no ecossistema Conn2Flow após alguma implementação de módulos, páginas, ou funcionalidades.
user-invocable: false
---

# Testes locais

Use esta skill quando a tarefa exigir testes para validação das implementações.

## Ordem padrão

1. Use a menor rotina de deploy, sincronização ou publish necessária para levar a mudança ao ambiente local de testes.
2. Acesse o ambiente de testes apenas depois de confirmar que os arquivos certos foram sincronizados.
3. Use logs, banco e checagens pontuais antes de partir para verificações maiores.
4. Feche a rodada com um checklist curto dos testes executados e do que ficou pendente.

## Ajuste este arquivo por projeto

- Troque nomes de tasks, scripts e URLs pelos equivalentes reais do repositório.
- Se o projeto usar `environment.json`, Docker local ou deploy via API, documente aqui o caminho operacional preferido.