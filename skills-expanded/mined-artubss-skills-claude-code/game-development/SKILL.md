---
name: game-development
description: Orquestrador de desenvolvimento de jogos. Roteia para skills especializadas por plataforma com base nas necessidades do projeto.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Desenvolvimento de Jogos

> **Skill orquestrador** que fornece princípios fundamentais e roteia para sub-skills especializadas.

---

## Quando Usar Esta Skill

Você está trabalhando em um projeto de desenvolvimento de jogos. Esta skill ensina os PRINCÍPIOS de desenvolvimento de jogos e o direciona para a sub-skill correta com base no contexto.

---

## Roteamento de Sub-Skills

### Seleção de Plataforma

| Se o jogo é direcionado para... | Use a Sub-Skill |
|----------------------------------|-----------------|
| Navegadores web (HTML5, WebGL) | `game-development/web-games` |
| Mobile (iOS, Android) | `game-development/mobile-games` |
| PC (Steam, Desktop) | `game-development/pc-games` |
| Headsets VR/AR | `game-development/vr-ar` |

### Seleção de Dimensão

| Se o jogo é... | Use a Sub-Skill |
|----------------|-----------------|
| 2D (sprites, tilemaps) | `game-development/2d-games` |
| 3D (meshes, shaders) | `game-development/3d-games` |

### Áreas de Especialidade

| Se você precisa de... | Use a Sub-Skill |
|----------------------|-----------------|
| GDD, balanceamento, psicologia do jogador | `game-development/game-design` |
| Multiplayer, networking | `game-development/multiplayer` |
| Estilo visual, pipeline de assets, animação | `game-development/game-art` |
| Design sonoro, música, áudio adaptativo | `game-development/game-audio` |

---

## Princípios Fundamentais (Todas as Plataformas)

### 1. O Game Loop

Todo jogo, independentemente da plataforma, segue este padrão:

```
INPUT  → Lê ações do jogador
UPDATE → Processa lógica do jogo (timestep fixo)
RENDER → Desenha o frame (interpolado)
```

**Regra do Timestep Fixo:**
- Física/lógica: Taxa fixa (ex: 50Hz)
- Renderização: O mais rápido possível
- Interpole entre estados para visuais suaves

---

### 2. Matriz de Seleção de Padrões

| Padrão | Use Quando | Exemplo |
|--------|-----------|---------|
| **State Machine** | 3-5 estados discretos | Jogador: Parado→Andando→Pulando |
| **Object Pooling** | Spawn/destroy frequentes | Balas, partículas |
| **Observer/Events** | Comunicação entre sistemas | Saúde→Atualizações de UI |
| **ECS** | Milhares de entidades similares | Unidades RTS, partículas |
| **Command** | Desfazer, replay, networking | Gravação de entrada |
| **Behavior Tree** | Decisões de IA complexas | IA do inimigo |

**Regra de Decisão:** Comece com State Machine. Adicione ECS apenas quando performance exigir.

---

### 3. Abstração de Entrada

Abstraia entrada em AÇÕES, não teclas brutas:

```
"jump"  → Space, Gamepad A, Toque na tela
"move"  → WASD, Left stick, Joystick virtual
```

**Por quê:** Habilita controles multi-plataforma e reconfigurável.

---

### 4. Orçamento de Performance (60 FPS = 16,67ms)

| Sistema | Orçamento |
|---------|-----------|
| Entrada | 1ms |
| Física | 3ms |
| IA | 2ms |
| Lógica do Jogo | 4ms |
| Renderização | 5ms |
| Buffer | 1,67ms |

**Prioridade de Otimização:**
1. Algoritmo (O(n²) → O(n log n))
2. Batching (reduz draw calls)
3. Pooling (evita picos de GC)
4. LOD (detalhe por distância)
5. Culling (pula invisíveis)

---

### 5. Seleção de IA por Complexidade

| Tipo de IA | Complexidade | Use Quando |
|-----------|-------------|-----------|
| **FSM** | Simples | 3-5 estados, comportamento previsível |
| **Behavior Tree** | Média | Modular, amigável para designer |
| **GOAP** | Alta | Emergente, baseada em planejamento |
| **Utility AI** | Alta | Decisões baseadas em pontuação |

---

### 6. Estratégia de Colisão

| Tipo | Melhor Para |
|------|------------|
| **AABB** | Retângulos, verificações rápidas |
| **Circle** | Objetos redondos, cálculo barato |
| **Spatial Hash** | Muitos objetos de tamanho similar |
| **Quadtree** | Mundos grandes, tamanhos variados |

---

## Anti-Padrões (Universal)

| Não faça | Faça |
|----------|------|
| Atualize tudo a cada frame | Use eventos, dirty flags |
| Crie objetos em loops quentes | Object pooling |
| Cache nada | Cache referências |
| Otimize sem fazer profile | Profile primeiro |
| Misture entrada com lógica | Camada de abstração de entrada |

---

## Exemplos de Roteamento

### Exemplo 1: "Quero fazer um platformer 2D em navegador"
→ Comece com `game-development/web-games` para seleção de framework
→ Depois `game-development/2d-games` para padrões de sprite/tilemap
→ Consulte `game-development/game-design` para design de níveis

### Exemplo 2: "Jogo de puzzle mobile para iOS e Android"
→ Comece com `game-development/mobile-games` para entrada por toque e lojas
→ Use `game-development/game-design` para balanceamento de puzzle

### Exemplo 3: "Shooter VR multiplayer"
→ `game-development/vr-ar` para conforto e imersão
→ `game-development/3d-games` para renderização
→ `game-development/multiplayer` para networking

---

> **Lembre-se:** Ótimos jogos vêm da iteração, não da perfeição. Prototype rápido, depois refine.