---
name: classificar-documentacao
description: Classifica, cria ou reorganiza documentação de engenharia em docs, distinguindo épicos, gaps, insights, ADRs e auditorias e mantendo seus vínculos. Use ao criar ou mover documentos de projeto; não para reclassificar decisões históricas automaticamente.
---

# Classificar pelo propósito

Leia o AGENTS e o índice documental do projeto. O padrão do kit é `docs/README.md`;
um projeto existente pode declarar outra raiz ou autoridade central. Em meta-repo,
identifique o escopo e os membros antes de atribuir IDs ou duplicar decisões.

| Pergunta respondida | Destino padrão |
|---|---|
| O que investigamos, com quais hipóteses/evidências? | `docs/insights/` |
| Que resultado queremos, em quais fases e com quais aceites? | `docs/epics/` |
| Qual discrepância foi medida e o que falta para resolvê-la? | `docs/gaps/` |
| Por que escolhemos uma solução estrutural? | `docs/adr/` |
| O que uma auditoria delimitada verificou? | `docs/audits/` ou `docs/security-audit/` |
| Como o sistema é organizado hoje? | `docs/architecture/` |
| Como operar/reproduzir um procedimento? | `docs/runbooks/` |
| Qual é o contrato visual e de acessibilidade? | `docs/design-system/` |

Escolha uma categoria primária. Um relatório com achados continua relatório:
crie gaps vinculados para o trabalho aberto, sem duplicar o relatório inteiro.
Insight não equivale a decisão; gap não equivale a épico; correção local não
exige ADR só por ter severidade alta. Não crie documentos sem função concreta.

Use os modelos em `docs/templates/`. Confira IDs existentes e reservas de outras
sessões. Preserve IDs após encerramento e nomes históricos na migração. Registre
estado, escopo/repos, origem, responsável, evidência e próximo passo apropriados
ao tipo. Idiomas/locales e aceites seguem a política do projeto, sem impor país,
stack, forge, ferramenta de testes ou estrutura de equipe do projeto de origem.

## Relações

Épico lista ADRs pertinentes com status; cada ADR lista os épicos que a consomem.
Gap liga sua origem e o épico/ADR quando existirem. Insight liga os documentos
que nasceram dele. Use links relativos, incluindo âncora quando necessária.
Adicionar referência não muda o status da decisão. Nem todo épico exige ADR.

PENDING aponta para trabalho aberto; ROADMAP ordena resultados/dependências;
CONCLUSION registra desfechos. O detalhe fica no documento da categoria.

## Migração

Faça inventário por repositório e mapa explícito origem → destino. Confira colisões,
arquivos não versionados, links, scripts, hooks e consumidores externos antes de
escrever. `documentation.py migrate <plano.json>` oferece prévia; `--apply` só
depois de revisar o mapa. Ferramenta não escolhe classificação semântica.

Preserve anexos e decisões. Compare inventário/hashes, revise o diff e rode o
verificador de referências do projeto; `documentation.py check` confere destinos
de links Markdown locais, mas não certifica âncoras, links web ou texto sem link.
Consumidores em outros repositórios exigem validação própria. Não declare uma
migração completa somente porque os arquivos foram movidos.
