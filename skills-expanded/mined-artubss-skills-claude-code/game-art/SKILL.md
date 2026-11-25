---
name: game-art
description: Princípios de arte para games. Seleção de estilo visual, pipeline de assets, workflow de animação.
allowed-tools: Read, Glob, Grep
---

# Princípios de Arte para Games

> Pensamento em design visual para games - seleção de estilo, pipelines de assets e direção de arte.

---

## 1. Seleção de Estilo de Arte

### Árvore de Decisão

```
Que sensação o game deve evocar?
│
├── Nostálgica / Retrô
│   ├── Paleta limitada? → Pixel Art
│   └── Aspecto desenhado à mão? → Estilo Vector / Flash
│
├── Realista / Imersiva
│   ├── Orçamento alto? → PBR 3D
│   └── Realismo estilizado? → Texturas pintadas à mão
│
├── Acessível / Casual
│   ├── Formas limpas? → Flat / Minimalista
│   └── Aspecto suave? → Gradiente / Sombras suaves
│
└── Única / Experimental
    └── Definir guia de estilo customizado
```

### Matriz de Comparação de Estilos

| Estilo | Velocidade de Produção | Curva de Aprendizado | Escalabilidade | Melhor para |
|--------|------------------------|----------------------|-----------------|-------------|
| **Pixel Art** | Média | Média | Difícil de contratar | Indie, retrô |
| **Vector/Flat** | Rápida | Baixa | Fácil | Mobile, casual |
| **Pintada à mão** | Lenta | Alta | Média | Fantasia, estilizado |
| **PBR 3D** | Lenta | Alta | Pipeline AAA | Games realistas |
| **Low-poly** | Rápida | Média | Fácil | Indie 3D |
| **Cel-shaded** | Média | Média | Média | Anime, cartoon |

---

## 2. Decisões de Pipeline de Assets

### Pipeline 2D

| Fase | Opções de Ferramentas | Output |
|------|----------------------|--------|
| **Conceito** | Papel, Procreate, Photoshop | Reference sheet |
| **Criação** | Aseprite, Photoshop, Krita | Sprites individuais |
| **Atlas** | TexturePacker, Aseprite | Spritesheet |
| **Animação** | Spine, DragonBones, Frame-by-frame | Dados de animação |
| **Integração** | Engine import | Assets prontos para o game |

### Pipeline 3D

| Fase | Opções de Ferramentas | Output |
|------|----------------------|--------|
| **Conceito** | Arte 2D, Blockout | Referência |
| **Modelagem** | Blender, Maya, 3ds Max | Mesh high-poly |
| **Retopologia** | Blender, ZBrush | Mesh pronta para o game |
| **UV/Texturização** | Substance Painter, Blender | Mapas de textura |
| **Rigging** | Blender, Maya | Esqueleto articulado |
| **Animação** | Blender, Maya, Mixamo | Clipes de animação |
| **Export** | FBX, glTF | Pronto para engine |

---

## 3. Decisões de Teoria das Cores

### Seleção de Paleta

| Objetivo | Estratégia | Exemplo |
|----------|-----------|---------|
| **Harmonia** | Complementar ou análoga | Games de natureza |
| **Contraste** | Diferenças de saturação alta | Games de ação |
| **Atmosfera** | Temperatura quente/fria | Horror, aconchego |
| **Legibilidade** | Contraste de valor sobre matiz | Clareza de gameplay |

### Princípios de Cor

- **Hierarquia:** Elementos importantes devem se destacar
- **Consistência:** Mesmo objeto = mesma família de cores
- **Contexto:** Cores se leem diferente em fundos diferentes
- **Acessibilidade:** Não dependa apenas de cor

---

## 4. Princípios de Animação

### Os 12 Princípios (Aplicados a Games)

| Princípio | Aplicação em Games |
|-----------|-------------------|
| **Squash & Stretch** | Arcos de pulo, impactos |
| **Antecipação** | Preparação antes do ataque |
| **Staging** | Silhuetas claras |
| **Follow-through** | Cabelo, capas após movimento |
| **Slow in/out** | Easing em transições |
| **Arcs** | Caminhos de movimento naturais |
| **Secondary Action** | Respiração, piscadas |
| **Timing** | Contagem de frames = peso/velocidade |
| **Exageração** | Legível à distância |
| **Appeal** | Design memorável |

### Diretrizes de Contagem de Frames

| Tipo de Ação | Frames Típicos | Sensação |
|-------------|----------------|----------|
| Respiração idle | 4-8 | Sutil |
| Ciclo de caminhada | 6-12 | Suave |
| Ciclo de corrida | 4-8 | Energético |
| Ataque | 3-6 | Rápido |
| Morte | 8-16 | Dramático |

---

## 5. Decisões de Resolução e Escala

### Resolução 2D por Plataforma

| Plataforma | Resolução Base | Escala de Sprite |
|-----------|----------------|-----------------|
| Mobile | 1080p | Personagens de 64-128px |
| Desktop | 1080p-4K | Personagens de 128-256px |
| Pixel art | 320x180 até 640x360 | Personagens de 16-32px |

### Regra de Consistência

Escolha uma unidade base e mantenha-a:
- Pixel art: Trabalhe em 1x, escale para cima (nunca para baixo)
- Arte HD: Defina DPI, mantenha a proporção
- 3D: 1 unidade = 1 metro (padrão da indústria)

---

## 6. Organização de Assets

### Convenção de Nomes

```
[tipo]_[objeto]_[variante]_[estado].[ext]

Exemplos:
spr_player_idle_01.png
tex_stone_wall_normal.png
mesh_tree_oak_lod2.fbx
```

### Princípio de Estrutura de Pastas

```
assets/
├── characters/
│   ├── player/
│   └── enemies/
├── environment/
│   ├── props/
│   └── tiles/
├── ui/
├── effects/
└── audio/
```

---

## 7. Anti-Padrões

| Não faça | Faça |
|----------|------|
| Misture estilos de arte aleatoriamente | Defina e siga guia de estilo |
| Trabalhe apenas em resolução final | Crie em resolução de origem |
| Ignore legibilidade de silhueta | Teste à distância de gameplay |
| Sobre-detalhe o fundo | Concentre detalhe na área do jogador |
| Pule testes de cor | Teste em display de destino |

---

> **Lembre-se:** Arte serve ao gameplay. Se não ajuda o jogador, é apenas decoração.