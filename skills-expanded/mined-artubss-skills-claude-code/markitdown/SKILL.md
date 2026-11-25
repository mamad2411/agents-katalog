---
name: markitdown
description: "Converta arquivos e documentos do Office para Markdown. Suporta PDF, DOCX, PPTX, XLSX, imagens (com OCR), áudio (com transcrição), HTML, CSV, JSON, XML, ZIP, URLs do YouTube, EPubs e muito mais."
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
source: https://github.com/microsoft/markitdown
---

# MarkItDown - Conversão de Arquivos para Markdown

## Visão Geral

MarkItDown é uma ferramenta Python desenvolvida pela Microsoft para converter diversos formatos de arquivo para Markdown. É particularmente útil para converter documentos em formato de texto amigável para LLMs, já que Markdown é eficiente em tokens e bem compreendido pelos modelos de linguagem modernos.

**Principais Benefícios**:
- Converta documentos para Markdown limpo e estruturado
- Formato eficiente em tokens para processamento por LLM
- Suporta 15+ formatos de arquivo
- Descrições de imagem aprimoradas por IA opcionais
- OCR para imagens e documentos digitalizados
- Transcrição de fala para arquivos de áudio

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com essa skill, sempre considere adicionar diagramas científicos e esquemas para aprimorar a comunicação visual.**

Se seu documento ainda não contém esquemas ou diagramas:
- Use a skill **scientific-schematics** para gerar diagramas de qualidade para publicação alimentados por IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relações descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "descrição do seu diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação adequada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de fluxo de trabalho de conversão de documentos
- Ilustrações de arquitetura de formatos de arquivo
- Diagramas de pipeline de processamento OCR
- Visualizações de fluxo de trabalho de integração
- Diagramas de arquitetura de sistema
- Diagramas de fluxo de dados
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre como criar esquemas, consulte a documentação da skill scientific-schematics.

---

## Formatos Suportados

| Formato | Descrição | Notas |
|---------|-----------|-------|
| **PDF** | Portable Document Format | Extração completa de texto |
| **DOCX** | Microsoft Word | Tabelas e formatação preservadas |
| **PPTX** | PowerPoint | Slides com notas |
| **XLSX** | Planilhas Excel | Tabelas e dados |
| **Imagens** | JPEG, PNG, GIF, WebP | Metadados EXIF + OCR |
| **Áudio** | WAV, MP3 | Metadados + transcrição |
| **HTML** | Páginas da web | Conversão limpa |
| **CSV** | Valores separados por vírgula | Formato de tabela |
| **JSON** | Dados JSON | Representação estruturada |
| **XML** | Documentos XML | Formato estruturado |
| **ZIP** | Arquivos compactados | Itera sobre conteúdos |
| **EPUB** | E-books | Extração completa de texto |
| **YouTube** | URLs de vídeos | Busca transcrições |

## Início Rápido

### Instalação

```bash
# Instale com todos os recursos
pip install 'markitdown[all]'

# Ou da fonte
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

### Uso na Linha de Comando

```bash
# Conversão básica
markitdown document.pdf > output.md

# Especifique arquivo de saída
markitdown document.pdf -o output.md

# Pipe de conteúdo
cat document.pdf | markitdown > output.md

# Ative plugins
markitdown --list-plugins  # Lista plugins disponíveis
markitdown --use-plugins document.pdf -o output.md
```

### API Python

```python
from markitdown import MarkItDown

# Uso básico
md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)

# Converta de stream
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)
```

## Recursos Avançados

### 1. Descrições de Imagem Aprimoradas por IA

Use LLMs via OpenRouter para gerar descrições detalhadas de imagens (para arquivos PPTX e imagens):

```python
from markitdown import MarkItDown
from openai import OpenAI

# Inicialize cliente OpenRouter (API compatível com OpenAI)
client = OpenAI(
    api_key="sua-chave-api-openrouter",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",  # recomendado para visão científica
    llm_prompt="Descreva esta imagem em detalhes para documentação científica"
)

result = md.convert("presentation.pptx")
print(result.text_content)
```

### 2. Azure Document Intelligence

Para conversão de PDF aprimorada com Microsoft Document Intelligence:

```bash
# Linha de comando
markitdown document.pdf -o output.md -d -e "<document_intelligence_endpoint>"
```

```python
# API Python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("complex_document.pdf")
print(result.text_content)
```

### 3. Sistema de Plugins

MarkItDown suporta plugins de terceiros para estender funcionalidades:

```bash
# Liste plugins instalados
markitdown --list-plugins

# Ative plugins
markitdown --use-plugins file.pdf -o output.md
```

Encontre plugins no GitHub com hashtag: `#markitdown-plugin`

## Dependências Opcionais

Controle quais formatos de arquivo você suporta:

```bash
# Instale formatos específicos
pip install 'markitdown[pdf, docx, pptx]'

# Todas as opções disponíveis:
# [all]                  - Todas as dependências opcionais
# [pptx]                 - Arquivos PowerPoint
# [docx]                 - Documentos Word
# [xlsx]                 - Planilhas Excel
# [xls]                  - Arquivos Excel mais antigos
# [pdf]                  - Documentos PDF
# [outlook]              - Mensagens do Outlook
# [az-doc-intel]         - Azure Document Intelligence
# [audio-transcription]  - Transcrição WAV e MP3
# [youtube-transcription] - Transcrição de vídeos YouTube
```

## Casos de Uso Comuns

### 1. Converta Artigos Científicos para Markdown

```python
from markitdown import MarkItDown

md = MarkItDown()

# Converta PDF do paper
result = md.convert("research_paper.pdf")
with open("paper.md", "w") as f:
    f.write(result.text_content)
```

### 2. Extraia Dados do Excel para Análise

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xlsx")

# O resultado estará em formato de tabela Markdown
print(result.text_content)
```

### 3. Processe Múltiplos Documentos

```python
from markitdown import MarkItDown
import os
from pathlib import Path

md = MarkItDown()

# Processe todos os PDFs em um diretório
pdf_dir = Path("papers/")
output_dir = Path("markdown_output/")
output_dir.mkdir(exist_ok=True)

for pdf_file in pdf_dir.glob("*.pdf"):
    result = md.convert(str(pdf_file))
    output_file = output_dir / f"{pdf_file.stem}.md"
    output_file.write_text(result.text_content)
    print(f"Convertido: {pdf_file.name}")
```

### 4. Converta PowerPoint com Descrições por IA

```python
from markitdown import MarkItDown
from openai import OpenAI

# Use OpenRouter para acesso a múltiplos modelos de IA
client = OpenAI(
    api_key="sua-chave-api-openrouter",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",  # recomendado para apresentações
    llm_prompt="Descreva esta imagem do slide em detalhes, focando em elementos visuais e dados importantes"
)

result = md.convert("presentation.pptx")
with open("presentation.md", "w") as f:
    f.write(result.text_content)
```

### 5. Conversão em Lote com Diferentes Formatos

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

# Arquivos para converter
files = [
    "document.pdf",
    "spreadsheet.xlsx",
    "presentation.pptx",
    "notes.docx"
]

for file in files:
    try:
        result = md.convert(file)
        output = Path(file).stem + ".md"
        with open(output, "w") as f:
            f.write(result.text_content)
        print(f"✓ Convertido {file}")
    except Exception as e:
        print(f"✗ Erro ao converter {file}: {e}")
```

### 6. Extraia Transcrição de Vídeo do YouTube

```python
from markitdown import MarkItDown

md = MarkItDown()

# Converta vídeo do YouTube para transcrição
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)
```

## Uso com Docker

```bash
# Construa imagem
docker build -t markitdown:latest .

# Execute conversão
docker run --rm -i markitdown:latest < ~/document.pdf > output.md
```

## Melhores Práticas

### 1. Escolha o Método de Conversão Certo

- **Documentos simples**: Use `MarkItDown()` básico
- **PDFs complexos**: Use Azure Document Intelligence
- **Conteúdo visual**: Ative descrições de imagem por IA
- **Documentos digitalizados**: Certifique-se de que dependências OCR estão instaladas

### 2. Trate Erros com Elegância

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except FileNotFoundError:
    print("Arquivo não encontrado")
except Exception as e:
    print(f"Erro de conversão: {e}")
```

### 3. Processe Arquivos Grandes Eficientemente

```python
from markitdown import MarkItDown

md = MarkItDown()

# Para arquivos grandes, use streaming
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    
    # Processe em chunks ou salve diretamente
    with open("output.md", "w") as out:
        out.write(result.text_content)
```

### 4. Otimize para Eficiência de Tokens

A saída Markdown já é eficiente em tokens, mas você pode:
- Remover espaços em branco excessivos
- Consolidar seções similares
- Remover metadados se não forem necessários

```python
from markitdown import MarkItDown
import re

md = MarkItDown()
result = md.convert("document.pdf")

# Limpe espaços em branco extra
clean_text = re.sub(r'\n{3,}', '\n\n', result.text_content)
clean_text = clean_text.strip()

print(clean_text)
```

## Integração com Fluxos de Trabalho Científicos

### Converta Literatura para Revisão

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

# Converta todos os papers na pasta de literatura
papers_dir = Path("literature/pdfs")
output_dir = Path("literature/markdown")
output_dir.mkdir(exist_ok=True)

for paper in papers_dir.glob("*.pdf"):
    result = md.convert(str(paper))
    
    # Salve com metadados
    output_file = output_dir / f"{paper.stem}.md"
    content = f"# {paper.stem}\n\n"
    content += f"**Fonte**: {paper.name}\n\n"
    content += "---\n\n"
    content += result.text_content
    
    output_file.write_text(content)

# Para conversão aprimorada por IA com figuras
from openai import OpenAI

client = OpenAI(
    api_key="sua-chave-api-openrouter",
    base_url="https://openrouter.ai/api/v1"
)

md_ai = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",
    llm_prompt="Descreva figuras científicas com precisão técnica"
)
```

### Extraia Tabelas para Análise

```python
from markitdown import MarkItDown
import re

md = MarkItDown()
result = md.convert("data_tables.xlsx")

# Tabelas Markdown podem ser analisadas ou usadas diretamente
print(result.text_content)
```

## Resolução de Problemas

### Problemas Comuns

1. **Dependências ausentes**: Instale pacotes específicos de recursos
   ```bash
   pip install 'markitdown[pdf]'  # Para suporte a PDF
   ```

2. **Erros de arquivo binário**: Certifique-se de abrir arquivos em modo binário
   ```python
   with open("file.pdf", "rb") as f:  # Note o "rb"
       result = md.convert_stream(f, file_extension=".pdf")
   ```

3. **OCR não funcionando**: Instale tesseract
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu
   sudo apt-get install tesseract-ocr
   ```

## Considerações de Desempenho

- **Arquivos PDF**: PDFs grandes podem levar tempo; considere intervalos de página se suportado
- **OCR de imagem**: Processamento OCR usa muita CPU
- **Transcrição de áudio**: Requer recursos de computação adicionais
- **Descrições de imagem por IA**: Requer chamadas de API (custos podem ser aplicáveis)

## Próximos Passos

- Consulte `references/api_reference.md` para documentação completa da API
- Verifique `references/file_formats.md` para detalhes específicos de formato
- Revise `scripts/batch_convert.py` para exemplos de automação
- Explore `scripts/convert_with_ai.py` para conversões aprimoradas por IA

## Recursos

- **GitHub MarkItDown**: https://github.com/microsoft/markitdown
- **PyPI**: https://pypi.org/project/markitdown/
- **OpenRouter**: https://openrouter.ai (para conversões aprimoradas por IA)
- **Chaves de API OpenRouter**: https://openrouter.ai/keys
- **Modelos OpenRouter**: https://openrouter.ai/models
- **Servidor MCP**: markitdown-mcp (para integração com Claude Desktop)
- **Desenvolvimento de Plugin**: Consulte `packages/markitdown-sample-plugin`