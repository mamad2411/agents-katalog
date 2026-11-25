# MCP Maker — Superpowers + GSD

Todas as diretivas operacionais estao DENTRO do MCP server (maker-flow-engine).
Ao iniciar qualquer sessao, chame `gsd_manual` para carregar o manual completo.

Resumo rapido:
- Use `gsd_criar_sistema` para criar sistemas completos (one-shot)
- Use `gsd_diagnosticar` para detectar e corrigir erros de metadados
- Use `gsd_manual` para consultar o manual operacional a qualquer momento
- O MCP decide autonomamente: nomes de tabelas, tipos SQL, componentes, mascaras
- Direct Access (banco) e o modo padrao. FRZ apenas sem acesso ao banco.
