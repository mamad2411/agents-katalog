---
name: invoice-organizer
description: Organiza automaticamente faturas e recibos para preparação de impostos lendo arquivos desorganizados, extraindo informações-chave, renomeando-os de forma consistente e classificando-os em pastas lógicas. Transforma horas de contabilidade manual em minutos de organização automatizada.
---

# Organizador de Faturas

Esta habilidade transforma pastas caóticas de faturas, recibos e documentos financeiros em um sistema de arquivamento limpo e pronto para impostos sem esforço manual.

## Quando Usar Esta Habilidade

- Preparando para a época de declaração de impostos e precisa de registros organizados
- Gerenciando despesas comerciais de múltiplos fornecedores
- Organizando recibos de uma pasta desorganizada ou downloads de email
- Configurando arquivamento automático de faturas para contabilidade contínua
- Arquivando registros financeiros por ano ou categoria
- Reconciliando despesas para reembolso
- Preparando documentação para contadores

## O Que Esta Habilidade Faz

1. **Lê Conteúdo de Faturas**: Extrai informações de PDFs, imagens e documentos:
   - Nome do fornecedor/empresa
   - Número da fatura
   - Data
   - Valor
   - Descrição do produto ou serviço
   - Método de pagamento

2. **Renomeia Arquivos Consistentemente**: Cria nomes de arquivo padronizados:
   - Formato: `YYYY-MM-DD Fornecedor - Fatura - ProdutoOuServico.pdf`
   - Exemplos: `2024-03-15 Adobe - Fatura - Creative Cloud.pdf`

3. **Organiza por Categoria**: Classifica em pastas lógicas:
   - Por fornecedor
   - Por categoria de despesa (software, escritório, viagens, etc.)
   - Por período (ano, trimestre, mês)
   - Por categoria fiscal (dedutível, pessoal, etc.)

4. **Lida com Múltiplos Formatos**: Funciona com:
   - Faturas em PDF
   - Recibos digitalizados (JPG, PNG)
   - Anexos de email
   - Screenshots
   - Extratos bancários

5. **Mantém Originais**: Preserva arquivos originais enquanto organiza cópias

## Como Usar

### Uso Básico

Navegue até sua pasta de faturas desorganizada:
```
cd ~/Desktop/recibos-para-classificar
```

Em seguida, peça ao Claude Code:
```
Organize these invoices for taxes
```

Ou mais especificamente:
```
Read all invoices in this folder, rename them to 
"YYYY-MM-DD Vendor - Invoice - Product.pdf" format, 
and organize them by vendor
```

### Organização Avançada

```
Organize these invoices:
1. Extract date, vendor, and description from each file
2. Rename to standard format
3. Sort into folders by expense category (Software, Office, Travel, etc.)
4. Create a CSV spreadsheet with all invoice details for my accountant
```

## Instruções

Quando um usuário solicitar organização de faturas:

1. **Escaneie a Pasta**
   
   Identifique todos os arquivos de fatura:
   ```bash
   # Find all invoice-related files
   find . -type f \( -name "*.pdf" -o -name "*.jpg" -o -name "*.png" \) -print
   ```
   
   Reporte os achados:
   - Número total de arquivos
   - Tipos de arquivo
   - Intervalo de datas (se discernível dos nomes)
   - Organização atual (ou falta dela)

2. **Extraia Informações de Cada Arquivo**
   
   Para cada fatura, extraia:
   
   **De faturas em PDF**:
   - Use extração de texto para ler conteúdo da fatura
   - Procure por padrões comuns:
     - "Data da Fatura:", "Data:", "Emitida:"
     - "Número da Fatura:", "Nº da Fatura:"
     - Nome da empresa (geralmente no topo)
     - "Valor Devido:", "Total:", "Valor:"
     - "Descrição:", "Serviço:", "Produto:"
   
   **De recibos em imagem**:
   - Leia texto visível em imagens
   - Identifique nome do fornecedor (geralmente no topo)
   - Procure pela data (formatos comuns)
   - Encontre valor total
   
   **Fallback para arquivos não claros**:
   - Use pistas do nome do arquivo
   - Verifique data de criação/modificação do arquivo
   - Sinalize para revisão manual se informações críticas estiverem faltando

3. **Determine a Estratégia de Organização**
   
   Pergunte preferência do usuário se não especificado:
   
   ```markdown
   Encontrei [X] faturas de [intervalo de datas].
   
   Como você gostaria de organizá-las?
   
   1. **Por Fornecedor** (Adobe/, Amazon/, Stripe/, etc.)
   2. **Por Categoria** (Software/, Escritório/, Viagens/, etc.)
   3. **Por Data** (2024/Q1/, 2024/Q2/, etc.)
   4. **Por Categoria Fiscal** (Dedutível/, Pessoal/, etc.)
   5. **Personalizado** (descreva sua estrutura)
   
   Ou posso usar uma estrutura padrão: Ano/Categoria/Fornecedor
   ```

4. **Crie Nome de Arquivo Padronizado**
   
   Para cada fatura, crie um nome de arquivo seguindo este padrão:
   
   ```
   YYYY-MM-DD Fornecedor - Fatura - Descrição.ext
   ```
   
   Exemplos:
   - `2024-03-15 Adobe - Fatura - Creative Cloud.pdf`
   - `2024-01-10 Amazon - Recibo - Suprimentos de Escritório.pdf`
   - `2023-12-01 Stripe - Fatura - Processamento Mensal de Pagamentos.pdf`
   
   **Melhores Práticas de Nome de Arquivo**:
   - Remova caracteres especiais exceto hífens
   - Capitalize nomes de fornecedores corretamente
   - Mantenha descrições concisas mas significativas
   - Use formato de data consistente (YYYY-MM-DD) para ordenação
   - Preserve extensão de arquivo original

5. **Execute a Organização**
   
   Antes de mover arquivos, exiba o plano:
   
   ```markdown
   # Plano de Organização
   
   ## Estrutura Proposta
   ```
   Faturas/
   ├── 2023/
   │   ├── Software/
   │   │   ├── Adobe/
   │   │   └── Microsoft/
   │   ├── Serviços/
   │   └── Escritório/
   └── 2024/
       ├── Software/
       ├── Serviços/
       └── Escritório/
   ```
   
   ## Exemplos de Mudanças
   
   Antes: `invoice_adobe_march.pdf`
   Depois: `2024-03-15 Adobe - Fatura - Creative Cloud.pdf`
   Localização: `Faturas/2024/Software/Adobe/`
   
   Antes: `IMG_2847.jpg`
   Depois: `2024-02-10 Staples - Recibo - Suprimentos de Escritório.jpg`
   Localização: `Faturas/2024/Escritório/Staples/`
   
   Processar [X] arquivos? (sim/não)
   ```
   
   Após aprovação:
   ```bash
   # Create folder structure
   mkdir -p "Faturas/2024/Software/Adobe"
   
   # Copy (don't move) to preserve originals
   cp "original.pdf" "Faturas/2024/Software/Adobe/2024-03-15 Adobe - Fatura - Creative Cloud.pdf"
   
   # Or move if user prefers
   mv "original.pdf" "new/path/standardized-name.pdf"
   ```

6. **Gere Relatório de Resumo**
   
   Crie um arquivo CSV com todos os detalhes de fatura:
   
   ```csv
   Data,Fornecedor,Número da Fatura,Descrição,Valor,Categoria,Caminho do Arquivo
   2024-03-15,Adobe,INV-12345,Creative Cloud,52.99,Software,Faturas/2024/Software/Adobe/2024-03-15 Adobe - Fatura - Creative Cloud.pdf
   2024-03-10,Amazon,123-4567890-1234567,Suprimentos de Escritório,127.45,Escritório,Faturas/2024/Escritório/Amazon/2024-03-10 Amazon - Recibo - Suprimentos de Escritório.pdf
   ...
   ```
   
   Este CSV é útil para:
   - Importar em software de contabilidade
   - Compartilhar com contadores
   - Rastreamento de despesas e relatórios
   - Preparação de impostos

7. **Forneça Resumo de Conclusão**
   
   ```markdown
   # Organização Concluída! 📊
   
   ## Resumo
   - **Processadas**: [X] faturas
   - **Intervalo de datas**: [mais antiga] a [mais recente]
   - **Valor total**: R$ [soma] (se valores extraídos)
   - **Fornecedores**: [Y] fornecedores únicos
   
   ## Nova Estrutura
   ```
   Faturas/
   ├── 2024/ (45 arquivos)
   │   ├── Software/ (23 arquivos)
   │   ├── Serviços/ (12 arquivos)
   │   └── Escritório/ (10 arquivos)
   └── 2023/ (12 arquivos)
   ```
   
   ## Arquivos Criados
   - `/Faturas/` - Faturas organizadas
   - `/Faturas/resumo-faturas.csv` - Planilha para contabilidade
   - `/Faturas/originais/` - Arquivos originais (se copiados)
   
   ## Arquivos Precisando Revisão
   [Liste arquivos onde informações não puderam ser extraídas completamente]
   
   ## Próximos Passos
   1. Revise o arquivo `resumo-faturas.csv`
   2. Verifique arquivos na pasta "Precisa de Revisão"
   3. Importe CSV em seu software de contabilidade
   4. Configure organização automática para futuras faturas
   
   Pronto para a época de impostos! 🎉
   ```

## Exemplos

### Exemplo 1: Preparação de Impostos (De Martin Merschroth)

**Usuário**: "Tenho uma pasta desorganizada de faturas para impostos. Classifique e renomeie corretamente."

**Processo**:
1. Escaneia pasta: encontra 147 PDFs e imagens
2. Lê cada fatura para extrair:
   - Data
   - Nome do fornecedor
   - Número da fatura
   - Descrição do produto/serviço
3. Renomeia todos os arquivos: `YYYY-MM-DD Fornecedor - Fatura - Produto.pdf`
4. Organiza em: `2024/Software/`, `2024/Viagens/`, etc.
5. Cria `resumo-faturas.csv` para contador
6. Resultado: Faturas organizadas e prontas para impostos em minutos

### Exemplo 2: Reconciliação de Despesas Mensais

**Usuário**: "Organize meus recibos comerciais do mês passado por categoria."

**Saída**:
```markdown
# Recibos de Março de 2024 Organizados

## Por Categoria
- Software e Ferramentas: R$ 847,32 (12 faturas)
- Suprimentos de Escritório: R$ 234,18 (8 recibos)
- Viagens e Refeições: R$ 1.456,90 (15 recibos)
- Serviços Profissionais: R$ 2.500,00 (3 faturas)

Total: R$ 5.038,40

Todos os recibos renomeados e arquivados em:
`Recibos-Comerciais/2024/03-Março/[Categoria]/`

Exportação CSV: `março-2024-despesas.csv`
```

### Exemplo 3: Arquivo Multi-Ano

**Usuário**: "Tenho 3 anos de faturas aleatórias. Organize por ano e depois por fornecedor."

**Saída**: Cria estrutura:
```
Faturas/
├── 2022/
│   ├── Adobe/
│   ├── Amazon/
│   └── ...
├── 2023/
│   ├── Adobe/
│   ├── Amazon/
│   └── ...
└── 2024/
    ├── Adobe/
    ├── Amazon/
    └── ...
```

Cada arquivo renomeado corretamente com data e descrição.

### Exemplo 4: Limpeza de Downloads de Email

**Usuário**: "Faço download de faturas do Gmail. Estão todas nomeadas como 'fatura.pdf', 'fatura(1).pdf', etc. Corrija essa bagunça."

**Saída**:
```markdown
Encontrados 89 arquivos todos nomeados como "fatura*.pdf"

Lendo cada arquivo para extrair informações reais...

Exemplos renomeados:
- fatura.pdf → 2024-03-15 Shopify - Fatura - Assinatura Mensal.pdf
- fatura(1).pdf → 2024-03-14 Google - Fatura - Workspace.pdf
- fatura(2).pdf → 2024-03-10 Netlify - Fatura - Plano Pro.pdf

Todos os arquivos renomeados e organizados por fornecedor.
```

## Padrões Comuns de Organização

### Por Fornecedor (Simples)
```
Faturas/
├── Adobe/
├── Amazon/
├── Google/
└── Microsoft/
```

### Por Ano e Categoria (Pronto para Impostos)
```
Faturas/
├── 2023/
│   ├── Software/
│   ├── Hardware/
│   ├── Serviços/
│   └── Viagens/
└── 2024/
    └── ...
```

### Por Trimestre (Rastreamento Detalhado)
```
Faturas/
├── 2024/
│   ├── Q1/
│   │   ├── Software/
│   │   ├── Escritório/
│   │   └── Viagens/
│   └── Q2/
│       └── ...
```

### Por Categoria Fiscal (Pronto para Contador)
```
Faturas/
├── Dedutível/
│   ├── Software/
│   ├── Escritório/
│   └── Serviços-Profissionais/
├── Parcialmente-Dedutível/
│   └── Refeições-Viagens/
└── Pessoal/
```

## Configuração de Automação

Para organização contínua:

```
Create a script that watches my ~/Downloads/invoices folder 
and auto-organizes any new invoice files using our standard 
naming and folder structure.
```

Isso cria uma solução persistente que organiza faturas conforme chegam.

## Dicas Profissionais

1. **Digitalize emails em PDF**: Use Preview ou similar para salvar faturas de email como PDFs primeiro
2. **Downloads consistentes**: Salve todas as faturas em uma pasta para processamento em lote
3. **Rotina mensal**: Organize faturas mensalmente, não anualmente
4. **Faça backup dos originais**: Mantenha arquivos originais antes de reorganizar
5. **Inclua valores em CSV**: Útil para rastreamento de orçamento
6. **Marque por dedutibilidade**: Anote quais despesas são dedutíveis em impostos
7. **Mantenha recibos por 7 anos**: Período padrão de auditoria

## Lidando com Casos Especiais

### Informações Faltando
Se data/fornecedor não puder ser extraído:
- Sinalize arquivo para revisão manual
- Use data de modificação do arquivo como fallback
- Crie pasta "Precisa-de-Revisão/"

### Faturas Duplicadas
Se a mesma fatura aparecer múltiplas vezes:
- Compare hash de arquivos
- Mantenha versão de melhor qualidade
- Anote duplicatas no resumo

### Faturas Multi-Página
Para faturas divididas entre arquivos:
- Mescle PDFs se necessário
- Use nomenclatura consistente para partes
- Anote em CSV se fatura está dividida

### Formatos Não-Padrão
Para formatos de recibos incomuns:
- Extraia o que for possível
- Padronize o que conseguir
- Sinalize para revisão se informações críticas faltarem

## Casos de Uso Relacionados

- Criando relatórios de despesas para reembolso
- Organizando extratos bancários
- Gerenciando contratos de fornecedor
- Arquivando registros financeiros antigos
- Preparando para auditorias
- Rastreando custos de assinatura ao longo do tempo