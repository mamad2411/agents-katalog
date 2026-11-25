---
name: multiplayer
description: Princípios de desenvolvimento de jogos multiplayer. Arquitetura, rede, sincronização.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Desenvolvimento de Jogos Multiplayer

> Princípios de arquitetura de rede e sincronização.

---

## 1. Seleção de Arquitetura

### Árvore de Decisão

```
Qual tipo de multiplayer?
│
├── Competitivo / Tempo real
│   └── Servidor Dedicado (autoritário)
│
├── Cooperativo / Casual
│   └── Baseado em Host (um jogador é servidor)
│
├── Baseado em turnos
│   └── Cliente-servidor (simples)
│
└── Massivo (MMO)
    └── Servidores distribuídos
```

### Comparação

| Arquitetura | Latência | Custo | Segurança |
|--------------|---------|-------|----------|
| **Dedicada** | Baixa | Alto | Forte |
| **P2P** | Variável | Baixo | Fraca |
| **Baseada em Host** | Média | Baixo | Média |

---

## 2. Princípios de Sincronização

### Estado vs Input

| Abordagem | O que Sincronizar | Melhor Para |
|----------|-------------------|-------------|
| **Sincronização de Estado** | Estado do jogo | Simples, poucos objetos |
| **Sincronização de Input** | Inputs do jogador | Jogos de ação |
| **Híbrida** | Ambos | Maioria dos jogos |

### Compensação de Latência

| Técnica | Propósito |
|---------|-----------|
| **Previsão** | Cliente prediz servidor |
| **Interpolação** | Suaviza jogadores remotos |
| **Reconciliação** | Corrige previsões erradas |
| **Compensação de lag** | Retrocede para detecção de impacto |

---

## 3. Otimização de Rede

### Redução de Largura de Banda

| Técnica | Economia |
|---------|----------|
| **Compressão delta** | Enviar apenas mudanças |
| **Quantização** | Reduzir precisão |
| **Prioridade** | Dados importantes primeiro |
| **Área de interesse** | Apenas entidades próximas |

### Taxas de Atualização

| Tipo | Taxa |
|------|------|
| Posição | 20-60 Hz |
| Saúde | Ao mudar |
| Inventário | Ao mudar |
| Chat | Ao enviar |

---

## 4. Princípios de Segurança

### Autoridade do Servidor

```
Cliente: "Acertei o inimigo"
Servidor: Validar → o projétil realmente acertou?
          → o jogador estava em estado válido?
          → o timing era possível?
```

### Anti-Cheat

| Trapaça | Prevenção |
|---------|-----------|
| Hack de velocidade | Servidor valida movimento |
| Aimbot | Servidor valida linha de visão |
| Duplicação de item | Servidor controla inventário |
| Wall hack | Não enviar dados ocultos |

---

## 5. Matchmaking

### Considerações

| Fator | Impacto |
|-------|---------|
| **Habilidade** | Partidas justas |
| **Latência** | Conexão jogável |
| **Tempo de espera** | Paciência do jogador |
| **Tamanho do grupo** | Jogo em grupo |

---

## 6. Anti-Padrões

| ❌ Não Faça | ✅ Faça |
|----------|--------|
| Confie no cliente | Servidor é a autoridade |
| Envie tudo | Envie apenas o necessário |
| Ignore latência | Projete para 100-200ms |
| Sincronize posições exatas | Interpole/preveja |

---

> **Lembre-se:** Nunca confie no cliente. O servidor é a fonte da verdade.