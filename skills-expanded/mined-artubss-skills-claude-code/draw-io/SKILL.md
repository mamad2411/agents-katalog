---
name: draw-io
description: Criação, edição e revisão de diagramas draw.io. Use para edição de XML .drawio, conversão PNG, ajuste de layout e uso de ícones AWS.
---

# Habilidade draw.io Diagram

## 1. Regras Básicas

- Edite apenas arquivos `.drawio`
- Não edite diretamente arquivos `.drawio.png`
- Use `.drawio.png` gerado automaticamente pelo hook pre-commit em slides

## 2. Configurações de Fonte

Para diagramas usados em slides Quarto,
especifique `defaultFontFamily` na tag mxGraphModel:

```xml
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
```

Especifique também explicitamente `fontFamily` no atributo style de cada elemento de texto:

```xml
style="text;html=1;fontSize=27;fontFamily=Noto Sans JP;"
```

## 3. Comandos de Conversão

Veja script de conversão em [scripts/convert-drawio-to-png.sh](scripts/convert-drawio-to-png.sh).

```sh
# Converter todos os arquivos .drawio
mise exec -- pre-commit run --all-files

# Converter arquivo .drawio específico
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# Executar script diretamente (usando o script da habilidade)
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio
```

Comando interno utilizado:

```sh
drawio -x -f png -s 2 -t -o output.drawio.png input.drawio
```

| Opção | Descrição |
|-------|-----------|
| `-x` | Modo de exportação |
| `-f png` | Formato de saída PNG |
| `-s 2` | Escala 2x (alta resolução) |
| `-t` | Fundo transparente |
| `-o` | Caminho do arquivo de saída |

## 4. Ajuste de Layout

### 4.1. Etapas de Ajuste de Coordenadas

1. Abra arquivo `.drawio` em editor de texto (formato XML puro)
2. Encontre `mxCell` do elemento a ajustar (pesquise pelo atributo `value` para o texto)
3. Ajuste as coordenadas na tag `mxGeometry`
   - `x`: Posição a partir da esquerda
   - `y`: Posição a partir do topo
   - `width`: Largura
   - `height`: Altura
4. Execute conversão e verifique

### 4.2. Cálculo de Coordenadas

- Coordenada do centro do elemento = `y + (height / 2)`
- Para alinhar múltiplos elementos, calcule e iguale as coordenadas do centro

## 5. Princípios de Design

### 5.1. Princípios Básicos

- Clareza: Crie diagramas simples e visualmente limpos
- Consistência: Unifique cores, fontes, tamanhos de ícones, espessura de linhas
- Precisão: Não sacrifique a precisão pela simplificação

### 5.2. Regras de Elementos

- Rotule todos os elementos
- Use setas para indicar direção
  (prefira 2 setas unidirecionais em vez de bidirecionais)
- Use ícones oficiais mais recentes
- Adicione legenda para explicar símbolos personalizados

### 5.3. Acessibilidade

- Garanta contraste de cor suficiente
- Use padrões além de cores

### 5.4. Divulgação Progressiva

Separe sistemas complexos em diagramas por etapas:

| Tipo de Diagrama | Propósito |
|------------------|-----------|
| Diagrama de Contexto | Visão geral do sistema de perspectiva externa |
| Diagrama de Sistema | Componentes principais e relacionamentos |
| Diagrama de Componentes | Detalhes técnicos e pontos de integração |
| Diagrama de Implantação | Configuração de infraestrutura |
| Diagrama de Fluxo de Dados | Fluxo e transformação de dados |
| Diagrama de Sequência | Interações em série temporal |

### 5.5. Metadados

Inclua título, descrição, última atualização, autor e versão nos diagramas.

## 6. Melhores Práticas

### 6.1. Cor de Fundo

- Remova `background="#ffffff"`
- Fundo transparente se adapta a vários temas

### 6.2. Tamanho da Fonte

- Use 1,5x o tamanho de fonte padrão (cerca de 18px) para legibilidade em PDF

### 6.3. Largura de Texto em Japonês

- Permita 30-40px por caractere
- Largura insuficiente causa quebras de linha indesejadas

```xml
<!-- Para texto com 10 caracteres, permita 300-400px -->
<mxGeometry x="140" y="60" width="400" height="40" />
```

### 6.4. Posicionamento de Setas

- Sempre coloque setas atrás (posicione no XML logo após o Título)
- Posicione setas para evitar sobreposição com rótulos
- Mantenha início/fim da seta a pelo menos 20px da borda inferior do rótulo

```xml
<!-- Título -->
<mxCell id="title" value="..." .../>

<!-- Setas (camada traseira) -->
<mxCell id="arrow1" style="edgeStyle=..." .../>

<!-- Outros elementos (camada frontal) -->
<mxCell id="box1" .../>
```

### 6.5. Conexão de Seta a Rótulos de Texto

Para elementos de texto, exitX/exitY não funcionam, então use coordenadas explícitas:

```xml
<!-- Bom: Coordenadas explícitas com sourcePoint/targetPoint -->
<mxCell id="arrow" style="..." edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="1279" y="500" as="sourcePoint"/>
    <mxPoint x="119" y="500" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="1279" y="560"/>
      <mxPoint x="119" y="560"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 6.6. Ajuste de Offset de edgeLabel

Ajuste o atributo offset para distanciar rótulos de seta das setas:

```xml
<!-- Colocar acima da seta (valor negativo para distanciar) -->
<mxPoint x="0" y="-40" as="offset"/>

<!-- Colocar abaixo da seta (valor positivo para distanciar) -->
<mxPoint x="0" y="40" as="offset"/>
```

### 6.7. Remover Elementos Desnecessários

- Remova ícones decorativos irrelevantes para o contexto
- Exemplo: Se ECR existe, ícone Docker separado é desnecessário

### 6.8. Rótulos e Títulos

- Nome do serviço apenas: 1 linha
- Nome do serviço + informação complementar: 2 linhas com quebra de linha
- Notação redundante (ex: ECR Container Registry): encurte para 1 linha
- Use tag `&lt;br&gt;` para quebras de linha

### 6.9. Frame de Fundo e Posicionamento de Elementos Internos

Ao colocar elementos dentro de frames de fundo (caixas de agrupamento),
garanta margem suficiente.

- OBRIGATÓRIO: Elementos internos devem ter pelo menos 30px de margem da borda do frame
- OBRIGATÓRIO: Considere cantos arredondados (`rounded=1`) e largura do traço
- OBRIGATÓRIO: Sempre verifique visualmente a saída PNG para overflow

Verificação de cálculo de coordenadas:

```text
Frame de fundo: y=20, height=400 -> intervalo é y=20-420
Topo do elemento interno: frame y + 30 ou mais (ex: y=50)
Base do elemento interno: frame y + height - 30 ou menos (ex: até y=390)
```

Exemplo ruim (pode ter overflow):

```xml
<!-- Frame de fundo -->
<mxCell id="bg" style="rounded=1;strokeWidth=3;...">
  <mxGeometry x="500" y="20" width="560" height="400" />
</mxCell>
<!-- Texto: y=30 é muito próximo do topo do frame (y=20) -->
<mxCell id="label" value="Title" style="text;...">
  <mxGeometry x="510" y="30" width="540" height="35" />
</mxCell>
```

Exemplo bom (margem suficiente):

```xml
<!-- Frame de fundo -->
<mxCell id="bg" style="rounded=1;strokeWidth=3;...">
  <mxGeometry x="500" y="20" width="560" height="430" />
</mxCell>
<!-- Texto: y=50 está 30px do topo do frame (y=20) -->
<mxCell id="label" value="Title" style="text;...">
  <mxGeometry x="510" y="50" width="540" height="35" />
</mxCell>
```

## 7. Referência

- [Diretrizes de Layout](references/layout-guidelines.md)
- [Ícones AWS](references/aws-icons.md)
- [Script de Busca de Ícones AWS](scripts/find_aws_icon.py)

Exemplos de busca de ícones AWS:

```sh
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py ec2
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py lambda
```

## 8. Checklist

- [ ] Nenhuma cor de fundo definida (page="0")
- [ ] Tamanho de fonte apropriado (maior recomendado)
- [ ] Setas posicionadas na camada traseira
- [ ] Setas não sobrepondo rótulos (verificar no PNG)
- [ ] Início/fim da seta suficientemente distante dos rótulos (pelo menos 20px)
- [ ] Setas não penetrando caixas ou ícones (verificar no PNG)
- [ ] Elementos internos não extravasando frame de fundo (verificar no PNG)
- [ ] Margem de 30px+ entre frame de fundo e elementos internos
- [ ] Nomes de serviços AWS são nomes oficiais/abreviações corretas
- [ ] Ícones AWS são versão mais recente (mxgraph.aws4.*)
- [ ] Nenhum elemento desnecessário restante
- [ ] Conversão PNG verificada visualmente

## 9. Exibição de Imagem em Slides reveal.js

Adicione `auto-stretch: false` ao cabeçalho YAML:

```yaml
---
title: "Sua Apresentação"
format:
  revealjs:
    auto-stretch: false
---
```

Isso garante exibição correta de imagem em dispositivos móveis.