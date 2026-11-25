---
name: obsidian-markdown
description: Crie e edite Markdown com suporte a Obsidian, incluindo wikilinks, embeds, callouts, properties e outras sintaxes específicas do Obsidian. Use quando trabalhar com arquivos .md no Obsidian, ou quando o usuário mencionar wikilinks, callouts, frontmatter, tags, embeds ou notas do Obsidian.
---

# Habilidade Obsidian Flavored Markdown

Esta habilidade permite que o Claude Code crie e edite Markdown válido com suporte a Obsidian, incluindo todas as extensões de sintaxe específicas do Obsidian.

## Visão Geral

O Obsidian usa uma combinação de variantes de Markdown:
- [CommonMark](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [LaTeX](https://www.latex-project.org/) para matemática
- Extensões específicas do Obsidian (wikilinks, callouts, embeds, etc.)

## Formatação Básica

### Parágrafos e Quebras de Linha

```markdown
This is a paragraph.

This is another paragraph (blank line between creates separate paragraphs).

For a line break within a paragraph, add two spaces at the end  
or use Shift+Enter.
```

### Títulos

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

### Formatação de Texto

| Estilo | Sintaxe | Exemplo | Resultado |
|--------|---------|---------|-----------|
| Negrito | `**text**` ou `__text__` | `**Bold**` | **Bold** |
| Itálico | `*text*` ou `_text_` | `*Italic*` | *Italic* |
| Negrito + Itálico | `***text***` | `***Both***` | ***Both*** |
| Tachado | `~~text~~` | `~~Striked~~` | ~~Striked~~ |
| Destaque | `==text==` | `==Highlighted==` | ==Highlighted== |
| Código inline | `` `code` `` | `` `code` `` | `code` |

### Escapando Formatação

Use barra invertida para escapar caracteres especiais:
```markdown
\*This won't be italic\*
\#This won't be a heading
1\. This won't be a list item
```

Caracteres comuns a escapar: `\*`, `\_`, `\#`, `` \` ``, `\|`, `\~`

## Links Internos (Wikilinks)

### Links Básicos

```markdown
[[Note Name]]
[[Note Name.md]]
[[Note Name|Display Text]]
```

### Link para Títulos

```markdown
[[Note Name#Heading]]
[[Note Name#Heading|Custom Text]]
[[#Heading in same note]]
[[##Search all headings in vault]]
```

### Link para Blocos

```markdown
[[Note Name#^block-id]]
[[Note Name#^block-id|Custom Text]]
```

Defina um ID de bloco adicionando `^block-id` ao final de um parágrafo:
```markdown
This is a paragraph that can be linked to. ^my-block-id
```

Para listas e citações, adicione o ID do bloco em uma linha separada:
```markdown
> This is a quote
> With multiple lines

^quote-id
```

### Links de Busca

```markdown
[[##heading]]     Search for headings containing "heading"
[[^^block]]       Search for blocks containing "block"
```

## Links no Estilo Markdown

```markdown
[Display Text](Note%20Name.md)
[Display Text](Note%20Name.md#Heading)
[Display Text](https://example.com)
[Note](obsidian://open?vault=VaultName&file=Note.md)
```

Nota: Espaços devem ser codificados como `%20` em links Markdown.

## Embeds

### Embed de Notas

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
```

### Embed de Imagens

```markdown
![[image.png]]
![[image.png|640x480]]    Width x Height
![[image.png|300]]        Width only (maintains aspect ratio)
```

### Imagens Externas

```markdown
![Alt text](https://example.com/image.png)
![Alt text|300](https://example.com/image.png)
```

### Embed de Áudio

```markdown
![[audio.mp3]]
![[audio.ogg]]
```

### Embed de PDF

```markdown
![[document.pdf]]
![[document.pdf#page=3]]
![[document.pdf#height=400]]
```

### Embed de Listas

```markdown
![[Note#^list-id]]
```

Onde a lista foi definida com um ID de bloco:
```markdown
- Item 1
- Item 2
- Item 3

^list-id
```

### Embed de Resultados de Busca

````markdown
```query
tag:#project status:done
```
````

## Callouts

### Callout Básico

```markdown
> [!note]
> This is a note callout.

> [!info] Custom Title
> This callout has a custom title.

> [!tip] Title Only
```

### Callouts Recolhíveis

```markdown
> [!faq]- Collapsed by default
> This content is hidden until expanded.

> [!faq]+ Expanded by default
> This content is visible but can be collapsed.
```

### Callouts Aninhados

```markdown
> [!question] Outer callout
> > [!note] Inner callout
> > Nested content
```

### Tipos de Callout Suportados

| Tipo | Aliases | Descrição |
|------|---------|-----------|
| `note` | - | Azul, ícone de lápis |
| `abstract` | `summary`, `tldr` | Teal, ícone de clipboard |
| `info` | - | Azul, ícone de info |
| `todo` | - | Azul, ícone de checkbox |
| `tip` | `hint`, `important` | Ciano, ícone de chama |
| `success` | `check`, `done` | Verde, ícone de checkmark |
| `question` | `help`, `faq` | Amarelo, ícone de interrogação |
| `warning` | `caution`, `attention` | Laranja, ícone de aviso |
| `failure` | `fail`, `missing` | Vermelho, ícone X |
| `danger` | `error` | Vermelho, ícone de raio |
| `bug` | - | Vermelho, ícone de bug |
| `example` | - | Roxo, ícone de lista |
| `quote` | `cite` | Cinza, ícone de citação |

### Callouts Personalizados (CSS)

```css
.callout[data-callout="custom-type"] {
  --callout-color: 255, 0, 0;
  --callout-icon: lucide-alert-circle;
}
```

## Listas

### Listas Não Ordenadas

```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3

* Also works with asterisks
+ Or plus signs
```

### Listas Ordenadas

```markdown
1. First item
2. Second item
   1. Nested numbered
   2. Another nested
3. Third item

1) Alternative syntax
2) With parentheses
```

### Listas de Tarefas

```markdown
- [ ] Incomplete task
- [x] Completed task
- [ ] Task with sub-tasks
  - [ ] Subtask 1
  - [x] Subtask 2
```

## Citações

```markdown
> This is a blockquote.
> It can span multiple lines.
>
> And include multiple paragraphs.
>
> > Nested quotes work too.
```

## Código

### Código Inline

```markdown
Use `backticks` for inline code.
Use double backticks for ``code with a ` backtick inside``.
```

### Blocos de Código

````markdown
```
Plain code block
```

```javascript
// Syntax highlighted code block
function hello() {
  console.log("Hello, world!");
}
```

```python
# Python example
def greet(name):
    print(f"Hello, {name}!")
```
````

### Aninhando Blocos de Código

Use mais crases ou til para o bloco externo:

`````markdown
````markdown
Here's how to create a code block:
```js
console.log("Hello")
```
````
`````

## Tabelas

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Alinhamento

```markdown
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| Left     | Center   | Right    |
```

### Usando Pipes em Tabelas

Escape pipes com barra invertida:
```markdown
| Column 1 | Column 2 |
|----------|----------|
| [[Link\|Display]] | ![[Image\|100]] |
```

## Matemática (LaTeX)

### Matemática Inline

```markdown
This is inline math: $e^{i\pi} + 1 = 0$
```

### Matemática em Bloco

```markdown
$$
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix} = ad - bc
$$
```

### Sintaxe Comum de Matemática

```markdown
$x^2$              Superscript
$x_i$              Subscript
$\frac{a}{b}$      Fraction
$\sqrt{x}$         Square root
$\sum_{i=1}^{n}$   Summation
$\int_a^b$         Integral
$\alpha, \beta$    Greek letters
```

## Diagramas (Mermaid)

````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Do this]
    B -->|No| D[Do that]
    C --> E[End]
    D --> E
```
````

### Diagramas de Sequência

````markdown
```mermaid
sequenceDiagram
    Alice->>Bob: Hello Bob
    Bob-->>Alice: Hi Alice
```
````

### Vinculando em Diagramas

````markdown
```mermaid
graph TD
    A[Biology]
    B[Chemistry]
    A --> B
    class A,B internal-link;
```
````

## Notas de Rodapé

```markdown
This sentence has a footnote[^1].

[^1]: This is the footnote content.

You can also use named footnotes[^note].

[^note]: Named footnotes still appear as numbers.

Inline footnotes are also supported.^[This is an inline footnote.]
```

## Comentários

```markdown
This is visible %%but this is hidden%% text.

%%
This entire block is hidden.
It won't appear in reading view.
%%
```

## Linhas Horizontais

```markdown
---
***
___
- - -
* * *
```

## Properties (Frontmatter)

Properties usam frontmatter YAML no início de uma nota:

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
aliases:
  - My Note
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 4.5
completed: false
due: 2024-02-01T14:30:00
---
```

### Tipos de Property

| Tipo | Exemplo |
|------|---------|
| Texto | `title: My Title` |
| Número | `rating: 4.5` |
| Checkbox | `completed: true` |
| Data | `date: 2024-01-15` |
| Data & Hora | `due: 2024-01-15T14:30:00` |
| Lista | `tags: [one, two]` ou lista YAML |
| Links | `related: "[[Other Note]]"` |

### Properties Padrão

- `tags` - Tags da nota
- `aliases` - Nomes alternativos para a nota
- `cssclasses` - Classes CSS aplicadas à nota

## Tags

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores

In frontmatter:
---
tags:
  - tag1
  - nested/tag2
---
```

Tags podem conter:
- Letras (qualquer idioma)
- Números (não como primeiro caractere)
- Underscores `_`
- Hífens `-`
- Barras `/` (para aninhamento)

## Conteúdo HTML

O Obsidian suporta HTML dentro de Markdown:

```markdown
<div class="custom-container">
  <span style="color: red;">Colored text</span>
</div>

<details>
  <summary>Click to expand</summary>
  Hidden content here.
</details>

<kbd>Ctrl</kbd> + <kbd>C</kbd>
```

## Exemplo Completo

````markdown
---
title: Project Alpha
date: 2024-01-15
tags:
  - project
  - active
status: in-progress
priority: high
---

# Project Alpha

## Overview

This project aims to [[improve workflow]] using modern techniques.

> [!important] Key Deadline
> The first milestone is due on ==January 30th==.

## Tasks

- [x] Initial planning
- [x] Resource allocation
- [ ] Development phase
  - [ ] Backend implementation
  - [ ] Frontend design
- [ ] Testing
- [ ] Deployment

## Technical Notes

The main algorithm uses the formula $O(n \log n)$ for sorting.

```python
def process_data(items):
    return sorted(items, key=lambda x: x.priority)
```

## Architecture

```mermaid
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
    B --> D[Cache]
```

## Related Documents

- ![[Meeting Notes 2024-01-10#Decisions]]
- [[Budget Allocation|Budget]]
- [[Team Members]]

## References

For more details, see the official documentation[^1].

[^1]: https://example.com/docs

%%
Internal notes:
- Review with team on Friday
- Consider alternative approaches
%%
````

## Referências

- [Basic formatting syntax](https://help.obsidian.md/syntax)
- [Advanced formatting syntax](https://help.obsidian.md/advanced-syntax)
- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Internal links](https://help.obsidian.md/links)
- [Embed files](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)