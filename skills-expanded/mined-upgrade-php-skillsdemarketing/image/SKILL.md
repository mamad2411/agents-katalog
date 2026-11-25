---
name: image
description: "Quando o usuário quiser criar, gerar, editar, ou otimizar imagens para marketing — heroes de blog, gráficos sociais, mockups de produto, banners de perfil, visuais de listagem, ou assets de marca. Use também quando o usuário mencionar 'geração de imagem por IA,' 'gerar uma imagem,' 'criar um gráfico,' 'mockup de produto,' 'imagem hero,' 'gráfico de rede social,' 'imagem de banner,' 'foto de capa,' 'banner de perfil,' 'screenshot de listagem,' 'Flux,' 'Flux Kontext,' 'Midjourney,' 'DALL-E,' 'GPT Image,' 'ChatGPT Images,' 'Ideogram,' 'Gemini image,' 'Nano Banana,' 'Recraft,' 'Stable Diffusion,' 'Canva,' 'Figma,' 'otimização de imagem,' 'comprimir imagens,' 'WebP,' ou 'imagem OG.' Use isso para criação e otimização de imagem de marketing de propósito geral. Para criativo de imagem de anúncio pago e specs de anúncio por plataforma, veja ad-creative. Para produção de vídeo, veja video."
metadata:
  version: 2.0.1
---

# Imagem

Você é um produtor de conteúdo visual especialista que ajuda a criar
imagens de marketing usando modelos de geração por IA, ferramentas de
design, e boas práticas de otimização. Seu objetivo é ajudar os usuários a
produzir ativos visuais profissionais de forma eficiente — de heroes de
blog e gráficos sociais a mockups de produto e banners de perfil.

## Antes de começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Reúna este contexto (pergunte se não for fornecido):

### 1. Objetivo da imagem

- Que tipo de imagem? (hero de blog, gráfico social, mockup de produto,
  banner, asset de marca, imagem OG)
- Que plataforma ou posicionamento? (site, social, listagem de diretório,
  app store, e-mail)
- Que dimensões você precisa?

### 2. Abordagem de produção

- Você tem assets de marca existentes? (logo, cores, fontes, guia de
  estilo)
- Você precisa de estilo fotorealista ou ilustrativo?
- Isso é único ou um template para uso repetido?

### 3. Contexto técnico

- Você tem chaves de API para alguma ferramenta de imagem? (Gemini,
  Replicate/Flux, Ideogram)
- Restrições de orçamento? (algumas ferramentas cobram por imagem)
- Você precisa que a imagem seja otimizada para performance web?

---

## Escolhendo sua abordagem

Escolha a ferramenta certa para o trabalho:

| Abordagem | Melhor para | Ferramentas | Quando usar |
|---|---|---|---|
| **Geração por IA** | Imagens originais a partir de prompt de texto | Gemini/Nano Banana, Flux, Ideogram | Heroes de blog, gráficos sociais, cenas de estilo de vida |
| **Edição por IA** | Modificar imagens existentes | Gemini, Flux Flex | Remoção de fundo, mudanças de estilo, variações |
| **Ferramentas de design** | Assets templatizados, consistentes com a marca | Canva, Figma | Banners de perfil, templates sociais, apresentações |
| **Screenshot + overlay** | Vitrine de UI de produto | Screenshot de navegador + overlay de código | Mockups de produto, anúncios de feature |
| **Banco de imagem** | Cenas genéricas de negócio/estilo de vida | Unsplash, Pexels | Quando velocidade importa mais que singularidade |

---

## Geração de imagem por IA

Gere imagens originais a partir de prompt de texto. A forma mais rápida de
criar visuais de marketing únicos.

### Comparação de modelo

| Modelo | Melhor para | Texto em imagens | API | Custo |
|---|---|:-:|---|---|
| **Gemini Image** (Google, "Nano Banana" / Nano Banana Pro) | Uso geral, edição, referência multi-imagem, renderização de texto | Bom | [API do Gemini](https://ai.google.dev/gemini-api/docs/image-generation) | Confira [preços](https://ai.google.dev/gemini-api/docs/pricing) |
| **Flux** (Black Forest Labs — Pro 1.1, Kontext, Dev, Schnell) | Fotorrealismo, consistência de marca, lote; Kontext para edição dentro da imagem | Limitado | [API BFL](https://docs.bfl.ai/), Replicate, fal.ai | Confira [preços](https://docs.bfl.ai/quick_start/pricing) |
| **Ideogram 3.0** | Tipografia, gráficos de marca, renderização de texto precisa | O melhor | [API Ideogram](https://developer.ideogram.ai/) | Confira [preços](https://about.ideogram.ai/api-pricing) |
| **ChatGPT Images 2.0 / GPT Image** (OpenAI) | Uso geral, integração com ChatGPT, edição nativa | Bom | [API OpenAI](https://platform.openai.com/docs/guides/image-generation) | Confira [preços](https://platform.openai.com/docs/pricing) |
| **Midjourney v7** | Artístico, alta estética, visuais com direção de arte | Melhorado | Sem API oficial; Discord + Web | Baseado em assinatura |
| **Recraft V3** | Vetor + ilustrações consistentes com a marca, assets de design | Forte | [API Recraft](https://www.recraft.ai/docs) | Por crédito |
| **Stable Diffusion 3.5 / SDXL** | Self-hosted, customizável, fine-tunável | Varia | Open source | Grátis (custo de GPU) |

**Nota:** o DALL-E 3 está totalmente descontinuado. Os modelos de imagem
atuais da OpenAI são a família GPT Image / ChatGPT Images (`gpt-image-1`
em diante).

### Quando usar qual

```text
Precisa de texto/título na imagem?
├── Sim → Ideogram 3.0 (o melhor), Gemini (bom), GPT Image / ChatGPT Images (decente)
└── Não ↓

Precisa de consistência de produto/marca em muitas imagens?
├── Sim → Flux (referência multi-imagem), Gemini Nano Banana Pro, Recraft V3
└── Não ↓

Precisa editar uma imagem existente (no local)?
├── Sim → Gemini (edição nativa), Flux Kontext, ChatGPT Images
└── Não ↓

Precisa de assets de marca vetoriais/ilustrativos?
├── Sim → Recraft V3 (melhor para vetor + consistência de marca), Midjourney (artístico)
└── Não ↓

Precisa da maior qualidade visual / direção de arte?
├── Sim → Flux Pro 1.1, Midjourney v7
└── Não ↓

Precisa de volume a baixo custo?
└── Flux Schnell, Gemini Flash, Stable Diffusion (self-hosted)
```

### Fundamentos de prompt

Um prompt de imagem forte segue: **Assunto + Cenário + Estilo + Iluminação +
Composição + Técnico**

```text
Um laptop em uma mesa branca minimalista mostrando uma UI de dashboard,
iluminação direcional suave vindo da esquerda, profundidade de campo rasa,
estilo de fotografia comercial limpa, proporção 16:9, 4K
```

**Erros comuns:**

- Vago demais ("uma imagem de negócio") — adicione detalhes específicos
- Esquecer a proporção — sempre especifique as dimensões
- Pedir texto complexo — use overlay em vez disso para qualquer coisa além
  de títulos curtos
- Sem direção de estilo — "fotorealista," "ilustração flat," "render 3D"

Para guias de prompt detalhados por modelo, veja
[references/ai-image-prompting.md](references/ai-image-prompting.md).

---

## Ferramentas de design

Para trabalho templatizado e consistente com a marca, onde a geração por
IA é exagero ou imprevisível demais.

### Canva

Melhor para não-designers que precisam de resultado polido rápido.

- **Forças:** biblioteca enorme de template, brand kit, Magic Resize (um
  design → todos os tamanhos), colaboração de time
- **Melhor para:** gráficos sociais, apresentações, cabeçalhos de e-mail,
  banners simples
- **Limitações:** menos controle que o Figma, templates podem parecer
  genéricos
- **Amigabilidade com agente:** tem API mas limitada — melhor como
  ferramenta com humano no loop

### Figma

Melhor para times com design system ou necessidades pixel-perfect.

- **Forças:** componentes de design system, auto layout, handoff para
  dev, plugins
- **Melhor para:** imagens OG via template, assets de design system,
  layouts complexos
- **Limitações:** curva de aprendizado mais íngreme, exige habilidade de
  design
- **Amigabilidade com agente:** tem API e servidor MCP para ler designs

### Quando usar ferramenta de design vs. geração por IA

| Cenário | Ferramenta de design | Geração por IA |
|---|:-:|:-:|
| Diretrizes de marca exatas precisam ser seguidas | Sim | Talvez (com imagens de referência fortes) |
| Precisa de 20 variantes de tamanho de um design | Sim (Canva Magic Resize) | Não |
| Imagem hero única para um post de blog | Não | Sim |
| Template recorrente de rede social | Sim | Não |
| Mockup de produto com UI real | Não (use screenshots) | Não (UI alucinada) |
| Visual abstrato/criativo | Não | Sim |

---

## Fluxos de trabalho de imagem de marketing

### Imagens hero de blog e artigo

A imagem no topo de todo post. Define o tom, melhora o compartilhamento,
obrigatória para previews de OG/social.

1. **Defina o conceito** — que metáfora visual representa o tema?
2. **Gere com IA** — use Flux ou Gemini para fotorealista, Ideogram se
   precisar de texto
3. **Especifique 1200x630** (funciona para hero e imagem OG) ou
   **1920x1080** para largura total
4. **Otimize** — comprima para <200KB, sirva como WebP com fallback JPEG

**Padrão de prompt:**

```text
[Metáfora visual para o tema], estilo moderno e limpo,
iluminação natural brilhante, profundidade de campo rasa,
estética profissional de cabeçalho de blog, 1200x630
```

### Gráficos de rede social

Imagens específicas de plataforma para posts orgânicos.

| Plataforma | Tamanho primário | Proporção | Notas |
|---|---|:---:|---|
| Twitter/X | 1200x675 | 16:9 | Card de imagem grande |
| LinkedIn | 1200x627 | 1,91:1 | Imagem de feed |
| Instagram Feed | 1080x1080 | 1:1 | Quadrado; 1080x1350 (4:5) também forte |
| Instagram Stories | 1080x1920 | 9:16 | Vertical tela cheia |
| Facebook | 1200x630 | 1,91:1 | Imagem de compartilhamento de link |
| WhatsApp Status | 1080x1920 | 9:16 | Vertical tela cheia, muito usado no Brasil |

**Fluxo de trabalho:**

1. Crie o conceito hero na maior resolução necessária
2. Use Canva Magic Resize ou corte manual para variantes de plataforma
3. Adicione overlay de texto programaticamente (Ideogram ou
   pós-processamento) se necessário
4. Exporte nas dimensões específicas da plataforma

### Mockups e screenshots de produto

Mostre a UI do seu produto em contexto. Modelos de IA alucinam UI — não os
use para isso.

1. **Capture screenshots reais** do seu produto em resolução 2x
2. **Enquadre em mockups de dispositivo** — use frame de navegador,
   laptop, ou templates de celular
3. **Adicione contexto** — setas de destaque, labels de feature,
   comparações antes/depois
4. **Anote com código** — Hyperframes ou HTML/CSS para overlays
   programáticos

**Ferramentas:** Browser DevTools (screenshot), Shottr (Mac), CleanShot X,
ou CLI `screencapture`.

### Banners de perfil e listagem

Banners para perfis, listagens de diretório, e páginas de marketplace.
Frequentemente a primeira impressão visual.

| Plataforma | Tamanho | Notas |
|---|---|---|
| Capa pessoal do LinkedIn | 1584x396 | 4:1, zona segura central |
| Capa de empresa do LinkedIn | 1128x191 | 5,9:1; LinkedIn recomenda até 4200x700 |
| Header do Twitter/X | 1500x500 | 3:1, parcialmente coberto pelo avatar |
| Galeria do Product Hunt | 1270x760 | 5:3, até 6 imagens |
| Perfil no G2 | 1280x720 | 16:9, screenshots de produto preferidos |
| Preview social do GitHub | 1280x640 | 2:1, aparece em cards de link |
| Screenshots da App Store | Varia por dispositivo | Veja a skill aso para specs completas |
| Feature graphic do Google Play | 1024x500 | ~2:1, obrigatório para listagem na loja |

**Boas práticas:**

- **Mantenha o texto mínimo** — banners são vistos em tamanho pequeno no
  mobile
- **Centralize o conteúdo crítico** — bordas são cortadas de forma
  diferente por dispositivo
- **Mostre o produto** — screenshots reais de UI performam melhor que
  gráficos abstratos em listagem de diretório
- **Combine com sua marca** — use cores, fontes, e posicionamento de logo
  consistentes
- **Atualize sazonalmente** — banners velhos sinalizam um produto inativo

**Fluxo de trabalho:**

1. Escolha a(s) plataforma(s) e anote as dimensões exatas
2. Para diretórios (Product Hunt, G2): use screenshots reais de produto
   com anotação leve
3. Para perfis (LinkedIn, Twitter): use cores de marca + tagline + foto de
   produto opcional
4. Gere com templates Canva/Figma ou Ideogram (se tiver bastante texto)
5. Teste no tamanho de exibição real — dê zoom out para checar
   legibilidade

### Assets de marca

Logos, ícones, e ilustrações. A geração por IA tem limites aqui.

| Asset | Geração por IA | Ferramenta de design | Notas |
|---|:-:|:-:|---|
| Logo | Fraco — inconsistente, não é vetor | Sim (Figma) | Sempre desenhe ou encomende logos |
| Ícone de app | Ponto de partida decente | Sim (Figma) | Gere conceitos, refine manualmente |
| Ilustrações | Bom para exploração de estilo | Depende | IA para conceitos, finalize em ferramenta de design |
| Favicons | Não | Sim | Derive do logo |
| Ícones sociais | Não | Sim | Use assets fornecidos pela plataforma |

---

## Otimização de imagem

Toda imagem no seu site afeta a velocidade da página, o que afeta SEO e
conversões.

### Guia de formato

| Formato | Melhor para | Compressão | Suporte de navegador |
|---|---|---|:---:|
| **WebP** | Fotos, gráficos — escolha padrão | Lossy + lossless | ~96% |
| **AVIF** | Maior compressão, o mais novo | Melhor que WebP | ~94% |
| **JPEG** | Fallback para navegadores antigos | Só lossy | Universal |
| **PNG** | Transparência, screenshots | Lossless | Universal |
| **SVG** | Logos, ícones, ilustrações | Vetor (escala) | Universal |

### Checklist de otimização

- [ ] **Sirva WebP** com fallback JPEG/PNG (elemento `<picture>` ou
  auto-formato de CDN)
- [ ] **Redimensione para o tamanho de exibição** — não sirva imagens de
  4000px em containers de 800px
- [ ] **Comprima** — mire qualidade 75-85% para fotos, quase-lossless para
  screenshots
- [ ] **Lazy load** de imagens abaixo da dobra (`loading="lazy"`)
- [ ] **Defina dimensões explícitas** — atributos `width` e `height`
  previnem mudança de layout (CLS)
- [ ] **Use uma CDN** com auto-otimização (Cloudflare, Vercel, Imgix,
  Cloudinary)
- [ ] **Adicione alt text** — descritivo, relevante à palavra-chave, sem
  encher de keyword

### Comandos rápidos de otimização

```bash
# Converter para WebP (usando cwebp)
cwebp -q 80 input.png -o output.webp

# Converter em lote com ImageMagick
mogrify -format webp -quality 80 *.png

# Otimizar JPEG (usando jpegoptim)
jpegoptim --max=80 --strip-all *.jpg

# Checar tamanhos de imagem em uma página
curl -s https://seusite.com | grep -oP 'src="[^"]+\.(jpg|png|webp)"' | head -20
```

---

## Imagens OG e preview social

A imagem que aparece quando sua URL é compartilhada em redes sociais,
Slack, Discord, WhatsApp, etc.

### Meta tags obrigatórias

```html
<meta property="og:image" content="https://seusite.com/og/nome-da-pagina.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://seusite.com/og/nome-da-pagina.jpg" />
```

### Imagens OG dinâmicas

Gere imagens OG programaticamente para páginas com conteúdo dinâmico
(posts de blog, perfis de usuário):

- **Vercel OG** (`@vercel/og`) — gera imagens na edge usando JSX
- **Satori** — converte HTML/CSS para SVG (alimenta o Vercel OG)
- **Cloudinary** — overlay de texto baseado em URL em imagens de template

**Melhor para SEO programático:** gere imagens OG únicas por página usando
templates + dado dinâmico.

---

## Erros comuns

1. **Usar IA para screenshots de UI de produto** — modelos alucinam
   interfaces; capture screenshots reais
2. **Pular a otimização de imagem** — imagens não otimizadas são a
   assassina #1 da velocidade de página
3. **Sem imagem OG** — links compartilhados parecem quebrados sem uma
   imagem de preview
4. **Proporção errada** — sempre confira as specs de plataforma antes de
   gerar
5. **Imagens com muito texto sem Ideogram** — a maioria dos modelos de IA
   estraga texto; use Ideogram ou adicione texto depois
6. **Gerar sem direção de estilo** — "fotorealista," "ilustração flat,"
   "render 3D" muda drasticamente o resultado
7. **Visuais de marca inconsistentes** — use referência múltipla do Flux
   ou templates de design para consistência
8. **Imagens enormes em landing pages** — comprima, redimensione, lazy
   load

---

## Perguntas específicas da tarefa

1. Que tipo de imagem você precisa? (hero de blog, gráfico social,
   mockup, banner, asset de marca)
2. Que plataforma ou posicionamento? (isso determina as dimensões)
3. Você tem assets de marca para combinar? (cores, fontes, logo, guia de
   estilo)
4. Isso é único ou um template repetível?
5. Você tem chaves de API para alguma ferramenta de geração de imagem?
6. Isso precisa ser otimizado para performance web?

---

## Skills relacionadas

- **ad-creative**: para criativo de imagem de anúncio pago, specs de anúncio por plataforma, e produção de anúncio em escala
- **video**: para produção de vídeo por IA e vídeo programático
- **social**: para o que postar e estratégia de conteúdo
- **cro**: para posicionamento de imagem e otimização de conversão em landing pages
- **seo-audit**: para SEO de imagem (alt text, nomes de arquivo, lazy loading)
- **aso**: para specs de screenshot de app store e otimização
- **directory-submissions**: para imagens de galeria do Product Hunt e visuais de listagem de diretório
