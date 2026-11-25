---
name: web-games
description: Princípios de desenvolvimento de games para navegador web. Seleção de framework, WebGPU, otimização, PWA.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento de Games para Navegador Web

> Seleção de framework e princípios específicos do navegador.

---

## 1. Seleção de Framework

### Árvore de Decisão

```
Que tipo de game?
│
├── Game 2D
│   ├── Recursos de engine completo? → Phaser
│   └── Poder bruto de rendering? → PixiJS
│
├── Game 3D
│   ├── Engine completo (física, XR)? → Babylon.js
│   └── Focado em rendering? → Three.js
│
└── Híbrido / Canvas
    └── Customizado → Raw Canvas/WebGL
```

### Comparação (2025)

| Framework | Tipo | Melhor para |
|-----------|------|----------|
| **Phaser 4** | 2D | Recursos completos de game |
| **PixiJS 8** | 2D | Rendering, UI |
| **Three.js** | 3D | Visualizações, leve |
| **Babylon.js 7** | 3D | Engine completo, XR |

---

## 2. Adoção WebGPU

### Suporte em Navegadores (2025)

| Navegador | Suporte |
|---------|---------|
| Chrome | ✅ Desde v113 |
| Edge | ✅ Desde v113 |
| Firefox | ✅ Desde v131 |
| Safari | ✅ Desde 18.0 |
| **Total** | **~73%** global |

### Decisão

- **Novos projetos**: Use WebGPU com fallback WebGL
- **Suporte legado**: Comece com WebGL
- **Detecção de recursos**: Verifique `navigator.gpu`

---

## 3. Princípios de Performance

### Restrições do Navegador

| Restrição | Estratégia |
|------------|----------|
| Sem acesso a arquivos locais | Asset bundling, CDN |
| Throttling em abas | Pause quando oculto |
| Limites de dados móvel | Comprima assets |
| Autoplay de áudio | Requer interação do usuário |

### Prioridade de Otimização

1. **Compressão de assets** - KTX2, Draco, WebP
2. **Lazy loading** - Carregue sob demanda
3. **Object pooling** - Evite GC
4. **Batching de draw calls** - Reduza mudanças de estado
5. **Web Workers** - Offload de computação pesada

---

## 4. Estratégia de Assets

### Formatos de Compressão

| Tipo | Formato |
|------|--------|
| Texturas | KTX2 + Basis Universal |
| Áudio | WebM/Opus (fallback: MP3) |
| Modelos 3D | glTF + Draco/Meshopt |

### Estratégia de Carregamento

| Fase | Carregue |
|-------|------|
| Inicialização | Assets principais, <2MB |
| Gameplay | Stream sob demanda |
| Background | Prefetch do próximo nível |

---

## 5. PWA para Games

### Benefícios

- Jogo offline
- Instalar na tela inicial
- Modo tela cheia
- Notificações push

### Requisitos

- Service worker para caching
- Web app manifest
- HTTPS

---

## 6. Manipulação de Áudio

### Requisitos do Navegador

- Audio context requer interação do usuário
- Crie AudioContext no primeiro clique/toque
- Retome context se suspenso

### Melhores Práticas

- Use Web Audio API
- Pool de fontes de áudio
- Pré-carregue sons comuns
- Comprima com WebM/Opus

---

## 7. Anti-Patterns

| ❌ Não faça | ✅ Faça |
|----------|-------|
| Carregue todos os assets antecipadamente | Carregamento progressivo |
| Ignore visibilidade da aba | Pause quando oculto |
| Bloqueie no carregamento de áudio | Lazy load de áudio |
| Pule compressão | Comprima tudo |
| Assuma conexão rápida | Lide com redes lentas |

---

> **Lembre-se:** Navegador é a plataforma mais acessível. Respeite suas restrições.