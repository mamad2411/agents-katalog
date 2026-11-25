---
name: link-in-bio
description: |
  Cria páginas de "link in bio" completas em HTML — aquelas páginas tipo Linktree que ficam no link da bio do Instagram/TikTok. Gera um arquivo HTML único, responsivo, com imagens embutidas em base64, pronto para hospedar gratuitamente. Use esta skill SEMPRE que alguém pedir para criar página de links, link in bio, linktree, página de bio, landing page pessoal com links, página com links para redes sociais, ou qualquer variação de "quero uma página pra colocar no link da minha bio". Também aciona quando mencionarem 'linktree', 'link na bio', 'página de links', 'bio link', 'link page', 'my links', 'social links page', 'página com meus links', ou qualquer pedido de criar uma página simples que centraliza links de redes sociais e projetos. Funciona para qualquer nicho: criadores de conteúdo, empresas, freelancers, artistas, profissionais liberais, etc.
---

# Link in Bio — Página de Links Personalizada

Você vai criar uma página HTML de "link in bio" completa, bonita, responsiva e pronta para hospedar. O resultado final é um **arquivo HTML único** com tudo embutido (CSS, imagens em base64, ícones SVG) — o usuário só precisa arrastar o arquivo para um serviço gratuito como Netlify Drop e pronto.

## O que você precisa coletar do usuário

Antes de começar a construir, colete estas informações. Se o usuário não fornecer tudo de uma vez, pergunte o que faltar — mas seja inteligente: se ele já deu o suficiente para começar (nome + links no mínimo), crie uma primeira versão e itere depois.

### Obrigatório
1. **Nome ou marca** — como aparece no topo (ex: "João Silva", "Studio Criativo", "Mari | Nutrição")
2. **Links** — lista de botões com texto + URL (ex: "Meu curso → https://...")

### Opcional (pergunte se não informado, mas não bloqueie a criação)
3. **Bio** — 1-2 frases curtas que aparecem abaixo do nome
4. **Foto de perfil** — arquivo enviado, URL, ou link do Google Drive
5. **Estilo/cores** — cores específicas (hex), tema (dark/light/colorido), ou referência visual
6. **Redes sociais** — links do Instagram, TikTok, YouTube, Twitter/X, LinkedIn, etc.
7. **Tags/palavras-chave** — badges que aparecem abaixo da bio (ex: "design", "fotografia", "marketing")
8. **Seções extras** — depoimentos, portfólio, vídeo embed, formulário de email, etc.
9. **Fonte preferida** — Google Fonts ou sistema
10. **Imagens nos botões** — thumbnail/ícone dentro de botões específicos (ex: capa de curso, logo de comunidade)

## Como lidar com imagens

Imagens são o ponto que mais gera atrito. Siga esta ordem de preferência:

1. **Arquivo enviado pelo usuário** (uploads/) → use diretamente
2. **URL pública ou Google Drive** → baixe com `curl` (para Google Drive: `https://drive.google.com/uc?export=download&id=FILE_ID`)
3. **Imagem colada na conversa** → NÃO vira arquivo no disco. Explique ao usuário que precisa do arquivo via anexo (📎) ou link. Enquanto isso, use um fallback elegante (monograma com as iniciais em gradiente).

Para embutir no HTML, **sempre converta para base64**:
```bash
# Redimensionar para web (máx 400x400 para perfil)
convert original.jpg -resize 400x400^ -gravity North -extent 400x400 -quality 85 web.jpg
# Converter para base64
base64 -w0 web.jpg > photo_b64.txt
```

Nunca use `sed` para injetar base64 em HTML — o tamanho do string quebra o sed. **Sempre use Python** para montar o HTML final com as imagens embutidas, usando f-strings ou `.replace()`.

## Construção da página

Use o script `scripts/build_page.py` para gerar a página. O script recebe os dados como argumentos JSON e produz o HTML final.

```bash
python3 /path/to/skill/scripts/build_page.py \
  --config '{"name": "...", "subtitle": "...", ...}' \
  --output /path/to/output.html
```

Se o script não estiver disponível ou houver algum problema, construa o HTML usando Python diretamente (nunca com heredoc do bash para HTML complexo — f-strings do Python são mais seguras para lidar com base64 e caracteres especiais).

### Estrutura HTML obrigatória

A página deve ter estes elementos, nesta ordem:
1. **Foto de perfil** — circular, com borda sutil, `object-fit: cover`
2. **Nome** — fonte serif para elegância (Playfair Display) ou sans-serif para modernidade
3. **Subtítulo/cargo** — menor, uppercase com letter-spacing
4. **Bio** — 1-2 linhas, cor suave
5. **Tags** (se houver) — pills/badges horizontais
6. **Botões de link** — o coração da página. Hierarquia visual: botão primário (destaque) e secundários
7. **Ícones de redes sociais** — rodapé, circulares, com SVGs inline
8. **Handle/username** — texto sutil no final

### Princípios de design

- **Mobile-first**: `max-width: 440px`, funciona em qualquer celular
- **Arquivo único**: todo CSS inline no `<style>`, imagens em base64, ícones SVG inline
- **Hierarquia visual**: o link mais importante deve ter destaque (cor, tamanho, animação sutil)
- **Micro-interações**: hover suave com `transform: translateY(-2px)` e transições de 0.3s
- **Acessibilidade**: `aria-label` nos ícones, contraste adequado, fontes legíveis

### Temas disponíveis

Quando o usuário não especificar cores, ofereça estas opções ou derive do contexto:

**Dark (padrão)**
- Background: `#0a0a0a`
- Texto: `#fff`
- Accent: derivado da foto ou preferência do usuário
- Botões: `rgba(255,255,255,0.04)` com borda sutil

**Light**
- Background: `#fafafa`
- Texto: `#1a1a1a`
- Accent: cor vibrante
- Botões: `#fff` com sombra suave

**Colorido**
- Background: gradiente suave
- Accent: cor dominante vibrante
- Botões: variações do accent

Adapte livremente — o importante é que o resultado final seja **coeso e profissional**. Se o usuário fornecer cores hex, use exatamente essas cores.

### Ícones de redes sociais (SVG)

Use SVGs inline para não depender de CDN. Os mais comuns:

Consulte `references/social-icons.md` para a biblioteca completa de SVGs de redes sociais.

### Fontes

Use Google Fonts com `<link>` no head. Combinações recomendadas:
- **Elegante**: Playfair Display (nome) + Inter (corpo)
- **Moderna**: Space Grotesk (nome) + Inter (corpo)
- **Minimalista**: Inter para tudo
- **Bold**: Bebas Neue (nome) + Inter (corpo)

### Seções extras

Se o usuário pedir funcionalidades avançadas:

**Depoimentos**: cards com aspas, nome e foto do autor
**Portfólio**: grid de imagens com lightbox CSS-only
**Vídeo embed**: iframe responsivo do YouTube/Vimeo
**Formulário de email**: integração com Formspree ou similar (form action externo)
**Música/Spotify**: embed do Spotify player
**Contador**: CSS animation de números subindo

## Entrega e instruções de hospedagem

Depois de criar o arquivo HTML, sempre:

1. Salve em `/sessions/.../mnt/outputs/link-in-bio.html` (ou nome personalizado)
2. Forneça o link computer:// para o usuário visualizar
3. Explique como hospedar gratuitamente:

> **Para colocar no ar (grátis):**
> 1. Acesse [app.netlify.com/drop](https://app.netlify.com/drop)
> 2. Arraste o arquivo HTML pra lá
> 3. Pronto — você recebe um link tipo `seusite.netlify.app`
> 4. Depois pode conectar um domínio personalizado se quiser

## Checklist de qualidade

Antes de entregar, verifique:
- [ ] Abre corretamente no preview (não está quebrado)
- [ ] Foto de perfil aparece (não é placeholder)
- [ ] Todos os links funcionam (URLs corretas)
- [ ] Responsivo em mobile (max-width funciona)
- [ ] Todas as imagens estão em base64 (arquivo independente)
- [ ] Sem erros de encoding em caracteres especiais (acentos, emojis)
- [ ] Hierarquia visual clara (botão principal se destaca)

