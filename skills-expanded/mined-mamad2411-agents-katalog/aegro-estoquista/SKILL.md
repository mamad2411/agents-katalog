---
name: aegro-estoquista
description: Dominio de estoque e insumos do Aegro - itens, locais, movimentacoes, catalogos e elementos
version: 0.5.1
---

# Aegro Estoquista

Skill especializada no dominio de estoque e insumos da plataforma Aegro. Cobre itens de estoque
(posicoes), locais de armazenamento, movimentacoes (logs), elementos (insumos) e catalogos.

---

## 1. Vocabulario

| Termo Aegro              | Termo CLI              | Descricao                                                                                 |
|---------------------------|------------------------|-------------------------------------------------------------------------------------------|
| Item de estoque           | `stock item`           | Posicao de estoque = cruzamento de um elemento em um local. Representa "quanto tem onde".  |
| Local de estoque          | `stock location`       | Armazem, deposito, silo ou qualquer local fisico de armazenamento.                         |
| Movimentacao de estoque   | `stock log`            | Registro de entrada, saida, transferencia ou consumo de um item.                           |
| Elemento                  | `elements`             | Insumo agricola. Categorias: DEFENSIVE, FERTILIZER, SEED, ITEM, SERVICE.                  |
| Catalogo                  | `catalogs`             | Base de dados pre-definida de elementos. Somente leitura. Usado como referencia.           |
| Entrada manual            | `stock entry`          | Tipo MANUAL_ENTRY. Registra compra ou recebimento. Possui valor monetario.                 |
| Remocao manual            | `stock removal`        | Tipo MANUAL_REMOVAL. Registra perda, ajuste ou descarte. Sem valor monetario.              |
| Transferencia             | `stock transfer`       | Tipo TRANSFER. Move quantidade entre dois locais. Sem valor monetario.                     |
| Consumo por atividade     | ACTIVITY_CONSUMPTION   | Automatico. Gerado quando uma atividade agricola realizada consome insumos.                |
| Tipo de defensivo         | `--type`               | HERBICIDE, INSECTICIDE, FUNGICIDE, ADJUVANT, BIOLOGICAL, OTHER.                           |
| Tipo de semente           | `--type`               | SOYBEAN, CORN, WHEAT, COTTON, RICE, BEAN, COFFEE, SUGARCANE, OTHER.                       |
| Unidade de medida         | `--unit`               | kg, L, un, t, sc (saca), mL, g, etc.                                                     |
| Quantidade                | `quantity`             | Objeto: `{"magnitude": X, "unit": "kg"}`. Magnitude pode ser negativa (divergencia).      |
| Associacao financeira     | `set-categories`       | Vincula elemento a categorias financeiras de receita e/ou despesa.                         |

---

## 2. Modelo de Dados

```
FARM
 +-- STOCK_LOCATION (local de armazenamento)
 |     +-- STOCK_ITEM (1:N posicoes de estoque por local)
 |           elementKey -> ELEMENT
 |           locationKey -> STOCK_LOCATION
 +-- ELEMENT (insumo cadastrado na fazenda)
 |     categoria: DEFENSIVE | FERTILIZER | SEED | ITEM | SERVICE
 |     +-- STOCK_ITEM (1:N posicoes em diferentes locais)
 |     +-- set-categories -> FINANCIAL_CATEGORY (ponte com dominio financeiro)
 +-- STOCK_LOG (historico de movimentacoes)
 |     elementKey -> ELEMENT
 |     sourceLocationKey -> STOCK_LOCATION (origem, para removal e transfer)
 |     destinationLocationKey -> STOCK_LOCATION (destino, para entry e transfer)
 +-- CATALOG (base pre-definida, somente leitura)
       +-- CATALOG_ELEMENT (referencia para criar elementos)
```

Relacionamentos-chave:
- STOCK_ITEM = intersecao ELEMENT x STOCK_LOCATION (posicao de estoque).
- STOCK_LOG registra toda movimentacao (entrada, saida, transferencia, consumo).
- ACTIVITY_REALIZATION gera STOCK_LOG de consumo automaticamente (dominio atividades).
- CATALOG e somente leitura; serve para buscar elementos padrao do mercado.
- `elements set-categories` conecta estoque ao dominio financeiro.

---

## 3. Regras de Negocio

1. **Quantidade pode ser negativa**: Se remocoes + consumos superam entradas, a posicao fica negativa. Isso indica divergencia de estoque, nao erro. O sistema permite.

2. **Formato de quantidade**: Sempre `{"magnitude": X, "unit": "kg"}`. O campo e `magnitude`, nao `amount` ou `quantity`.

3. **Entry tem valor monetario, Removal e Transfer nao**:
   - `stock entry`: requer `--amount` e `--currency`. Body: `{"amount": {"amount": X, "currencyCode": "BRL"}}`.
   - `stock removal`: NAO possui campo de valor. Apenas `elementKey`, `quantity`, `occurrenceDate`, `sourceLocationKey`.
   - `stock transfer`: NAO possui campo de valor. Possui `sourceLocationKey` E `destinationLocationKey`.

4. **Endpoints de criacao de movimentacao**:
   - Entry: `POST /pub/v1/stock-logs/manual-entries`
   - Removal: `POST /pub/v1/stock-logs/manual-removals`
   - Transfer: `POST /pub/v1/stock-logs` (endpoint generico)

5. **Elementos por categoria tem endpoints especificos**:
   - Defensivos: `POST /pub/v1/elements/defensives` (requer `--type`)
   - Fertilizantes: `POST /pub/v1/elements/fertilizers` (sem `--type`)
   - Sementes: `POST /pub/v1/elements/seeds` (requer `--type`)
   - Itens: `POST /pub/v1/elements/items` (requer `--type`)
   - Servicos: `POST /pub/v1/elements/services` (sem `--type`, sem `--manufacturer`)

6. **set-categories e ponte entre dominios**: Vincula elemento a categorias financeiras. Formato do body:
   ```json
   {"associations": {"revenueFinancialCategory": {"key": "financialCategory::abc"}, "expenseFinancialCategory": {"key": "financialCategory::def"}}}
   ```

7. **Catalogos sao somente leitura**: Nao e possivel criar, editar ou excluir elementos de catalogo. Use-os como referencia para criar seus proprios elementos.

8. **Paginacao padrao**: Todos os filtros usam `requiredPageNumber` e `maximumItemsPerPageCount: 50`.

---

## 4. Referencia de Comandos

### 4.1 stock (itens, locais e movimentacoes)

| Comando                | Tipo     | Parametros obrigatorios                                                     | Parametros opcionais                                      |
|-------------------------|----------|-----------------------------------------------------------------------------|-----------------------------------------------------------|
| `item <key>`            | GET      | `key` (argumento)                                                           | `--output`                                                |
| `location <key>`        | GET      | `key` (argumento)                                                           | `--output`                                                |
| `items`                 | POST     | (nenhum)                                                                    | `--location-key`, `--element-key`, `--crop-key`, `--page` |
| `locations`             | POST     | (nenhum)                                                                    | `--page`                                                  |
| `logs`                  | POST     | (nenhum)                                                                    | `--element-key`, `--start-date`, `--end-date`, `--source-key`, `--dest-key`, `--page` |
| `log <key>`             | GET      | `key` (argumento)                                                           | `--output`                                                |
| `entry`                 | POST     | `--element-key`, `--quantity`, `--unit`, `--date`, `--amount`, `--dest-key` | `--currency` (default BRL), `--observations`              |
| `removal`               | POST     | `--element-key`, `--quantity`, `--unit`, `--date`, `--source-key`           | `--observations`                                          |
| `transfer`              | POST     | `--element-key`, `--quantity`, `--unit`, `--date`, `--source-key`, `--dest-key` | `--observations`                                      |

**Exemplos reais:**

```bash
# Listar todos os itens de estoque de um elemento
aegro stock items --element-key element::abc123

# Listar itens em um local especifico
aegro stock items --location-key stockLocation::def456

# Listar locais de estoque
aegro stock locations --output table

# Consultar historico de movimentacoes de um elemento no periodo da safra
aegro stock logs --element-key element::abc123 \
  --start-date 2025-09-01 --end-date 2026-03-13

# Filtrar movimentacoes por local de origem
aegro stock logs --source-key stockLocation::def456

# Registrar entrada de estoque (compra de 50kg a R$ 500)
aegro stock entry --element-key element::abc123 \
  --quantity 50 --unit kg --date 2026-03-13 \
  --amount 500 --currency BRL --dest-key stockLocation::def456

# Registrar remocao de estoque (perda/ajuste de 5kg)
aegro stock removal --element-key element::abc123 \
  --quantity 5 --unit kg --date 2026-03-13 \
  --source-key stockLocation::def456 --observations "Perda por validade"

# Transferir 10kg entre locais
aegro stock transfer --element-key element::abc123 \
  --quantity 10 --unit kg --date 2026-03-13 \
  --source-key stockLocation::s1 --dest-key stockLocation::s2
```

### 4.2 elements (insumos)

| Comando                  | Tipo     | Parametros obrigatorios            | Parametros opcionais                       |
|---------------------------|----------|------------------------------------|--------------------------------------------|
| `get <key>`               | GET      | `key` (argumento)                  | `--output`                                 |
| `list`                    | POST     | (nenhum)                           | `--category` (repetivel), `--type` (repetivel), `--page` |
| `create-defensive`        | POST     | `--name`, `--type`, `--unit`       | `--manufacturer`, `--observations`         |
| `create-fertilizer`       | POST     | `--name`, `--unit`                 | `--manufacturer`, `--observations`         |
| `create-seed`             | POST     | `--name`, `--type`, `--unit`       | `--manufacturer`, `--observations`         |
| `create-item`             | POST     | `--name`, `--type`, `--unit`       | `--manufacturer`, `--observations`         |
| `create-service`          | POST     | `--name`, `--unit`                 | (nenhum)                                   |
| `set-categories <key>`    | POST     | `element_key` (argumento)          | `--revenue-category-key`, `--expense-category-key` |

**Exemplos reais:**

```bash
# Listar todos os defensivos
aegro elements list --category DEFENSIVE

# Listar herbicidas especificamente
aegro elements list --category DEFENSIVE --type HERBICIDE

# Listar fertilizantes e sementes
aegro elements list --category FERTILIZER --category SEED

# Criar defensivo herbicida
aegro elements create-defensive --name "Roundup Original" \
  --type HERBICIDE --unit L --manufacturer "Bayer"

# Criar fertilizante
aegro elements create-fertilizer --name "Ureia 46%" --unit kg \
  --manufacturer "Mosaic"

# Criar semente de soja
aegro elements create-seed --name "TMG 2381 IPRO" --type SOYBEAN --unit kg

# Criar servico
aegro elements create-service --name "Pulverizacao Aerea" --unit HA

# Criar item generico
aegro elements create-item --name "Sacaria 60kg" --type GENERAL --unit UN

# Vincular elemento a categorias financeiras
aegro elements set-categories element::abc123 \
  --revenue-category-key financialCategory::rev1 \
  --expense-category-key financialCategory::exp1
```

### 4.3 catalogs (catalogos de referencia)

| Comando                    | Tipo     | Parametros obrigatorios     | Parametros opcionais                           |
|-----------------------------|----------|-----------------------------|------------------------------------------------|
| `list`                      | GET      | (nenhum)                    | `--output`                                     |
| `element-keys <key>`        | GET      | `catalog_key` (argumento)   | `--output`                                     |
| `elements <key>`            | POST     | `catalog_key` (argumento)   | `--category` (repetivel), `--search-text`, `--page` |

**Exemplos reais:**

```bash
# Listar catalogos disponiveis
aegro catalogs list

# Listar chaves de elementos de um catalogo
aegro catalogs element-keys catalog::abc123

# Buscar elemento no catalogo por nome
aegro catalogs elements catalog::abc123 --search-text "Roundup" --category DEFENSIVE

# Listar sementes disponiveis no catalogo
aegro catalogs elements catalog::abc123 --category SEED --page 1
```

---

## 5. Gotchas

### CRITICO: Formato de valor monetario em entry

O campo `amount` da entrada de estoque usa `currencyCode` (nao `currency`):
```json
{"amount": {"amount": 500.00, "currencyCode": "BRL"}}
```
Isso e DIFERENTE do formato da parcela financeira (`{"amount": X, "currency": "BRL"}`).

### create-seed retorna HTTP 500 (Bug #5)

A criacao de sementes via API retorna erro 500 intermitentemente. Este e um bug conhecido da API Aegro. Workaround: criar a semente pela interface web do Aegro e depois consultar via CLI com `aegro elements list --category SEED`.

### set-categories usa formato aninhado

O body de `set-categories` nao e uma lista simples de keys. E um objeto aninhado:
```json
{
  "associations": {
    "revenueFinancialCategory": {"key": "financialCategory::abc"},
    "expenseFinancialCategory": {"key": "financialCategory::def"}
  }
}
```
Ambos os campos sao opcionais, mas pelo menos um deve ser fornecido.

### Transfer usa endpoint generico

Enquanto entry usa `/stock-logs/manual-entries` e removal usa `/stock-logs/manual-removals`, transfer usa o endpoint raiz `/stock-logs`. Nao confunda os endpoints.

### Filtros de logs sem --element-key podem retornar volumes enormes

O endpoint `stock logs` sem filtro de elemento retorna TODAS as movimentacoes da fazenda. Sempre filtre por `--element-key` ou por periodo (`--start-date` / `--end-date`) para evitar respostas enormes.

### Campo "occurrenceDate" no body (nao "date")

O CLI aceita `--date`, mas no body JSON o campo se chama `occurrenceDate`. Isso e tratado pelo CLI, mas e importante saber ao debugar.

### Fertilizante e servico NAO tem --type

Diferente de defensivo, semente e item, os endpoints de criacao de fertilizante e servico nao aceitam `--type`. Enviar `--type` gera erro.

---

## 6. Padroes e Exemplos

### Verificar estoque total de um elemento em todos os locais

```bash
# 1. Listar todas as posicoes do elemento
aegro stock items --element-key element::abc123 --output table

# Cada item retorna a quantidade atual no local. Some as magnitudes para o total.
```

### Historico de movimentacoes no periodo de safra

```bash
# Movimentacoes de semente de soja na safra 2025/2026
aegro stock logs --element-key element::abc123 \
  --start-date 2025-09-01 --end-date 2026-03-31

# Para filtrar por local especifico
aegro stock logs --element-key element::abc123 \
  --source-key stockLocation::def456 --start-date 2025-09-01
```

### Formula de reconciliacao de estoque

```
Posicao atual = Saldo inicial
              + SUM(entradas manuais)
              - SUM(remocoes manuais)
              - SUM(consumos por atividade)
              +/- SUM(transferencias)

Para verificar:
1. aegro stock items --element-key element::xxx  (posicao atual)
2. aegro stock logs --element-key element::xxx --start-date YYYY-MM-DD  (historico)
3. Comparar soma dos logs com posicao atual
```

### Fluxo completo: cadastrar insumo e dar entrada

```bash
# 1. Consultar catalogo para referencia
aegro catalogs elements catalog::abc --search-text "Glifosato" --category DEFENSIVE

# 2. Criar o elemento na fazenda
aegro elements create-defensive --name "Glifosato 480 SL" \
  --type HERBICIDE --unit L --manufacturer "Nortox"

# 3. Anotar a key retornada (element::xyz789)

# 4. Verificar locais de estoque disponiveis
aegro stock locations --output table

# 5. Registrar entrada de compra
aegro stock entry --element-key element::xyz789 \
  --quantity 200 --unit L --date 2026-03-13 \
  --amount 3600 --currency BRL \
  --dest-key stockLocation::armazem1 \
  --observations "NF 12345 - Nortox"

# 6. Vincular a categoria financeira de despesa
aegro elements set-categories element::xyz789 \
  --expense-category-key financialCategory::defensivos
```

### Transferir estoque entre depositos

```bash
# 1. Verificar posicao no deposito de origem
aegro stock items --element-key element::abc123 --location-key stockLocation::origem

# 2. Executar transferencia
aegro stock transfer --element-key element::abc123 \
  --quantity 50 --unit L --date 2026-03-13 \
  --source-key stockLocation::origem --dest-key stockLocation::destino

# 3. Verificar posicoes atualizadas
aegro stock items --element-key element::abc123 --output table
```

### Buscar elemento no catalogo e criar na fazenda

```bash
# 1. Listar catalogos
aegro catalogs list

# 2. Buscar no catalogo
aegro catalogs elements catalog::padrao --search-text "Ureia" --category FERTILIZER

# 3. Criar na fazenda baseado nos dados do catalogo
aegro elements create-fertilizer --name "Ureia 46%" --unit kg --manufacturer "Petrobras"
```

---

## 7. Anti-padroes

1. **Nao faca removal maior que o disponivel sem avisar.** O sistema permite e cria posicao negativa. Sempre verifique a posicao atual com `aegro stock items --element-key <key>` antes de executar removal.

2. **Nao confunda items (posicao) com logs (historico).** `stock items` mostra quanto tem agora. `stock logs` mostra o que aconteceu ao longo do tempo. Para saber o saldo, use `items`. Para auditoria, use `logs`.

3. **Sempre especifique --element-key em logs.** Sem filtro, `stock logs` retorna todas as movimentacoes da fazenda inteira, potencialmente milhares de registros. Filtre sempre.

4. **Nao tente modificar catalogos.** Catalogos sao somente leitura. Para personalizar um elemento do catalogo, crie um novo elemento na fazenda usando os dados do catalogo como referencia.

5. **Nao envie --type ao criar fertilizante ou servico.** Esses endpoints nao aceitam tipo. Defensivo, semente e item aceitam e exigem `--type`.

6. **Nao ignore o Bug #5 (create-seed).** Se `create-seed` falhar com 500, nao tente repetir varias vezes. Use a interface web do Aegro para criar a semente.

7. **Nao confunda endpoints de movimentacao.** Entry usa `/manual-entries`, removal usa `/manual-removals`, transfer usa o endpoint raiz `/stock-logs`. Usar o endpoint errado causa erro ou comportamento inesperado.

8. **Nao esqueca set-categories apos criar elemento.** Sem a associacao financeira, lancamentos de compra desse insumo nao serao classificados corretamente no financeiro.
