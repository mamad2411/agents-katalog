---
name: xlsx
description: "Kit de ferramentas para planilhas (.xlsx/.csv). Criar/editar com fórmulas/formatação, analisar dados, visualização, recalcular fórmulas, para processamento e análise de planilhas."
license: Proprietária. LICENSE.txt contém os termos completos
---

# Requisitos para Outputs

## Todos os arquivos Excel

### Zero Erros de Fórmula
- Todos os modelos Excel DEVEM ser entregues com ZERO erros de fórmula (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preservar Templates Existentes (ao atualizar templates)
- Estude e CORRESPONDA EXATAMENTE ao formato, estilo e convenções existentes ao modificar arquivos
- Nunca imponha formatação padronizada em arquivos com padrões estabelecidos
- Convenções de templates existentes SEMPRE substituem estas diretrizes

## Modelos financeiros

### Padrões de Codificação por Cores
Exceto quando indicado diferentemente pelo usuário ou template existente

#### Convenções de Cores Padrão da Indústria
- **Texto azul (RGB: 0,0,255)**: Entradas codificadas e números que usuários alterarão para cenários
- **Texto preto (RGB: 0,0,0)**: TODAS as fórmulas e cálculos
- **Texto verde (RGB: 0,128,0)**: Links que puxam de outras planilhas dentro da mesma workbook
- **Texto vermelho (RGB: 255,0,0)**: Links externos para outros arquivos
- **Fundo amarelo (RGB: 255,255,0)**: Pressupostos-chave que precisam atenção ou células que precisam ser atualizadas

### Padrões de Formatação de Números

#### Regras de Formato Obrigatórias
- **Anos**: Formatar como strings de texto (ex: "2024" não "2.024")
- **Moeda**: Usar formato $#,##0; SEMPRE especificar unidades nos cabeçalhos ("Receita (R$ mm)")
- **Zeros**: Usar formatação de números para deixar todos os zeros como "-", incluindo percentuais (ex: "$#,##0;($#,##0);-")
- **Percentuais**: Padrão de 0,0% (uma casa decimal)
- **Múltiplos**: Formatar como 0,0x para múltiplos de valuation (EV/EBITDA, P/E)
- **Números negativos**: Usar parênteses (123) não menos -123

### Regras de Construção de Fórmulas

#### Colocação de Pressupostos
- Coloque TODOS os pressupostos (taxas de crescimento, margens, múltiplos, etc.) em células de pressupostos separadas
- Use referências de células em vez de valores codificados em fórmulas
- Exemplo: Use =B5*(1+$B$6) em vez de =B5*1,05

#### Prevenção de Erros de Fórmula
- Verifique se todas as referências de células estão corretas
- Procure por erros off-by-one em intervalos
- Garanta fórmulas consistentes em todos os períodos de projeção
- Teste com casos extremos (valores zero, números negativos)
- Verifique se não há referências circulares não intencionais

#### Requisitos de Documentação para Valores Codificados
- Comentar ou em células ao lado (se fim de tabela). Formato: "Fonte: [Sistema/Documento], [Data], [Referência Específica], [URL se aplicável]"
- Exemplos:
  - "Fonte: 10-K Empresa, FY2024, Página 45, Nota de Receita, [URL SEC EDGAR]"
  - "Fonte: 10-Q Empresa, Q2 2025, Exhibit 99.1, [URL SEC EDGAR]"
  - "Fonte: Terminal Bloomberg, 15/08/2025, AAPL US Equity"
  - "Fonte: FactSet, 20/08/2025, Consensus Estimates Screen"

# Criação, edição e análise XLSX

## Visão Geral

Criar, editar ou analisar planilhas Excel com fórmulas, formatação e análise de dados. Aplicar esta habilidade para processamento de planilhas usando openpyxl e pandas. Recalcular fórmulas e garantir zero erros para outputs com qualidade de publicação.

## Aprimoramento Visual com Esquemáticos Científicos

**Ao criar documentos com esta habilidade, sempre considere adicionar diagramas científicos e esquemáticos para aprimorar a comunicação visual.**

Se seu documento ainda não contém esquemáticos ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade de publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquemático

**Para novos documentos:** Esquemáticos científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemáticos:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade de publicação com formatação adequada
- Revisão e refinamento através de múltiplas iterações
- Acessibilidade garantida (amigável para daltônicos, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemáticos:**
- Diagramas de workflow de planilhas
- Ilustrações de pipeline de processamento de dados
- Diagramas de fluxo de cálculo de fórmulas
- Diagramas de estrutura de modelos financeiros
- Fluxogramas de análise de dados
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemáticos, consulte a documentação da habilidade scientific-schematics.

---

## Requisitos Importantes

**LibreOffice Necessário para Recálculo de Fórmulas**: Você pode assumir que LibreOffice está instalado para recalcular valores de fórmulas usando o script `recalc.py`. O script configura automaticamente LibreOffice na primeira execução

## Leitura e análise de dados

### Análise de dados com pandas
Para análise de dados, visualização e operações básicas, use **pandas** que fornece poderosas capacidades de manipulação de dados:

```python
import pandas as pd

# Ler Excel
df = pd.read_excel('file.xlsx')  # Padrão: primeira planilha
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # Todas as planilhas como dict

# Analisar
df.head()      # Visualizar dados
df.info()      # Informações de coluna
df.describe()  # Estatísticas

# Escrever Excel
df.to_excel('output.xlsx', index=False)
```

## Workflows de Arquivo Excel

## CRÍTICO: Use Fórmulas, Não Valores Codificados

**Sempre use fórmulas Excel em vez de calcular valores em Python e codificá-los.** Isso garante que a planilha permaneça dinâmica e atualizável.

### ❌ ERRADO - Codificar Valores Calculados
```python
# Ruim: Calcular em Python e codificar resultado
total = df['Sales'].sum()
sheet['B10'] = total  # Codifica 5000

# Ruim: Computar taxa de crescimento em Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Codifica 0,15

# Ruim: Cálculo Python para média
avg = sum(values) / len(values)
sheet['D20'] = avg  # Codifica 42,5
```

### ✅ CORRETO - Usar Fórmulas Excel
```python
# Bom: Deixar Excel calcular a soma
sheet['B10'] = '=SUM(B2:B9)'

# Bom: Taxa de crescimento como fórmula Excel
sheet['C5'] = '=(C4-C2)/C2'

# Bom: Média usando função Excel
sheet['D20'] = '=AVERAGE(D2:D19)'
```

Isso se aplica a TODOS os cálculos - totais, percentuais, proporções, diferenças, etc. A planilha deve ser capaz de recalcular quando dados fonte mudam.

## Workflow Comum
1. **Escolher ferramenta**: pandas para dados, openpyxl para fórmulas/formatação
2. **Criar/Carregar**: Criar nova workbook ou carregar arquivo existente
3. **Modificar**: Adicionar/editar dados, fórmulas e formatação
4. **Salvar**: Escrever em arquivo
5. **Recalcular fórmulas (OBRIGATÓRIO SE USAR FÓRMULAS)**: Use o script recalc.py
   ```bash
   python recalc.py output.xlsx
   ```
6. **Verificar e corrigir erros**: 
   - O script retorna JSON com detalhes de erro
   - Se `status` é `errors_found`, verifique `error_summary` para tipos e locais de erro específicos
   - Corrija os erros identificados e recalcule novamente
   - Erros comuns a corrigir:
     - `#REF!`: Referências de célula inválidas
     - `#DIV/0!`: Divisão por zero
     - `#VALUE!`: Tipo de dados errado em fórmula
     - `#NAME?`: Nome de fórmula não reconhecido

### Criar novos arquivos Excel

```python
# Usar openpyxl para fórmulas e formatação
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Adicionar dados
sheet['A1'] = 'Olá'
sheet['B1'] = 'Mundo'
sheet.append(['Linha', 'de', 'dados'])

# Adicionar fórmula
sheet['B2'] = '=SUM(A1:A10)'

# Formatação
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Largura de coluna
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editar arquivos Excel existentes

```python
# Usar openpyxl para preservar fórmulas e formatação
from openpyxl import load_workbook

# Carregar arquivo existente
wb = load_workbook('existing.xlsx')
sheet = wb.active  # ou wb['SheetName'] para planilha específica

# Trabalhar com múltiplas planilhas
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Planilha: {sheet_name}")

# Modificar células
sheet['A1'] = 'Novo Valor'
sheet.insert_rows(2)  # Inserir linha na posição 2
sheet.delete_cols(3)  # Deletar coluna 3

# Adicionar nova planilha
new_sheet = wb.create_sheet('NovaPlanilha')
new_sheet['A1'] = 'Dados'

wb.save('modified.xlsx')
```

## Recalcular fórmulas

Arquivos Excel criados ou modificados por openpyxl contêm fórmulas como strings mas não valores calculados. Use o script fornecido `recalc.py` para recalcular fórmulas:

```bash
python recalc.py <excel_file> [timeout_seconds]
```

Exemplo:
```bash
python recalc.py output.xlsx 30
```

O script:
- Configura automaticamente macro LibreOffice na primeira execução
- Recalcula todas as fórmulas em todas as planilhas
- Escaneia TODAS as células para erros Excel (#REF!, #DIV/0!, etc.)
- Retorna JSON com locais de erro detalhados e contagens
- Funciona em Linux e macOS

## Checklist de Verificação de Fórmula

Verificações rápidas para garantir que fórmulas funcionem corretamente:

### Verificação Essencial
- [ ] **Testar 2-3 referências de amostra**: Verificar que puxam valores corretos antes de construir modelo completo
- [ ] **Mapeamento de coluna**: Confirmar que colunas Excel correspondem (ex: coluna 64 = BL, não BK)
- [ ] **Deslocamento de linha**: Lembrar que linhas Excel são indexadas a partir de 1 (linha DataFrame 5 = linha Excel 6)

### Armadilhas Comuns
- [ ] **Tratamento de NaN**: Verificar valores nulos com `pd.notna()`
- [ ] **Colunas mais à direita**: Dados FY frequentemente em colunas 50+ 
- [ ] **Múltiplas correspondências**: Procurar todas as ocorrências, não apenas a primeira
- [ ] **Divisão por zero**: Verificar denominadores antes de usar `/` em fórmulas (#DIV/0!)
- [ ] **Referências erradas**: Verificar que todas as referências de células apontam para células pretendidas (#REF!)
- [ ] **Referências entre planilhas**: Usar formato correto (Plan1!A1) para vincular planilhas

### Estratégia de Teste de Fórmula
- [ ] **Começar pequeno**: Testar fórmulas em 2-3 células antes de aplicar amplamente
- [ ] **Verificar dependências**: Procurar que todas as células referenciadas em fórmulas existem
- [ ] **Testar casos extremos**: Incluir zero, negativo e valores muito grandes

### Interpretando Output de recalc.py
O script retorna JSON com detalhes de erro:
```json
{
  "status": "success",           // ou "errors_found"
  "total_errors": 0,              // Contagem total de erros
  "total_formulas": 42,           // Número de fórmulas no arquivo
  "error_summary": {              // Apenas presente se erros encontrados
    "#REF!": {
      "count": 2,
      "locations": ["Plan1!B5", "Plan1!C10"]
    }
  }
}
```

## Melhores Práticas

### Seleção de Biblioteca
- **pandas**: Melhor para análise de dados, operações em massa e exportação de dados simples
- **openpyxl**: Melhor para formatação complexa, fórmulas e recursos específicos de Excel

### Trabalhando com openpyxl
- Índices de célula são baseados em 1 (row=1, column=1 refere-se à célula A1)
- Use `data_only=True` para ler valores calculados: `load_workbook('file.xlsx', data_only=True)`
- **Aviso**: Se aberto com `data_only=True` e salvo, fórmulas são substituídas por valores e permanentemente perdidas
- Para arquivos grandes: Use `read_only=True` para leitura ou `write_only=True` para escrita
- Fórmulas são preservadas mas não avaliadas - use recalc.py para atualizar valores

### Trabalhando com pandas
- Especifique tipos de dados para evitar problemas de inferência: `pd.read_excel('file.xlsx', dtype={'id': str})`
- Para arquivos grandes, ler colunas específicas: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Tratar datas corretamente: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Diretrizes de Estilo de Código
**IMPORTANTE**: Ao gerar código Python para operações Excel:
- Escrever código Python mínimo e conciso sem comentários desnecessários
- Evitar nomes de variáveis verbosos e operações redundantes
- Evitar statements print desnecessários

**Para arquivos Excel em si**:
- Adicionar comentários a células com fórmulas complexas ou pressupostos importantes
- Documentar fontes de dados para valores codificados
- Incluir notas para cálculos-chave e seções do modelo