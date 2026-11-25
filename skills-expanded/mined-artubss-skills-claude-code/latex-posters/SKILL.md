---
name: latex-posters
description: "Crie pôsteres de pesquisa profissionais em LaTeX usando beamerposter, tikzposter ou baposter. Suporte para apresentações em conferências, pôsteres acadêmicos e comunicação científica. Inclui design de layout, esquemas de cores, formatos multi-coluna, integração de figuras e melhores práticas específicas para pôsteres para comunicação visual."
allowed-tools: [Read, Write, Edit, Bash]
---

# Pôsteres de Pesquisa em LaTeX

## Visão Geral

Pôsteres de pesquisa são um meio crítico para comunicação científica em conferências, simpósios e eventos acadêmicos. Esta habilidade fornece orientação abrangente para criar pôsteres de pesquisa profissionais e visualmente atraentes usando pacotes LaTeX. Gere pôsteres com qualidade de publicação com layout adequado, tipografia, esquemas de cores e hierarquia visual.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criar pôsteres de pesquisa para conferências, simpósios ou sessões de pôsteres
- Projetar pôsteres acadêmicos para eventos universitários ou defesas de teses
- Preparar resumos visuais de pesquisa para engajamento público
- Converter artigos científicos em formato de pôster
- Criar templates de pôsteres para grupos de pesquisa ou departamentos
- Projetar pôsteres que atendam requisitos específicos de tamanho de conferência (A0, A1, 36×48", etc.)
- Construir pôsteres com layouts multi-coluna complexos
- Integrar figuras, tabelas, equações e citações em formato de pôster

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Cada pôster de pesquisa DEVE incluir pelo menos 2-3 figuras geradas por IA usando a habilidade scientific-schematics.**

Isso não é opcional. Pôsteres são principalmente mídia visual - pôsteres repletos de texto falham em comunicar efetivamente. Antes de finalizar qualquer pôster:
1. Gere no mínimo DOIS esquemas ou diagramas
2. Alvo de 3-4 figuras para pôsteres abrangentes (fluxograma de metodologia, visualização de resultados-chave, marco conceitual)
3. Figuras devem ocupar 40-50% da área do pôster

**Como gerar figuras:**
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro irá gerar automaticamente, revisar e refinar o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

A IA irá automaticamente:
- Criar imagens com qualidade para publicação com formatação adequada
- Revisar e refinar através de múltiplas iterações
- Garantir acessibilidade (amigável a daltônico, alto contraste)
- Salvar saídas no diretório figures/

**Quando adicionar esquemas:**
- Fluxogramas de metodologia de pesquisa para conteúdo do pôster
- Diagramas de marco conceitual
- Visualizações de design experimental
- Diagramas de pipeline de análise de dados
- Diagramas de arquitetura de sistema
- Ilustrações de vias biológicas
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre como criar esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Capacidades Centrais

### 1. Pacotes LaTeX para Pôsteres

Suporte para três principais pacotes LaTeX para pôsteres, cada um com vantagens distintas. Para comparação detalhada e orientação específica de pacotes, consulte `references/latex_poster_packages.md`.

**beamerposter**:
- Extensão da classe de apresentação Beamer
- Sintaxe familiar para usuários de Beamer
- Excelente suporte de temas e customização
- Melhor para: Pôsteres acadêmicos tradicionais, marca institucional

**tikzposter**:
- Design moderno e flexível com integração TikZ
- Temas de cores incorporados e templates de layout
- Customização extensa através de comandos TikZ
- Melhor para: Designs coloridos e modernos, gráficos customizados

**baposter**:
- Sistema de layout baseado em caixas
- Espaçamento e posicionamento automáticos
- Estilos padrão com aparência profissional
- Melhor para: Layouts multi-coluna, espaçamento consistente

### 2. Layout e Estrutura de Pôster

Crie layouts de pôster eficazes seguindo princípios de comunicação visual. Para orientação abrangente sobre layout, consulte `references/poster_layout_design.md`.

**Seções Comuns de Pôster**:
- **Cabeçalho/Título**: Título, autores, afiliações, logos
- **Introdução/Contexto**: Contexto de pesquisa e motivação
- **Métodos/Abordagem**: Metodologia e design experimental
- **Resultados**: Descobertas principais com figuras e visualizações de dados
- **Conclusões**: Principais conclusões e implicações
- **Referências**: Citações principais (tipicamente abreviadas)
- **Agradecimentos**: Financiamento, colaboradores, instituições

**Estratégias de Layout**:
- **Layouts baseados em coluna**: Grids de 2-coluna, 3-coluna ou 4-coluna
- **Layouts baseados em blocos**: Arranjo flexível de blocos de conteúdo
- **Fluxo em padrão Z**: Guie leitores através do conteúdo logicamente
- **Hierarquia visual**: Use tamanho, cor e espaçamento para enfatizar pontos-chave

### 3. Princípios de Design para Pôsteres de Pesquisa

Aplique princípios de design baseados em evidências para máximo impacto. Para orientação detalhada sobre design, consulte `references/poster_design_principles.md`.

**Tipografia**:
- Título: 72-120pt para visibilidade à distância
- Cabeçalhos de seção: 48-72pt
- Texto do corpo: Mínimo de 24-36pt para legibilidade a 4-6 pés de distância
- Use fontes sem-serifa (Arial, Helvetica, Calibri) para clareza
- Limite a 2-3 famílias de fonte no máximo

**Cor e Contraste**:
- Use esquemas de cores com alto contraste para legibilidade
- Paletas de cores institucionais para marca
- Paletas amigáveis a daltônicos (evite combinações vermelho-verde)
- Espaço em branco é espaço ativo—não sobrecarregue

**Elementos Visuais**:
- Figuras em alta resolução (mínimo 300 DPI para impressão)
- Rótulos grandes e claros em todas as figuras
- Estilo de figura consistente em todo o documento
- Uso estratégico de ícones e gráficos
- Equilíbrio de texto com conteúdo visual (40-50% visual recomendado)

**Diretrizes de Conteúdo**:
- **Menos é mais**: 300-800 palavras totais recomendadas
- Bullets em vez de parágrafos para scannability
- Mensagens claras e concisas
- Figuras auto-explicativas com mínima explicação em texto
- Códigos QR para materiais suplementares ou recursos online

### 4. Tamanhos Padrão de Pôster

Suporte para dimensões de pôster internacionais e específicas de conferência:

**Padrões Internacionais**:
- A0 (841 × 1189 mm / 33,1 × 46,8 polegadas) - Padrão europeu mais comum
- A1 (594 × 841 mm / 23,4 × 33,1 polegadas) - Formato menor
- A2 (420 × 594 mm / 16,5 × 23,4 polegadas) - Pôsteres compactos

**Padrões Norte-Americanos**:
- 36 × 48 polegadas (914 × 1219 mm) - Tamanho comum em conferência dos EUA
- 42 × 56 polegadas (1067 × 1422 mm) - Formato grande
- 48 × 72 polegadas (1219 × 1829 mm) - Extra grande

**Orientação**:
- Retrato (vertical) - Mais comum, tradicional
- Paisagem (horizontal) - Melhor para conteúdo amplo, cronogramas

### 5. Templates Específicos de Pacote

Forneça templates prontos para uso para cada pacote principal. Templates disponíveis no diretório `assets/`.

**Templates beamerposter**:
- `beamerposter_classic.tex` - Estilo acadêmico tradicional
- `beamerposter_modern.tex` - Design limpo e minimalista
- `beamerposter_colorful.tex` - Tema vibrante com blocos

**Templates tikzposter**:
- `tikzposter_default.tex` - Layout tikzposter padrão
- `tikzposter_rays.tex` - Design moderno com tema rays
- `tikzposter_wave.tex` - Tema wave profissional

**Templates baposter**:
- `baposter_portrait.tex` - Layout clássico em retrato
- `baposter_landscape.tex` - Multi-coluna em paisagem
- `baposter_minimal.tex` - Design minimalista

### 6. Integração de Figuras e Imagens

Otimize conteúdo visual para apresentações de pôster:

**Melhores Práticas**:
- Use gráficos vetoriais (PDF, SVG) quando possível para escalabilidade
- Imagens raster: mínimo 300 DPI no tamanho final de impressão
- Estilo de imagem consistente (bordas, captions, tamanhos)
- Agrupe figuras relacionadas
- Use subfiguras para comparações

**Comandos LaTeX para Figuras**:
```latex
% Include graphics package
\usepackage{graphicx}

% Simple figure
\includegraphics[width=0.8\linewidth]{figure.pdf}

% Figure with caption in tikzposter
\block{Results}{
  \begin{tikzfigure}
    \includegraphics[width=0.9\linewidth]{results.png}
  \end{tikzfigure}
}

% Multiple subfigures
\usepackage{subcaption}
\begin{figure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig1.pdf}
    \caption{Condition A}
  \end{subfigure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig2.pdf}
    \caption{Condition B}
  \end{subfigure}
\end{figure}
```

### 7. Esquemas de Cores e Temas

Forneça paletas de cores profissionais para vários contextos:

**Cores de Instituição Acadêmica**:
- Combine com marca universitária ou de departamento
- Use códigos de cor oficiais (RGB, CMYK ou definições de cor LaTeX)

**Paletas de Cores Científicas** (amigáveis a daltônicos):
- Viridis: Gradiente profissional de roxo para amarelo
- ColorBrewer: Paletas testadas em pesquisa para visualização de dados
- IBM Color Blind Safe: Paleta corporativa acessível

**Seleção de Tema Específico de Pacote**:

**beamerposter**:
```latex
\usetheme{Berlin}
\usecolortheme{beaver}
```

**tikzposter**:
```latex
\usetheme{Rays}
\usecolorstyle{Denmark}
```

**baposter**:
```latex
\begin{poster}{
  background=plain,
  bgColorOne=white,
  headerColorOne=blue!70,
  textborder=rounded
}
```

### 8. Tipografia e Formatação de Texto

Garanta legibilidade e apelo visual:

**Seleção de Fonte**:
```latex
% Sans-serif fonts recommended for posters
\usepackage{helvet}      % Helvetica
\usepackage{avant}       % Avant Garde
\usepackage{sfmath}      % Sans-serif math fonts

% Set default to sans-serif
\renewcommand{\familydefault}{\sfdefault}
```

**Tamanho de Texto**:
```latex
% Adjust text sizes for visibility
\setbeamerfont{title}{size=\VeryHuge}
\setbeamerfont{author}{size=\Large}
\setbeamerfont{institute}{size=\normalsize}
```

**Ênfase e Destaque**:
- Use negrito para termos-chave: `\textbf{important}`
- Destaques de cor com moderação: `\textcolor{blue}{highlight}`
- Caixas para informações críticas
- Evite itálico (mais difícil de ler à distância)

### 9. Códigos QR e Elementos Interativos

Aprimorar a interatividade do pôster para conferências modernas:

**Integração de Código QR**:
```latex
\usepackage{qrcode}

% Link to paper, code repository, or supplementary materials
\qrcode[height=2cm]{https://github.com/username/project}

% QR code with caption
\begin{center}
  \qrcode[height=3cm]{https://doi.org/10.1234/paper}\\
  \small Scan for full paper
\end{center}
```

**Aprimoramentos Digitais**:
- Link para repositórios GitHub para código
- Link para apresentações em vídeo ou demos
- Link para visualizações web interativas
- Link para dados suplementares ou apêndices

### 10. Compilação e Saída

Gere saída PDF de alta qualidade para impressão ou exibição digital:

**Comandos de Compilação**:
```bash
# Basic compilation
pdflatex poster.tex

# With bibliography
pdflatex poster.tex
bibtex poster
pdflatex poster.tex
pdflatex poster.tex

# For beamer-based posters
lualatex poster.tex  # Better font support
xelatex poster.tex   # Unicode and modern fonts
```

**Garantindo Cobertura Completa da Página**:

Pôsteres devem usar a página inteira sem margens excessivas. Configure os pacotes corretamente:

**beamerposter - Configuração de Página Completa**:
```latex
\documentclass[final,t]{beamer}
\usepackage[size=a0,scale=1.4,orientation=portrait]{beamerposter}

% Remove default beamer margins
\setbeamersize{text margin left=0mm, text margin right=0mm}

% Use geometry for precise control
\usepackage[margin=10mm]{geometry}  % 10mm margins all around

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Remove footline and headline if not needed
\setbeamertemplate{footline}{}
\setbeamertemplate{headline}{}
```

**tikzposter - Configuração de Página Completa**:
```latex
\documentclass[
  25pt,                      % Font scaling
  a0paper,                   % Paper size
  portrait,                  % Orientation
  margin=10mm,               % Outer margins (minimal)
  innermargin=15mm,          % Space inside blocks
  blockverticalspace=15mm,   % Space between blocks
  colspace=15mm,             % Space between columns
  subcolspace=8mm            % Space between subcolumns
]{tikzposter}

% This ensures content fills the page
```

**baposter - Configuração de Página Completa**:
```latex
\documentclass[a0paper,portrait,fontscale=0.285]{baposter}

\begin{poster}{
  grid=false,
  columns=3,
  colspacing=1.5em,          % Space between columns
  eyecatcher=true,
  background=plain,
  bgColorOne=white,
  borderColor=blue!50,
  headerheight=0.12\textheight,  % 12% for header
  textborder=roundedleft,
  headerborder=closed,
  boxheaderheight=2em        % Consistent box header heights
}
% Content here
\end{poster}
```

**Problemas Comuns e Correções**:

**Problema**: Grandes margens em branco ao redor do pôster
```latex
% Fix for beamerposter
\setbeamersize{text margin left=5mm, text margin right=5mm}

% Fix for tikzposter
\documentclass[..., margin=5mm, innermargin=10mm]{tikzposter}

% Fix for baposter - adjust in document class
\documentclass[a0paper, margin=5mm]{baposter}
```

**Problema**: Conteúdo não preenche o espaço vertical
```latex
% Use \vfill between sections to distribute space
\block{Introduction}{...}
\vfill
\block{Methods}{...}
\vfill
\block{Results}{...}

% Or manually adjust block spacing
\vspace{1cm}  % Add space between specific blocks
```

**Problema**: Pôster ultrapassa os limites da página
```latex
% Check total width calculation
% For 3 columns with spacing:
% Total = 3×columnwidth + 2×colspace + 2×margins
% Ensure this equals \paperwidth

% Debug by adding visible page boundary
\usepackage{eso-pic}
\AddToShipoutPictureBG{
  \AtPageLowerLeft{
    \put(0,0){\framebox(\LenToUnit{\paperwidth},\LenToUnit{\paperheight}){}}
  }
}
```

**Preparação para Impressão**:
- Gere PDF/X-1a para impressão profissional
- Incorpore todas as fontes
- Converta cores para CMYK se necessário
- Verifique resolução de todas as imagens (mínimo 300 DPI)
- Adicione área de sangria se necessário pela impressora (geralmente 3-5mm)
- Verifique se o tamanho da página corresponde aos requisitos exatamente

**Exibição Digital**:
- Espaço de cores RGB para exibição em tela
- Otimize tamanho de arquivo para email/web
- Teste legibilidade em diferentes telas

### 11. Revisão e Controle de Qualidade de PDF

**CRÍTICO**: Sempre revise o PDF gerado antes de imprimir ou apresentar. Use esta lista de verificação sistemática:

**Passo 1: Verificação de Tamanho de Página**
```bash
# Check PDF dimensions (should match poster size exactly)
pdfinfo poster.pdf | grep "Page size"

# Expected outputs:
# A0: 2384 x 3370 points (841 x 1189 mm)
# 36x48": 2592 x 3456 points
# A1: 1684 x 2384 points (594 x 841 mm)
```

**Passo 2: Lista de Verificação de Inspeção Visual**

Abra o PDF com zoom de 100% e verifique:

**Layout e Espaçamento**:
- [ ] Conteúdo preenche página inteira (sem grandes margens em branco)
- [ ] Espaçamento consistente entre colunas
- [ ] Espaçamento consistente entre blocos/seções
- [ ] Todos os elementos alinhados propriamente (use ferramenta de régua)
- [ ] Sem texto ou figuras sobrepostos
- [ ] Espaço em branco distribuído uniformemente

**Tipografia**:
- [ ] Título claramente visível e grande (72pt+)
- [ ] Cabeçalhos de seção legíveis (48-72pt)
- [ ] Texto do corpo legível com zoom de 100% (mínimo 24-36pt)
- [ ] Sem corte de texto ou saída das bordas
- [ ] Uso de fonte consistente em todo o documento
- [ ] Todos os caracteres especiais renderizam corretamente (símbolos, letras gregas)

**Elementos Visuais**:
- [ ] Todas as figuras exibem corretamente
- [ ] Sem imagens pixeladas ou desfocadas
- [ ] Captions de figura presentes e legíveis
- [ ] Cores renderizam como esperado (não desbotadas ou muito escuras)
- [ ] Logos exibem claramente
- [ ] Códigos QR visíveis e escaneáveis

**Completude de Conteúdo**:
- [ ] Título e autores completos
- [ ] Todas as seções presentes (Intro, Métodos, Resultados, Conclusões)
- [ ] Referências incluídas
- [ ] Informações de contato visíveis
- [ ] Agradecimentos (se aplicável)
- [ ] Sem texto placeholder restante (Lorem ipsum, TODO, etc.)

**Qualidade Técnica**:
- [ ] Sem avisos de compilação LaTeX em áreas importantes
- [ ] Todas as citações resolvidas (sem marcas [?])
- [ ] Todas as referências cruzadas funcionando
- [ ] Limites de página corretos (sem conteúdo cortado)

**Passo 3: Teste de Impressão em Escala Reduzida**

**Teste Essencial Pré-Impressão**:
```bash
# Create reduced-size test print (25% of final size)
# This simulates viewing full poster from ~8-10 feet

# For A0 poster, print on A4 paper (24.7% scale)
# For 36x48" poster, print on letter paper (~25% scale)
```

**Lista de Verificação de Teste de Impressão**:
- [ ] Título legível a 6 pés de distância
- [ ] Cabeçalhos de seção legíveis a 4 pés de distância
- [ ] Texto do corpo legível a 2 pés de distância
- [ ] Figuras claras e compreensíveis
- [ ] Cores impressas com precisão
- [ ] Sem falhas óbvias de design

**Passo 4: Verificações de Qualidade Digital**

**Verificação de Incorporação de Fonte**:
```bash
# Check that all fonts are embedded (required for printing)
pdffonts poster.pdf

# All fonts should show "yes" in "emb" column
# If any show "no", recompile with:
pdflatex -dEmbedAllFonts=true poster.tex
```

**Verificação de Resolução de Imagem**:
```bash
# Extract image information
pdfimages -list poster.pdf

# Check that all images are at least 300 DPI
# Formula: DPI = pixels / (inches in poster)
# For A0 width (33.1"): 300 DPI = 9930 pixels minimum
```

**Otimização de Tamanho de Arquivo**:
```bash
# For email/web, compress if needed (>50MB)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=poster_compressed.pdf poster.pdf

# For printing, keep original (no compression)
```

**Passo 5: Verificação de Acessibilidade**

**Verificação de Contraste de Cor**:
- [ ] Contraste de texto-fundo ≥ 4.5:1 (WCAG AA)
- [ ] Contraste de elementos importantes ≥ 7:1 (WCAG AAA)
- Teste online: https://webaim.org/resources/contrastchecker/

**Simulação de Daltonismo**:
- [ ] Ver PDF através de simulador de daltonismo
- [ ] Informação não perdida com simulação vermelho-verde
- [ ] Use Coblis (color-blindness.com) ou ferramenta similar

**Passo 6: Revisão de Conteúdo**

**Revisão Sistemática**:
- [ ] Verificar ortografia em todo texto
- [ ] Verificar todos os nomes de autores e afiliações
- [ ] Confirmar todos os números e estatísticas para precisão
- [ ] Revisar todas as citações para correção
- [ ] Verificar rótulos e captions de figuras
- [ ] Procurar por typos em cabeçalhos e títulos

**Revisão por Pares**:
- [ ] Pedir a colega para revisar pôster
- [ ] Teste de 30 segundos: Conseguem identificar a mensagem principal?
- [ ] Revisão de 5 minutos: Conseguem entender as conclusões?
- [ ] Anotar elementos confusos

**Passo 7: Validação Técnica**

**Revisão de Log de Compilação LaTeX**:
```bash
# Check for warnings in .log file
grep -i "warning\|error\|overfull\|underfull" poster.log

# Common issues to fix:
# - Overfull hbox: Text extending beyond margins
# - Underfull hbox: Excessive spacing
# - Missing references: Citations not resolved
# - Missing figures: Image files not found
```

**Corrigir Avisos Comuns**:
```latex
% Overfull hbox (text too wide)
\usepackage{microtype}  % Better spacing
\sloppy  % Allow slightly looser spacing
\hyphenation{long-word}  % Manual hyphenation

% Missing fonts
\usepackage[T1]{fontenc}  % Better font encoding

% Image not found
% Ensure paths are correct and files exist
\graphicspath{{./figures/}{./images/}}
```

**Passo 8: Lista de Verificação Final Pré-Impressão**

**Antes de Enviar para Impressora**:
- [ ] Tamanho de PDF corresponde exatamente aos requisitos (verifique com pdfinfo)
- [ ] Todas as fontes incorporadas (verifique com pdffonts)
- [ ] Modo de cor correto (RGB para tela, CMYK para impressão se necessário)
- [ ] Área de sangria adicionada se necessário (geralmente 3-5mm)
- [ ] Marcas de corte visíveis se necessário
- [ ] Teste de impressão completo e revisado
- [ ] Nome de arquivo claro: [SobreNome]_[Conferência]_Pôster.pdf
- [ ] Cópia de backup salva

**Especificações de Impressão para Confirmar**:
- [ ] Tipo de papel (matte vs. glossy)
- [ ] Método de impressão (inkjet, large format, tecido)
- [ ] Perfil de cor (fornecido à impressora se necessário)
- [ ] Deadline de entrega e endereço de envio
- [ ] Preferência de embalagem (tubo ou plano)

**Lista de Verificação de Apresentação Digital**:
- [ ] Tamanho de PDF otimizado (<10MB para email)
- [ ] Testado em múltiplos visualizadores de PDF (Adobe, Preview, etc.)
- [ ] Exibe corretamente em diferentes telas
- [ ] Códigos QR testados e funcionais
- [ ] Formatos alternativos preparados (PNG para redes sociais)

**Script de Revisão** (Disponível em `scripts/review_poster.sh`):
```bash
#!/bin/bash
# Automated poster PDF review script

echo "Poster PDF Quality Check"
echo "======================="

# Check file exists
if [ ! -f "$1" ]; then
    echo "Error: File not found"
    exit 1
fi

echo "File: $1"
echo ""

# Check page size
echo "1. Page Dimensions:"
pdfinfo "$1" | grep "Page size"
echo ""

# Check fonts
echo "2. Font Embedding:"
pdffonts "$1" | head -20
echo ""

# Check file size
echo "3. File Size:"
ls -lh "$1" | awk '{print $5}'
echo ""

# Count pages (should be 1 for poster)
echo "4. Page Count:"
pdfinfo "$1" | grep "Pages"
echo ""

echo "Manual checks required:"
echo "- Visual inspection at 100% zoom"
echo "- Reduced-scale print test (25%)"
echo "- Color contrast verification"
echo "- Proofreading for typos"
```

**Problemas Comuns de PDF e Soluções**:

| Problema | Causa | Solução |
|----------|-------|---------|
| Grandes margens em branco | Configuração de margem incorreta | Reduzir margem no documentclass |
| Conteúdo cortado | Ultrapassa limites de página | Verificar cálculos de largura/altura total |
| Imagens borradas | Resolução baixa (<300 DPI) | Substituir por imagens de resolução superior |
| Fontes faltando | Fontes não incorporadas | Compilar com -dEmbedAllFonts=true |
| Tamanho de página errado | Configuração de papel incorreta | Verificar tamanho de papel no documentclass |
| Cores com aparência errada | Incompatibilidade RGB vs CMYK | Converter espaço de cores para impressão |
| Arquivo muito grande (>50MB) | Imagens não comprimidas | Otimizar imagens ou comprimir PDF |
| Códigos QR não funcionam | Muito pequenos ou baixo contraste | Mínimo 2×2cm, alto contraste |

### 11. Padrões Comuns de Conteúdo de Pôster

Organização eficaz de conteúdo para diferentes tipos de pesquisa:

**Pôster de Pesquisa Experimental**:
1. Título e autores
2. Introdução: Problema e hipótese
3. Métodos: Design experimental (com diagrama)
4. Resultados: Descobertas principais (2-4 figuras principais)
5. Conclusões: Principais conclusões