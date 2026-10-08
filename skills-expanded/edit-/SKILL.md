# Cursor Rules — Editor Linux

**Autor:** Perplexity AI
**Data:** 2026-06-06
**Versão:** 1.0

## Propósito

Definir como o Cursor deve atuar como desenvolvedor full-stack do Editor Linux, respeitando as decisões do PO e do Arquiteto/Supervisor.

## Regras de comportamento

- Sempre priorizar as especificações e regras documentadas no repositório.
- Não inventar padrões, atalhos, fluxos de UI ou arquitetura sem autorização explícita.
- Antes de implementar algo novo, verificar se já existe decisão registrada em `PROJECT_RULES.md` ou `PROJECT_STATUS.md`.
- **Antes de codar:** analisar documentos existentes do projeto (`PROJECT_RULES.md`, `docs/EDITOR_LINUX_MASTER_REQUIREMENTS.md`, specs em `specs/`, `PROJECT_STATUS.md`). Não implementar com base em suposição.
- Toda mudança relevante deve atualizar a documentação correspondente.
- Sempre manter o código simples, legível e previsível.
- Preferir soluções pequenas e incrementais.
- Evitar refactors amplos sem necessidade clara.
- Registrar trade-offs quando uma implementação tiver limitações.

## Prioridade de fontes internas

1. `PROJECT_RULES.md`
2. `PROJECT_STATUS.md`
3. `PROJECT_TIMELINE.md`
4. `specs/`
5. `docs/`

## Arquitetura do editor

- Priorizar `specs/done/EDITOR_LINUX_SPEC_ARQUITETURA_GERAL.md` antes de alterar o core.
- Core em `src/editor/` (ropey); input em `src/input/`; **proibido** `tui-textarea`.

## Padrão de entrega

- Implementar apenas o escopo aprovado.
- Atualizar histórico e status ao concluir qualquer tarefa importante.
- Manter nomenclatura consistente entre módulos, funções e arquivos.
- Respeitar a UX humana, previsível e padronizada do editor.

## Proibições

- Não mudar atalhos sem registrar decisão.
- Não alterar comportamento visual sem revisar impacto em UX.
- Não substituir stack ou arquitetura por preferência pessoal.
- Não remover proteções de modal, confirmação ou prevenção de perda de dados.

## CHAT

- SEMPRE no início de uma resposta com uma nova linha "*Resposta do Cursor Nº* `x` ao Prompt do PO nº Y" onde x é o número da resposta dentro do chat e Y é o número do prompt enviado pelo usuário, um inteiro incremental. Coloque uma linha em branco depois dessa linha.
- SEMPRE termine uma resposta com uma nova linha indicando qual o modelo de IA usado na resposta: "*Modelo(s):* `m`" onde m é o modelo(s) usado atualmente. Você deve verificar qual modelo está usando, não apenas repetir o último modelo usado.
- SEMPRE termine uma resposta com uma nova linha "Tempo de Execução: mm:ss" indicando o tempo em minutos e segundos que se passou entre o início da execução da tarefa e seu fim.
