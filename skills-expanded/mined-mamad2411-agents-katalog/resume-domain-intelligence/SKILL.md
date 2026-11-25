---
name: resume-domain-intelligence
description: Use when building, reviewing, or rewriting a software developer resume and you need to gather domain intelligence about the candidate's work, terminology, technical depth, market expectations, and hiring signals before writing.
---

# Resume Domain Intelligence

> "Um currículo técnico forte não nasce de copy bonita. Nasce de leitura correta do trabalho real."

Use esta skill quando o usuário quiser criar, revisar ou reescrever um currículo de desenvolvedor de forma que o texto soe como se tivesse sido escrito por:

- um especialista técnico da área dele;
- um recruiter técnico;
- e alguém que entende triagem de RH e ATS.

## Core Goal

Antes de escrever ou revisar qualquer currículo, construir um `domain intelligence map` do trabalho real da pessoa.

Esse mapa é obrigatório e deve responder:

- com que tecnologias e sistemas ela realmente trabalha;
- quais termos e conceitos são nativos da área dela;
- quais sinais demonstram profundidade técnica naquele nicho;
- o que o mercado e RH procuram naquele tipo de vaga;
- como traduzir essa bagagem para linguagem forte de currículo.
- como expandir cada competência técnica listada em subcompetências, ecossistema e sinais de mercado;
- o que o usuário realmente usa, o que só estudou e o que não deve vender no currículo.

## Quando Usar

- reescrita de currículo de software engineer;
- revisão crítica de currículo técnico;
- adaptação de currículo por stack, senioridade ou família de vaga;
- casos em que o texto atual está genérico e não parece escrito por alguém do domínio;
- perfis com bagagem técnica real, mas comunicação fraca;
- transições de carreira dentro de software onde a tradução do histórico é o principal problema.

## Quando NÃO Usar

- currículo de áreas não técnicas fora de software engineering;
- revisão puramente gramatical;
- criação de currículo sem contexto nenhum do trabalho da pessoa;
- quando o pedido é só formatar layout sem entender conteúdo.

## Non-Negotiable Rules

- Não reescreva o currículo antes de fechar o `domain intelligence map`.
- Não invente tecnologias, escopo, senioridade, resultados ou impacto.
- Não trate termos genéricos de software como prova de especialidade.
- Não assuma que o mesmo vocabulário serve para backend, frontend, mobile, platform, DevOps, data platform ou manager.
- Para cada item listado em `competências técnicas`, faça obrigatoriamente um `competency expansion sweep` antes de aceitar a skill no currículo.
- Separe explicitamente:
  - bagagem técnica real
  - linguagem de mercado
  - sinais de RH
  - sinais de avaliador técnico
  - evidência forte vs heurística
- Toda afirmação de mercado atual, ATS, demanda de stack ou hiring deve ser sustentada por pesquisa atual.

## Domain Intelligence Requirement

O `domain intelligence map` precisa cobrir, no mínimo:

- role cluster principal
- job titles alvo e adjacentes
- tecnologias principais
- tecnologias adjacentes
- sistemas e problemas típicos desse domínio
- glossário técnico e termos nativos da área
- sinais de maturidade e senioridade nesse nicho
- métricas que fazem sentido nesse tipo de trabalho
- artefatos de prova valorizados no mercado
- skills de RH/recruiter search
- expectativas da área técnica
- gaps entre bagagem real e comunicação atual
- competency expansion matrix
- user validation findings

Se faltar contexto do usuário, busque primeiro em:

- currículo/CV
- LinkedIn
- GitHub
- portfolio
- descrições de vaga-alvo
- repositórios, READMEs, package manifests, docs e histórico técnico local
- fontes públicas da empresa ou do mercado do usuário

## Recommended Workflow

1. Parsear o material do usuário com o checklist de intake.
2. Mapear o `role family` real do perfil:
   - backend
   - frontend
   - fullstack
   - mobile
   - platform/SRE
   - data/platform
   - security
   - manager/staff
3. Construir o `domain intelligence map`.
4. Rodar o `competency expansion sweep` nas competências técnicas listadas no currículo.
5. Fazer um `user validation loop` perguntando, de forma explícita, o que o usuário realmente usa, o que só estudou e o que não quer vender.
6. Fazer pesquisa atual em três eixos:
   - terminologia e sinais técnicos do domínio
   - mercado e vagas reais
   - RH, ATS e recrutamento
7. Extrair o que deve aparecer no currículo:
   - linguagem forte
   - sinais obrigatórios
   - sinais de bônus
   - anti-patterns do domínio
8. Só então revisar ou reescrever o currículo.

## Optional Subagent Split

Use até 3 subagentes se isso acelerar e houver benefício claro:

1. `domain-tech`
   - stack, terminologia, profundidade, sinais de senioridade, métricas do nicho
2. `market-hiring`
   - vagas reais, job titles, skills recorrentes, recruiter keywords, expectativas de mercado
3. `ats-rh`
   - ATS, triagem, leitura de RH, framing de currículo, clareza e adaptabilidade

O agente principal consolida, resolve conflitos e escreve a estratégia final.

## Source Hierarchy

Priorize nesta ordem:

1. material real do usuário
2. docs oficiais e handbooks públicos
3. vagas reais atuais
4. engineering blogs e job families de empresas fortes
5. papers e docs de ATS
6. recruiters/coaches reconhecidos
7. comunidade pública apenas como suporte

## Resume Translation Rule

Toda bagagem técnica precisa ser traduzida em cinco camadas:

1. `o que a pessoa fez`
2. `em que contexto`
3. `com que tecnologia`
4. `com que nível de complexidade/ownership`
5. `qual impacto ou resultado isso sugere`

Se um bullet não consegue responder pelo menos 3 dessas 5 camadas, ele provavelmente está fraco.

## HR + Technical Dual Lens

Antes de aprovar qualquer seção do currículo, teste duas perguntas:

### Lente RH

- o encaixe da vaga está claro em menos de 10 segundos?
- o vocabulário está alinhado ao mercado?
- a senioridade parece coerente?
- o documento está fácil de triar?

### Lente técnica

- esse texto parece escrito por alguém que entende o domínio?
- a contribuição individual está clara?
- há sinais de qualidade, escala, arquitetura, performance, segurança, testes ou operação quando relevantes?
- a senioridade é observável ou só declarada?

## Output Requirements

Quando a task envolver análise ou rewrite de currículo, a saída deve sempre incluir:

- `domain intelligence map`
- `competency expansion matrix`
- `user validation findings`
- `resume positioning` por role family
- `terminologia obrigatória` vs `terminologia opcional`
- `sinais obrigatórios` do domínio
- `provas fortes` e `provas ausentes`
- `anti-patterns` do domínio
- `rewrites` que soem nativos do nicho e legíveis para RH

## References

- `references/intake_checklist.md`
- `references/domain_map_schema.md`
- `references/competency_expansion_protocol.md`
- `references/research_protocol.md`
- `references/rewrite_lens.md`

## Final Reminder

Não escreva um currículo “bonito”. Escreva um currículo que faça um backend engineer soar backend, um mobile engineer soar mobile, um platform engineer soar platform, e ainda passe pela leitura de RH sem perder substância.
