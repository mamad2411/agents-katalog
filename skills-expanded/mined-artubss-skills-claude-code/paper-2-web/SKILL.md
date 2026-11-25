---
name: paper-2-web
description: Esta habilidade deve ser usada ao converter artigos acadêmicos em formatos promocionais e de apresentação, incluindo sites interativos (Paper2Web), vídeos de apresentação (Paper2Video) e pôsteres de conferência (Paper2Poster). Use esta habilidade para tarefas envolvendo disseminação de papers, preparação de conferências, criação de homepages acadêmicas exploráveis, geração de vídeos abstratos ou produção de pôsteres prontos para impressão a partir de fontes LaTeX ou PDF.
allowed-tools: [Read, Write, Edit, Bash]
---

# Paper2All: Pipeline de Transformação de Papers Acadêmicos

## Visão Geral

Esta habilidade permite transformar artigos acadêmicos em múltiplos formatos promocionais e de apresentação usando o pipeline autônomo Paper2All. O sistema converte papers de pesquisa (LaTeX ou PDF) em três saídas principais:

1. **Paper2Web**: Homepages acadêmicas interativas e exploráveis com design consciente de layout
2. **Paper2Video**: Vídeos de apresentação profissionais com narração, slides e talking-head opcional
3. **Paper2Poster**: Pôsteres de conferência prontos para impressão com layouts profissionais

O pipeline usa extração de conteúdo baseada em LLM, geração de design e refinamento iterativo para criar saídas de alta qualidade adequadas para conferências, periódicos, repositórios de preprints e promoção acadêmica.

## Quando Usar Esta Habilidade

Use esta habilidade quando:

- **Criando materiais de conferência**: Pôsteres, vídeos de apresentação e sites complementares para conferências acadêmicas
- **Promovendo pesquisa**: Convertendo papers publicados ou preprints em formatos web acessíveis e envolventes
- **Preparando apresentações**: Gerando vídeos abstratos ou vídeos de apresentação completos a partir do conteúdo do paper
- **Disseminando descobertas**: Criando materiais promocionais para redes sociais, sites de laboratórios ou showcases institucionais
- **Aprimorando preprints**: Adicionando homepages interativas a submissões no bioRxiv, arXiv ou outros repositórios de preprints
- **Processamento em lote**: Gerando materiais promocionais para múltiplos papers simultaneamente

**Frases de ativação**:
- "Converta este paper para um site"
- "Gere um pôster de conferência a partir do meu paper LaTeX"
- "Crie uma apresentação em vídeo a partir desta pesquisa"
- "Faça uma homepage interativa para meu paper"
- "Transforme meu paper em materiais promocionais"
- "Gere um pôster e vídeo para minha apresentação de conferência"

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com esta habilidade, sempre considere adicionar diagramas científicos e esquemas para aprimorar a comunicação visual.**

Se seu documento ainda não contém esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação baseados em IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relações descritas no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de pipeline de transformação de papers
- Diagramas de arquitetura de layout de websites
- Ilustrações de fluxo de trabalho de produção de vídeo
- Fluxogramas de processo de design de pôsteres
- Diagramas de extração de conteúdo
- Visualizações de arquitetura de sistema
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Capacidades Principais

### 1. Paper2Web: Geração de Website Interativo

Converte papers em homepages acadêmicas interativas e layout-conscientes que vão além de simples conversão HTML.

**Características Principais**:
- Layouts responsivos e multi-seção adaptados ao conteúdo do paper
- Figuras interativas, tabelas e citações
- Design amigável para dispositivos móveis com navegação
- Descoberta automática de logos (com Google Search API)
- Refinamento estético e avaliação de qualidade

**Melhor Para**: Promoção pós-publicação, aprimoramento de preprints, websites de laboratórios, showcases de pesquisa permanentes

→ **Consulte `references/paper2web.md` para documentação detalhada**

---

### 2. Paper2Video: Geração de Vídeo de Apresentação

Gera vídeos de apresentação profissionais com slides, narração, movimentos de cursor e talking-head opcional.

**Características Principais**:
- Geração automatizada de slides a partir da estrutura do paper
- Síntese de voz com som natural
- Movimentos de cursor e destaques sincronizados
- Vídeo talking-head opcional usando Hallo2 (requer GPU)
- Suporte a múltiplos idiomas

**Melhor Para**: Vídeos abstratos, apresentações de conferência, palestras online, materiais de cursos, promoção no YouTube

→ **Consulte `references/paper2video.md` para documentação detalhada**

---

### 3. Paper2Poster: Geração de Pôster de Conferência

Cria pôsteres acadêmicos prontos para impressão com layouts e design profissionais.

**Características Principais**:
- Dimensões de pôster personalizadas (qualquer tamanho)
- Templates de design profissional
- Suporte a branding institucional
- Geração de código QR para links
- Saída de alta resolução (300+ DPI)

**Melhor Para**: Sessões de pôster de conferência, simpósios, exposições acadêmicas, conferências virtuais

→ **Consulte `references/paper2poster.md` para documentação detalhada**

---

## Início Rápido

### Pré-requisitos

1. **Instale Paper2All**:
   ```bash
   git clone https://github.com/YuhangChen1/Paper2All.git
   cd Paper2All
   conda create -n paper2all python=3.11
   conda activate paper2all
   pip install -r requirements.txt
   ```

2. **Configure Chaves de API** (crie arquivo `.env`):
   ```
   OPENAI_API_KEY=sua_chave_openai_aqui
   # Opcional: GOOGLE_API_KEY e GOOGLE_CSE_ID para busca de logos
   ```

3. **Instale Dependências de Sistema**:
   - LibreOffice (conversão de documentos)
   - Utilitários Poppler (processamento de PDF)
   - GPU NVIDIA com 48GB (opcional, para vídeos com talking-head)

→ **Consulte `references/installation.md` para guia completo de instalação**

---

### Uso Básico

**Gere Todos os Componentes** (website + pôster + vídeo):
```bash
python pipeline_all.py \
  --input-dir "caminho/para/paper" \
  --output-dir "caminho/para/saida" \
  --model-choice 1
```

**Gere Apenas Website**:
```bash
python pipeline_all.py \
  --input-dir "caminho/para/paper" \
  --output-dir "caminho/para/saida" \
  --model-choice 1 \
  --generate-website
```

**Gere Pôster com Tamanho Personalizado**:
```bash
python pipeline_all.py \
  --input-dir "caminho/para/paper" \
  --output-dir "caminho/para/saida" \
  --model-choice 1 \
  --generate-poster \
  --poster-width-inches 60 \
  --poster-height-inches 40
```

**Gere Vídeo** (pipeline leve):
```bash
python pipeline_light.py \
  --model_name_t gpt-4.1 \
  --model_name_v gpt-4.1 \
  --result_dir "caminho/para/saida" \
  --paper_latex_root "caminho/para/paper"
```

→ **Consulte `references/usage_examples.md` para exemplos de fluxo de trabalho abrangentes**

---

## Árvore de Decisão de Fluxo de Trabalho

Use esta árvore de decisão para determinar quais componentes gerar:

```
Você precisa de materiais promocionais para o paper?
│
├─ Precisa de presença permanente online?
│  └─→ Gere Paper2Web (website interativo)
│
├─ Precisa de materiais de conferência física?
│  ├─→ Sessão de pôster? → Gere Paper2Poster
│  └─→ Apresentação oral? → Gere Paper2Video
│
├─ Precisa de conteúdo em vídeo?
│  ├─→ Vídeo abstrato de periódico? → Gere Paper2Video (5-10 min)
│  ├─→ Palestra de conferência? → Gere Paper2Video (15-20 min)
│  └─→ Redes sociais? → Gere Paper2Video (1-3 min)
│
└─ Precisa de pacote completo?
   └─→ Gere todos os três componentes
```

## Requisitos de Entrada

### Formatos de Entrada Suportados

**1. Fonte LaTeX** (Recomendado):
```
diretorio_paper/
├── main.tex              # Arquivo principal do paper
├── sections/             # Opcional: seções separadas
├── figures/              # Todos os arquivos de figuras
├── tables/               # Arquivos de tabelas
└── bibliography.bib      # Referências
```

**2. PDF**:
- PDF de alta qualidade com fontes incorporadas
- Texto selecionável (não imagens escaneadas)
- Figuras de alta resolução (300+ DPI preferível)

### Organização de Entrada

**Paper Único**:
```bash
input/
└── nome_paper/
    ├── main.tex (ou paper.pdf)
    ├── figures/
    └── bibliography.bib
```

**Múltiplos Papers** (processamento em lote):
```bash
input/
├── paper1/
│   └── main.tex
├── paper2/
│   └── main.tex
└── paper3/
    └── main.tex
```

## Parâmetros Comuns

### Seleção de Modelo
- `--model-choice 1`: GPT-4 (melhor balanço entre qualidade e custo)
- `--model-choice 2`: GPT-4.1 (recursos mais recentes, custo superior)
- `--model_name_t gpt-3.5-turbo`: Mais rápido, custo menor (qualidade aceitável)

### Seleção de Componentes
- `--generate-website`: Ativar geração de website
- `--generate-poster`: Ativar geração de pôster
- `--generate-video`: Ativar geração de vídeo
- `--enable-talking-head`: Adicionar talking-head ao vídeo (requer GPU)

### Personalização
- `--poster-width-inches [largura]`: Largura de pôster personalizada
- `--poster-height-inches [altura]`: Altura de pôster personalizada
- `--video-duration [segundos]`: Duração de vídeo desejada
- `--enable-logo-search`: Descoberta automática de logo institucional

## Estrutura de Saída

As saídas geradas são organizadas por paper e componente:

```
output/
└── nome_paper/
    ├── website/
    │   ├── index.html
    │   ├── styles.css
    │   └── assets/
    ├── poster/
    │   ├── poster_final.pdf
    │   ├── poster_final.png
    │   └── poster_source/
    └── video/
        ├── final_video.mp4
        ├── slides/
        ├── audio/
        └── subtitles/
```

## Melhores Práticas

### Preparação de Entrada
1. **Use LaTeX quando possível**: Fornece melhor extração de conteúdo e estrutura
2. **Organize arquivos corretamente**: Mantenha todos os assets (figuras, tabelas, bibliografia) no diretório do paper
3. **Figuras de alta qualidade**: Use formatos vetoriais (PDF, SVG) ou rasters de alta resolução (300+ DPI)
4. **LaTeX limpo**: Remova artefatos de compilação, garanta que a fonte compile com sucesso

### Estratégia de Seleção de Modelo
- **GPT-4**: Melhor para saídas de qualidade produção, conferências, publicações
- **GPT-4.1**: Use quando precisar dos recursos mais recentes ou melhor qualidade possível
- **GPT-3.5-turbo**: Use para rascunhos rápidos, testes ou papers simples

### Prioridade de Componentes
Para prazos apertados, gere nesta ordem:
1. **Website** (mais rápido, mais versátil, ~15-30 min)
2. **Pôster** (velocidade moderada, para prazos de impressão, ~10-20 min)
3. **Vídeo** (mais lento, pode ser gerado depois, ~20-60 min)

### Garantia de Qualidade
Antes de finalizar saídas:
1. **Website**: Teste em múltiplos dispositivos, verifique se todos os links funcionam, verifique qualidade das figuras
2. **Pôster**: Imprima página de teste, verifique legibilidade do texto a 3-6 pés de distância, verifique cores
3. **Vídeo**: Assista todo o vídeo, verifique sincronização de áudio, teste em diferentes dispositivos

## Requisitos de Recursos

### Tempo de Processamento
- **Website**: 15-30 minutos por paper
- **Pôster**: 10-20 minutos por paper
- **Vídeo (sem talking-head)**: 20-60 minutos por paper
- **Vídeo (com talking-head)**: 60-120 minutos por paper

### Requisitos Computacionais
- **CPU**: Processador multi-core para processamento paralelo
- **RAM**: 16GB mínimo, 32GB recomendado para papers grandes
- **GPU**: Opcional para saídas padrão, obrigatória para talking-head (NVIDIA A6000 48GB)
- **Armazenamento**: 1-5GB por paper dependendo de componentes e configurações de qualidade

### Custos de API (Aproximado)
- **Website**: R$ 2,50-10,00 por paper (GPT-4)
- **Pôster**: R$ 1,50-5,00 por paper (GPT-4)
- **Vídeo**: R$ 5,00-15,00 por paper (GPT-4)
- **Pacote completo**: R$ 10,00-30,00 por paper (GPT-4)

## Resolução de Problemas

### Problemas Comuns

**Erros de análise LaTeX**:
- Garanta que a fonte LaTeX compile com sucesso: `pdflatex main.tex`
- Verifique se todos os arquivos referenciados estão presentes
- Confirme que nenhum pacote personalizado impede a análise

**Qualidade de figura baixa**:
- Use formatos vetoriais (PDF, SVG, EPS) em vez de rasters
- Garanta que imagens raster sejam 300+ DPI
- Verifique se as figuras renderizam corretamente no PDF compilado

**Falhas na geração de vídeo**:
- Verifique espaço em disco suficiente (5GB+ recomendado)
- Verifique se todas as dependências foram instaladas (LibreOffice, Poppler)
- Revise logs de erro no diretório de saída

**Problemas de layout de pôster**:
- Verifique se as dimensões do pôster são razoáveis (intervalo 24"-72")
- Verifique comprimento de conteúdo (papers muito longos podem precisar de curadoria manual)
- Garanta que figuras têm resolução apropriada para tamanho do pôster

**Erros de API**:
- Verifique chaves de API no arquivo `.env`
- Verifique saldo de crédito de API
- Garanta que não há limitação de taxa (aguarde e tente novamente)

## Recursos Específicos de Plataforma

### Otimização para Redes Sociais

O sistema detecta automaticamente plataformas de destino:

**Twitter/X** (inglês, nomes de pasta numéricos):
```bash
mkdir -p input/001_twitter/
# Gera conteúdo promocional em inglês
```

**Xiaohongshu/小红书** (chinês, nomes de pasta alfanuméricos):
```bash
mkdir -p input/xhs_paper/
# Gera conteúdo promocional em chinês
```

### Formatação Específica de Conferência

Especifique requisitos de conferência:
- Tamanhos de pôster padrão (4'×3', 5'×4', A0, A1)
- Limites de duração de vídeo abstrato (geralmente 3-5 minutos)
- Requisitos de branding institucional
- Preferências de esquema de cores

## Integração e Implantação

### Implantação de Website
Implante websites gerados em:
- **GitHub Pages**: Hospedagem gratuita com domínio personalizado
- **Hospedagem acadêmica**: Servidores web universitários
- **Servidores pessoais**: AWS, DigitalOcean, etc.
- **Netlify/Vercel**: Hospedagem moderna com CI/CD

### Impressão de Pôster
Arquivos prontos para impressão funcionam com:
- Serviços profissionais de impressão de pôsteres
- Gráficas universitárias
- Serviços online (ex: Spoonflower, VistaPrint)
- Impressoras de grande formato (se disponível)

### Distribuição de Vídeo
Compartilhe vídeos em:
- **YouTube**: Público ou não listado para alcance máximo
- **Repositórios institucionais**: Plataformas de vídeo universitários
- **Plataformas de conferência**: Sistemas de conferência virtual
- **Redes sociais**: Twitter, LinkedIn, ResearchGate

## Uso Avançado

### Processamento em Lote
Processe múltiplos papers eficientemente:
```bash
# Organize papers em diretório em lote
for paper in paper1 paper2 paper3; do
    python pipeline_all.py \
      --input-dir input/$paper \
      --output-dir output/$paper \
      --model-choice 1 &
done
wait
```

### Branding Personalizado
Aplique branding de instituição ou laboratório:
- Forneça arquivos de logo no diretório do paper
- Especifique esquemas de cores na configuração
- Use templates personalizados (avançado)
- Corresponda aos requisitos de tema de conferência

### Suporte a Múltiplos Idiomas
Gere conteúdo em diferentes idiomas:
- Especifique idioma de destino na configuração
- O sistema traduz conteúdo apropriadamente
- Seleciona voz apropriada para narração de vídeo
- Adapta convenções de design à cultura

## Referências e Recursos

Esta habilidade inclui documentação de referência abrangente:

- **`references/installation.md`**: Guia completo de instalação e configuração
- **`references/paper2web.md`**: Documentação detalhada de Paper2Web com todos os recursos
- **`references/paper2video.md`**: Guia abrangente de Paper2Video incluindo configuração de talking-head
- **`references/paper2poster.md`**: Documentação completa de Paper2Poster com templates de design
- **`references/usage_examples.md`**: Exemplos do mundo real e padrões de fluxo de trabalho

**Recursos Externos**:
- Repositório GitHub: https://github.com/YuhangChen1/Paper2All
- Dataset Curado: Disponível no Hugging Face (13 categorias de pesquisa)
- Suite de Benchmark: Websites de referência e métricas de avaliação

## Avaliação e Métricas de Qualidade

O sistema Paper2All inclui avaliação de qualidade integrada:

### Qualidade de Conteúdo
- **Completude**: Cobertura de conteúdo do paper
- **Precisão**: Representação fiel dos achados
- **Clareza**: Acessibilidade e compreensibilidade
- **Informativeness**: Destaque de informações-chave

### Qualidade de Design
- **Estética**: Apelo visual e profissionalismo
- **Layout**: Equilíbrio, hierarquia e organização
- **Legibilidade**: Legibilidade de texto e clareza de figuras
- **Consistência**: Estilo uniforme e branding

### Qualidade Técnica
- **Performance**: Tempos de carregamento, responsividade
- **Compatibilidade**: Suporte entre navegadores e dispositivos
- **Acessibilidade**: Conformidade WCAG, suporte para leitor de tela
- **Padrões**: HTML/CSS válido, PDFs prontos para impressão

Todas as saídas passam por verificações de qualidade automatizadas antes de completar a geração.