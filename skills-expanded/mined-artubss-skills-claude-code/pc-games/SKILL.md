---
name: pc-games
description: Princípios de desenvolvimento de jogos para PC e console. Seleção de engine, recursos específicos de plataforma, estratégias de otimização.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento de Jogos para PC/Console

> Seleção de engine e princípios específicos de plataforma.

---

## 1. Seleção de Engine

### Árvore de Decisão

```
O que você está desenvolvendo?
│
├── Jogo 2D
│   ├── Open source importante? → Godot
│   └── Grande equipe/assets? → Unity
│
├── Jogo 3D
│   ├── Qualidade visual AAA? → Unreal
│   ├── Prioridade multiplataforma? → Unity
│   └── Indie/open source? → Godot 4
│
└── Necessidades Específicas
    ├── Performance DOTS? → Unity
    ├── Nanite/Lumen? → Unreal
    └── Leve? → Godot
```

### Comparação

| Fator | Unity 6 | Godot 4 | Unreal 5 |
|-------|---------|---------|----------|
| 2D | Bom | Excelente | Limitado |
| 3D | Bom | Bom | Excelente |
| Curva de Aprendizado | Média | Fácil | Difícil |
| Custo | Divisão de receita | Gratuito | 5% após $1M |
| Equipe | Qualquer | Solo-Média | Média-Grande |

---

## 2. Recursos de Plataforma

### Integração Steam

| Recurso | Propósito |
|---------|-----------|
| Achievements | Objetivos do jogador |
| Cloud Saves | Progresso entre dispositivos |
| Leaderboards | Competição |
| Workshop | Mods de usuários |
| Rich Presence | Mostrar status no jogo |

### Requisitos de Console

| Plataforma | Certificação |
|------------|--------------|
| PlayStation | Conformidade TRC |
| Xbox | Conformidade XR |
| Nintendo | Lotcheck |

---

## 3. Suporte a Controle

### Abstração de Entrada

```
Mapeie AÇÕES, não botões:
- "confirmar" → A (Xbox), Cross (PS), B (Nintendo)
- "cancelar" → B (Xbox), Circle (PS), A (Nintendo)
```

### Feedback Háptico

| Intensidade | Uso |
|-------------|-----|
| Leve | Feedback de UI |
| Média | Impactos |
| Forte | Eventos principais |

---

## 4. Otimização de Performance

### Profiling em Primeiro Lugar

| Engine | Ferramenta |
|--------|-----------|
| Unity | Janela Profiler |
| Godot | Debugger → Profiler |
| Unreal | Unreal Insights |

### Gargalos Comuns

| Gargalo | Solução |
|---------|---------|
| Draw calls | Batching, atlases |
| Picos de GC | Object pooling |
| Física | Colisores mais simples |
| Shaders | LOD shaders |

---

## 5. Princípios Específicos de Engine

### Unity 6

- DOTS para sistemas críticos de performance
- Compilador Burst para caminhos críticos
- Addressables para streaming de assets

### Godot 4

- GDScript para iteração rápida
- C# para lógica complexa
- Signals para desacoplamento

### Unreal 5

- Blueprint para designers
- C++ para performance
- Nanite para ambientes de alta complexidade poligonal
- Lumen para iluminação dinâmica

---

## 6. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|------------|--------|
| Escolha engine por hype | Escolha pelas necessidades do projeto |
| Ignore diretrizes de plataforma | Estude requisitos de certificação |
| Hardcode botões de entrada | Abstraia para ações |
| Pule profiling | Profile desde cedo e frequentemente |

---

> **Lembre-se:** Engine é uma ferramenta. Domine os princípios, depois adapte-se a qualquer engine.