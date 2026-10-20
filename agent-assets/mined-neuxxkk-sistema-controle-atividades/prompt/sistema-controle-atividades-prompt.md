Objetivo
Implementar a TASK 1 de docs/tasks.md no dashboard do funcionário.

Task 1
/funcionarios/dashboard:
- Adicionar filtro de "Edifício" (dropdown/select) como filtro principal.
- O filtro deve aparecer acima ou ao lado da busca por texto atual.
- Quando um edifício for selecionado, apenas a árvore desse edifício deve ser renderizada.
- Manter a funcionalidade do filtro de texto existente (busca por tarefa, pavimento, status) dentro do edifício selecionado.
- Opção padrão: "Todos os Edifícios".

Arquivos Alvo
- frontend/src/app/dashboard/page.tsx

Diretrizes
- Seguir AGENTS.md (separação API/UI, mudanças cirúrgicas).
- Reutilizar estilos e componentes existentes (ex: inputs/selects da página de relatórios).
- Não alterar contratos da API.
- Preservar estados de carregamento e vazio.

Execução (Token-saving)
- Resposta direta ao ponto.
- Listar arquivos alterados antes de aplicar patches.
- Implementar apenas o necessário para a Task 1.

Formato da Resposta (Obrigatório)
1) Plano curto (max 5 linhas).
2) Patches aplicados.
3) Resultado da validação (build/lint visual).
4) Riscos identificados.
