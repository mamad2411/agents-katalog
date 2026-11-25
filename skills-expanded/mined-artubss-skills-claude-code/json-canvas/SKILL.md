---
name: json-canvas
description: Crie e edite arquivos JSON Canvas (.canvas) com nós, arestas, grupos e conexões. Use ao trabalhar com arquivos .canvas, criar telas visuais, mapas mentais, fluxogramas ou quando o usuário mencionar arquivos Canvas no Obsidian.
---

# Skill JSON Canvas

Esta skill permite que o Claude Code crie e edite arquivos JSON Canvas válidos (`.canvas`) usados no Obsidian e outras aplicações.

## Visão Geral

JSON Canvas é um formato de arquivo aberto para dados de tela infinita. Arquivos Canvas usam a extensão `.canvas` e contêm JSON válido seguindo a [especificação JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/).

## Estrutura do Arquivo

Um arquivo canvas contém dois arrays no nível superior:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (opcional): Array de objetos de nó
- `edges` (opcional): Array de objetos de aresta que conectam nós

## Nós

Nós são objetos colocados na tela. Existem quatro tipos de nó:
- `text` - Conteúdo de texto com Markdown
- `file` - Referência a arquivos/anexos
- `link` - URL externa
- `group` - Contêiner visual para outros nós

### Ordenação Z-Index

Nós são ordenados por z-index no array:
- Primeiro nó = camada inferior (exibido abaixo dos outros)
- Último nó = camada superior (exibido acima dos outros)

### Atributos Genéricos de Nó

Todos os nós compartilham estes atributos:

| Atributo | Obrigatório | Tipo | Descrição |
|----------|-------------|------|-----------|
| `id` | Sim | string | Identificador único do nó |
| `type` | Sim | string | Tipo de nó: `text`, `file`, `link` ou `group` |
| `x` | Sim | integer | Posição X em pixels |
| `y` | Sim | integer | Posição Y em pixels |
| `width` | Sim | integer | Largura em pixels |
| `height` | Sim | integer | Altura em pixels |
| `color` | Não | canvasColor | Cor do nó (veja seção Cores) |

### Nós de Texto

Nós de texto contêm conteúdo Markdown.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

| Atributo | Obrigatório | Tipo | Descrição |
|----------|-------------|------|-----------|
| `text` | Sim | string | Texto simples com sintaxe Markdown |

### Nós de Arquivo

Nós de arquivo referenciam arquivos ou anexos (imagens, vídeos, PDFs, notas, etc.).

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

```json
{
  "id": "b2c3d4e5f6789012",
  "type": "file",
  "x": 500,
  "y": 400,
  "width": 400,
  "height": 300,
  "file": "Notes/Project Overview.md",
  "subpath": "#Implementation"
}
```

| Atributo | Obrigatório | Tipo | Descrição |
|----------|-------------|------|-----------|
| `file` | Sim | string | Caminho do arquivo dentro do sistema |
| `subpath` | Não | string | Link para título ou bloco (começa com `#`) |

### Nós de Link

Nós de link exibem URLs externas.

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://obsidian.md"
}
```

| Atributo | Obrigatório | Tipo | Descrição |
|----------|-------------|------|-----------|
| `url` | Sim | string | URL externa |

### Nós de Grupo

Nós de grupo são contêineres visuais para organizar outros nós.

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

```json
{
  "id": "e5f67890123456ab",
  "type": "group",
  "x": 0,
  "y": 700,
  "width": 800,
  "height": 500,
  "label": "Resources",
  "background": "Attachments/background.png",
  "backgroundStyle": "cover"
}
```

| Atributo | Obrigatório | Tipo | Descrição |
|----------|-------------|------|-----------|
| `label` | Não | string | Rótulo de texto para o grupo |
| `background` | Não | string | Caminho para imagem de fundo |
| `backgroundStyle` | Não | string | Estilo de renderização do fundo |

#### Estilos de Fundo

| Valor | Descrição |
|-------|-----------|
| `cover` | Preenche toda a largura e altura do nó |
| `ratio` | Mantém proporção de aspecto da imagem de fundo |
| `repeat` | Repete a imagem como padrão em ambas as direções |

## Arestas

Arestas são linhas que conectam nós.

```json
{
  "id": "f67890123456789a",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "a1b2c3d4e5f67890"
}
```

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "fromEnd": "none",
  "toNode": "b2c3d4e5f6789012",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "1",
  "label": "leads to"
}
```

| Atributo | Obrigatório | Tipo | Padrão | Descrição |
|----------|-------------|------|--------|-----------|
| `id` | Sim | string | - | Identificador único da aresta |
| `fromNode` | Sim | string | - | ID do nó onde a conexão começa |
| `fromSide` | Não | string | - | Lado onde a aresta começa |
| `fromEnd` | Não | string | `none` | Forma no início da aresta |
| `toNode` | Sim | string | - | ID do nó onde a conexão termina |
| `toSide` | Não | string | - | Lado onde a aresta termina |
| `toEnd` | Não | string | `arrow` | Forma no final da aresta |
| `color` | Não | canvasColor | - | Cor da linha |
| `label` | Não | string | - | Rótulo de texto para a aresta |

### Valores de Lado

| Valor | Descrição |
|-------|-----------|
| `top` | Borda superior do nó |
| `right` | Borda direita do nó |
| `bottom` | Borda inferior do nó |
| `left` | Borda esquerda do nó |

### Formas de Extremidade

| Valor | Descrição |
|-------|-----------|
| `none` | Nenhuma forma de extremidade |
| `arrow` | Extremidade em forma de seta |

## Cores

O tipo `canvasColor` pode ser especificado de duas formas:

### Cores Hexadecimais

```json
{
  "color": "#FF0000"
}
```

### Cores Predefinidas

```json
{
  "color": "1"
}
```

| Predefinida | Cor |
|------------|-----|
| `"1"` | Vermelho |
| `"2"` | Laranja |
| `"3"` | Amarelo |
| `"4"` | Verde |
| `"5"` | Ciano |
| `"6"` | Roxo |

Nota: Os valores de cor específicos para predefinidas são intencionalmente indefinidos, permitindo que aplicações usem suas próprias cores de marca.

## Exemplos Completos

### Canvas Simples com Texto e Conexões

```json
{
  "nodes": [
    {
      "id": "8a9b0c1d2e3f4a5b",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 150,
      "text": "# Main Idea\n\nThis is the central concept."
    },
    {
      "id": "1a2b3c4d5e6f7a8b",
      "type": "text",
      "x": 400,
      "y": -100,
      "width": 250,
      "height": 100,
      "text": "## Supporting Point A\n\nDetails here."
    },
    {
      "id": "2b3c4d5e6f7a8b9c",
      "type": "text",
      "x": 400,
      "y": 100,
      "width": 250,
      "height": 100,
      "text": "## Supporting Point B\n\nMore details."
    }
  ],
  "edges": [
    {
      "id": "3c4d5e6f7a8b9c0d",
      "fromNode": "8a9b0c1d2e3f4a5b",
      "fromSide": "right",
      "toNode": "1a2b3c4d5e6f7a8b",
      "toSide": "left"
    },
    {
      "id": "4d5e6f7a8b9c0d1e",
      "fromNode": "8a9b0c1d2e3f4a5b",
      "fromSide": "right",
      "toNode": "2b3c4d5e6f7a8b9c",
      "toSide": "left"
    }
  ]
}
```

### Quadro de Projeto com Grupos

```json
{
  "nodes": [
    {
      "id": "5e6f7a8b9c0d1e2f",
      "type": "group",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 500,
      "label": "To Do",
      "color": "1"
    },
    {
      "id": "6f7a8b9c0d1e2f3a",
      "type": "group",
      "x": 350,
      "y": 0,
      "width": 300,
      "height": 500,
      "label": "In Progress",
      "color": "3"
    },
    {
      "id": "7a8b9c0d1e2f3a4b",
      "type": "group",
      "x": 700,
      "y": 0,
      "width": 300,
      "height": 500,
      "label": "Done",
      "color": "4"
    },
    {
      "id": "8b9c0d1e2f3a4b5c",
      "type": "text",
      "x": 20,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 1\n\nImplement feature X"
    },
    {
      "id": "9c0d1e2f3a4b5c6d",
      "type": "text",
      "x": 370,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 2\n\nReview PR #123",
      "color": "2"
    },
    {
      "id": "0d1e2f3a4b5c6d7e",
      "type": "text",
      "x": 720,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 3\n\n~~Setup CI/CD~~"
    }
  ],
  "edges": []
}
```

### Canvas de Pesquisa com Arquivos e Links

```json
{
  "nodes": [
    {
      "id": "1e2f3a4b5c6d7e8f",
      "type": "text",
      "x": 300,
      "y": 200,
      "width": 400,
      "height": 200,
      "text": "# Research Topic\n\n## Key Questions\n\n- How does X affect Y?\n- What are the implications?",
      "color": "5"
    },
    {
      "id": "2f3a4b5c6d7e8f9a",
      "type": "file",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 150,
      "file": "Literature/Paper A.pdf"
    },
    {
      "id": "3a4b5c6d7e8f9a0b",
      "type": "file",
      "x": 0,
      "y": 200,
      "width": 250,
      "height": 150,
      "file": "Notes/Meeting Notes.md",
      "subpath": "#Key Insights"
    },
    {
      "id": "4b5c6d7e8f9a0b1c",
      "type": "link",
      "x": 0,
      "y": 400,
      "width": 250,
      "height": 100,
      "url": "https://example.com/research"
    },
    {
      "id": "5c6d7e8f9a0b1c2d",
      "type": "file",
      "x": 750,
      "y": 150,
      "width": 300,
      "height": 250,
      "file": "Attachments/diagram.png"
    }
  ],
  "edges": [
    {
      "id": "6d7e8f9a0b1c2d3e",
      "fromNode": "2f3a4b5c6d7e8f9a",
      "fromSide": "right",
      "toNode": "1e2f3a4b5c6d7e8f",
      "toSide": "left",
      "label": "supports"
    },
    {
      "id": "7e8f9a0b1c2d3e4f",
      "fromNode": "3a4b5c6d7e8f9a0b",
      "fromSide": "right",
      "toNode": "1e2f3a4b5c6d7e8f",
      "toSide": "left",
      "label": "informs"
    },
    {
      "id": "8f9a0b1c2d3e4f5a",
      "fromNode": "4b5c6d7e8f9a0b1c",
      "fromSide": "right",
      "toNode": "1e2f3a4b5c6d7e8f",
      "toSide": "left",
      "toEnd": "arrow",
      "color": "6"
    },
    {
      "id": "9a0b1c2d3e4f5a6b",
      "fromNode": "1e2f3a4b5c6d7e8f",
      "fromSide": "right",
      "toNode": "5c6d7e8f9a0b1c2d",
      "toSide": "left",
      "label": "visualized by"
    }
  ]
}
```

### Fluxograma

```json
{
  "nodes": [
    {
      "id": "a0b1c2d3e4f5a6b7",
      "type": "text",
      "x": 200,
      "y": 0,
      "width": 150,
      "height": 60,
      "text": "**Start**",
      "color": "4"
    },
    {
      "id": "b1c2d3e4f5a6b7c8",
      "type": "text",
      "x": 200,
      "y": 100,
      "width": 150,
      "height": 60,
      "text": "Step 1:\nGather data"
    },
    {
      "id": "c2d3e4f5a6b7c8d9",
      "type": "text",
      "x": 200,
      "y": 200,
      "width": 150,
      "height": 80,
      "text": "**Decision**\n\nIs data valid?",
      "color": "3"
    },
    {
      "id": "d3e4f5a6b7c8d9e0",
      "type": "text",
      "x": 400,
      "y": 200,
      "width": 150,
      "height": 60,
      "text": "Process data"
    },
    {
      "id": "e4f5a6b7c8d9e0f1",
      "type": "text",
      "x": 0,
      "y": 200,
      "width": 150,
      "height": 60,
      "text": "Request new data",
      "color": "1"
    },
    {
      "id": "f5a6b7c8d9e0f1a2",
      "type": "text",
      "x": 400,
      "y": 320,
      "width": 150,
      "height": 60,
      "text": "**End**",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "a6b7c8d9e0f1a2b3",
      "fromNode": "a0b1c2d3e4f5a6b7",
      "fromSide": "bottom",
      "toNode": "b1c2d3e4f5a6b7c8",
      "toSide": "top"
    },
    {
      "id": "b7c8d9e0f1a2b3c4",
      "fromNode": "b1c2d3e4f5a6b7c8",
      "fromSide": "bottom",
      "toNode": "c2d3e4f5a6b7c8d9",
      "toSide": "top"
    },
    {
      "id": "c8d9e0f1a2b3c4d5",
      "fromNode": "c2d3e4f5a6b7c8d9",
      "fromSide": "right",
      "toNode": "d3e4f5a6b7c8d9e0",
      "toSide": "left",
      "label": "Yes",
      "color": "4"
    },
    {
      "id": "d9e0f1a2b3c4d5e6",
      "fromNode": "c2d3e4f5a6b7c8d9",
      "fromSide": "left",
      "toNode": "e4f5a6b7c8d9e0f1",
      "toSide": "right",
      "label": "No",
      "color": "1"
    },
    {
      "id": "e0f1a2b3c4d5e6f7",
      "fromNode": "e4f5a6b7c8d9e0f1",
      "fromSide": "top",
      "fromEnd": "none",
      "toNode": "b1c2d3e4f5a6b7c8",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "f1a2b3c4d5e6f7a8",
      "fromNode": "d3e4f5a6b7c8d9e0",
      "fromSide": "bottom",
      "toNode": "f5a6b7c8d9e0f1a2",
      "toSide": "top"
    }
  ]
}
```

## Geração de IDs

IDs de nó e aresta devem ser strings únicas. O Obsidian gera IDs hexadecimais de 16 caracteres:

```json
"id": "6f0ad84f44ce9c17"
"id": "a3b2c1d0e9f8g7h6"
"id": "1234567890abcdef"
```

Este formato é uma string hex minúscula de 16 caracteres (valor aleatório de 64 bits).

## Diretrizes de Layout

### Posicionamento

- As coordenadas podem ser negativas (a tela se estende infinitamente)
- `x` aumenta para a direita
- `y` aumenta para baixo
- A posição se refere ao canto superior esquerdo do nó

### Tamanhos Recomendados

| Tipo de Nó | Largura Sugerida | Altura Sugerida |
|-----------|-----------------|-----------------|
| Texto pequeno | 200-300 | 80-150 |
| Texto médio | 300-450 | 150-300 |
| Texto grande | 400-600 | 300-500 |
| Visualização de arquivo | 300-500 | 200-400 |
| Visualização de link | 250-400 | 100-200 |
| Grupo | Varia | Varia |

### Espaçamento

- Deixe 20-50px de preenchimento dentro de grupos
- Espaçar nós 50-100px para melhor legibilidade
- Alinhar nós à grade (múltiplos de 10 ou 20) para layouts mais limpos

## Regras de Validação

1. Todos os valores `id` devem ser únicos entre nós e arestas
2. `fromNode` e `toNode` devem referenciar IDs de nó existentes
3. Campos obrigatórios devem estar presentes para cada tipo de nó
4. `type` deve ser um de: `text`, `file`, `link`, `group`
5. `backgroundStyle` deve ser um de: `cover`, `ratio`, `repeat`
6. `fromSide`, `toSide` devem ser um de: `top`, `right`, `bottom`, `left`
7. `fromEnd`, `toEnd` devem ser um de: `none`, `arrow`
8. Cores predefinidas devem ser `"1"` a `"6"` ou cor hexadecimal válida

## Referências

- [Especificação JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/)
- [GitHub JSON Canvas](https://github.com/obsidianmd/jsoncanvas)