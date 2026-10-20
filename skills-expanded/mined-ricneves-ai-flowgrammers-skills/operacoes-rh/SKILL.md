---
name: "operacoes-rh"
description: |
  Skills para documentar processos, estruturar times, criar políticas de RH e
  automatizar operações com contexto da legislação trabalhista brasileira (CLT/PJ/MEI).
  Cobre desde SOPs e onboarding até OKRs, avaliação de desempenho e cultura organizacional.
version: 1.0.0
license: MIT
tags:
  - operacoes
  - rh
  - sop
  - okr
  - onboarding
  - gestao
  - automacao
  - clt
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/operacoes-rh.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Operações, RH & Gestão (Nível PODEROSO)

Skills especializadas para estruturar, documentar e escalar operações e gestão de pessoas com contexto da legislação trabalhista brasileira. Cobre desde a criação de procedimentos operacionais até a gestão de cultura e automação de processos internos.

Este domínio é ideal para COOs, gerentes de operações, profissionais de RH, fundadores de startups e gestores que precisam construir uma máquina operacional eficiente com processos claros, times bem estruturados e conformidade com a CLT e legislação trabalhista brasileira.

## Início Rápido

### Claude Code
```
/read operacoes-rh/SKILL.md
```
Depois acesse a sub-skill pelo contexto:
```
/read operacoes-rh/criador-de-sop/SKILL.md
/read operacoes-rh/gestao-de-okrs/SKILL.md
/read operacoes-rh/onboarding/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/operacoes-rh.md`:
```
Use as skills de operacoes-rh para documentação de processos, RH e gestão.
Sempre considere: legislação trabalhista brasileira (CLT), regimes de contratação
(CLT, PJ, MEI), e o contexto cultural do ambiente de trabalho brasileiro.
```

### Codex
Adicione em `AGENTS.md`:
```markdown
## Operações, RH e Gestão
Ao criar documentos de RH, processos ou políticas internas, use os padrões de
operacoes-rh/SKILL.md. Contexto BR obrigatório: CLT, PJ, MEI, eSocial, FGTS, INSS.
Políticas de RH devem respeitar a legislação trabalhista brasileira.
```

### Windsurf
Em Windsurf Settings > AI Rules, adicione:
```
Para tarefas de RH e operações: aplique os frameworks de operacoes-rh.
Legislação: CLT brasileira para relações de emprego. Regimes: CLT, PJ, MEI, CLT-Flex.
Cultura: adaptar ao contexto do ambiente de trabalho brasileiro.
```

### OpenClaw
```
/skill operacoes-rh
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| SOP Creator | `criador-de-sop/` | Criação de SOPs com fluxogramas e checklists |
| Job Description | `descricao-de-vagas/` | Descrições de vagas e perfis de seleção |
| Onboarding | `onboarding/` | Planos de onboarding para CLT/PJ e clientes |
| OKR Manager | `gestao-de-okrs/` | Definição, cascateamento e acompanhamento de OKRs |
| Avaliação de Desempenho | `avaliacao-desempenho/` | Templates 360°, PDI, calibração e promoções |
| Políticas de RH | `politicas-rh/` | Políticas internas e handbook do colaborador |
| Automação de Processos | `automacao-processos/` | Automação com Make/Zapier/n8n para operações |
| Meeting Facilitator | `facilitador-de-reunioes/` | Facilitação de reuniões produtivas |
| Cultura de Empresa | `cultura-empresa/` | Valores, rituais e desenvolvimento de cultura |
| CLT/PJ/MEI | `clt-pj-mei/` | Orientação sobre regimes de contratação BR |

---

## Exemplos de Uso

### Criar SOP de processo crítico
```
Use a skill criador-de-sop para documentar o processo de onboarding de novos clientes
de uma agência de marketing digital. O processo atual tem 8 etapas mas está na
cabeça de 2 pessoas. Preciso de um SOP completo com: responsável por etapa,
prazo, ferramentas utilizadas, critério de qualidade e ponto de handoff.
```

### Criar job description para vaga técnica
```
Use a skill descricao-de-vagas para criar a descrição de vaga de Engenheiro(a) de
Software Sênior para uma fintech em São Paulo. Stack: Python, AWS, Kubernetes.
Regime: CLT. Formato híbrido 3x na semana. Salário: R$ 18k-25k + benefícios.
Inclua responsabilidades, requisitos obrigatórios, diferenciais e sobre a empresa.
```

### Estruturar OKRs trimestrais
```
Use a skill gestao-de-okrs para criar os OKRs do próximo trimestre para uma startup
de edtech no início da escala. Contexto: acabamos de fechar R$ 2M de investimento,
time de 18 pessoas, meta de triplicar o MRR de R$ 120k para R$ 360k em 9 meses.
Crie: 3 Objectives para a empresa e 3-4 Key Results para cada, com owners e
indicadores de progresso mensal.
```

### Criar programa de onboarding
```
Use a skill onboarding para criar o plano de onboarding de 30/60/90 dias para
um Gerente de Vendas contratado via CLT. Inclua: semana 1 (estrutura, ferramentas,
pessoas), primeiros 30 dias (aprendizado), 60 dias (primeiras entregas) e
90 dias (resultados esperados). Inclua checkpoints e critérios de sucesso.
```

### Estruturar política de home office
```
Use a skill politicas-rh para criar a política de home office e trabalho remoto
da empresa. Precisamos cobrir: quem pode trabalhar remoto, equipamentos (quem fornece),
ajuda de custo home office (art. 75-D CLT), frequência de dias presenciais,
comunicação e disponibilidade, e critérios de revisão do benefício.
```

### Automatizar processo de onboarding de colaborador
```
Use a skill automacao-processos para mapear e automatizar o processo de onboarding
de novos colaboradores. Ferramentas disponíveis: Make (antigo Integromat), Notion,
Slack e Google Workspace. Mapeie as etapas manuais e proponha automações para:
criação de contas, envio de documentos, agenda da primeira semana e checklist de TI.
```

### Facilitar reunião de OKR review
```
Use a skill facilitador-de-reunioes para criar a agenda e guia de facilitação para
uma reunião de OKR Review trimestral com time de 12 pessoas.
Duração: 2 horas. Preciso que o time revise o progresso de cada OKR, celebre
conquistas, entenda os bloqueios e ajuste as prioridades para o próximo trimestre.
```

### Resolver dúvida sobre contratação PJ vs CLT
```
Use a skill clt-pj-mei. Tenho um desenvolvedor que trabalha 40h/semana há 8 meses
como PJ (nota fiscal mensal R$ 12k). Ele trabalha exclusivamente para minha empresa,
com horário definido e subordinação direta ao tech lead. Quais são os riscos de
reconhecimento de vínculo empregatício e o que devo fazer para mitigar?
```

---

## Contexto Brasileiro

### Legislação Trabalhista Essencial

**CLT — Consolidação das Leis do Trabalho**
- Jornada máxima: 8h/dia, 44h/semana (com horas extras regulamentadas)
- 13º salário: obrigatório, em novembro e dezembro (ou antecipado nas férias)
- Férias: 30 dias após 12 meses, com acréscimo de 1/3 sobre o salário
- FGTS: 8% do salário bruto depositado mensalmente pelo empregador
- INSS empregado: 7,5-14% (escalonado por faixa salarial)
- INSS patronal: 20% sobre folha (exceto Simples Nacional)
- Aviso prévio: proporcional ao tempo de empresa (mínimo 30 dias)

**Contratos de Trabalho Legítimos**
- CLT: vínculo empregatício formal — previsível e protegido por lei
- PJ (Pessoa Jurídica): prestação de serviços sem subordinação, exclusividade ou habitualidade
- MEI: empreendedor individual — limite R$ 81k/ano, não pode ter sócios
- CLT-Flex / Trabalho Intermitente: jornada variável, pagamento por hora trabalhada
- Estágio: obrigatório ter seguro de acidentes pessoais + bolsa + supervisão

**Risco de Vínculo Empregatício (PJ Disfarçada)**
Os 4 elementos que configuram relação de emprego (art. 3º CLT):
1. **Pessoalidade** — Só aquela pessoa executa o serviço
2. **Habitualidade** — Frequência regular e contínua
3. **Subordinação** — Segue ordens, horários e processos definidos pelo contratante
4. **Onerosidade** — Recebe remuneração

Se os 4 elementos estão presentes, há risco de reconhecimento de vínculo.

### Cultura Organizacional Brasileira

- **Hierarquia respeitada mas relacional** — Formalidade existe mas o brasileiro espera acesso e conversa
- **Feedback indireto** — Brasileiros tendem a ser menos diretos em feedbacks negativos; treinamento explícito ajuda
- **Celebração e reconhecimento** — Alto impacto em engajamento; culturas que comemoram retêm melhor
- **WhatsApp como ferramenta de trabalho** — Limites claros de horário são necessários para saúde mental
- **Diversidade regional** — Times remotos com pessoas do Norte, Nordeste, Sul têm culturas diferentes; inclusão ativa é necessária

### ESocial e Obrigações Digitais
- eSocial: sistema unificado de obrigações trabalhistas, previdenciárias e fiscais
- CAGED: controle de admissões e demissões — substituído pelo eSocial
- RAIS: relação anual de informações sociais — ainda vigente para fins estatísticos
- CTPS Digital: Carteira de Trabalho digital obrigatória desde 2019

---

## Configuração de Harness

### Para Claude Code — trecho de CLAUDE.md global a adicionar

```markdown
## Operações e RH (BR)
- Documentos de RH devem considerar a legislação trabalhista brasileira (CLT)
- Regimes de contratação: identificar CLT, PJ, MEI ou estágio antes de qualquer análise
- Políticas de home office: verificar art. 75-D da CLT (ajuda de custo)
- OKRs: usar a metodologia Google/Intel adaptada ao contexto de PME brasileira
- Aviso legal: para questões trabalhistas complexas, recomendar advogado trabalhista
- eSocial: mencionar impacto no eSocial ao criar ou modificar qualquer política de RH
```

### Para Cursor — trecho de .cursorrules a adicionar

```
## RH e Operações (BR)
- Legislação trabalhista: CLT, eSocial, FGTS, INSS, 13º salário, férias
- Contratação: verificar risco de vínculo empregatício para contratos PJ
- Processos: documentar como SOP com owner, prazo e critério de qualidade
- OKRs: Objective qualitativo + Key Results quantitativos e mensuráveis
- Reuniões: sempre com agenda prévia, duração definida e ata de decisões
```

### Para Codex — trecho de AGENTS.md a adicionar

```markdown
## Agente de Operações e RH
Especialidade: gestão de pessoas e operações no contexto brasileiro

Regras:
1. CLT para vínculos de emprego — verificar 4 elementos antes de recomendar PJ
2. SOPs devem ter: objetivo, escopo, responsável, passo a passo, exceções e métricas
3. OKRs: máximo 3-5 KRs por Objective, todos mensuráveis com número e prazo
4. Onboarding 30/60/90 dias é padrão para posições de liderança
5. Políticas de RH devem ser revisadas por advogado trabalhista antes da implementação
6. Automação: priorizar ferramentas disponíveis no Brasil com suporte em PT-BR
```

---

## Regras

1. **CLT é a Base** — Toda análise de relação de trabalho parte da CLT. A informalidade e o PJ sem critério geram passivos trabalhistas que podem destruir uma empresa.

2. **SOP com Owner e Prazo** — Procedimento sem responsável definido não é executado. Todo SOP deve ter: quem faz, quando faz, como faz e como se sabe que foi feito corretamente.

3. **OKR: Qualitativo + Quantitativo** — O Objective deve ser aspiracional e qualitativo; os Key Results devem ser numéricos, mensuráveis e com data. "Melhorar o engajamento" não é KR; "Aumentar o NPS de 42 para 65 até dezembro" é.

4. **Onboarding é ROI** — O custo médio de substituição de um colaborador é 50-150% do salário anual. Um bom onboarding reduz drasticamente o turnover nos primeiros 90 dias.

5. **Feedback Estruturado** — No contexto brasileiro, feedback precisa ser ensinado. Implemente frameworks (SBI, STAR) e crie cadência de 1:1 para normalizar a cultura de feedback.

6. **Documentação Antes de Automatizar** — Não automatize processos ruins. Primeiro documente, depois otimize manualmente, então automatize. Automação de caos gera caos mais rápido.

7. **Reuniões com Ata** — Toda reunião que gera decisão precisa de ata com: decisões tomadas, ações, responsáveis e prazos. Reunião sem ata é conversa, não trabalho.

8. **Cultura se Demonstra, Não se Declara** — Valores na parede sem comportamento correspondente da liderança são ruído. Cada ritual, reconhecimento e política deve reforçar os valores declarados.

9. **Risco de Vínculo PJ** — Antes de recomendar ou estruturar qualquer contrato PJ, verificar os 4 elementos do art. 3º da CLT. Em caso de dúvida, recomende consulta com advogado trabalhista.

10. **eSocial e Compliance Trabalhista** — Toda admissão, demissão, alteração salarial, afastamento ou férias tem prazo de registro no eSocial. Atraso gera multa. Alertar sempre sobre os prazos legais.
