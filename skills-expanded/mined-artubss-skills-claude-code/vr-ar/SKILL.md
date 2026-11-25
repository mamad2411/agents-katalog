---
name: vr-ar
description: Princípios de desenvolvimento em VR/AR. Conforto, interação, requisitos de performance.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento VR/AR

> Princípios de experiências imersivas.

---

## 1. Seleção de Plataforma

### Plataformas VR

| Plataforma | Caso de Uso |
|----------|----------|
| **Quest** | Standalone, wireless |
| **PCVR** | Alta fidelidade |
| **PSVR** | Mercado console |
| **WebXR** | Baseado em navegador |

### Plataformas AR

| Plataforma | Caso de Uso |
|----------|----------|
| **ARKit** | Dispositivos iOS |
| **ARCore** | Dispositivos Android |
| **WebXR** | AR em navegador |
| **HoloLens** | Enterprise |

---

## 2. Princípios de Conforto

### Prevenção de Cinetose

| Causa | Solução |
|-------|----------|
| **Locomoção** | Teletransporte, snap turn |
| **FPS baixo** | Manter 90 FPS |
| **Tremor de câmera** | Evitar ou minimizar |
| **Aceleração rápida** | Movimento gradual |

### Configurações de Conforto

- Vignette durante movimento
- Snap vs turning suave
- Modos sentado vs em pé
- Calibração de altura

---

## 3. Requisitos de Performance

### Métricas Alvo

| Plataforma | FPS | Resolução |
|----------|-----|------------|
| Quest 2 | 72-90 | 1832x1920 |
| Quest 3 | 90-120 | 2064x2208 |
| PCVR | 90 | 2160x2160+ |
| PSVR2 | 90-120 | 2000x2040 |

### Orçamento de Frame

- VR requer tempos de frame consistentes
- Um frame perdido = judder visível
- 90 FPS = orçamento de 11,11ms

---

## 4. Princípios de Interação

### Interação com Controle

| Tipo | Uso |
|------|-----|
| **Apontar + clicar** | UI, objetos distantes |
| **Pegar** | Manipulação |
| **Gesto** | Magia, ações especiais |
| **Física** | Lançar, balançar |

### Hand Tracking

- Mais imersivo mas menos preciso
- Bom para: social, casual
- Desafiador para: ação, precisão

---

## 5. Design Espacial

### Escala do Mundo

- 1 unidade = 1 metro (crítico)
- Objetos devem ter o tamanho certo
- Teste com medidas reais

### Pistas de Profundidade

| Pista | Importância |
|-----|------------|
| Estéreo | Profundidade primária |
| Parallax de movimento | Secundária |
| Sombras | Ancoragem |
| Oclusão | Camadas |

---

## 6. Anti-padrões

| ❌ Não faça | ✅ Faça |
|----------|-------|
| Mover câmera sem o jogador | Jogador controla câmera |
| Cair abaixo de 90 FPS | Manter taxa de frames |
| Usar texto de UI minúsculo | Texto grande e legível |
| Ignorar comprimento do braço | Escalar para alcance do jogador |

---

> **Lembre-se:** Conforto não é opcional. Jogadores enjoados não jogam.