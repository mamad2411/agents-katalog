---
name: diagrammer
description: Renderize diagramas SVG limpos em estilo blueprint a partir de specs JSON. Use quando usuários pedirem para desenhar, esboçar ou diagramar um fluxo de requisição, rede neural, bloco transformer, arquitetura de sistema, máquina de estados, pipeline de dados, ou qualquer visual técnico de nós e arestas que queiram como SVG para docs, READMEs, posts ou slides.
---

# diagrammer

Use `diagrammer` para transformar uma pequena spec JSON em um diagrama SVG limpo. É útil quando o usuário quer um diagrama técnico preciso sem abrir uma ferramenta de design.

## Instalação

O renderizador deve ser instalado localmente:

```bash
pipx install diagrammer
```

## Fluxo de trabalho

1. Converta o pedido de diagrama em linguagem natural do usuário para uma spec JSON.
2. Salve a spec em um arquivo temporário ou do projeto.
3. Renderize:

```bash
diagrammer path/to/spec.json > path/to/diagram.svg
```

4. Retorne o caminho do SVG ao usuário.

## Essenciais da Spec

```json
{
  "nodes": [
    {"id": "client", "type": "box", "label": "client"},
    {"id": "api", "type": "box", "label": "api"},
    {"id": "db", "type": "database", "label": "postgres"}
  ],
  "edges": [
    {"from": "client", "to": "api", "label": "request"},
    {"from": "api", "to": "db", "label": "query"}
  ]
}
```

Tipos de nós integrados: `box`, `circle`, `text`, `database`, `stack`, `group`, `note` e `custom`.

Campos opcionais úteis:

- `direction`: `"LR"` ou `"TB"`
- `router`: `"straight"` ou `"ortho"`
- `label` em arestas
- `style`: `"solid"` ou `"dashed"`
- `weight`: `"thin"` ou `"thick"`

Para a referência completa, execute:

```bash
diagrammer prompt
```

## Quando escolher isto

Use `diagrammer` quando a saída deve ser um artefato SVG que fica no repositório, especialmente para:

- Diagramas em README
- Esboços de arquitetura
- Fluxos de requisição
- Máquinas de estados
- Diagramas de rede neural ou transformer
- Pipelines de dados simples

Prefira Mermaid quando o usuário especificamente pedir sintaxe Mermaid ou quiser diagramas renderizados por uma plataforma Markdown. Prefira Excalidraw quando o usuário quiser arquivos de canvas editáveis com aparência desenhada à mão.