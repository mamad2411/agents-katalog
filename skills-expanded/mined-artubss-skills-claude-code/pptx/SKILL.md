---
name: pptx
description: "Kit de ferramentas de apresentação (.pptx). Criar/editar slides, layouts, conteúdo, anotações do apresentador, comentários para criação e modificação programática de apresentações."
license: Proprietary. LICENSE.txt has complete terms
---

# Criação, edição e análise de PPTX

## Visão geral

Um arquivo .pptx é um arquivo ZIP contendo arquivos XML e recursos. Crie, edite ou analise apresentações do PowerPoint usando extração de texto, acesso raw XML ou workflows html2pptx. Aplique essa habilidade para criação e modificação programática de apresentações.

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com essa habilidade, sempre considere adicionar diagramas e esquemas científicos para melhorar a comunicação visual.**

Se o seu documento ainda não contém esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro irá gerar, revisar e refinar o esquema automaticamente

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o figures/output.png
```

A IA irá automaticamente:
- Criar imagens de qualidade para publicação com formatação apropriada
- Revisar e refinar através de múltiplas iterações
- Garantir acessibilidade (amigável a daltonismo, alto contraste)
- Salvar outputs no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de workflow de apresentação para slides
- Fluxogramas do processo de design de slides
- Diagramas de organização de conteúdo
- Ilustrações de arquitetura de sistemas
- Visualizações de fluxo de processos
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Leitura e análise de conteúdo

### Extração de texto
Para ler o conteúdo de texto de uma apresentação, converta o documento para markdown:

```bash
# Converter documento para markdown
python -m markitdown path-to-file.pptx
```

### Acesso raw XML
Acesso raw XML é necessário para: comentários, anotações do apresentador, layouts de slides, animações, elementos de design e formatação complexa. Para qualquer um desses recursos, desempacote uma apresentação e leia seu conteúdo XML raw.

#### Desempacotando um arquivo
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**Nota**: O script unpack.py está localizado em `skills/pptx/ooxml/scripts/unpack.py` relativo à raiz do projeto. Se o script não existir nesse caminho, use `find . -name "unpack.py"` para localizá-lo.

#### Estruturas de arquivos principais
* `ppt/presentation.xml` - Metadados de apresentação principal e referências de slides
* `ppt/slides/slide{N}.xml` - Conteúdo de slides individuais (slide1.xml, slide2.xml, etc.)
* `ppt/notesSlides/notesSlide{N}.xml` - Anotações do apresentador para cada slide
* `ppt/comments/modernComment_*.xml` - Comentários para slides específicos
* `ppt/slideLayouts/` - Modelos de layout para slides
* `ppt/slideMasters/` - Modelos de master slide
* `ppt/theme/` - Informações de tema e estilos
* `ppt/media/` - Imagens e outros arquivos de mídia

#### Extração de tipografia e cor
**Quando receber um design de exemplo para emular**: Sempre analise a tipografia e cores da apresentação primeiro usando os métodos abaixo:
1. **Leia arquivo de tema**: Verifique `ppt/theme/theme1.xml` para cores (`<a:clrScheme>`) e fontes (`<a:fontScheme>`)
2. **Examine conteúdo de slide**: Examine `ppt/slides/slide1.xml` para uso real de fonte (`<a:rPr>`) e cores
3. **Busque padrões**: Use grep para encontrar referências de cor (`<a:solidFill>`, `<a:srgbClr>`) e font em todos os arquivos XML

## Criando uma nova apresentação do PowerPoint **sem um template**

Ao criar uma nova apresentação do PowerPoint do zero, use o workflow **html2pptx** para converter slides HTML em PowerPoint com posicionamento preciso.

### Princípios de Design

**CRÍTICO**: Antes de criar qualquer apresentação, analise o conteúdo e escolha elementos de design apropriados:
1. **Considere o assunto**: Do que se trata essa apresentação? Qual tom, indústria ou clima ela sugere?
2. **Verifique marca**: Se o usuário menciona uma empresa/organização, considere suas cores de marca e identidade
3. **Combine paleta com conteúdo**: Selecione cores que reflitam o assunto
4. **Declare sua abordagem**: Explique suas escolhas de design antes de escrever código

**Requisitos**:
- ✅ Declare sua abordagem de design baseada em conteúdo ANTES de escrever código
- ✅ Use apenas fontes web-safe: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Crie clara hierarquia visual através de tamanho, peso e cor
- ✅ Garanta legibilidade: contraste forte, texto adequadamente dimensionado, alinhamento limpo
- ✅ Seja consistente: repita padrões, espaçamento e linguagem visual entre slides

#### Seleção de Paleta de Cores

**Escolhendo cores criativamente**:
- **Pense além dos defaults**: Que cores genuinamente combinam com este tópico específico? Evite escolhas no automático.
- **Considere múltiplos ângulos**: Tópico, indústria, clima, nível de energia, público-alvo, identidade de marca (se mencionada)
- **Seja aventureiro**: Tente combinações inesperadas - uma apresentação de saúde não precisa ser verde, finanças não precisa ser azul marinho
- **Construa sua paleta**: Escolha 3-5 cores que funcionem bem juntas (cores dominantes + tons de suporte + acentos)
- **Garanta contraste**: Texto deve ser claramente legível sobre fundos

**Exemplos de paletas de cores** (use estes para inspirar criatividade - escolha uma, adapte ou crie a sua):

1. **Blue Clássico**: Azul marinho profundo (#1C2833), cinza ardósia (#2E4053), prata (#AAB7B8), branco desativado (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), teal profundo (#277884), coral (#FE4447), branco (#FFFFFF)
3. **Vermelho Ousado**: Vermelho (#C0392B), vermelho brilhante (#E74C3C), laranja (#F39C12), amarelo (#F1C40F), verde (#2ECC71)
4. **Blush Caloroso**: Malva (#A49393), blush (#EED6D3), rosa (#E8B4B8), creme (#FAF7F2)
5. **Luxo Borgonha**: Borgonha (#5D1D2E), carmesim (#951233), ferrugem (#C15937), ouro (#997929)
6. **Roxo Profundo & Esmeralda**: Roxo (#B165FB), azul escuro (#181B24), esmeralda (#40695B), branco (#FFFFFF)
7. **Creme & Verde Floresta**: Creme (#FFE1C7), verde floresta (#40695B), branco (#FCFCFC)
8. **Rosa & Roxo**: Rosa (#F8275B), coral (#FF574A), rosa (#FF737D), roxo (#3D2F68)
9. **Limão & Ameixa**: Limão (#C5DE82), ameixa (#7C3A5F), coral (#FD8C6E), cinza-azulado (#98ACB5)
10. **Preto & Ouro**: Ouro (#BF9A4A), preto (#000000), creme (#F4F6F6)
11. **Sálvia & Terracota**: Sálvia (#87A96B), terracota (#E07A5F), creme (#F4F1DE), carvão (#2C2C2C)
12. **Carvão & Vermelho**: Carvão (#292929), vermelho (#E33737), cinza-claro (#CCCBCB)
13. **Laranja Vibrante**: Laranja (#F96D00), cinza-claro (#F2F2F2), carvão (#222831)
14. **Verde Floresta**: Preto (#191A19), verde (#4E9F3D), verde escuro (#1E5128), branco (#FFFFFF)
15. **Arco-Íris Retrô**: Roxo (#722880), rosa (#D72D51), laranja (#EB5C18), âmbar (#F08800), ouro (#DEB600)
16. **Terroso Vintage**: Mostarda (#E3B448), sálvia (#CBD18F), verde floresta (#3A6B35), creme (#F4F1DE)
17. **Rosa Costeira**: Rosa envelhecida (#AD7670), castor (#B49886), casca de ovo (#F3ECDC), cinza cinzento (#BFD5BE)
18. **Laranja & Turquesa**: Laranja-claro (#FC993E), turquesa acinzentada (#667C6F), branco (#FCFCFC)

#### Opções de Detalhes Visuais

**Padrões Geométricos**:
- Divisores de seção diagonal em vez de horizontal
- Larguras de coluna assimétricas (30/70, 40/60, 25/75)
- Texto de header rotacionado em 90° ou 270°
- Frames circulares/hexagonais para imagens
- Formas triangulares de destaque nos cantos
- Formas sobrepostas para profundidade

**Tratamentos de Borda & Frame**:
- Bordas de cor única espessa (10-20pt) apenas em um lado
- Bordas de duas linhas com cores contrastantes
- Colchetes de canto em vez de frames completos
- Bordas em L (superior+esquerda ou inferior+direita)
- Acentos de sublinhado sob headers (3-5pt de espessura)

**Tratamentos de Tipografia**:
- Contraste de tamanho extremo (headlines de 72pt vs corpo de 11pt)
- Headers em all-caps com espaçamento de letra amplo
- Seções numeradas em tipo de exibição oversized
- Monospace (Courier New) para dados/estatísticas/conteúdo técnico
- Fontes condensadas (Arial Narrow) para informações densas
- Texto delineado para ênfase

**Estilo de Gráfico & Dados**:
- Gráficos monocromáticos com cor de destaque única para dados-chave
- Gráficos de barra horizontal em vez de vertical
- Gráficos de pontos em vez de gráficos de barra
- Linhas de grade mínimas ou nenhuma
- Rótulos de dados diretamente em elementos (sem legendas)
- Números oversized para métricas-chave

**Inovações de Layout**:
- Imagens full-bleed com sobreposições de texto
- Coluna da lateral (20-30% de largura) para navegação/contexto
- Sistemas de grade modular (blocos 3×3, 4×4)
- Fluxo de conteúdo padrão Z ou F
- Caixas de texto flutuante sobre formas coloridas
- Layouts de múltiplas colunas estilo revista

**Tratamentos de Fundo**:
- Blocos de cor sólida ocupando 40-60% do slide
- Preenchimentos de gradiente (apenas vertical ou diagonal)
- Fundos divididos (duas cores, diagonal ou vertical)
- Bandas de cor de borda a borda
- Espaço negativo como elemento de design

### Dicas de Layout
**Para slides com gráficos ou tabelas:**
- **Layout de duas colunas (PREFERIDO)**: Use um header abrangendo a largura total, depois duas colunas abaixo - texto/bullets em uma coluna e o conteúdo em destaque em outra. Isso proporciona melhor equilíbrio e torna gráficos/tabelas mais legíveis. Use flexbox com larguras de coluna desiguais (ex: divisão 40%/60%) para otimizar espaço para cada tipo de conteúdo.
- **Layout de slide completo**: Deixe o conteúdo em destaque (gráfico/tabela) ocupar o slide inteiro para máximo impacto e legibilidade
- **NUNCA empilhe verticalmente**: Não coloque gráficos/tabelas abaixo de texto em uma única coluna - isso causa problemas de legibilidade e layout

### Workflow
1. **OBRIGATÓRIO - LEIA ARQUIVO INTEIRO**: Leia [`html2pptx.md`](html2pptx.md) completamente do início ao fim. **NUNCA defina limites de intervalo ao ler este arquivo.** Leia o conteúdo completo do arquivo para sintaxe detalhada, regras de formatação críticas e melhores práticas antes de prosseguir com a criação de apresentação.
2. Crie um arquivo HTML para cada slide com dimensões apropriadas (ex: 720pt × 405pt para 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` para todo conteúdo de texto
   - Use `class="placeholder"` para áreas onde gráficos/tabelas serão adicionados (renderize com fundo cinza para visibilidade)
   - **CRÍTICO**: Rasterize gradientes e ícones como imagens PNG PRIMEIRO usando Sharp, depois referencie em HTML
   - **LAYOUT**: Para slides com gráficos/tabelas/imagens, use layout de slide completo ou layout de duas colunas para melhor legibilidade
3. Crie e execute um arquivo JavaScript usando a biblioteca [`html2pptx.js`](scripts/html2pptx.js) para converter slides HTML em PowerPoint e salvar a apresentação
   - Use a função `html2pptx()` para processar cada arquivo HTML
   - Adicione gráficos e tabelas a áreas placeholder usando API PptxGenJS
   - Salve a apresentação usando `pptx.writeFile()`
4. **Validação visual**: Gere miniaturas e inspecione problemas de layout
   - Crie grid de miniaturas: `python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - Leia e examine cuidadosamente a imagem de miniatura para:
     - **Corte de texto**: Texto sendo cortado por barras de header, formas ou bordas de slide
     - **Sobreposição de texto**: Texto sobrepondo outro texto ou formas
     - **Problemas de posicionamento**: Conteúdo muito perto de bordas de slide ou outros elementos
     - **Problemas de contraste**: Contraste insuficiente entre texto e fundos
   - Se problemas encontrados, ajuste margens/espaçamento/cores de HTML e regenere a apresentação
   - Repita até que todos os slides estejam visualmente corretos

## Editando uma apresentação do PowerPoint existente

Para editar slides em uma apresentação do PowerPoint existente, trabalhe com o formato Office Open XML (OOXML) raw. Isso envolve desempacotar o arquivo .pptx, editar conteúdo XML e reempacotá-lo.

### Workflow
1. **OBRIGATÓRIO - LEIA ARQUIVO INTEIRO**: Leia [`ooxml.md`](ooxml.md) (~500 linhas) completamente do início ao fim. **NUNCA defina limites de intervalo ao ler este arquivo.** Leia o conteúdo completo do arquivo para orientação detalhada sobre estrutura OOXML e workflows de edição antes de qualquer edição de apresentação.
2. Desempacote a apresentação: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. Edite os arquivos XML (principalmente `ppt/slides/slide{N}.xml` e arquivos relacionados)
4. **CRÍTICO**: Valide imediatamente após cada edição e corrija erros de validação antes de prosseguir: `python ooxml/scripts/validate.py <dir> --original <file>`
5. Empacote a apresentação final: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Criando uma nova apresentação do PowerPoint **usando um template**

Para criar uma apresentação que segue o design de um template existente, duplique e reorganize slides de template antes de substituir conteúdo placeholder.

### Workflow
1. **Extraia texto do template E crie grid de miniaturas visuais**:
   * Extraia texto: `python -m markitdown template.pptx > template-content.md`
   * Leia `template-content.md`: Leia o arquivo inteiro para entender os conteúdos da apresentação do template. **NUNCA defina limites de intervalo ao ler este arquivo.**
   * Crie grids de miniaturas: `python scripts/thumbnail.py template.pptx`
   * Veja seção [Criando Grids de Miniaturas](#criando-grids-de-miniaturas) para mais detalhes

2. **Analise template e salve inventário em um arquivo**:
   * **Análise Visual**: Revise grid de miniaturas para entender layouts de slides, padrões de design e estrutura visual
   * Crie e salve um arquivo de inventário de template em `template-inventory.md` contendo:
     ```markdown
     # Análise de Inventário de Template
     **Total de Slides: [contagem]**
     **IMPORTANTE: Slides são 0-indexados (primeiro slide = 0, último slide = contagem-1)**

     ## [Nome da Categoria]
     - Slide 0: [Código de layout se disponível] - Descrição/propósito
     - Slide 1: [Código de layout] - Descrição/propósito
     - Slide 2: [Código de layout] - Descrição/propósito
     [... CADA slide deve ser listado individualmente com seu índice ...]
     ```
   * **Usando grid de miniaturas**: Referencie as miniaturas visuais para identificar:
     - Padrões de layout (slides de título, layouts de conteúdo, divisores de seção)
     - Localizações e contagens de placeholder de imagem
     - Consistência de design entre grupos de slides
     - Hierarquia visual e estrutura
   * Este arquivo de inventário é OBRIGATÓRIO para selecionar templates apropriados no próximo passo

3. **Crie outline de apresentação baseado em inventário de template**:
   * Revise templates disponíveis do passo 2.
   * Escolha um template de intro ou título para o primeiro slide. Este deve ser um dos primeiros templates.
   * Escolha layouts seguros, baseados em texto para os outros slides.
   * **CRÍTICO: Combine estrutura de layout com conteúdo real**:
     - Layouts de coluna única: Use para narrativa unificada ou tópico único
     - Layouts de duas colunas: Use APENAS quando houver exatamente 2 itens/conceitos distintos
     - Layouts de três colunas: Use APENAS quando houver exatamente 3 itens/conceitos distintos
     - Layouts de imagem + texto: Use APENAS quando houver imagens reais para inserir
     - Layouts de citação: Use APENAS para citações reais de pessoas (com atribuição), nunca para ênfase
     - Nunca use layouts com mais placeholders que conteúdo disponível
     - Se houver 2 itens, não force em layout de 3 colunas
     - Se houver 4+ itens, considere quebrar em múltiplos slides ou usar formato de lista
   * Conte as peças de conteúdo reais ANTES de selecionar o layout
   * Verifique cada placeholder no layout escolhido será preenchido com conteúdo significativo
   * Selecione uma opção representando o layout **melhor** para cada seção de conteúdo.
   * Salve `outline.md` com conteúdo E mapeamento de template que aproveita designs disponíveis
   * Exemplo de mapeamento de template:
      ```
      # Templates de slides a usar (indexação baseada em 0)
      # AVISO: Verifique que índices estão no intervalo! Template com 73 slides tem índices 0-72
      # Mapeamento: números de slide do outline -> índices de slide do template
      template_mapping = [
          0,   # Use slide 0 (Title/Cover)
          34,  # Use slide 34 (B1: Title and body)
          34,  # Use slide 34 novamente (duplicar para segundo B1)
          50,  # Use slide 50 (E1: Quote)
          54,  # Use slide 54 (F2: Closing + Text)
      ]
      ```

4. **Duplique, reorganize e delete slides usando `rearrange.py`**:
   * Use o script `scripts/rearrange.py` para criar uma nova apresentação com slides na ordem desejada:
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * O script lida com duplicação de slides repetidos, deletion de slides não utilizados e reordenação automaticamente
   * Índices de slide são baseados em 0 (primeiro slide é 0, segundo é 1, etc.)
   * O mesmo índice de slide pode aparecer múltiplas vezes para duplicar esse slide

5. **Extraia TODO o texto usando o script `inventory.py`**:
   * **Execute extração de inventário**:
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **Leia text-inventory.json**: Leia o arquivo text-inventory.json inteiro para entender todas as formas e suas propriedades. **NUNCA defina limites de intervalo ao ler este arquivo.**

   * A estrutura JSON de inventário:
      ```json
        {
          "slide-0": {
            "shape-0": {
              "placeholder_type": "TITLE",  // ou null para não-placeholders
              "left": 1.5,                  // posição em polegadas
              "top": 2.0,
              "width": 7.5,
              "height": 1.2,
              "paragraphs": [
                {
                  "text": "Texto do parágrafo",
                  // Propriedades opcionais (incluídas apenas quando não-padrão):
                  "bullet": true,           // bullet explícito detectado
                  "level": 0,               // incluído apenas quando bullet é true
                  "alignment": "CENTER",    // CENTER, RIGHT (não LEFT)
                  "space_before": 10.0,     // espaço antes do parágrafo em pontos
                  "space_after": 6.0,       // espaço após parágrafo em pontos
                  "line_spacing": 22.4,     // espaçamento de linha em pontos
                  "font_name": "Arial",     // da primeira execução
                  "font_size": 14.0,        // em pontos
                  "bold": true,
                  "italic": false,
                  "underline": false,
                  "color": "FF0000"         // cor RGB
                }
              ]
            }
          }
        }
      ```

   * Principais características:
     - **Slides**: Nomeados como "slide-0", "slide-1", etc.
     - **Formas**: Ordenadas por posição visual (topo-para-baixo, esquerda-para-direita) como "shape-0", "shape-1", etc.
     - **Tipos de placeholder**: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, ou null
     - **Tamanho de fonte padrão**: `default_font_size` em pontos extraído de placeholders de layout (quando disponível)
     - **Números de slide são filtrados**: Formas com tipo de placeholder SLIDE_NUMBER são automaticamente excluídas do inventário
     - **Bullets**: Quando `bullet: true`, `level` é sempre incluído (mesmo que 0)
     - **Espaçamento**: `space_before`, `space_after` e `line_spacing` em pontos (incluídos apenas quando definidos)
     - **Cores**: `color` para RGB (ex: "FF0000"), `theme_color` para cores de tema (ex: "DARK_1")
     - **Propriedades**: Apenas valores não-padrão são incluídos no output

6. **Gere texto de substituição e salve os dados em um arquivo JSON**
   Baseado no inventário de texto do passo anterior:
   - **CRÍTICO**: Primeiro verifique quais formas existem no inventário - apenas referencie formas que estão realmente presentes
   - **VALIDAÇÃO**: O script replace.py irá validar que todas as formas no JSON de substituição existem no inventário
     - Se uma forma não-existente for referenciada, um erro mostrará as formas disponíveis
     - Se um slide não-existente for referenciado, um erro indicará que o slide não existe
     - Todos os erros de validação são mostrados de uma vez antes do script sair
   - **IMPORTANTE**: O script replace.py usa inventory.py internamente para identificar TODAS as formas de texto
   - **LIMPEZA AUTOMÁTICA**: TODAS as formas de texto do inventário serão limpas a menos que você forneça "paragraphs" para elas
   - Adicione um campo "paragraphs" a formas que precisam de conteúdo (não "replacement_paragraphs")
   - Formas sem "paragraphs" no JSON de substituição terão seu texto limpo automaticamente
   - Parágrafos com bullets serão automaticamente alinhados à esquerda. Não defina a propriedade `alignment` quando `"bullet": true`
   - Gere conteúdo de substituição apropriado para texto placeholder
   - Use tamanho de forma para determinar comprimento apropriado de conteúdo
   - **CRÍTICO**: Inclua propriedades de parágrafo do inventário original - não apenas forneça texto
   - **IMPORTANTE**: Quando bullet: true, NÃO inclua símbolos de bullet (•, -, *) no texto - eles são adicionados automaticamente
   - **REGRAS ESSENCIAIS DE FORMATAÇÃO**:
     - Headers/títulos devem tipicamente ter `"bold": true`
     - Itens de lista devem ter `"bullet": true, "level": 0` (level é necessário quando bullet é true)
     - Preserve qualquer propriedade de alinhamento (ex: `"alignment": "CENTER"` para texto centralizado)
     - Inclua propriedades de fonte quando diferentes do padrão (ex: `"font_size": 14.0`, `"font_name": "Lora"`)
     - Cores: Use `"color": "FF0000"` para RGB ou `"theme_color": "DARK_1"` para cores de tema
     - O script de substituição espera **parágrafos adequadamente formatados**, não apenas strings de texto
     - **Formas sobrepostas**: Prefira formas com maior default_font_size ou placeholder_type mais apropriado
   - Salve o inventário atualizado com substituições em `replacement-text.json`
   - **AVISO**: Diferentes layouts de template têm contagens de formas diferentes - sempre verifique o inventário real antes de criar substituições

   Exemplo de campo paragraphs mostrando formatação apropriada:
   ```json
   "paragraphs": [
     {
       "text": "Novo texto de título de apresentação",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "Cabeçalho de Seção",
       "bold": true
     },
     {
       "text": "Primeiro ponto de bullet sem símbolo de bullet",
       "bullet": true,
       "level": 0
     },
     {
       "text": "Texto com cor vermelha",
       "color": "FF0000"
     },
     {
       "text": "Texto com cor de tema",
       "theme_color": "DARK_1"
     },
     {
       "text": "Texto de parágrafo regular sem formatação especial"
     }
   ]
   ```

   **Formas não listadas no JSON de substituição são automaticamente limpas**:
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // Esta forma obtém novo texto
       }
       // shape-1 e shape-2 do inventário serão limpas automaticamente
     }
   }
   ```

   **Padrões de formatação comuns para apresentações**:
   - Slides de título: Texto em bold, às vezes centralizado
   - Headers de seção dentro de slides: Texto em bold
   - Listas de bullets: Cada item precisa `"bullet": true, "level": 0`
   - Texto de corpo: Geralmente sem propriedades especiais
   - Citações: Podem ter propriedades de alinhamento ou fonte especiais

7. **Aplique substituições usando o script `replace.py`**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   O script irá:
   - Primeiro extrair o inventário de TODAS as formas de texto usando funções de inventory.py
   - Validar que todas as formas no JSON de substituição existem no inventário
   - Limpar texto de TODAS as formas identificadas no inventário
   - Aplicar novo texto apenas às formas com "paragraphs" defin