---
name: "descricao-de-vagas"
description: |
  Cria descrições de vagas, perfis de candidatos e critérios de seleção para
  o mercado de trabalho brasileiro. Adapta o formato para CLT e PJ, inclui
  faixa salarial em R$, benefícios obrigatórios (CLT) e modelo de trabalho.
version: 1.0.0
license: MIT
tags:
  - vaga
  - recrutamento
  - selecao
  - job-description
  - clt
  - rh
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/job-description/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/job-description.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Job Description

Especialista em criação de descrições de vagas atrativas e precisas para o mercado brasileiro. Atrai os candidatos certos e filtra os inadequados antes da triagem.

## Estrutura da JD

1. **Título da Vaga** — Claro, com nível (Júnior/Pleno/Sênior) e regime (CLT/PJ)
2. **Sobre a Empresa** — 3-4 linhas; cultura e missão
3. **O que você vai fazer** — Responsabilidades em bullets, ativas e concretas
4. **O que buscamos** — Requisitos obrigatórios vs. diferenciais (separados!)
5. **O que oferecemos** — Salário, benefícios CLT (VA, VT, plano de saúde, etc.)
6. **Modelo de trabalho** — Presencial/híbrido/remoto + localização

## Benefícios CLT Comuns no Brasil

- Vale Refeição / Alimentação (VR/VA)
- Vale Transporte (VT) — obrigatório se presencial/híbrido
- Plano de Saúde (Amil, Unimed, SulAmérica, Bradesco)
- Plano Odontológico
- PLR (Participação nos Lucros)
- Gympass / Total Pass
- Home Office Allowance (art. 75-D CLT)
- Day Off no aniversário

## Exemplos de Uso

```
Use job-description para criar a JD de um Analista de Marketing Digital Pleno
para uma startup de SaaS em São Paulo. CLT. Híbrido 3x/semana. Salário: R$ 7k-9k.
Responsabilidades: gestão de tráfego pago (Meta + Google), relatórios de performance,
criação de landing pages. Requisitos: 3 anos de experiência, inglês intermediário.
```

## Regras

1. Nunca misture requisitos obrigatórios com desejáveis — candidatos não se candidatam se "não atendem tudo"
2. Salário é o campo mais importante para atrair candidatos qualificados — seja específico
3. Evite termos excludentes: "jovem dinâmico", "rockstar", "ninja" afastam candidatos sênior e diversidade
4. Descreva o trabalho REAL — JD inflada de responsabilidades gera frustração e turnover
5. Para vagas PJ: deixar explícito que não há vínculo empregatício e que é contrato de prestação de serviços
