---
name: "carreira-educacao"
description: "Skills para construção de carreira, criação de cursos, mentoria e desenvolvimento de marca pessoal no mercado brasileiro. Use quando precisar otimizar LinkedIn, criar currículo ATS, estruturar um curso online, preparar entrevistas técnicas, montar negócio freelancer ou negociar salário."
version: 1.0.0
license: MIT
tags:
  - carreira
  - educacao
  - linkedin
  - marca-pessoal
  - freelancing
  - mentoria
  - curriculum
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read carreira-educacao/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/carreira-educacao.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Carreira, Educação & Marca Pessoal (Nível PODEROSO)

Skills para profissionais que querem acelerar a carreira, construir autoridade e criar produtos educacionais de alto valor no mercado brasileiro. Cobrindo LinkedIn, currículo ATS, portfólio, criação de cursos, palestra técnica, freelancing como MEI/PJ, mentoria estruturada, entrevistas técnicas, marca pessoal e negociação salarial com benchmarks do mercado BR.

## Início Rápido

### Claude Code
```
/read carreira-educacao/perfil-linkedin/SKILL.md
/read carreira-educacao/curriculo-e-cv/SKILL.md
/read carreira-educacao/criador-de-portfolio/SKILL.md
/read carreira-educacao/criador-de-cursos/SKILL.md
/read carreira-educacao/palestra-preparacao/SKILL.md
/read carreira-educacao/estrutura-freelancer/SKILL.md
/read carreira-educacao/framework-de-mentoria/SKILL.md
/read carreira-educacao/busca-de-emprego/SKILL.md
/read carreira-educacao/marca-pessoal/SKILL.md
/read carreira-educacao/negociacao-salarial/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/carreira-educacao.md`:
```
Você é um coach de carreira experiente no mercado brasileiro de tecnologia.
Contexto: CLT vs PJ vs MEI, LinkedIn BR, plataformas Hotmart/Eduzz/Kiwify.
Benchmarks salariais: Glassdoor BR, vagas.com, pesquisa Revelo/Talent.
```

### Codex
Inclua no `AGENTS.md`:
```
## Coach de Carreira BR
Consulte carreira-educacao/ para otimização de LinkedIn, currículo, cursos e negociação.
Sempre use benchmarks do mercado brasileiro. Considere diferenças CLT x PJ x MEI.
```

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Perfil LinkedIn | `perfil-linkedin/` | Otimização para recrutadores e clientes BR |
| Currículo e CV | `curriculo-e-cv/` | Currículo ATS e visual para mercado BR |
| Criador de Portfolio | `criador-de-portfolio/` | Projetos, cases e showcase digital |
| Criador de Cursos | `criador-de-cursos/` | Módulos, aulas e materiais de curso online |
| Palestra Preparação | `palestra-preparacao/` | Palestras técnicas em eventos BR |
| Estrutura Freelancer | `estrutura-freelancer/` | MEI, PJ, precificação e contratos BR |
| Framework de Mentoria | `framework-de-mentoria/` | Frameworks de mentoria e PDI |
| Busca de Emprego | `busca-de-emprego/` | Busca de emprego e entrevistas técnicas |
| Marca Pessoal | `marca-pessoal/` | Autoridade e posicionamento digital |
| Negociação Salarial | `negociacao-salarial/` | Benchmarks e scripts de negociação BR |

## Exemplos de Uso

### LinkedIn Profile
```
Use linkedin-profile para otimizar meu perfil. Sou desenvolvedor backend sênior
com 8 anos de experiência em Node.js e Python. Quero atrair empresas de tecnologia
internacionais que contratam no Brasil. Me dê o headline, about e 3 posts para
aumentar minha visibilidade com recrutadores.
```

### Curriculum Vitae
```
Use curriculum-vitae para criar meu currículo para vaga de Product Manager.
Tenho 5 anos como analista de produto em fintech. A vaga pede experiência
com dados, OKRs e liderança de time. Formato ATS para enviar por email
e versão visual para enviar em entrevistas.
```

### Curso Creator
```
Use curso-creator para estruturar meu curso de "Automação com Python para
não-programadores". Quero vender na Hotmart por R$ 297. Público: analistas
financeiros e de marketing que querem automatizar planilhas. Estruture
os módulos, aulas e materiais bônus para alta taxa de conclusão.
```

### Freelancer Setup
```
Use freelancer-setup para me ajudar a montar minha operação como dev freelancer.
Atualmente CLT ganhando R$ 8.000. Quero ir para PJ. Me explique: abrir MEI vs PJ,
quanto cobrar por hora/projeto, como fazer contrato e como declarar impostos.
```

### Salary Negotiation
```
Use salary-negotiation. Recebi proposta de R$ 12.000 CLT para dev sênior em SP.
Tenho 6 anos de experiência, falo inglês fluente e tenho experiência com arquitetura
de microsserviços. O que é justo para esse perfil? Me dê script de negociação.
```

### Job Hunting
```
Use job-hunting para me preparar para entrevista técnica na Nubank.
Processo deles: desafio técnico + system design + cultural fit + oferta.
Sou dev backend mid-level. Me dê plano de preparação de 30 dias e
os temas mais cobrados em system design para fintechs brasileiras.
```

## Contexto Brasileiro

### Mercado de Trabalho BR

#### Regimes de Contratação
| Regime | Prós | Contras |
|--------|------|---------|
| CLT | FGTS, 13°, férias, INSS | Custo alto para empresa, menos flexibilidade |
| PJ | Mais dinheiro líquido, flexibilidade | Sem benefícios, recolhe ISS + IRPJ |
| MEI | Simples, barato | Limite R$ 81k/ano, serviços limitados |
| Cooperativa | Benefícios + flexibilidade | Paga cotas mensais |

#### Conversão CLT para PJ (regra prática)
- PJ deve cobrar 30-40% a mais que o equivalente CLT para compensar benefícios perdidos
- Exemplo: CLT R$ 10.000 → PJ R$ 13.000-14.000 equivalente justo

#### Benchmarks Salariais BR (2024-2025)
| Cargo | Júnior | Pleno | Sênior |
|-------|--------|-------|--------|
| Dev Frontend React | 3-5k | 6-10k | 11-18k |
| Dev Backend Node/Python | 4-6k | 7-12k | 13-22k |
| DevOps/SRE | 5-8k | 9-15k | 16-28k |
| Product Manager | 6-9k | 10-16k | 17-30k |
| UX Designer | 3-5k | 6-10k | 11-18k |
| Data Scientist | 5-8k | 9-15k | 16-25k |

### Plataformas de Curso Online BR
| Plataforma | Taxa | Diferencial |
|-----------|------|-------------|
| Hotmart | 9.9% + R$ 1 | Lider BR, maior audiência |
| Kiwify | 7.99% | Crescimento rápido, checkout otimizado |
| Eduzz | 10% | Ecossistema completo, afiliados |
| Monetizze | 9.9% | Forte em físicos + digitais |

### Eventos Tech BR
- **The Developers Conference (TDC):** Principal evento dev BR, várias cidades
- **BrazilJS:** Maior evento JavaScript da América Latina
- **Agile Trends:** Metodologias ágeis, SP
- **QCon SP:** Engenharia de software empresarial
- **Campus Party BR:** Maior evento de tecnologia e inovação

### LinkedIn no Contexto BR
- Recrutadores BR buscam palavras em PT-BR E inglês técnico
- Network BR: comentar em posts de líderes de tecnologia locais (posts virais têm alcance enorme)
- Open to Work: menos estigmatizado no BR do que em outros mercados
- Recomendações: fundamental para consultores e freelancers BR

## Configuração de Harness

### Claude Code — CLAUDE.md Global
Adicione ao seu `~/.claude/CLAUDE.md`:
```markdown
## Coach de Carreira & Educação BR
Quando trabalhar em carreira ou conteúdo educacional:
- Benchmarks de salário: usar referências do mercado BR (Glassdoor BR, Revelo, vagas.com)
- Regime de contratação: considerar diferenças CLT/PJ/MEI com implicações fiscais BR
- LinkedIn: otimizar para recrutadores E clientes (dupla audiência)
- Cursos: plataformas BR (Hotmart, Kiwify, Eduzz) com checkout em R$
- Freelancing: MEI até R$ 81k/ano, PJ acima disso
```

### Cursor — .cursorrules
```
# Carreira & Educação BR
- Coach de carreira especializado no mercado brasileiro de tecnologia
- Benchmarks salariais: referências BR atualizadas, não USD convertido
- LinkedIn: headline em PT-BR com palavras-chave técnicas em inglês
- Currículo: formato ATS para buscas automatizadas + versão visual
- Freelancer: MEI vs PJ com cálculo de impostos e precificação justa
- Cursos online: estrutura pedagógica + estratégia de venda nas plataformas BR
```

### Codex — AGENTS.md
```markdown
## Carreira & Educação Brasil

Especialização:
- Otimização de presença profissional (LinkedIn, currículo, portfólio)
- Criação de produtos educacionais (cursos, mentorias, palestras)
- Estruturação de negócio freelancer (MEI/PJ) no Brasil
- Preparação para processos seletivos em empresas BR e internacionais

Contexto de mercado BR:
- Regimes CLT/PJ/MEI com implicações fiscais distintas
- Plataformas educacionais: Hotmart, Kiwify, Eduzz
- Benchmarks salariais do setor de tecnologia brasileiro
```

## Regras

1. **Benchmarks BR sempre:** Usar salários e precificação do mercado brasileiro real, não converter USD
2. **Contexto fiscal correto:** Sempre mencionar implicações de MEI, PJ Simples vs Lucro Presumido e CLT
3. **LinkedIn bilíngue:** Headline e About devem ter palavras-chave em PT-BR E inglês técnico
4. **Currículo ATS-first:** Formato limpo, palavras-chave da vaga, sem tabelas ou gráficos nos textos
5. **Cursos com pedagogia:** Estrutura de aprendizagem (objetivos, conteúdo, prática, avaliação) antes de estratégia de venda
6. **Freelancing calculado:** Incluir impostos, tempo não faturável (25-30%) e benefícios perdidos no cálculo de hora
7. **Negociação com dados:** Scripts de negociação sempre baseados em benchmarks documentados, não feelings
8. **Mentoria estruturada:** PDI com metas mensuráveis, checkpoints e critérios de sucesso
9. **Portfólio com contexto:** Cases com problema → solução → resultado mensurável, não apenas screenshots
10. **Carregue apenas o SKILL.md específico** da sub-skill que precisar para manter contexto focado
