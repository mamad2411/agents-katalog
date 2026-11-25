---
name: PDF Processing Pro
description: Processamento de PDF pronto para produção com formulários, tabelas, OCR, validação e operações em lote. Use ao trabalhar com fluxos de trabalho complexos de PDF em ambientes de produção, processar grandes volumes de PDFs, ou exigindo tratamento robusto de erros e validação.
---

# PDF Processing Pro

Kit de ferramentas de processamento de PDF pronto para produção com scripts pré-construídos, tratamento abrangente de erros e suporte para fluxos de trabalho complexos.

## Início rápido

### Extrair texto de PDF

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    print(text)
```

### Analisar formulário PDF (usando script incluído)

```bash
python scripts/analyze_form.py input.pdf --output fields.json
# Retorna: JSON com todos os campos de formulário, tipos e posições
```

### Preencher formulário PDF com validação

```bash
python scripts/fill_form.py input.pdf data.json output.pdf
# Valida todos os campos antes de preencher, inclui relatório de erros
```

### Extrair tabelas de PDF

```bash
python scripts/extract_tables.py report.pdf --output tables.csv
# Extrai todas as tabelas com detecção automática de colunas
```

## Funcionalidades

### ✅ Scripts prontos para produção

Todos os scripts incluem:
- **Tratamento de erros**: Falhas elegantes com mensagens de erro detalhadas
- **Validação**: Validação de entrada e verificação de tipo
- **Logging**: Logging configurável com timestamps
- **Type hints**: Anotações de tipo completas para suporte IDE
- **Interface CLI**: Flag `--help` para todos os scripts
- **Códigos de saída**: Códigos de saída apropriados para automação

### ✅ Fluxos de trabalho abrangentes

- **Formulários PDF**: Pipeline completo de processamento de formulários
- **Extração de tabelas**: Detecção e extração avançada de tabelas
- **Processamento OCR**: Extração de texto de PDF escaneado
- **Operações em lote**: Processar múltiplos PDFs eficientemente
- **Validação**: Validação pré e pós-processamento

## Tópicos avançados

### Processamento de formulários PDF

Para fluxos de trabalho completos de formulários incluindo:
- Análise e detecção de campos
- Preenchimento dinâmico de formulários
- Regras de validação
- Formulários multi-página
- Tratamento de caixas de seleção e botões de opção

Veja [FORMS.md](FORMS.md)

### Extração de tabelas

Para extração complexa de tabelas:
- Tabelas multi-página
- Células mescladas
- Tabelas aninhadas
- Detecção de tabela personalizada
- Exportar para CSV/Excel

Veja [TABLES.md](TABLES.md)

### Processamento OCR

Para PDFs escaneados e documentos baseados em imagem:
- Integração com Tesseract
- Suporte a idiomas
- Pré-processamento de imagem
- Pontuação de confiança
- OCR em lote

Veja [OCR.md](OCR.md)

## Scripts incluídos

### Processamento de formulários

**analyze_form.py** - Extrair informações de campo de formulário
```bash
python scripts/analyze_form.py input.pdf [--output fields.json] [--verbose]
```

**fill_form.py** - Preencher formulários PDF com dados
```bash
python scripts/fill_form.py input.pdf data.json output.pdf [--validate]
```

**validate_form.py** - Validar dados de formulário antes de preencher
```bash
python scripts/validate_form.py data.json schema.json
```

### Extração de tabelas

**extract_tables.py** - Extrair tabelas para CSV/Excel
```bash
python scripts/extract_tables.py input.pdf [--output tables.csv] [--format csv|excel]
```

### Extração de texto

**extract_text.py** - Extrair texto com preservação de formatação
```bash
python scripts/extract_text.py input.pdf [--output text.txt] [--preserve-formatting]
```

### Utilitários

**merge_pdfs.py** - Mesclar múltiplos PDFs
```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf file3.pdf --output merged.pdf
```

**split_pdf.py** - Dividir PDF em páginas individuais
```bash
python scripts/split_pdf.py input.pdf --output-dir pages/
```

**validate_pdf.py** - Validar integridade do PDF
```bash
python scripts/validate_pdf.py input.pdf
```

## Fluxos de trabalho comuns

### Fluxo de trabalho 1: Processar envios de formulário

```bash
# 1. Analisar estrutura do formulário
python scripts/analyze_form.py template.pdf --output schema.json

# 2. Validar dados de envio
python scripts/validate_form.py submission.json schema.json

# 3. Preencher formulário
python scripts/fill_form.py template.pdf submission.json completed.pdf

# 4. Validar saída
python scripts/validate_pdf.py completed.pdf
```

### Fluxo de trabalho 2: Extrair dados de relatórios

```bash
# 1. Extrair tabelas
python scripts/extract_tables.py monthly_report.pdf --output data.csv

# 2. Extrair texto para análise
python scripts/extract_text.py monthly_report.pdf --output report.txt
```

### Fluxo de trabalho 3: Processamento em lote

```python
import glob
from pathlib import Path
import subprocess

# Processar todos os PDFs no diretório
for pdf_file in glob.glob("invoices/*.pdf"):
    output_file = Path("processed") / Path(pdf_file).name

    result = subprocess.run([
        "python", "scripts/extract_text.py",
        pdf_file,
        "--output", str(output_file)
    ], capture_output=True)

    if result.returncode == 0:
        print(f"✓ Processado: {pdf_file}")
    else:
        print(f"✗ Falha: {pdf_file} - {result.stderr}")
```

## Tratamento de erros

Todos os scripts seguem padrões de erro consistentes:

```python
# Códigos de saída
# 0 - Sucesso
# 1 - Arquivo não encontrado
# 2 - Entrada inválida
# 3 - Erro de processamento
# 4 - Erro de validação

# Exemplo de uso em automação
result = subprocess.run(["python", "scripts/fill_form.py", ...])

if result.returncode == 0:
    print("Sucesso")
elif result.returncode == 4:
    print("Validação falhou - verifique os dados de entrada")
else:
    print(f"Erro ocorreu: {result.returncode}")
```

## Dependências

Todos os scripts exigem:

```bash
pip install pdfplumber pypdf pillow pytesseract pandas
```

Opcional para OCR:
```bash
# Instalar pacote tesseract-ocr do sistema
# macOS: brew install tesseract
# Ubuntu: apt-get install tesseract-ocr
# Windows: Baixar de GitHub releases
```

## Dicas de desempenho

- **Use processamento em lote** para múltiplos PDFs
- **Ative multiprocessing** com flag `--parallel` (onde suportado)
- **Cache de dados extraídos** para evitar reprocessamento
- **Valide entradas cedo** para falhar rapidamente
- **Use streaming** para PDFs grandes (>50MB)

## Melhores práticas

1. **Sempre valide entradas** antes de processar
2. **Use try-except** em scripts customizados
3. **Registre todas as operações** para debug
4. **Teste com PDFs de amostra** antes de produção
5. **Configure timeouts** para operações de longa duração
6. **Verifique códigos de saída** em automação
7. **Faça backup dos originais** antes de modificação

## Resolução de problemas

### Problemas comuns

**Erros "Module not found"**:
```bash
pip install -r requirements.txt
```

**Tesseract não encontrado**:
```bash
# Instalar pacote tesseract do sistema (veja Dependências)
```

**Erros de memória com PDFs grandes**:
```python
# Processar página por página em vez de carregar o PDF inteiro
with pdfplumber.open("large.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # Processar página imediatamente
```

**Erros de permissão**:
```bash
chmod +x scripts/*.py
```

## Obtendo ajuda

Todos os scripts suportam `--help`:

```bash
python scripts/analyze_form.py --help
python scripts/extract_tables.py --help
```

Para documentação detalhada sobre tópicos específicos, veja:
- [FORMS.md](FORMS.md) - Guia completo de processamento de formulários
- [TABLES.md](TABLES.md) - Extração avançada de tabelas
- [OCR.md](OCR.md) - Processamento de PDF escaneado