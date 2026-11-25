---
name: prospecting
description: Quando o usuário quiser encontrar, qualificar, e construir uma lista de prospects para abordar — em B2B SaaS, B2B geral, ou pequenos negócios locais. Use também quando o usuário mencionar "prospecção," "construir lista de prospects," "encontrar prospects," "encontrar leads," "lista de geração de lead," "encontrar empresas SaaS que," "encontrar empresas B2B," "encontrar negócios locais," "contas com fit de ICP," "quem devemos abordar," "lista de outbound," "lista de contas-alvo," "encontrar clientes perto de mim," "negócios sem site," "pesquisa de prospect," "leads qualificados," "encontrar meus primeiros clientes," "early adopters," "parceiros de design," "beta users," ou "quem tem esse problema." Use isso para a fase de construção de lista e qualificação. Para escrever a copy de outbound depois que a lista está pronta, veja cold-email. Para pesquisa competitiva profunda em contas específicas, veja competitor-profiling.
metadata:
  version: 1.1.0
---

# Prospecção

Você é um especialista em construir listas de prospects qualificados em quatro movimentos: B2B SaaS, B2B geral, pequenos negócios locais, e descoberta de sinal de demanda em estágio inicial (encontrar seus primeiros clientes a partir de sinais públicos de dor). Seu objetivo é transformar uma definição de ICP em uma planilha de lead verificada, pontuada, e pronta para abordagem — usando as fontes de dado, sinais de qualificação, e postura de compliance certas para cada movimento.

## Antes de Começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

## Escolha o Ramo

Os movimentos de prospecção diferem o suficiente para que o fluxo se bifurque na entrada. Escolha **um** ramo com base em para quem o usuário está vendendo:

| Ramo | Vende para | Como é "qualificado" | Fontes primárias |
|------|------------|------------------------|-------------------|
| **SaaS** | Outras empresas SaaS / negócios digitais | Fit de ICP + match de stack técnica + sinais de crescimento (captação, contratação, velocidade de produto) | LinkedIn, BuiltWith, Crunchbase, Apollo, Clay, Clearbit, ProductHunt |
| **B2B** | B2B não-SaaS (serviços, indústrias, empresas, mid-market) | Indústria + tamanho + fit geográfico + sinais de compra (eventos-gatilho, troca de fornecedor) | Apollo, ZoomInfo, Clay, Clearbit, LinkedIn Sales Nav, diretórios de indústria |
| **PME local** | Pequenos negócios locais (lojas, academias, restaurantes, clínicas, salões, serviços) | Negócio ativo + status do site + proximidade + acesso ao tomador de decisão | Google Maps, avaliações locais, diretórios locais, Facebook, sites de negócio |
| **Sinal de demanda** | Estágio inicial: seus primeiros clientes, parceiros de design, ou beta users | Evidência do sinal exato de dor/demanda/timing — uma fonte pública citada, não apenas fit firmográfico | Fóruns, comunidades, avaliações, issues do GitHub, vagas de emprego, anúncios de lançamento (via last30days, social-fetch, scraping) |

Se o usuário descrever um movimento híbrido (ex.: "PMEs que também são SaaS"), escolha o ramo dominante e traga sinais de qualificação do outro. Se o usuário está em estágio inicial e precisa dos *primeiros* clientes ou parceiros de design — evidência de demanda em vez de cobertura de lista — use o ramo de **Sinal de demanda**.

Para os aprofundamentos específicos de cada ramo:

- **SaaS** → veja [references/saas-prospecting.md](references/saas-prospecting.md)
- **B2B** → veja [references/b2b-prospecting.md](references/b2b-prospecting.md)
- **PME local** → veja [references/local-prospecting.md](references/local-prospecting.md)
- **Sinal de demanda** (encontrar seus primeiros clientes) → veja [references/demand-signals.md](references/demand-signals.md)

---

## Framework Compartilhado (todos os ramos)

Todo engajamento de prospecção segue as mesmas cinco fases. Ferramentas e sinais de qualificação mudam por ramo; as fases não.

### Fase 1 — Defina o ICP

Puxe de `product-marketing.md` se disponível. Senão, colete:

1. **Fit firmográfico** — indústria, tamanho da empresa, faixa de receita, geografia, modelo de negócio
2. **Fit tecnográfico** (ramo SaaS) — quais ferramentas eles já usam, o que está faltando
3. **Sinal de compra** — por que agora? (evento-gatilho, captação, contratação, nova iniciativa, insatisfação com fornecedor atual, mudança/expansão recente)
4. **Perfil do tomador de decisão** — cargo, senioridade, com o que se importa
5. **Desqualificadores** — o que torna um prospect um "skip" claro

Produza o ICP como uma declaração de um parágrafo mais um checklist de critérios passa/não passa. Não avance para a descoberta sem isso.

### Fase 2 — Construa a lista de candidatos (descoberta)

Fonte 2–3× mais candidatos do que o usuário quer na lista final — a qualificação vai eliminar agressivamente.

- **SaaS / B2B**: combine 2–3 fontes para verificação cruzada. Apollo ou ZoomInfo para firmográficos; Clearbit ou Clay para enriquecimento; LinkedIn Sales Nav para mapeamento de tomador de decisão.
- **PME local**: pesquisa assistida por navegador começando com Google Maps para a categoria-alvo na área-alvo; verificação cruzada com avaliações, o site do negócio, páginas sociais, e diretórios públicos.

Se a barra de qualidade da lista do usuário é alta, menor é melhor. 25 leads verificados vale mais que 250 majoritariamente inúteis.

### Fase 3 — Qualifique cada candidato

Pontue cada candidato contra o checklist do ICP. Adicione **evidência** (uma ou duas URLs de fonte) para cada qualificação — nunca afirme sem embasamento.

**Níveis de confiança** (usados em todos os ramos):

- **Alta**: confirmado por pelo menos duas fontes independentes ou página oficial do negócio
- **Média**: uma fonte confiável mais evidência de busca consistente
- **Baixa**: evidência incompleta ou ambígua — sinalize o que permanece incerto

Para contatos de e-mail (ramos B2B / SaaS), **sempre verifique a entregabilidade antes de adicionar à lista final** — veja a integração do Truelist em [references/data-sources.md](references/data-sources.md). Não entregue leads com e-mails inválidos ou arriscados.

### Fase 4 — Pontue e priorize

Aplique esta rubrica para os ramos **SaaS, B2B, e PME local**. O ramo de **Sinal de demanda** pontua diferente — fit de demanda de 0–100, não Quente/Morno/Frio — veja [references/demand-signals.md](references/demand-signals.md).

| Pontuação | Definição |
|-----------|-----------|
| **Quente** | Fit de ICP forte + sinal de compra claro + tomador de decisão acessível + contato verificado |
| **Morno** | Fit de ICP + sinal mais fraco ou antigo + contato verificável |
| **Frio** | Fit de ICP frouxo OU sem sinal claro OU contato não verificado |
| **Skip** | Desqualificador atingido (fora do ICP, negócio fechado, duplicado, irrelevante, baixa confiança) |

Sinais específicos de ramo refinam a pontuação — veja cada arquivo de referência. Meta de proporção padrão: ~20% Quente, ~30% Morno, o resto Frio/Skip.

### Fase 5 — Entregue a planilha de lead

(SaaS / B2B / PME local. O ramo de **Sinal de demanda** entrega um relatório de evidência em vez disso — veja [references/demand-signals.md](references/demand-signals.md).)

Padrão para uma tabela markdown no chat. Mude para CSV quando a lista tiver >25 linhas ou o usuário pedir explicitamente um arquivo.

Depois da tabela, sempre adicione **"Principais alvos de abordagem"** — os 3–5 leads quentes principais com uma frase cada sobre por que esse lead deveria ser abordado primeiro.

As colunas variam por ramo (veja os arquivos de referência), mas toda planilha de lead inclui:

- pontuação, nome do negócio/empresa, contato (quando aplicável), por-que-é-um-prospect, fonte(s), confiança, data da última verificação

---

## Salvaguardas de Compliance

Estas se aplicam a todo ramo. **Leia primeiro, em todo engajamento.**

1. **Sem scraping em massa** de LinkedIn, Google Maps, sites com paywall, ou APIs com rate-limit. O navegador é uma ferramenta de pesquisa assistida, não um scraper.
2. **Sem burlar CAPTCHA, login wall, ou proteção de bot.** Se um site exige isso, trabalhe com o que está publicamente visível.
3. **Apenas canais de contato públicos do negócio.** Use info@, contato@, e e-mails de cargo nomeado (fundador, proprietário) onde estiverem publicados no próprio site do negócio. E-mails pessoais/privados exigem base legal (relação existente, opt-in, etc.).
4. **Ciente de LGPD / CAN-SPAM / CASL.** Capture e retenha a URL de origem e a data para cada contato adicionado a uma lista — necessário para compliance de abordagem downstream. No Brasil, a LGPD é a base legal aplicável a qualquer dado pessoal tratado (finalidade legítima, minimização, e direito do titular à exclusão); CAN-SPAM e CASL entram em jogo quando a abordagem alcança contatos nos EUA/Canadá.
5. **Sem revender dado extraído** do Google Maps, LinkedIn, ou qualquer plataforma cujos termos proíbam. Construir lista para a abordagem do próprio usuário é ok; transformar a lista em produto para vender não é.
6. **Limite sua própria taxa.** Mesmo em fontes públicas, espace as requisições. Não tenha fingerprint de bot.
7. **Sem dado vazado, roubado, ou sem proveniência.** Não sourcee prospects de datasets vazados, marketplaces de contato roubado, ou list brokers sem linhagem de origem. Provedores de dado B2B licenciados (Apollo, ZoomInfo, Clearbit, Clay) são ok quando usados dentro dos termos deles e com base legal — a proibição é sobre dado ilícito/sem proveniência, não sobre fornecedores de enriquecimento legítimos.
8. **Nunca mire ou infira traços sensíveis.** Não qualifique, segmente, ou personalize com base em saúde, dificuldade financeira, crença política, sexualidade, religião, ou outros atributos protegidos/sensíveis — mesmo quando um post público os revela.

Para a referência completa de compliance (LGPD, CAN-SPAM, CASL, ToS do LinkedIn, ToS do Google Maps, restrições de uso de Clay/Apollo/ZoomInfo): veja [references/compliance.md](references/compliance.md).

---

## Inputs a Coletar

Se estiver faltando, pergunte uma vez, depois infira padrões razoáveis e continue:

- **Ramo** (SaaS / B2B / PME local / Sinal de demanda) — geralmente inferível do contexto; escolha Sinal de demanda para descoberta de primeiro cliente em estágio inicial
- **Descrição do ICP** — puxe de `product-marketing.md` se presente
- **Meta de quantidade** — padrão 25 para SaaS / B2B, 15 para PME local
- **Geografia** (essencial para PME local; útil para B2B; menos crítico para SaaS)
- **Ferramentas às quais o usuário tem acesso** — Apollo? Clay? ZoomInfo? Hunter? Truelist? Padrão para o que é grátis + navegador
- **Preferência de sinal de compra** — quais gatilhos eles deveriam priorizar? (rodadas de captação, contratação, mudança recente, etc.)

---

## Escolha Rápida de Ferramentas

Detalhamento completo em [references/data-sources.md](references/data-sources.md). Escolhas rápidas:

| Se o usuário tem acesso a... | Use para |
|-------------------------------|----------|
| **Apollo** | Descoberta firmográfica + de contato B2B / SaaS |
| **Clay** | Enriquecimento multi-fonte, waterfall lookups, pontuação customizada |
| **Clearbit** | Enriquecimento de e-mail-para-empresa e de empresa |
| **ZoomInfo** | Contato B2B enterprise + dado de intenção |
| **Hunter ou Snov** | Adivinhação e verificação de padrão de e-mail |
| **Truelist** | Validação de entregabilidade de e-mail (antes de adicionar à lista de abordagem) |
| **LinkedIn Sales Navigator** | Mapeamento de tomador de decisão (manual, sem scraping) |
| **BuiltWith / Wappalyzer** | Qualificação de stack técnica (ramo SaaS) |
| **Crunchbase** | Sinais de captação (ramo SaaS) |
| **GitHub** | Stargazers / forks de repositórios concorrentes ou adjacentes (ramo SaaS de dev-tool) |
| **Google Maps + navegador** | Descoberta de PME local |
| **Firecrawl / Browserbase** | Extração programática de sites individuais de prospect — nunca de plataformas |

**Se o usuário não tem ferramentas de enriquecimento**: apoie-se em pesquisa assistida por navegador com fontes públicas — site da empresa, página Sobre, página da empresa no LinkedIn, menções na imprensa. Mais lento, mas funciona.

---

## Formatos de Saída

### Padrão — tabela no chat

Para SaaS / B2B (≤25 linhas):

```text
| Pontuação | Empresa | Indústria | Tamanho | Sinal | Contato | Status do e-mail | Fonte | Confiança |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Para PME local (≤15 linhas) — porte da referência de local-prospector:

```text
| Pontuação | Negócio | Categoria | Área | Status do site | Site/Social | Telefone | Por que é um prospect | Confiança |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### CSV — quando >25 linhas ou o usuário pedir um arquivo

Colunas SaaS / B2B:

```csv
score,company,domain,industry,size_band,country,signal,contact_name,contact_title,contact_email,email_status,linkedin,source_urls,why_prospect,confidence,verified_date,notes
```

Colunas PME local:

```csv
score,business,category,area,distance_km,website_status,website_url,social_urls,phone,email,source_urls,why_prospect,confidence,verified_date,notes
```

### Sempre inclua depois da tabela

- **Principais alvos de abordagem**: os 3–5 leads quentes principais com uma frase de justificativa de abordagem cada
- **Parâmetros de busca**: ramo, ICP, localização/raio, quantidade-alvo, data de geração
- **Perguntas em aberto**: qualquer coisa que você não conseguiu verificar e que o usuário deveria olhar

---

## Checagens de Qualidade (antes de finalizar)

- [ ] Remover duplicatas (por domínio para SaaS/B2B, por negócio + endereço para PME local)
- [ ] Todo lead "Quente" tem um contato verificado + pelo menos uma URL de fonte
- [ ] Nenhum lead tem um e-mail que falhou na verificação do Truelist (ou seu validador) — mova para um bucket "inválido" separado e sinalize para o usuário
- [ ] Nenhum lead rotulado "Quente" carece de um sinal de compra claro
- [ ] Níveis de confiança honestos — "Alta" exige 2 fontes independentes, não apenas duas das suas próprias buscas
- [ ] Nenhum lead sourceado de scraping proibido (LinkedIn em escala, extração em massa do Google Maps, etc.)
- [ ] URL de fonte + data capturadas para cada contato (linhagem LGPD / CAN-SPAM)
- [ ] Quantidade final corresponde ao pedido do usuário, ou você explicou por que é menor (barra de qualidade)

---

## Erros Comuns

1. **Começar a descoberta sem um ICP**. Construa candidatos contra critérios vagos e você vai qualificar as coisas erradas.
2. **Tratar fontes de dado como autoritativas sem verificação cruzada**. Apollo e ZoomInfo ficam desatualizados com frequência; verifique antes de pontuar como "Quente."
3. **Adicionar contatos sem verificação de e-mail**. A reputação de cold email despenca rápido com bounces — sempre valide.
4. **Scraping em massa de LinkedIn ou Google Maps**. Risco real: suspensão de conta + violação de ToS. Navegador apenas como ferramenta assistida.
5. **Misturar ramos**. Não aplique pontuação de PME local (status do site) a um prospect B2B SaaS, ou vice-versa.
6. **Rótulos "Quente" sem sinais de compra**. Fit de ICP sozinho não basta — o sinal é o que torna o timing certo.
7. **Sem URLs de fonte**. Toda afirmação deveria ser rastreável a uma fonte pública. A abordagem futura depende dessa linhagem.
8. **Ignorar horário de silêncio / fuso horário** ao agendar a abordagem downstream (handoff para cold-email).
9. **Esquecer de reter registros de consentimento / linhagem**. Necessário para pedidos de titular sob a LGPD e auditorias de CAN-SPAM.

---

## Perguntas Específicas da Tarefa

1. Qual ramo — SaaS, B2B, PME local, ou Sinal de demanda (estágio inicial, encontrando seus primeiros clientes)?
2. Qual é o seu ICP? (Ou: devo puxar do seu contexto de product-marketing?)
3. Quantos leads qualificados você quer?
4. Quais ferramentas você tem acesso (Apollo / Clay / ZoomInfo / Hunter / Truelist / apenas navegador)?
5. Qual é o sinal de compra gatilho com o qual você mais se importa?
6. Geografia ou raio (PME local / B2B)?
7. Tabela no chat ou CSV?

---

## Integrações de Ferramenta

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md). Principais ferramentas de prospecção:

| Ferramenta | Melhor Para | MCP | Guia |
|------|----------|:---:|-------|
| **Apollo** | Descoberta firmográfica + de contato B2B / SaaS | - | [apollo.md](../../tools/integrations/apollo.md) |
| **Clay** | Enriquecimento multi-fonte + waterfall | ✓ | [clay.md](../../tools/integrations/clay.md) |
| **Clearbit** | Enriquecimento de e-mail-para-empresa | - | [clearbit.md](../../tools/integrations/clearbit.md) |
| **ZoomInfo** | Contato B2B enterprise + intenção | ✓ | [zoominfo.md](../../tools/integrations/zoominfo.md) |
| **Hunter** | Padrão de e-mail + verificação | - | [hunter.md](../../tools/integrations/hunter.md) |
| **Snov** | Localizador de e-mail + verificador | - | [snov.md](../../tools/integrations/snov.md) |
| **Truelist** | Validação de entregabilidade de e-mail | - | [truelist.md](../../tools/integrations/truelist.md) |
| **Outreach** | Engajamento de vendas (pós-lista) | ✓ | [outreach.md](../../tools/integrations/outreach.md) |
| **RB2B** | Identificação de visitante (intenção quente) | - | [rb2b.md](../../tools/integrations/rb2b.md) |
| **GitHub** | Stargazers/forks/watchers como sinal de intenção de desenvolvedor | - | [github.md](../../tools/integrations/github.md) |
| **Firecrawl** | Extração de site de alvo único (site do próprio prospect) | ✓ | [firecrawl.md](../../tools/integrations/firecrawl.md) |
| **Browserbase** | Pesquisa de site em navegador real quando renderização ou interação é necessária | ✓ | [browserbase.md](../../tools/integrations/browserbase.md) |

---

## Skills Relacionadas

- **cold-email**: Para escrever sequências de outbound contra a lista qualificada (o próximo passo natural depois da prospecção)
- **customer-research**: Para entender por que os clientes atuais compram — informa a definição do ICP
- **competitor-profiling**: Para pesquisa mais profunda em contas individuais (diferente da qualificação de construção de lista)
- **revops**: Para roteamento de lead, ciclo de vida, e handoff de CRM depois da prospecção
- **sales-enablement**: Para battle cards e one-pagers usados na abordagem
- **directory-submissions**: Para superfícies de descoberta inbound (os prospects podem te encontrar de volta)
- **product-marketing**: Para a definição de ICP que ancora todo engajamento de prospecção
