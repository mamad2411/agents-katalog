---
name: "conteudo-copy"
description: |
  Skills para criação de conteúdo escrito, copy persuasivo, headlines, emails e artigos
  em português BR. Cobre todos os formatos digitais com contexto cultural brasileiro:
  tom informal/formal, gírias regionais, plataformas locais e métricas de engajamento BR.
version: 1.0.0
license: MIT
tags:
  - conteudo
  - copywriting
  - headlines
  - email
  - artigos
  - posts
  - storytelling
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/conteudo-copy.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Conteúdo & Copy (Nível PODEROSO)

Skills especializadas para criação de conteúdo escrito e copy persuasivo no mercado brasileiro. Cobrem desde geração de headlines virais até páginas de vendas completas, sempre com linguagem nativa, referências culturais BR e adaptações para as plataformas mais usadas no Brasil.

Este domínio é ideal para criadores de conteúdo, copywriters, profissionais de marketing e empreendedores que precisam produzir conteúdo de alta performance em português brasileiro com consistência e escala.

## Início Rápido

### Claude Code
```
/read conteudo-copy/SKILL.md
```
Depois escolha a sub-skill pelo contexto:
```
/read conteudo-copy/gerador-de-headlines/SKILL.md
/read conteudo-copy/criador-de-hooks/SKILL.md
/read conteudo-copy/escritor-de-emails/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/conteudo-copy.md`:
```
Use as skills de conteudo-copy para qualquer tarefa de escrita, copy ou conteúdo.
Sempre escreva em português brasileiro com tom adequado ao público-alvo.
Priorize clareza, persuasão e contexto cultural BR.
```

### Codex
Adicione em `AGENTS.md`:
```markdown
## Conteúdo e Copy
Ao criar qualquer conteúdo de marketing ou copy, use os padrões definidos em
conteudo-copy/SKILL.md. Sempre considere o contexto brasileiro e as plataformas
mais usadas no Brasil (Instagram, WhatsApp, YouTube, TikTok).
```

### Windsurf
Em Windsurf Settings > AI Rules, adicione:
```
Para tarefas de escrita e copy: aplique os frameworks de conteudo-copy.
Escreva sempre em PT-BR com contexto cultural brasileiro.
Use frameworks AIDA, PAS, 4U e Curiosity Gap conforme o formato.
```

### OpenClaw
```
/skill conteudo-copy
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Headline Generator | `gerador-de-headlines/` | Headlines com AIDA, PAS, 4U, Curiosity Gap para todos os canais |
| Hook Writer | `criador-de-hooks/` | Hooks para posts, vídeos, threads e stories — atenção nos primeiros 3 segundos |
| Ad Copy | `copy-de-anuncio/` | Copy de anúncio para Meta Ads, Google Ads, LinkedIn com contexto BR |
| Email Writer | `escritor-de-emails/` | Sequências de email, newsletters, cold email e automações |
| Article Writer | `escritor-de-artigos/` | Artigos de blog, conteúdo SEO, white papers e long-form |
| Social Posts | `posts-sociais/` | Posts para Instagram, LinkedIn, Twitter/X, TikTok otimizados por plataforma |
| Sales Copy | `copy-de-vendas/` | Páginas de vendas, VSL, copy de produto e checkout |
| Content Repurposing | `reaproveitamento-de-conteudo/` | Reaproveitamento entre formatos: vídeo → post → email → thread |
| Storytelling | `storytelling/` | Narrativas de marca, storytelling pessoal e corporativo |
| Product Description | `descricao-de-produto/` | Descrições para e-commerce e marketplaces brasileiros |

---

## Exemplos de Uso

### Gerar headlines para landing page
```
Use a skill gerador-de-headlines e crie 10 headlines para minha landing page de curso
de Excel para profissionais de RH. Produto: Curso Excel Avançado, R$ 497.
Público: Analistas de RH que querem automatizar relatórios e ganhar promoção.
Aplique os frameworks AIDA, 4U e Curiosity Gap.
```

### Criar hook para Reels do Instagram
```
Use a skill criador-de-hooks e crie 5 hooks para um Reels sobre os erros mais comuns
ao emitir nota fiscal MEI. Público: microempreendedores com 1-2 anos de negócio.
Os primeiros 3 segundos precisam parar o scroll.
```

### Escrever sequência de email de boas-vindas
```
Use a skill escritor-de-emails e crie uma sequência de 5 emails de boas-vindas para
novos assinantes de uma newsletter sobre investimentos para iniciantes.
Tom: educativo, acessível, sem jargões financeiros. Inclua CTAs para
o grupo no WhatsApp e o canal no YouTube.
```

### Criar copy para anúncio no Meta Ads
```
Use a skill copy-de-anuncio para criar 3 variações de copy para anúncio no Facebook
e Instagram. Produto: consultoria de tráfego pago para e-commerce.
Público: donos de loja virtual com faturamento entre R$ 20k e R$ 100k/mês
que estão desperdiçando verba em anúncios. Formato: carrossel e single image.
```

### Escrever artigo para blog com SEO
```
Use a skill escritor-de-artigos para escrever um artigo completo sobre
"como precificar serviços freelancer no Brasil". Inclua dados do mercado BR,
estratégias práticas e otimize para SEO com as palavras-chave:
"precificação freelancer", "quanto cobrar serviço", "tabela de preços freelancer".
Mínimo 1.500 palavras.
```

### Criar descrição de produto para Mercado Livre
```
Use a skill descricao-de-produto para criar a descrição de um kit skincare
feminino para venda no Mercado Livre. Produto: Kit Rotina Noturna com 3 itens.
Preço: R$ 189,90. Destaque benefícios, diferenciais e inclua gatilhos de urgência.
```

### Transformar webinar em múltiplos formatos
```
Use a skill reaproveitamento-de-conteudo. Tenho a transcrição de um webinar de 90 minutos
sobre gestão financeira para pequenas empresas. Crie:
- 1 artigo de blog de 1.200 palavras
- 5 posts para LinkedIn
- 1 thread para Twitter/X (10 tweets)
- 3 emails para a lista
- 10 tópicos para stories do Instagram
```

### Escrever copy de página de vendas
```
Use a skill copy-de-vendas e escreva a página de vendas completa para um programa
de mentoria individual em vendas B2B. Investimento: R$ 3.500/mês.
Público: representantes comerciais e gerentes de vendas. Inclua headline,
subheadline, benefícios, prova social, bônus, FAQ e CTA.
```

---

## Contexto Brasileiro

Esta skill foi desenvolvida com atenção específica ao mercado e cultura brasileira:

### Plataformas Prioritárias no Brasil
- **WhatsApp Business** — Canal de comunicação e vendas mais usado no Brasil; integrar CTAs para WhatsApp em todo copy
- **Instagram** — Alta taxa de engajamento com Reels e Stories; adaptar formato e linguagem para mobile-first
- **YouTube** — Segunda maior plataforma de busca no Brasil; hooks para os primeiros 30 segundos são críticos
- **TikTok** — Crescimento acelerado especialmente entre 18-35 anos; linguagem mais informal e autêntica
- **LinkedIn BR** — Diferente do LinkedIn global: brasileiros preferem tom mais pessoal e histórias humanizadas
- **Mercado Livre / Shopee** — Marketplaces dominantes; palavras-chave e estrutura de descrição específica

### Linguagem e Tom
- Português BR com regionalismos quando apropriado (Sul, Nordeste, Sudeste têm preferências distintas)
- Gírias e expressões coloquiais aceitas em contextos informais (startup, moda, entretenimento)
- Tom formal preservado para setores: jurídico, saúde, financeiro, B2B enterprise
- Uso de "você" (não "tu") como padrão; adaptado para o público-alvo

### Gatilhos Culturais Brasileiros
- **Prova social coletiva** — Brasileiros confiam muito em indicações de amigos e grupos
- **Urgência com datas comemorativas** — Black Friday, Natal, Dia das Mães, Carnaval, Copa do Mundo
- **Parcelamento** — Sempre mencionar parcelamento no PIX/cartão (ex: "12x sem juros")
- **Garantia e segurança** — Selos de segurança, garantia de satisfação, reembolso são fundamentais
- **Autoridade regional** — Mencionar cases e referências brasileiras gera mais identificação

### Métricas de Referência BR (2024-2025)
- Taxa média de abertura de email marketing: 19,7% (média geral) / 28%+ para segmentos de nicho
- CTR médio Meta Ads: 0,9-2,3% dependendo do setor
- Engajamento médio Instagram BR: 3,1% (perfis até 10k seguidores)
- Taxa de conversão e-commerce BR: 1,2-2,5% média do setor

---

## Configuração de Harness

### Para Claude Code — trecho de CLAUDE.md global a adicionar

```markdown
## Conteúdo e Copy
- Ao criar qualquer conteúdo escrito ou copy, use os padrões de conteudo-copy/SKILL.md
- Sempre escreva em português brasileiro nativo
- Aplique o framework adequado ao objetivo: AIDA (awareness), PAS (problema), 4U (urgência)
- Para posts em redes sociais, adapte o formato e tom por plataforma
- Inclua sempre CTAs claros e contextualizados ao público brasileiro
- Mencione parcelamento (PIX, cartão) quando se tratar de copy de vendas
```

### Para Cursor — trecho de .cursorrules a adicionar

```
## Copy e Conteúdo (PT-BR)
- Escreva todo conteúdo de marketing em português brasileiro coloquial/profissional conforme o público
- Use frameworks: AIDA para awareness, PAS para dor/solução, 4U para urgência
- Headlines: teste variações com números, perguntas e promessas específicas
- CTAs: sempre diretos e com verbo de ação ("Quero", "Preciso", "Acesse agora")
- Contexto BR: mencione PIX, parcelamento, e datas sazonais brasileiras quando relevante
```

### Para Codex — trecho de AGENTS.md a adicionar

```markdown
## Agente de Conteúdo e Copy
Especialidade: criação de conteúdo e copy persuasivo em PT-BR

Regras principais:
1. Português BR nativo — evite anglicismos desnecessários
2. Tom: adapte ao público (informal para DTC/e-commerce, formal para B2B/saúde/jurídico)
3. Frameworks: AIDA, PAS, 4U, Curiosity Gap, Storytelling
4. Sempre inclua CTA claro e contextualizado
5. Para e-commerce: mencione parcelamento, frete grátis, prazo de entrega
6. Para SaaS: mencione trial grátis, sem cartão de crédito, suporte em português
```

---

## Regras

1. **Português Brasileiro Nativo** — Nunca use construções gramaticais de Portugal ou anglicismos desnecessários. Escreva como um brasileiro educado falaria em 2025.

2. **Framework Primeiro** — Antes de escrever qualquer copy, identifique o framework mais adequado: AIDA (Atenção → Interesse → Desejo → Ação), PAS (Problema → Agitação → Solução), 4U (Útil → Urgente → Único → Ultra-específico) ou Curiosity Gap.

3. **Público-Alvo Explícito** — Todo copy deve ter um público-alvo definido. Se não for informado, pergunte antes de escrever. Copy genérico converte menos.

4. **Prova Social e Credibilidade** — Sempre sugira onde incluir depoimentos, cases, números de clientes ou resultados concretos. No Brasil, prova social é fator de conversão crítico.

5. **Mobile First** — A maioria dos brasileiros consome conteúdo pelo celular. Headlines curtas, parágrafos curtos (máximo 3 linhas), bullets generosos.

6. **CTA Claro e Direto** — Todo conteúdo de copy deve terminar com uma chamada para ação inequívoca. Use verbos imperativos: "Clique aqui", "Quero garantir minha vaga", "Baixar agora".

7. **Otimização por Plataforma** — Instagram não é igual a LinkedIn, que não é igual a Email, que não é igual a WhatsApp. Adapte tom, formato, comprimento e recurso visual conforme a plataforma destino.

8. **Versões A/B por Padrão** — Para qualquer copy de anúncio, headline ou subject de email, entregue pelo menos 2-3 variações para teste A/B.

9. **Contextualização Sazonal BR** — Considere o calendário brasileiro: Black Friday (novembro), Natal (dezembro), Carnaval (fevereiro), Dia das Mães (maio), Dia dos Pais (agosto), Dia do Consumidor (março).

10. **Compliance e Ética** — Não escreva copy que faça promessas falsas ou enganosas. Siga as diretrizes do CONAR (Conselho Nacional de Autorregulamentação Publicitária) e o CDC (Código de Defesa do Consumidor) brasileiro.
