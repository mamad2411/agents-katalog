---
name: 2d-games
description: Princípios de desenvolvimento de jogos 2D. Sprites, tilemaps, física, câmera.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento de Jogos 2D

> Princípios para sistemas de jogos 2D.

---

## 1. Sistemas de Sprite

### Organização de Sprite

| Componente | Propósito |
|-----------|---------|
| **Atlas** | Combinar texturas, reduzir draw calls |
| **Animation** | Sequências de frames |
| **Pivot** | Origem de rotação/escala |
| **Layering** | Controle de Z-order |

### Princípios de Animação

- Frame rate: 8-24 FPS típico
- Squash and stretch para impacto
- Antecipação antes da ação
- Follow-through após a ação

---

## 2. Design de Tilemap

### Considerações de Tile

| Fator | Recomendação |
|-------|----------------|
| **Tamanho** | 16x16, 32x32, 64x64 |
| **Auto-tiling** | Use para terreno |
| **Collision** | Formas simplificadas |

### Camadas

| Camada | Conteúdo |
|-------|---------|
| Background | Cenário não-interativo |
| Terrain | Terreno transitável |
| Props | Objetos interativos |
| Foreground | Overlay de parallax |

---

## 3. Física 2D

### Formas de Colisão

| Forma | Caso de Uso |
|-------|----------|
| Box | Objetos retangulares |
| Circle | Bolas, arredondadas |
| Capsule | Personagens |
| Polygon | Formas complexas |

### Considerações de Física

- Pixel-perfect vs baseado em física
- Timestep fixo para consistência
- Camadas para filtragem

---

## 4. Sistemas de Câmera

### Tipos de Câmera

| Tipo | Uso |
|------|-----|
| **Follow** | Rastrear jogador |
| **Look-ahead** | Antecipar movimento |
| **Multi-target** | Dois jogadores |
| **Room-based** | Metroidvania |

### Screen Shake

- Duração curta (50-200ms)
- Intensidade decrescente
- Use com moderação

---

## 5. Padrões de Gênero

### Platformer

- Coyote time (tolerância após borda)
- Jump buffering
- Altura de pulo variável

### Top-down

- Movimento 8-direcional ou livre
- Baseado em aim ou auto-aim
- Considere rotação ou não

---

## 6. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|----------|-------|
| Texturas separadas | Use atlases |
| Formas de colisão complexas | Colisão simplificada |
| Câmera tremida | Seguimento suave |
| Pixel-perfect em física | Escolha uma abordagem |

---

> **Lembre-se:** 2D é sobre clareza. Cada pixel deve comunicar.