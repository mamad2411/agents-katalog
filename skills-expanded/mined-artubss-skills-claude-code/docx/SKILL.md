---
name: docx
description: "Kit de ferramentas de documentos (.docx). Criar/editar documentos, alterações rastreadas, comentários, preservação de formatação, extração de texto, para processamento profissional de documentos."
license: Proprietary. LICENSE.txt has complete terms
---

# Criação, edição e análise de DOCX

## Visão geral

Um arquivo .docx é um arquivo ZIP contendo arquivos XML e recursos. Crie, edite ou analise documentos Word usando extração de texto, acesso XML bruto ou fluxos de trabalho de controle de alterações. Aplique essa habilidade para processamento profissional de documentos, rastreamento de alterações e manipulação de conteúdo.

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com essa habilidade, sempre considere adicionar diagramas e esquemas científicos para aprimorar a comunicação visual.**

Se seu documento ainda não contiver esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro irá gerar, revisar e refinar o esquema automaticamente

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

A IA irá automaticamente:
- Criar imagens de qualidade para publicação com formatação apropriada
- Revisar e refinar por meio de múltiplas iterações
- Garantir acessibilidade (amigável a daltônicos, alto contraste)
- Salvar outputs no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de fluxo de trabalho de documentos
- Fluxogramas de processos
- Ilustrações de arquitetura de sistemas
- Diagramas de fluxo de dados
- Diagramas de estrutura organizacional
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Árvore de Decisão de Fluxo de Trabalho

### Leitura/Análise de Conteúdo
Use as seções "Extração de texto" ou "Acesso XML bruto" abaixo

### Criação de Novo Documento
Use o fluxo de trabalho "Criando um novo documento Word"

### Edição de Documento Existente
- **Seu próprio documento + alterações simples**
  Use o fluxo de trabalho "Edição OOXML básica"

- **Documento de outro**
  Use **"Fluxo de trabalho de redlining"** (padrão recomendado)

- **Documentos legais, acadêmicos, comerciais ou governamentais**
  Use **"Fluxo de trabalho de redlining"** (obrigatório)

## Leitura e análise de conteúdo

### Extração de texto
Para ler o conteúdo de texto de um documento, converta o documento para markdown usando pandoc. Pandoc fornece excelente suporte para preservar a estrutura do documento e pode mostrar alterações rastreadas:

```bash
# Converter documento para markdown com alterações rastreadas
pandoc --track-changes=all path-to-file.docx -o output.md
# Opções: --track-changes=accept/reject/all
```

### Acesso XML bruto
Acesso XML bruto é necessário para: comentários, formatação complexa, estrutura de documento, mídia incorporada e metadados. Para qualquer um desses recursos, desempacote um documento e leia seu conteúdo XML bruto.

#### Desempacotando um arquivo
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### Estruturas de arquivo principais
* `word/document.xml` - Conteúdo principal do documento
* `word/comments.xml` - Comentários referenciados em document.xml
* `word/media/` - Imagens incorporadas e arquivos de mídia
* Alterações rastreadas usam tags `<w:ins>` (inserções) e `<w:del>` (exclusões)

## Criando um novo documento Word

Ao criar um novo documento Word do zero, use **docx-js**, que permite criar documentos Word usando JavaScript/TypeScript.

### Fluxo de trabalho
1. **OBRIGATÓRIO - LER ARQUIVO INTEIRO**: Leia [`docx-js.md`](docx-js.md) (~500 linhas) completamente do início ao fim. **NUNCA defina limites de intervalo ao ler este arquivo.** Leia o conteúdo completo do arquivo para sintaxe detalhada, regras de formatação críticas e melhores práticas antes de prosseguir com a criação do documento.
2. Crie um arquivo JavaScript/TypeScript usando componentes Document, Paragraph, TextRun (você pode assumir que todas as dependências estão instaladas, mas se não estiverem, consulte a seção de dependências abaixo)
3. Exporte como .docx usando Packer.toBuffer()

## Editando um documento Word existente

Ao editar um documento Word existente, use a **Document library** (uma biblioteca Python para manipulação OOXML). A biblioteca manipula automaticamente a configuração de infraestrutura e fornece métodos para manipulação de documentos. Para cenários complexos, você pode acessar o DOM subjacente diretamente através da biblioteca.

### Fluxo de trabalho
1. **OBRIGATÓRIO - LER ARQUIVO INTEIRO**: Leia [`ooxml.md`](ooxml.md) (~600 linhas) completamente do início ao fim. **NUNCA defina limites de intervalo ao ler este arquivo.** Leia o conteúdo completo do arquivo para a API da Document library e padrões XML para editar diretamente arquivos de documento.
2. Desempacote o documento: `python ooxml/scripts/unpack.py <office_file> <output_directory>`
3. Crie e execute um script Python usando a Document library (veja a seção "Document Library" em ooxml.md)
4. Empacote o documento final: `python ooxml/scripts/pack.py <input_directory> <office_file>`

A Document library fornece métodos de alto nível para operações comuns e acesso direto ao DOM para cenários complexos.

## Fluxo de trabalho de redlining para revisão de documento

Este fluxo de trabalho permite planejar alterações rastreadas abrangentes usando markdown antes de implementá-las em OOXML. **CRÍTICO**: Para alterações rastreadas completas, implemente TODAS as alterações sistematicamente.

**Estratégia de Agrupamento**: Agrupe alterações relacionadas em lotes de 3-10 alterações. Isso torna a depuração gerenciável mantendo eficiência. Teste cada lote antes de passar para o próximo.

**Princípio: Edições Mínimas e Precisas**
Ao implementar alterações rastreadas, marque apenas o texto que realmente muda. Repetir texto inalterado torna as edições mais difíceis de revisar e parece pouco profissional. Divida substituições em: [texto inalterado] + [exclusão] + [inserção] + [texto inalterado]. Preserve o RSID da execução original para texto inalterado extraindo o elemento `<w:r>` do original e reutilizando-o.

Exemplo - Alterando "30 dias" para "60 dias" em uma sentença:
```python
# ERRADO - Substitui a sentença inteira
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'

# CORRETO - Marca apenas o que mudou, preserva <w:r> original para texto inalterado
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

### Fluxo de trabalho de alterações rastreadas

1. **Obter representação em markdown**: Converta documento para markdown com alterações rastreadas preservadas:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identificar e agrupar alterações**: Revise o documento e identifique TODAS as alterações necessárias, organizando-as em lotes lógicos:

   **Métodos de localização** (para encontrar alterações em XML):
   - Números de seção/título (ex: "Seção 3.2", "Artigo IV")
   - Identificadores de parágrafo se numerados
   - Padrões grep com texto circundante único
   - Estrutura do documento (ex: "primeiro parágrafo", "bloco de assinatura")
   - **NÃO use números de linha de markdown** - eles não mapeiam para estrutura XML

   **Organização de lote** (agrupe 3-10 alterações relacionadas por lote):
   - Por seção: "Lote 1: Emendas da Seção 2", "Lote 2: Atualizações da Seção 5"
   - Por tipo: "Lote 1: Correções de data", "Lote 2: Alterações de nome de partes"
   - Por complexidade: Comece com substituições de texto simples, depois aborde alterações estruturais complexas
   - Sequencial: "Lote 1: Páginas 1-3", "Lote 2: Páginas 4-6"

3. **Leia documentação e desempacote**:
   - **OBRIGATÓRIO - LER ARQUIVO INTEIRO**: Leia [`ooxml.md`](ooxml.md) (~600 linhas) completamente do início ao fim. **NUNCA defina limites de intervalo ao ler este arquivo.** Preste atenção especial às seções "Document Library" e "Tracked Change Patterns".
   - **Desempacote o documento**: `python ooxml/scripts/unpack.py <file.docx> <dir>`
   - **Anote o RSID sugerido**: O script de desempacotamento sugerirá um RSID a usar para suas alterações rastreadas. Copie este RSID para uso na etapa 4b.

4. **Implemente alterações em lotes**: Agrupe alterações logicamente (por seção, por tipo ou por proximidade) e implemente-as juntas em um único script. Esta abordagem:
   - Torna a depuração mais fácil (lote menor = mais fácil isolar erros)
   - Permite progresso incremental
   - Mantém eficiência (tamanho de lote de 3-10 alterações funciona bem)

   **Agrupamentos de lote sugeridos:**
   - Por seção do documento (ex: "Alterações da Seção 3", "Definições", "Cláusula de Rescisão")
   - Por tipo de alteração (ex: "Alterações de data", "Atualizações de nome de partes", "Substituições de termos legais")
   - Por proximidade (ex: "Alterações nas páginas 1-3", "Alterações na primeira metade do documento")

   Para cada lote de alterações relacionadas:

   **a. Mapeie texto para XML**: Grep para texto em `word/document.xml` para verificar como o texto é dividido em elementos `<w:r>`.

   **b. Crie e execute script**: Use `get_node` para encontrar nós, implemente alterações, então `doc.save()`. Veja a seção **"Document Library"** em ooxml.md para padrões.

   **Nota**: Sempre faça grep em `word/document.xml` imediatamente antes de escrever um script para obter números de linha atuais e verificar conteúdo de texto. Os números de linha mudam após cada execução de script.

5. **Empacote o documento**: Após todos os lotes estarem completos, converta o diretório desempacotado de volta para .docx:
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **Verificação final**: Faça uma verificação abrangente do documento completo:
   - Converta documento final para markdown:
     ```bash
     pandoc --track-changes=all reviewed-document.docx -o verification.md
     ```
   - Verifique que TODAS as alterações foram aplicadas corretamente:
     ```bash
     grep "original phrase" verification.md  # NÃO deve encontrar
     grep "replacement phrase" verification.md  # Deve encontrar
     ```
   - Verifique se nenhuma alteração não intencional foi introduzida


## Convertendo Documentos para Imagens

Para analisar visualmente documentos Word, converta-os para imagens usando um processo de duas etapas:

1. **Converta DOCX para PDF**:
   ```bash
   soffice --headless --convert-to pdf document.docx
   ```

2. **Converta páginas PDF para imagens JPEG**:
   ```bash
   pdftoppm -jpeg -r 150 document.pdf page
   ```
   Isso cria arquivos como `page-1.jpg`, `page-2.jpg`, etc.

Opções:
- `-r 150`: Define resolução para 150 DPI (ajuste para equilíbrio qualidade/tamanho)
- `-jpeg`: Formato de saída JPEG (use `-png` para PNG se preferir)
- `-f N`: Primeira página a converter (ex: `-f 2` começa na página 2)
- `-l N`: Última página a converter (ex: `-l 5` para na página 5)
- `page`: Prefixo para arquivos de saída

Exemplo para intervalo específico:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # Converte apenas páginas 2-5
```

## Diretrizes de Estilo de Código
**IMPORTANTE**: Ao gerar código para operações DOCX:
- Escreva código conciso
- Evite nomes de variáveis verbosos e operações redundantes
- Evite declarações print desnecessárias

## Dependências

Dependências necessárias (instale se não disponível):

- **pandoc**: `sudo apt-get install pandoc` (para extração de texto)
- **docx**: `npm install -g docx` (para criar novos documentos)
- **LibreOffice**: `sudo apt-get install libreoffice` (para conversão PDF)
- **Poppler**: `sudo apt-get install poppler-utils` (para pdftoppm converter PDF em imagens)
- **defusedxml**: `pip install defusedxml` (para análise XML segura)