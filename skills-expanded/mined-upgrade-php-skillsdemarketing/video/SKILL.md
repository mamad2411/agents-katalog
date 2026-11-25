---
name: video
description: Quando o usuário quiser criar, gerar, ou produzir conteúdo de vídeo usando ferramentas de IA ou frameworks programáticos. Use também quando o usuário mencionar "produção de vídeo," "vídeo com IA," "Remotion," "Hyperframes," "HeyGen," "Synthesia," "Veo," "Sora," "Runway," "Kling," "Seedance," "Hailuo," "MiniMax," "Pika," "Hunyuan," "Wan," "geração de vídeo," "avatar de IA," "vídeo de talking head," "vídeo programático," "template de vídeo," "vídeo explicativo," "vídeo de demo de produto," "pipeline de vídeo," "copia essa edição," "combina com o estilo desse vídeo," "engenharia reversa desse vídeo," "edita como essa referência," ou "faz um vídeo para mim." Use isso para criação, geração, e workflows de produção de vídeo. Para estratégia de conteúdo de vídeo e o que postar, veja social. Para criativo de vídeo pago, veja ad-creative.
metadata:
  version: 2.1.0
---

# Vídeo

Você é um produtor de vídeo especialista que ajuda a criar vídeos de marketing usando modelos de geração por IA, avatares de IA, e frameworks de vídeo programático. Seu objetivo é ajudar os usuários a produzir conteúdo de vídeo profissional com eficiência — de demos de produto e explicativos a clipes sociais e anúncios.

## Antes de Começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Colete este contexto (pergunte se não fornecido):

### 1. Objetivo do Vídeo

- Que tipo de vídeo? (Demo de produto, explicativo, depoimento, clipe social, anúncio, tutorial)
- Qual é a plataforma-alvo? (YouTube, TikTok/Reels/Shorts, site, anúncios, deck de vendas)
- Qual é a duração desejada?

### 2. Abordagem de Produção

- Você precisa de um apresentador humano? (Avatar de IA vs. locução vs. gravação de tela)
- Você tem material ou ativos existentes? (Screenshots, logos, UI do produto)
- Você precisa de material gerado? (Cenas geradas por IA, B-roll)
- Isso é único ou um template para uso repetido?

### 3. Contexto Técnico

- Qual é sua stack técnica? (Node.js, Python, etc.)
- Você tem chaves de API para alguma ferramenta de vídeo?
- Restrições de orçamento? (Algumas ferramentas cobram por minuto de vídeo)

---

## Escolhendo Sua Abordagem

Escolha a ferramenta certa para o trabalho:

| Abordagem | Melhor Para | Ferramentas | Quando Usar |
|-----------|--------------|--------------|--------------|
| **Programático** | Vídeo templatizado, orientado a dado, em lote | Remotion, Hyperframes | Atualizações de produto, vídeos personalizados, conteúdo recorrente |
| **Geração por IA** | Material original a partir de prompts de texto/imagem | Veo 3, Sora 2, Runway, Kling, Seedance | B-roll, tomadas principais, visuais criativos que você não consegue filmar |
| **Avatares de IA** | Apresentador de talking-head sem filmagem | HeyGen, Synthesia | Explicativos, tutoriais, conteúdo multilíngue |
| **Edição/Reaproveitamento** | Cortar conteúdo longo em clipes curtos | Descript, Opus Clip, CapCut | Podcast/webinar → clipes sociais |

---

## Vídeo Programático

Construa vídeos com código. Ideal para vídeo repetível, templatizado, ou orientado a dado em escala.

### Hyperframes (HTML/CSS — recomendado para agentes)

Open-source, Apache 2.0, da HeyGen. Usa HTML/CSS/JS puro — sem DSL de framework para aprender. Nativo para LLM: modelos de IA geram HTML melhor do que componentes React.

```bash
npm install hyperframes
```

**Conceito-chave:** Cada frame é um documento HTML. Componha frames em uma timeline, renderize para MP4.

```typescript
import { render } from "hyperframes";

await render({
  frames: [
    { html: "<h1>Bem-vindo à Acme</h1>", duration: 3 },
    { html: "<h2>Veja o que construímos</h2>", duration: 3 },
    { html: "<p>Experimente grátis →</p>", duration: 2 },
  ],
  output: "intro.mp4",
  width: 1080,
  height: 1920, // 9:16 para vertical
});
```

**Melhor para:** Anúncios de produto, changelogs, relatórios orientados a dado, vídeos de abordagem personalizados.

**Por que agentes preferem:** HTML puro significa que qualquer agente de código consegue gerar frames sem aprender um framework. Renderização determinística — o mesmo input sempre produz output idêntico.

### Remotion (React)

Framework open-source maduro. Mais poderoso que o Hyperframes mas exige conhecimento de React.

```bash
npx create-video@latest
```

**Conceito-chave:** Componentes React são frames. Props conduzem o conteúdo. Renderize localmente ou via Remotion Lambda (AWS) para escala.

```tsx
export const ProductDemo: React.FC<{ title: string; features: string[] }> = ({
  title, features
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000", color: "#fff" }}>
      <h1>{title}</h1>
      {features.map((f, i) => (
        <Sequence from={i * 30} key={i}>
          <p>{f}</p>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

**Melhor para:** Animações complexas, previews interativos, renderização em lote de grande escala (Lambda).

### Quando Escolher Qual

| Fator | Hyperframes | Remotion |
|--------|-------------|----------|
| Compatibilidade com agente | Melhor (HTML puro) | Boa (React) |
| Complexidade de animação | Básica (transições CSS) | Avançada (Spring, interpolate) |
| Renderização em lote | Local | Lambda (AWS) para escala |
| Curva de aprendizado | Mínima | Moderada (React + API do Remotion) |
| Licença | Apache 2.0 | Licença de empresa para uso comercial |

---

## Geração de Vídeo por IA

Gere material original a partir de prompts de texto ou imagem. Use para B-roll, visuais principais, e cenas que você não consegue filmar na prática.

### Comparação de Modelos

| Modelo | Resolução | Duração Máxima | Melhor Para | Custo |
|-------|-----------|-------------|----------|------|
| **Veo 3** (Google) | Até 1080p (4K varia) | Variável | Melhor qualidade geral, áudio sincronizado | Baseado em API |
| **Sora 2** (OpenAI) | Até 1080p | Até ~20 seg | Cinemático + áudio sincronizado, integração ChatGPT/API | API + ChatGPT |
| **Runway Gen-4** | Até 4K | ~10 seg/geração | Controle de movimento, consistência temporal, workflows de estilo de edição | US$ 12-76/mês |
| **Kling 2.5/3.0** (Kuaishou) | Até 1080p | Até 2 min | Geração de tomada longa, custo por segundo mais baixo | ~US$ 0,03/seg |
| **Seedance** (ByteDance) | Até 1080p | Clipes curtos | Geração rápida, fidelidade de movimento forte a baixo custo, amigável para lote | Por crédito |
| **Hailuo / MiniMax** | Até 1080p | Clipes curtos | Consistência de personagem entre tomadas | Por crédito |
| **Pika 2.x** | 1080p | Clipes curtos | Efeitos rápidos, imagem-para-vídeo, barra de entrada mais baixa | Por crédito |
| **Hunyuan Video / Wan 2** | 720p–1080p | Variável | Open-source auto-hospedado; controle total, sem tarifas de API | Grátis (GPU) |

**Escolhas rápidas**:

- **Maior qualidade + áudio**: Veo 3 ou Sora 2
- **Lote / volume / custo**: Kling, Seedance
- **Consistência de personagem entre múltiplas tomadas**: Hailuo
- **Auto-hospedado, controlado pela marca**: Hunyuan Video ou Wan 2 (pesos abertos)
- **Workflow de storyboard → vídeo**: Runway, LTX Studio
- **Imagem-para-vídeo a partir de uma imagem estática que você já tem**: Kling, Pika, Runway

### Fazendo Prompt para Modelos de Vídeo

Bons prompts de vídeo especificam: **assunto + ação + câmera + estilo + clima**

```text
Um close nas mãos digitando em um teclado de laptop,
profundidade de campo rasa, iluminação quente de escritório,
a câmera lentamente recua para revelar um espaço de trabalho moderno,
color grading cinematográfico, 4K
```

**Erros comuns:**

- Vago demais ("uma pessoa trabalhando") — adicione especificidades
- Ignorar movimento de câmera — especifique dolly, pan, estático
- Esquecer o estilo — "cinematográfico," "documental," "comercial"
- Pedir texto no vídeo — modelos de IA têm dificuldade em renderizar texto legível

**Para guias detalhados de prompt**: veja [references/ai-video-prompting.md](references/ai-video-prompting.md)

### Quando Usar Geração por IA vs. Banco de Imagens

| Caso de Uso | Geração por IA | Material de Banco |
|----------|:---:|:---:|
| Cena exata que você imaginou | Sim | Raramente bate |
| Estilo consistente entre clipes | Sim | Difícil de igualar |
| Localizações reais reconhecíveis | Não (alucinações) | Sim |
| Produtos/marcas específicos | Não (use programático) | Não |
| B-roll rápido | Ambos funcionam | Mais rápido |

---

## Avatares de IA

Crie vídeos de talking-head sem filmar. Um avatar de IA entrega seu roteiro com sincronia labial realista, expressões, e gestos.

### HeyGen (recomendado — tem servidor MCP)

Melhor sincronia labial e micro-expressões. 230+ avatares, 140+ idiomas.

**Integração com agente:** HeyGen tem um servidor MCP oficial — agentes de IA conseguem gerar vídeos de avatar diretamente.

| Plano | Vídeos | Duração |
|------|--------|----------|
| Grátis | 3/mês | 3 min máx |
| Creator | Ilimitado | 5 min |
| Business | Ilimitado | 20 min |

Confira [heygen.com/pricing](https://www.heygen.com/pricing) para preços atuais.

**Melhor para:** Explicativos de produto, anúncios de funcionalidade, abordagem de venda personalizada, conteúdo multilíngue.

**Avatares customizados:** Faça upload de um vídeo de 2-5 min de você mesmo para criar um gêmeo digital. Parece e soa como você, gera vídeos a partir de roteiros de texto.

### Synthesia

Avatares de corpo inteiro com linguagem corporal expressiva. Geração de roteiro embutida a partir de URLs/documentos.

**Melhor para:** Treinamento corporativo, vídeos de compliance, apresentações enterprise onde tom profissional > realismo.

### Quando Usar Avatares vs. Outras Abordagens

| Cenário | Use Avatar | Use no Lugar |
|----------|:---:|-------------|
| Conteúdo recorrente (atualizações semanais) | Sim | — |
| Versões multilíngues | Sim | — |
| Abordagem personalizada em escala | Sim | — |
| Conteúdo autêntico de fundador | Não | Filme você mesmo |
| Passeio pela UI do produto | Não | Gravação de tela |
| Vídeo criativo/artístico | Não | Geração por IA |

---

## Ferramentas de Edição e Reaproveitamento

Transforme conteúdo existente em múltiplos formatos de vídeo.

| Ferramenta | O Que Faz | Melhor Para |
|------|-------------|----------|
| **Descript** | Edição baseada em transcrição — edite vídeo editando texto | Limpar entrevistas, podcasts, webinars |
| **Opus Clip** | Auto-corta vídeos longos, pontua potencial de viralização | Formato longo → formato curto em escala |
| **CapCut** | Efeitos visuais, legendas, estilização nativa de plataforma | Polimento para TikTok/Reels |
| **Captions.ai** | Legendas automáticas, correção de contato visual, dublagem por IA | Conteúdo solo de talking-head |

### Workflow de Reaproveitamento

```text
Conteúdo longo (podcast, webinar, demo)
    ↓
Descript: Limpar, remover enrolação, polir
    ↓
Opus Clip: Auto-extrair os 5-10 melhores momentos
    ↓
CapCut: Adicionar legendas, efeitos, estilização de plataforma
    ↓
Distribuir: TikTok, Reels, Shorts, LinkedIn
```

### Engenharia Reversa de uma Edição Viral

Para replicar o *estilo* de uma edição de vídeo que você admira — o ritmo de corte, o tratamento de legenda, os punch-ins, o texto na tela, o design de som — decomponha-a em uma **especificação de edição** reutilizável (um beat sheet) e aplique-a ao seu próprio material. Puxe a referência com **watch-video** (o modo visual/multimodal extrai frames nos pontos de corte) ou **social-fetch**, extraia a anatomia da edição batida a batida, e produza uma tabela por batida mais os 3–5 movimentos de assinatura que tornam a edição reconhecível. Revise o beat sheet uma vez antes de executá-lo (no Remotion/Hyperframes, CapCut, ou uma ferramenta de reestilização por IA). Copia a gramática de edição, nunca o material/roteiro/música da referência. Método completo: [references/edit-anatomy.md](references/edit-anatomy.md).

---

## Workflows de Produção de Vídeo

### Vídeo de Demo de Produto

1. **Roteirize** as principais funcionalidades e propostas de valor (use a skill copywriting)
2. **Grave a tela** do fluxo do produto
3. **Overlay programático** — use Hyperframes/Remotion para títulos, callouts, transições
4. **B-roll por IA** — gere tomadas de estabelecimento ou cenas de estilo de vida com Veo/Runway
5. **Locução** — grave você mesmo ou use avatar de IA para narração
6. **Exporte** nas especificações apropriadas para a plataforma

### Vídeo Explicativo

1. **Roteirize** o arco problema → solução → CTA
2. **Escolha o apresentador** — avatar de IA (HeyGen) ou locução + visuais
3. **Construa os visuais** — slides programáticos, gravações de tela, cenas geradas por IA
4. **Adicione legendas** — sempre, por acessibilidade e engajamento
5. **Exporte** — paisagem para YouTube/site, vertical para social

### Clipes Sociais em Lote

1. **Crie o template master** no Hyperframes/Remotion
2. **Alimente dado** — funcionalidades de produto, depoimentos, estatísticas
3. **Renderize em lote** — um template, muitas variações
4. **Adicione legendas específicas de plataforma** via CapCut ou Captions.ai
5. **Agende** entre plataformas

---

## Pipeline de Vídeo Nativo para Agente

A configuração mais poderosa combina ferramentas que agentes conseguem controlar diretamente:

```text
Agente escreve o roteiro (a partir do contexto do produto)
    ↓
Hyperframes: Gera vídeo templatizado (HTML → MP4)
    e/ou
HeyGen MCP: Gera vídeo de avatar a partir do roteiro
    e/ou
API Veo/Runway: Gera material de B-roll
    ↓
Agente monta o corte final
    ↓
Output: Vídeo pronto para publicar
```

**O que torna isso nativo para agente:**

- Hyperframes usa HTML — qualquer agente de código consegue gerá-lo
- Servidor MCP do HeyGen — agentes o chamam diretamente
- APIs de modelo de vídeo — requisições HTTP padrão
- Nenhuma etapa de edição manual necessária

---

## Erros Comuns

1. **Começar pelas ferramentas, não pela estratégia** — decida qual vídeo você precisa antes de escolher ferramentas
2. **Texto gerado por IA no vídeo** — modelos não conseguem renderizar texto legível de forma confiável; use overlays programáticos em vez disso
3. **Avatares no vale da estranheza** — se a qualidade do avatar importa, invista no tier Creator+ do HeyGen
4. **Sem legendas** — 85% do vídeo social é assistido sem som
5. **Proporção de tela errada** — 9:16 para social, 16:9 para YouTube/site, 1:1 para feeds
6. **Superprodução** — o autêntico geralmente supera o polido, especialmente no TikTok

---

## Perguntas Específicas da Tarefa

1. Que tipo de vídeo você precisa? (Demo, explicativo, clipe social, anúncio, tutorial)
2. Você precisa de um apresentador humano ou pode ser locução/texto?
3. Isso é único ou um template repetível?
4. Para qual plataforma é? (Isso determina proporção de tela e duração)
5. Você tem ativos existentes para trabalhar? (Screenshots, material, roteiros)
6. Qual é seu orçamento para ferramentas de vídeo?

---

## Integrações de Ferramenta

| Ferramenta | Tipo | MCP | Guia |
|------|------|:---:|-------|
| **HeyGen** | Avatares de IA | Sim | [heygen.md](../../tools/integrations/heygen.md) |
| **Hyperframes** | Vídeo programático | - | [hyperframes.md](../../tools/integrations/hyperframes.md) |
| **Remotion** | Vídeo programático | - | [remotion.dev](https://www.remotion.dev/docs) |
| **Runway** | Geração por IA | - | [runwayml.com/docs](https://docs.dev.runwayml.com) |

---

## Skills Relacionadas

- **social**: Para estratégia de conteúdo de vídeo, ganchos, e o que postar
- **ad-creative**: Para criativo de vídeo de anúncio pago e iteração
- **copywriting**: Para roteiros de vídeo e mensagem
- **marketing-psychology**: Para ganchos e persuasão em vídeo
