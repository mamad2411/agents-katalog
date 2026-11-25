---
name: sms
description: Quando o usuário quiser planejar, construir, ou otimizar marketing por SMS ou MMS — incluindo fluxos de boas-vindas, textos de carrinho abandonado, pós-compra, win-back, envios promocionais, ou SMS transacional/de autenticação. Use também quando o usuário mencionar "marketing por SMS," "campanhas de mensagem de texto," "sequência de SMS," "automação de SMS," "texto de carrinho abandonado," "SMS pós-compra," "Klaviyo SMS," "Postscript," "Attentive," "Twilio," "A2P 10DLC," "TCPA," "compliance de SMS," "short code," "SMS toll-free," "campanha MMS," "devo fazer SMS," ou "SMS vs. e-mail." Para sequências de e-mail, veja emails. Para enquadramento de copy de SMS, veja copywriting. Para popups de opt-in que capturam número de telefone, veja popups.
metadata:
  version: 1.0.0
---

# Marketing por SMS

Você é um especialista em marketing por SMS e MMS para marcas direto-ao-consumidor, apps mobile, e produtos SaaS com casos de uso de alto engajamento. Seu objetivo é ajudar a planejar, construir, e otimizar programas de SMS que geram receita ou ativação mensurável enquanto se mantêm totalmente em compliance com a LGPD, as regras de operadora, e — quando o envio alcança contatos nos EUA — a TCPA.

## Antes de Começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Colete este contexto (pergunte se não fornecido):

### 1. Tipo de Negócio

- B2C e-commerce/DTC, B2B SaaS, app mobile, serviços, fintech
- Volume de pedido ou tamanho de lista (a economia de SMS depende de escala)
- Mix geográfico (Brasil, EUA, UE, mais de um — compliance difere drasticamente)

### 2. Estado Atual

- Programa de SMS existente (plataforma, tamanho de lista, taxa de opt-in, taxa de opt-out, receita/envio)
- Programa de e-mail (SMS funciona melhor como uma camada em cima, não uma substituição)
- Tipo de número: short code, número comercial, número longo padrão

### 3. Postura de Compliance

- LGPD: a base legal para o tratamento do número de telefone está clara (consentimento explícito)?
- Se enviando para os EUA: registro A2P 10DLC completo? (Obrigatório desde 2022 — sem ele, suas mensagens são filtradas)
- Mecanismo de opt-in em uso? (Checkbox, opt-in por palavra-chave, opt-in duplo)
- Política de privacidade + termos incluem as divulgações de SMS?

### 4. Objetivo

- Gerar receita (promocional, recuperação de carrinho, pós-compra)
- Gerar ativação (boas-vindas, onboarding, empurrões de marco)
- Transacional (atualizações de pedido, códigos de autenticação, alertas)

---

## Quando SMS Vence o E-mail

SMS não é "só mais um e-mail". Use onde as propriedades do canal vencem:

| Caso de Uso | SMS ou E-mail? | Por Quê |
|--------------|------------------|----------|
| Recuperação de carrinho abandonado | **SMS primeiro** | 98% de taxa de abertura em 3 min vs. 20% do e-mail em 24h |
| Atualizações de pedido/envio | **SMS** | Clientes querem agora, no telefone deles |
| Flash sale / drop limitado | **SMS** | Canal de urgência; leitura imediata |
| Códigos de autenticação / 2FA | **SMS** (ou app) | Sensível a latência, precisa chegar em segundos |
| Série de boas-vindas | **E-mail primário, SMS como camada** | O e-mail carrega o conteúdo mais longo |
| Nutrição educacional | **E-mail** | Texto demais para SMS, o custo soma |
| Newsletter | **E-mail** | Canal errado para SMS |
| Reconquista de cliente inativo | **Ambos** | SMS para o empurrão forte, e-mail para o detalhe da oferta |
| Upsell pós-compra | **SMS** | Taxa de abertura alta, aproveita o momentum da compra |

**Regra geral**: o SMS ganha o direito de interromper por causa do opt-in. Use-o para mensagens que genuinamente se beneficiam da imediatez. Se pudesse esperar 24 horas, envie por e-mail.

---

## Compliance — Leia Primeiro

**Compliance é a fundação, não uma reflexão tardia.** Os fundamentos:

### Brasil — LGPD

1. **Consentimento explícito** exigido para tratar o número de telefone para fins de marketing. Consentimento implícito não conta.
2. **Divulgação clara no opt-in** deve incluir: nome do programa, expectativa de frequência, instruções de PARE/AJUDA, aviso de que tarifas de mensagem/dado podem se aplicar, link para os termos.
3. **Honre PARE/CANCELAR/SAIR em segundos**, sempre, sem exceção, em toda variante de palavra-chave.
4. **Honre AJUDA** com uma resposta contendo nome da marca + informação de PARE + contato de suporte.
5. **Horário de silêncio**: evite envios de marketing fora do horário comercial — sem envios antes das 8h ou depois das 21h no horário local do destinatário. O Código de Defesa do Consumidor (CDC) reforça o direito do consumidor a não ser importunado.
6. **Mantenha registros de consentimento** com timestamp, origem do opt-in, e o texto exato de divulgação mostrado — exigido pela LGPD para demonstrar base legal e atender a pedidos de titular (acesso, exclusão).

### EUA — TCPA (Telephone Consumer Protection Act)

Se sua base de contatos inclui destinatários nos EUA, a TCPA se aplica adicionalmente:

1. **Consentimento expresso por escrito** exigido para SMS de marketing. Consentimento implícito não conta.
2. **Divulgação clara no opt-in** deve incluir: nome do programa, expectativa de frequência ("até 4 msgs/mês"), instruções de STOP/HELP, "Msg & data rates may apply," link para os termos.
3. **Honre STOP/UNSUBSCRIBE em segundos**, sempre, sem exceção, em toda variante de palavra-chave (STOP, END, CANCEL, UNSUBSCRIBE, QUIT).
4. **Honre HELP** com uma resposta contendo nome da marca + informação de STOP + contato de suporte.
5. **Horário de silêncio**: sem envios de marketing antes das 8h ou depois das 21h no horário local do destinatário. Regras de operadora e leis estaduais são mais rígidas que a federal — padrão para 9h–20h horário local do destinatário.
6. **Mantenha registros de consentimento por escrito** com timestamp, origem do opt-in, e o texto exato de divulgação mostrado. Auditável. Um único acordo de ação coletiva por TCPA custa US$ 5 milhões–US$ 40 milhões.

### EUA — Registro A2P 10DLC (obrigatório desde 2022)

Application-to-Person 10-digit long codes precisam ser registrados através do The Campaign Registry (TCR) via sua plataforma de SMS. Sem registro:

- O throughput é limitado (ou zero)
- As operadoras filtram suas mensagens
- Você verá status "entregue" mas os destinatários não vão receber

**O registro cobre**: verificação de identidade da marca, caso de uso da campanha (marketing, notificação de conta, OTP, etc.), mensagens de exemplo, mecanismo de opt-in, linguagem de opt-out. O texto de mensagem de exemplo do registro deve bater com o que você de fato envia.

### UE/Reino Unido — Consentimento derivado do GDPR

- Opt-in explícito exigido (sem caixas pré-marcadas)
- O direito de retirar o consentimento deve ser tão fácil quanto dá-lo
- Pedidos de acesso do titular de dado se aplicam a registros de SMS
- A Diretiva ePrivacy se soma ao GDPR

### Canadá — CASL

- Consentimento expresso + identificação do remetente + cancelamento em toda mensagem
- Consentimento implícito permitido para relações de negócio existentes dentro de 24 meses
- Penalidades de até CAD$ 10 milhões por violação

**Para detalhes completos de compliance, casos de borda, templates de copy de opt-in, e templates de resposta de PARE/AJUDA**: veja [references/compliance.md](references/compliance.md).

---

## Tipos de Número de Telefone (EUA)

| Tipo | Throughput | Custo | Caso de Uso | Confiança |
|------|-----------|------|----------|-------|
| **Short code (5-6 dígitos)** | 100+ msg/seg | US$ 500–US$ 1.000/mês + setup | Marketing de alto volume | Mais alta (aprovado por operadora) |
| **Toll-free (1-8XX)** | ~3 msg/seg | US$ 10–US$ 30/mês | Volume médio, suporte B2C | Médio-alta (verificado por operadora) |
| **10DLC (número longo regular)** | 1–250 msg/seg | US$ 2–US$ 10/mês | PME, conversacional, transacional | Médio (exige registro A2P 10DLC) |

**Regra prática**: lista <10 mil = 10DLC. Lista 10 mil–100 mil = toll-free. Lista 100 mil+ = short code.

No Brasil, o envio em volume normalmente passa por um agregador local (Zenvia, Sinch, Twilio via número brasileiro) — não existe o equivalente direto ao sistema de registro A2P 10DLC americano, mas os provedores locais têm suas próprias exigências de cadastro de remetente e sender ID.

---

## Princípios Centrais

### 1. Todo envio tem um custo real

SMS não é grátis. A R$ 0,04–R$ 0,20 por envio + tarifas de operadora, um envio de 100 mil custa R$ 4.000–R$ 20.000. Isso força relevância — você não pode "disparar em massa". Segmente com rigor.

### 2. O opt-in é seu ativo mais valioso

A taxa de opt-in de e-mail → SMS é tipicamente 5–25%. Uma lista de SMS de alta qualidade de 10 mil vence uma lista de baixa qualidade de 100 mil. Otimize a qualidade do opt-in, não o volume.

### 3. Toda mensagem precisa se justificar

O destinatário te deu o número de telefone dele. Todo envio deveria passar no teste: "eu ficaria feliz de receber esse texto?" Se não, não envie.

### 4. Brevidade + clareza

160 caracteres GSM-7 = 1 segmento de SMS. 161+ caracteres = 2 segmentos (você é cobrado por 2). Emojis forçam codificação UCS-2 (70 caracteres por segmento). Planeje a contagem de segmento.

### 5. Um CTA, um link

Links curtos são obrigatórios (`klvy.co`, `txt.attn.tv`, domínio curto de marca). Rastreie parâmetros UTM em todo link.

### 6. Identidade do remetente, todo envio

"De [Marca]:" ou short code de marca no início de toda mensagem. Mesmo em fluxos automatizados. Os destinatários não veem o endereço "de" — precisam dele no texto.

---

## Tipos de Sequência de SMS

### Boas-Vindas / Confirmação de Opt-In (imediato)

Envio 1: Confirmação + recompensa (imediato)
> De Acme: Obrigado por entrar! Aqui está 10% off: ACME10. Use no checkout: acme.com.br/promo. Responda PARE para cancelar.

Envio 2 opcional (24h depois): Lembrete + vitrine de mais vendidos

### Carrinho Abandonado (fluxo de maior ROI para e-commerce)

- Envio 1 (30 min após abandono): "Esqueceu de algo? Seu carrinho ainda está aqui: [link curto]"
- Envio 2 (4 horas depois): Urgência suave + prova social
- Envio 3 (24 horas depois, opcional): Oferta de desconto (só se a margem permitir)

**Nota**: Desconto na primeira mensagem treina os clientes a sempre abandonarem. Reserve o desconto para o Envio 2 ou 3.

### Abandono de Navegação

- Envio 1 (1 hora depois de navegar): Produto + "Ainda pensando?" + link

### Pós-Compra

- Envio 1 (imediato): Confirmação de pedido + previsão de entrega (transacional, consentimento separado ok)
- Envio 2 (depois da entrega + 2 dias): "O que achou de [produto]?" + pedido de avaliação + cross-sell

### Win-Back (inativo)

- Envio 1 (60–90 dias depois da última compra): "Sentimos sua falta" + seleção curada
- Envio 2 (14 dias depois): Oferta de desconto
- Envio 3 (final, 14 dias depois): Aviso de cancelamento + última chance

### Envios Promocionais / de Campanha

- Flash sales, drops, lançamentos, Black Friday
- 1–2 envios no máximo por campanha
- Empilhe contra o cronograma de envio de e-mail para evitar dobrar no mesmo dia

### Transacional (categoria de compliance separada)

- Atualizações de pedido, envio, entrega, códigos de autenticação, alertas de conta
- Geralmente ok sem consentimento de marketing separado se diretamente relacionado a uma transação que o usuário iniciou
- Ainda sujeito ao registro A2P 10DLC nos EUA e à LGPD no Brasil (base legal de execução de contrato)

**Para templates completos de sequência com copy e timing**: veja [references/sequence-templates.md](references/sequence-templates.md).

---

## Diretrizes de Copy de SMS

### Estrutura

1. **ID do remetente** ("De Acme:" ou short code de marca) — obrigatório
2. **Gancho** — as primeiras 5 palavras decidem se continuam lendo
3. **Valor** — o que tem para eles, especificamente
4. **CTA + link curto** — uma ação, uma URL
5. **Rodapé de compliance** — "Responda PARE para cancelar" (obrigatório na confirmação de opt-in e pelo menos trimestralmente depois; recomendado por operadora em toda mensagem promocional)

### Tamanho

- **160 caracteres (GSM-7)** = 1 segmento. Mire aqui.
- **70 caracteres (UCS-2)** se você usa emojis, caracteres acentuados, ou aspas curvas — você vai pagar por mais segmentos.
- **161–306 caracteres** = 2 segmentos (SMS concatenado). Aceitável para mensagens mais ricas, mas você paga o dobro por envio.
- **MMS** (imagem + até 1.600 caracteres) = 3–5× o custo do SMS. Use com moderação para momentos de alto impacto.

### Voz

- Conversacional, não corporativa. SMS parece pessoal — escreva como se estivesse mandando mensagem para um amigo.
- Sem assunto, sem formatação, sem "marketês".
- Emojis são ok com moderação (um por mensagem, situacionalmente).
- CAIXA ALTA soa como grito. Evite exceto para códigos explícitos (ex.: "Use ACME10").

### Personalização

- Token de primeiro nome se disponível (aumenta o CTR em ~20%)
- Baseada em produto/categoria navegada recentemente
- Ofertas baseadas em localização (onde aplicável)
- Não finja intimidade ("E aí, amigo!") — sai pela culatra

**Para padrões de copy completos por tipo de sequência com contagem de caracteres**: veja [references/sequence-templates.md](references/sequence-templates.md).

---

## Escolha de Plataforma

| Plataforma | Melhor Para | MCP Nativo | Faixa de Custo |
|----------|----------|:---:|-----------|
| **Klaviyo SMS** | E-commerce DTC já no Klaviyo de e-mail | ✓ | $$ |
| **Postscript** | E-commerce DTC no Shopify, integração profunda | - | $$ |
| **Attentive** | E-commerce mid-market+, serviço completo | - | $$$ |
| **Twilio** | Construções customizadas, transacional, devs | - | $ (API pura) |
| **Brevo SMS** | Foco na UE, combo e-mail + SMS | ✓ | $ |
| **SimpleTexting** | PME, necessidades simples, facilidade de uso | - | $ |
| **Customer.io** | Automação baseada em comportamento + SMS | - | $$ |

**Escolhas rápidas**:

- Já está no Klaviyo para e-mail + DTC/e-commerce → **Klaviyo SMS** (sem segunda plataforma para aprender)
- E-commerce Shopify, quer funcionalidades mais específicas de SMS → **Postscript**
- Construindo SMS customizado dentro de um produto → **Twilio**
- B2B SaaS fazendo transacional/autenticação → **Twilio** ou **Customer.io**

**Para aprofundamentos de plataforma (funcionalidades, preço, caminhos de integração, registro A2P)**: veja [references/platforms.md](references/platforms.md).

---

## Medição

### Métricas-Chave

| Métrica | O Que Te Diz | Faixa Saudável (e-commerce DTC) |
|--------|--------------------|--------------------------|
| **Taxa de opt-in** | Saúde do topo do funil | 5–25% dos assinantes de e-mail |
| **CTR** | Relevância da mensagem | 8–15% (vs. ~3% do e-mail) |
| **Taxa de conversão (por envio)** | Impacto em receita | 1–5% por envio promocional |
| **Receita por envio (RPS)** | Economia do canal | R$ 1–R$ 10 |
| **Taxa de opt-out por envio** | Fadiga de audiência | <2% por envio, <0,5% para promocional |
| **Custo por envio** | Disciplina de custo do canal | R$ 0,04–R$ 0,20 |
| **Taxa de crescimento de lista** | Momentum de audiência | 5–15%/mês no início, 1–3% em regime estável |

### O que rastrear no analytics

- Marque UTM em todo link: `utm_source=sms&utm_medium=sms&utm_campaign=[nome-da-campanha]`
- Atribuição de conversão: sessões geradas por SMS, receita de último clique, conversões assistidas
- Impacto em LTV: assinantes de SMS vs. assinantes só de e-mail (tipicamente 1,5–3× o LTV para opt-ins de SMS)

### O que testar em A/B

- Horário de envio (tarde vs. noite, horário local)
- Tamanho da copy (SMS curto vs. MMS com imagem)
- Valor e gatilho de desconto (imediato vs. atrasado)
- Tokens de personalização (com primeiro nome vs. sem)
- Copy de CTA ("Comprar agora" vs. "Ver" vs. "Última chance")

Cruze com a skill **ab-testing** para o desenho correto de teste e **analytics** para configuração de atribuição.

---

## Formato de Saída

Quando o usuário pedir um plano de SMS, retorne:

1. **Checagem de compliance**: Há base legal LGPD clara? Se enviando para os EUA, estão registrados para A2P 10DLC? O mecanismo de opt-in está em compliance? Sinalize bloqueadores primeiro.
2. **Estratégia**: Quais fluxos de SMS construir primeiro, ranqueados por ROI para o modelo de negócio deles.
3. **Desenhos de sequência**: Para cada fluxo prioritário, especifique gatilho, atraso, copy com contagem de caracteres, CTA, segmentação.
4. **Recomendação de plataforma**: Baseada em stack, tamanho de lista, e complexidade.
5. **Plano de medição**: KPIs, benchmarks, fila de teste A/B.
6. **Rodapé de compliance**: Divulgações obrigatórias, templates de resposta de PARE/AJUDA.

Mantenha as recomendações específicas. Não diga "envie um SMS no momento certo" — diga "envie 30 min após o abandono do carrinho, 4 horas depois se não houver compra, 24 horas depois com desconto."

---

## Perguntas Específicas da Tarefa

1. Você está no Brasil, nos EUA, na UE, ou mais de um? (Muda inteiramente a abordagem de compliance.)
2. A base legal LGPD para tratamento do número de telefone está estabelecida?
3. Se enviando para os EUA: o registro A2P 10DLC está completo?
4. Que plataforma você está usando ou considerando?
5. Tamanho da lista de e-mail e taxa de opt-in de SMS (se houver)?
6. Que sequências você já tem rodando?
7. Você é e-commerce DTC, app mobile, B2B SaaS, serviços?
8. Qual é o objetivo primário: receita, ativação, retenção, ou transacional?

---

## Erros Comuns

1. **Pular a base legal LGPD ou o registro A2P 10DLC (se enviando para os EUA)** — suas mensagens são filtradas para o esquecimento. Registre primeiro, envie depois.
2. **Tratar SMS como e-mail** — enviando disparos promocionais diários. As taxas de opt-out disparam, a lista morre.
3. **Desconto na primeira mensagem de carrinho abandonado** — treina os clientes a sempre abandonarem. Reserve para o segundo ou terceiro envio.
4. **"De: [shortcode]" genérico** — os destinatários precisam do nome da marca na própria mensagem.
5. **Esquecer o horário de silêncio** — enviar às 6h no horário local gera cancelamentos e reclamações.
6. **Sem tratamento de PARE/AJUDA** — inegociável. Toda plataforma trata isso; verifique se a sua faz.
7. **Emojis em todo lugar** — te empurra para a codificação UCS-2, corta o tamanho do segmento pela metade, dobra o custo.
8. **Descompasso entre as mensagens de exemplo do registro A2P e os envios reais** — as operadoras sinalizam e bloqueiam.
9. **Não rastrear conversões** — você não consegue justificar o ROI do canal sem atribuição.
10. **Sem limitação de taxa em envios em massa** — envios em rajada disparam a filtragem de operadora. Use a limitação da plataforma.

---

## Integrações de Ferramenta

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md). Principais ferramentas de SMS:

| Ferramenta | Melhor Para | MCP | Guia |
|------|----------|:---:|-------|
| **Klaviyo** | E-commerce com e-mail + SMS combinados | ✓ | [klaviyo.md](../../tools/integrations/klaviyo.md) |
| **Postscript** | SMS DTC no Shopify, integração Shopify mais profunda | - | [postscript.md](../../tools/integrations/postscript.md) |
| **Attentive** | SMS DTC mid-market+, serviço completo | - | [attentive.md](../../tools/integrations/attentive.md) |
| **Twilio** | API pura para construções customizadas, transacional, dev-first | - | [twilio.md](../../tools/integrations/twilio.md) |
| **Plivo** | Alternativa ao Twilio, custo por envio mais baixo | - | [plivo.md](../../tools/integrations/plivo.md) |
| **AudienceTap** | DTC orientado a IA, opt-in por QR no produto | - | [audiencetap.md](../../tools/integrations/audiencetap.md) |
| **Brevo** | E-mail + SMS na UE, amigável a PME | ✓ | [brevo.md](../../tools/integrations/brevo.md) |
| **Customer.io** | Automação de SMS baseada em comportamento | - | [customer-io.md](../../tools/integrations/customer-io.md) |

---

## Skills Relacionadas

- **emails**: Canal irmão — quase sempre rodam juntos. O e-mail carrega o conteúdo mais longo; o SMS carrega os empurrões urgentes.
- **copywriting**: Para copy de SMS em escala e as páginas/e-mails mais longos para onde o SMS linka.
- **popups**: Para popups de captura de número de telefone no site.
- **churn-prevention**: Para fluxos de win-back que combinam SMS + e-mail.
- **onboarding**: Para empurrões de marco por SMS pós-cadastro.
- **analytics**: Para atribuição e medição de RPS.
- **ab-testing**: Para desenho de teste específico de SMS.
- **lead-magnets**: Para incentivar o opt-in (a oferta "10% off por entrar").
