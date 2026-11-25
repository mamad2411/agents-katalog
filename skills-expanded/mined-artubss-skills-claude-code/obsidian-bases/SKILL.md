---
name: obsidian-bases
description: Criar e editar Obsidian Bases (arquivos .base) com views, filtros, fórmulas e resumos. Use quando trabalhar com arquivos .base, criar views de banco de dados de notas, ou quando o usuário mencionar Bases, table views, card views, filtros ou fórmulas no Obsidian.
---

# Skill Obsidian Bases

Este skill permite que o Claude Code crie e edite Obsidian Bases válidos (arquivos `.base`), incluindo views, filtros, fórmulas e todas as configurações relacionadas.

## Visão Geral

Obsidian Bases são arquivos baseados em YAML que definem views dinâmicas de notas em um vault Obsidian. Um arquivo Base pode conter múltiplas views, filtros globais, fórmulas, configurações de propriedades e resumos personalizados.

## Formato de Arquivo

Arquivos Base usam a extensão `.base` e contêm YAML válido. Também podem ser incorporados em blocos de código Markdown.

## Schema Completo

```yaml
# Filtros globais se aplicam a TODAS as views na base
filters:
  # Pode ser uma string de filtro única
  # OU um objeto de filtro recursivo com and/or/not
  and: []
  or: []
  not: []

# Define propriedades de fórmula que podem ser usadas em todas as views
formulas:
  formula_name: 'expression'

# Configure nomes de exibição e configurações para propriedades
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# Define fórmulas de resumo personalizadas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# Define uma ou mais views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # Opcional: limita resultados
    groupBy:                     # Opcional: agrupa resultados
      property: property_name
      direction: ASC | DESC
    filters:                     # Filtros específicos da view
      and: []
    order:                       # Propriedades para exibir em ordem
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Mapeia propriedades para fórmulas de resumo
      property_name: Average
```

## Sintaxe de Filtros

Filtros reduzem resultados. Podem ser aplicados globalmente ou por view.

### Estrutura de Filtros

```yaml
# Filtro único
filters: 'status == "done"'

# AND - todas as condições devem ser verdadeiras
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR - qualquer condição pode ser verdadeira
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

# NOT - exclui itens correspondentes
filters:
  not:
    - 'file.hasTag("archived")'

# Filtros aninhados
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

### Operadores de Filtro

| Operador | Descrição |
|----------|-----------|
| `==` | igual |
| `!=` | não igual |
| `>` | maior que |
| `<` | menor que |
| `>=` | maior ou igual |
| `<=` | menor ou igual |
| `&&` | e lógico |
| `\|\|` | ou lógico |
| `!` | não lógico |

## Propriedades

### Três Tipos de Propriedades

1. **Propriedades de nota** - Do frontmatter: `note.author` ou apenas `author`
2. **Propriedades de arquivo** - Metadados do arquivo: `file.name`, `file.mtime`, etc.
3. **Propriedades de fórmula** - Valores computados: `formula.my_formula`

### Referência de Propriedades de Arquivo

| Propriedade | Tipo | Descrição |
|----------|------|-----------|
| `file.name` | String | Nome do arquivo |
| `file.basename` | String | Nome do arquivo sem extensão |
| `file.path` | String | Caminho completo do arquivo |
| `file.folder` | String | Caminho da pasta pai |
| `file.ext` | String | Extensão do arquivo |
| `file.size` | Number | Tamanho do arquivo em bytes |
| `file.ctime` | Date | Tempo de criação |
| `file.mtime` | Date | Tempo de modificação |
| `file.tags` | List | Todas as tags no arquivo |
| `file.links` | List | Links internos no arquivo |
| `file.backlinks` | List | Arquivos que fazem link para este arquivo |
| `file.embeds` | List | Incorporações na nota |
| `file.properties` | Object | Todas as propriedades do frontmatter |

### A Palavra-chave `this`

- Em área de conteúdo principal: refere-se ao arquivo base em si
- Quando incorporado: refere-se ao arquivo que está incorporando
- Na sidebar: refere-se ao arquivo ativo no conteúdo principal

## Sintaxe de Fórmulas

Fórmulas computam valores de propriedades. Definidas na seção `formulas`.

```yaml
formulas:
  # Aritmética simples
  total: "price * quantity"
  
  # Lógica condicional
  status_icon: 'if(done, "✅", "⏳")'
  
  # Formatação de string
  formatted_price: 'if(price, price.toFixed(2) + " reais")'
  
  # Formatação de data
  created: 'file.ctime.format("YYYY-MM-DD")'
  
  # Expressões complexas
  days_old: '((now() - file.ctime) / 86400000).round(0)'
```

## Referência de Funções

### Funções Globais

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `date()` | `date(string): date` | Converte string para data. Formato: `YYYY-MM-DD HH:mm:ss` |
| `duration()` | `duration(string): duration` | Converte string para duração |
| `now()` | `now(): date` | Data e hora atuais |
| `today()` | `today(): date` | Data atual (hora = 00:00:00) |
| `if()` | `if(condition, trueResult, falseResult?)` | Condicional |
| `min()` | `min(n1, n2, ...): number` | Menor número |
| `max()` | `max(n1, n2, ...): number` | Maior número |
| `number()` | `number(any): number` | Converte para número |
| `link()` | `link(path, display?): Link` | Cria um link |
| `list()` | `list(element): List` | Encapsula em lista se não for já |
| `file()` | `file(path): file` | Obtém objeto de arquivo |
| `image()` | `image(path): image` | Cria imagem para renderização |
| `icon()` | `icon(name): icon` | Ícone Lucide pelo nome |
| `html()` | `html(string): html` | Renderiza como HTML |
| `escapeHTML()` | `escapeHTML(string): string` | Escapa caracteres HTML |

### Funções de Qualquer Tipo

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `isTruthy()` | `any.isTruthy(): boolean` | Coerce para boolean |
| `isType()` | `any.isType(type): boolean` | Verifica tipo |
| `toString()` | `any.toString(): string` | Converte para string |

### Funções e Campos de Data

**Campos:** `date.year`, `date.month`, `date.day`, `date.hour`, `date.minute`, `date.second`, `date.millisecond`

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `date()` | `date.date(): date` | Remove a porção de hora |
| `format()` | `date.format(string): string` | Formata com padrão Moment.js |
| `time()` | `date.time(): string` | Obtém hora como string |
| `relative()` | `date.relative(): string` | Tempo relativo legível |
| `isEmpty()` | `date.isEmpty(): boolean` | Sempre falso para datas |

### Aritmética de Data

```yaml
# Unidades de duração: y/year/years, M/month/months, d/day/days, 
#                       w/week/weeks, h/hour/hours, m/minute/minutes, s/second/seconds

# Adiciona/subtrai durações
"date + \"1M\""           # Adiciona 1 mês
"date - \"2h\""           # Subtrai 2 horas
"now() + \"1 day\""       # Amanhã
"today() + \"7d\""        # Uma semana a partir de hoje

# Subtrai datas para diferença em milissegundos
"now() - file.ctime"

# Aritmética de duração complexa
"now() + (duration('1d') * 2)"
```

### Funções de String

**Campo:** `string.length`

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `contains()` | `string.contains(value): boolean` | Verifica substring |
| `containsAll()` | `string.containsAll(...values): boolean` | Todas as substrings presentes |
| `containsAny()` | `string.containsAny(...values): boolean` | Qualquer substring presente |
| `startsWith()` | `string.startsWith(query): boolean` | Começa com query |
| `endsWith()` | `string.endsWith(query): boolean` | Termina com query |
| `isEmpty()` | `string.isEmpty(): boolean` | Vazio ou não presente |
| `lower()` | `string.lower(): string` | Para minúsculas |
| `title()` | `string.title(): string` | Para Title Case |
| `trim()` | `string.trim(): string` | Remove espaços em branco |
| `replace()` | `string.replace(pattern, replacement): string` | Substitui padrão |
| `repeat()` | `string.repeat(count): string` | Repete string |
| `reverse()` | `string.reverse(): string` | Inverte string |
| `slice()` | `string.slice(start, end?): string` | Substring |
| `split()` | `string.split(separator, n?): list` | Divide em lista |

### Funções de Número

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `abs()` | `number.abs(): number` | Valor absoluto |
| `ceil()` | `number.ceil(): number` | Arredonda para cima |
| `floor()` | `number.floor(): number` | Arredonda para baixo |
| `round()` | `number.round(digits?): number` | Arredonda para dígitos |
| `toFixed()` | `number.toFixed(precision): string` | Notação de ponto fixo |
| `isEmpty()` | `number.isEmpty(): boolean` | Não presente |

### Funções de Lista

**Campo:** `list.length`

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `contains()` | `list.contains(value): boolean` | Elemento existe |
| `containsAll()` | `list.containsAll(...values): boolean` | Todos os elementos existem |
| `containsAny()` | `list.containsAny(...values): boolean` | Qualquer elemento existe |
| `filter()` | `list.filter(expression): list` | Filtra por condição (usa `value`, `index`) |
| `map()` | `list.map(expression): list` | Transforma elementos (usa `value`, `index`) |
| `reduce()` | `list.reduce(expression, initial): any` | Reduz para valor único (usa `value`, `index`, `acc`) |
| `flat()` | `list.flat(): list` | Achata listas aninhadas |
| `join()` | `list.join(separator): string` | Une em string |
| `reverse()` | `list.reverse(): list` | Inverte ordem |
| `slice()` | `list.slice(start, end?): list` | Sublista |
| `sort()` | `list.sort(): list` | Ordena crescente |
| `unique()` | `list.unique(): list` | Remove duplicatas |
| `isEmpty()` | `list.isEmpty(): boolean` | Sem elementos |

### Funções de Arquivo

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `asLink()` | `file.asLink(display?): Link` | Converte para link |
| `hasLink()` | `file.hasLink(otherFile): boolean` | Tem link para arquivo |
| `hasTag()` | `file.hasTag(...tags): boolean` | Tem qualquer uma das tags |
| `hasProperty()` | `file.hasProperty(name): boolean` | Tem propriedade |
| `inFolder()` | `file.inFolder(folder): boolean` | Em pasta ou subpasta |

### Funções de Link

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `asFile()` | `link.asFile(): file` | Obtém objeto de arquivo |
| `linksTo()` | `link.linksTo(file): boolean` | Faz link para arquivo |

### Funções de Objeto

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `isEmpty()` | `object.isEmpty(): boolean` | Sem propriedades |
| `keys()` | `object.keys(): list` | Lista de chaves |
| `values()` | `object.values(): list` | Lista de valores |

### Funções de Expressão Regular

| Função | Assinatura | Descrição |
|----------|-----------|-------------|
| `matches()` | `regexp.matches(string): boolean` | Testa se corresponde |

## Tipos de View

### Table View

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

### Cards View

```yaml
views:
  - type: cards
    name: "Gallery"
    order:
      - file.name
      - cover_image
      - description
```

### List View

```yaml
views:
  - type: list
    name: "Simple List"
    order:
      - file.name
      - status
```

### Map View

Requer propriedades de latitude/longitude e o plugin Maps.

```yaml
views:
  - type: map
    name: "Locations"
    # Configurações específicas do mapa para propriedades lat/lng
```

## Fórmulas de Resumo Padrão

| Nome | Tipo de Entrada | Descrição |
|------|------------|-------------|
| `Average` | Number | Média matemática |
| `Min` | Number | Menor número |
| `Max` | Number | Maior número |
| `Sum` | Number | Soma de todos os números |
| `Range` | Number | Max - Min |
| `Median` | Number | Mediana matemática |
| `Stddev` | Number | Desvio padrão |
| `Earliest` | Date | Data mais antiga |
| `Latest` | Date | Data mais recente |
| `Range` | Date | Mais recente - Mais antiga |
| `Checked` | Boolean | Contagem de valores verdadeiros |
| `Unchecked` | Boolean | Contagem de valores falsos |
| `Empty` | Any | Contagem de valores vazios |
| `Filled` | Any | Contagem de valores não-vazios |
| `Unique` | Any | Contagem de valores únicos |

## Exemplos Completos

### Base de Rastreamento de Tarefas

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "🔴 Alta", if(priority == 2, "🟡 Média", "🟢 Baixa"))'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: "Dias até Vencimento"
  formula.priority_label:
    displayName: Prioridade

views:
  - type: table
    name: "Tarefas Ativas"
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.priority_label
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average

  - type: table
    name: "Concluídas"
    filters:
      and:
        - 'status == "done"'
    order:
      - file.name
      - completed_date
```

### Base de Lista de Leitura

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

formulas:
  reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
  status_icon: 'if(status == "reading", "📖", if(status == "done", "✅", "📚"))'
  year_read: 'if(finished_date, date(finished_date).year, "")'

properties:
  author:
    displayName: Autor
  formula.status_icon:
    displayName: ""
  formula.reading_time:
    displayName: "Tempo Est."

views:
  - type: cards
    name: "Biblioteca"
    order:
      - cover
      - file.name
      - author
      - formula.status_icon
    filters:
      not:
        - 'status == "dropped"'

  - type: table
    name: "Lista de Leitura"
    filters:
      and:
        - 'status == "to-read"'
    order:
      - file.name
      - author
      - pages
      - formula.reading_time
```

### Base de Notas de Projeto

```yaml
filters:
  and:
    - file.inFolder("Projects")
    - 'file.ext == "md"'

formulas:
  last_updated: 'file.mtime.relative()'
  link_count: 'file.links.length'
  
summaries:
  avgLinks: 'values.filter(value.isType("number")).mean().round(1)'

properties:
  formula.last_updated:
    displayName: "Atualizado"
  formula.link_count:
    displayName: "Links"

views:
  - type: table
    name: "Todos os Projetos"
    order:
      - file.name
      - status
      - formula.last_updated
      - formula.link_count
    summaries:
      formula.link_count: avgLinks
    groupBy:
      property: status
      direction: ASC

  - type: list
    name: "Lista Rápida"
    order:
      - file.name
      - status
```

### Índice de Notas Diárias

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")
    - '/^\d{4}-\d{2}-\d{2}$/.matches(file.basename)'

formulas:
  word_estimate: '(file.size / 5).round(0)'
  day_of_week: 'date(file.basename).format("dddd")'

properties:
  formula.day_of_week:
    displayName: "Dia"
  formula.word_estimate:
    displayName: "~Palavras"

views:
  - type: table
    name: "Notas Recentes"
    limit: 30
    order:
      - file.name
      - formula.day_of_week
      - formula.word_estimate
      - file.mtime
```

## Incorporando Bases

Incorpore em arquivos Markdown:

```markdown
![[MyBase.base]]

<!-- View específica -->
![[MyBase.base#View Name]]
```

## Regras de Aspas YAML

- Use aspas simples para fórmulas contendo aspas duplas: `'if(done, "Yes", "No")'`
- Use aspas duplas para strings simples: `"My View Name"`
- Escape aspas aninhadas corretamente em expressões complexas

## Padrões Comuns

### Filtrar por Tag
```yaml
filters:
  and:
    - file.hasTag("project")
```

### Filtrar por Pasta
```yaml
filters:
  and:
    - file.inFolder("Notes")
```

### Filtrar por Intervalo de Data
```yaml
filters:
  and:
    - 'file.mtime > now() - "7d"'
```

### Filtrar por Valor de Propriedade
```yaml
filters:
  and:
    - 'status == "active"'
    - 'priority >= 3'
```

### Combinar Múltiplas Condições
```yaml
filters:
  or:
    - and:
        - file.hasTag("important")
        - 'status != "done"'
    - and:
        - 'priority == 1'
        - 'due != ""'
```

## Referências

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
- [Formulas](https://help.obsidian.md/formulas)