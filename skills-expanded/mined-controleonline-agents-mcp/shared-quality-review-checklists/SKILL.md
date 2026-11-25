# Review Checklists

Estas listas sao o criterio de aprovacao que deve ser copiado para a task quando QA ou Security registrarem a decisao.

## QA

- base da implementação confirmada em `master` remoto atualizado; em cada
  correção/retomada, a nova rodada foi sincronizada novamente com `master`
- limite de linhas e tamanho do componente estao coerentes com o escopo
- componentes, hooks, services e helpers existentes foram reaproveitados quando possivel
- subchecklist de reaproveitamento de componentes em `agents/skills/controleonline/shared-quality-review-checklists/component-reuse-checklist.md` foi executado quando a entrega afetar frontend
- **cores:** proibido cor literal no codigo (hex/rgb/rgba/hsl/nome), inclusive fallback, overlay de modal e props de cor; arquivo tocado com cor legada e migrado; `grep -nE "#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\("` vazio nos arquivos tocados
- **termos:** todo texto de UI do delta vem da traducao; sem string literal e sem chave crua como label
- padroes de codigo (modularizacao, reuso, ≤500 linhas) respeitados
- **testes automatizados nao sao obrigatorios**; se a entrega inserir ou alterar testes, eles devem passar na execucao local registrada
- helpers da pasta `ui-common` / `ui-commun` foram usados quando aplicavel
- a issue e o `AGENTS.md` mais especifico do escopo foram consultados

## Gate de primeira passagem do Developer

O Developer deve ler este checklist no início da primeira passagem, registrar
os itens aplicáveis na issue e manter a lista como critério de entrega. A
primeira passagem nao pode ser encerrada sem evidência dos criterios QA
aplicaveis (cores, traducoes, padroes de codigo) ou sem encaminhar o
impedimento objetivo ao Manager. Testes automatizados sao opcionais; se
incluidos, devem passar.

## Security

- autorizacao e controle de acesso foram validados
- exposicao de dados e leituras indevidas foram revisadas
- IDOR, mass assignment e alteracao indevida de status foram considerados
- o `securityFilter` do service equivalente foi localizado e validado para proteger leitura e escrita quando aplicavel
- as regras sensiveis do dominio e o `AGENTS.md` do escopo foram conferidos
