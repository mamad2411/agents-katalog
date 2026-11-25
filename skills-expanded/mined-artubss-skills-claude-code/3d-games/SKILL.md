---
name: 3d-games
description: Princípios de desenvolvimento de jogos 3D. Renderização, shaders, física, câmeras.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento de Jogos 3D

> Princípios para sistemas de jogos 3D.

---

## 1. Pipeline de Renderização

### Etapas

```
1. Vertex Processing → Transformar geometria
2. Rasterization → Converter em pixels
3. Fragment Processing → Colorir pixels
4. Output → Para a tela
```

### Princípios de Otimização

| Técnica | Propósito |
|---------|-----------|
| **Frustum culling** | Não renderizar fora da tela |
| **Occlusion culling** | Não renderizar objetos ocultos |
| **LOD** | Menos detalhes à distância |
| **Batching** | Combinar chamadas de desenho |

---

## 2. Princípios de Shaders

### Tipos de Shader

| Tipo | Propósito |
|------|-----------|
| **Vertex** | Posição, normais |
| **Fragment/Pixel** | Cor, iluminação |
| **Compute** | Computação geral |

### Quando Escrever Shaders Personalizados

- Efeitos especiais (água, fogo, portais)
- Renderização estilizada (toon, sketch)
- Otimização de desempenho
- Identidade visual única

---

## 3. Física 3D

### Formas de Colisão

| Forma | Caso de Uso |
|-------|-------------|
| **Box** | Edifícios, caixas |
| **Sphere** | Bolas, verificações rápidas |
| **Capsule** | Personagens |
| **Mesh** | Terreno (custoso) |

### Princípios

- Colisores simples, visuais complexos
- Filtragem baseada em camadas
- Raycasting para linha de visão

---

## 4. Sistemas de Câmera

### Tipos de Câmera

| Tipo | Uso |
|------|-----|
| **Terceira pessoa** | Ação, aventura |
| **Primeira pessoa** | Imersivo, FPS |
| **Isométrica** | Estratégia, RPG |
| **Orbital** | Inspeção, editores |

### Sensação de Câmera

- Seguimento suave (lerp)
- Evitação de colisão
- Look-ahead para movimento
- Mudanças de FOV para velocidade

---

## 5. Iluminação

### Tipos de Luz

| Tipo | Uso |
|------|-----|
| **Direcional** | Sol, lua |
| **Pontual** | Lâmpadas, tochas |
| **Spot** | Lanterna, palco |
| **Ambiente** | Iluminação base |

### Consideração de Desempenho

- Sombras em tempo real são custosas
- Faça baking quando possível
- Cascatas de sombra para mundos grandes

---

## 6. Nível de Detalhe (LOD)

### Estratégia de LOD

| Distância | Modelo |
|-----------|--------|
| Próximo | Detalhe completo |
| Médio | 50% de triângulos |
| Longe | 25% ou billboard |

---

## 7. Anti-padrões

| ❌ Não Faça | ✅ Faça |
|-----------|-------|
| Mesh colliders em todos os lugares | Formas simples |
| Sombras em tempo real em mobile | Sombras baked ou blob |
| Um LOD para todas as distâncias | LOD baseado em distância |
| Shaders não otimizados | Perfil e simplifique |

---

> **Lembre-se:** 3D é sobre ilusão. Crie a impressão de detalhe, não o detalhe em si.