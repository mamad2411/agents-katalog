---
name: mobile-games
description: Princípios de desenvolvimento de jogos mobile. Entrada por toque, bateria, performance, app stores.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Desenvolvimento de Jogos Mobile

> Restrições de plataforma e princípios de otimização.

---

## 1. Considerações de Plataforma

### Restrições Principais

| Restrição | Estratégia |
|------------|----------|
| **Entrada por toque** | Áreas de contato grandes, gestos |
| **Bateria** | Limitar uso de CPU/GPU |
| **Térmica** | Estrangular quando quente |
| **Tamanho de tela** | UI responsiva |
| **Interrupções** | Pausar em background |

---

## 2. Princípios de Entrada por Toque

### Toque vs Controlador

| Toque | Desktop/Console |
|-------|-----------------|
| Impreciso | Preciso |
| Oclude a tela | Sem oclusão |
| Botões limitados | Muitos botões |
| Gestos disponíveis | Botões/sticks |

### Melhores Práticas

- Alvo de toque mínimo: 44x44 pontos
- Feedback visual ao tocar
- Evitar requisitos de tempo preciso
- Suportar retrato e paisagem

---

## 3. Metas de Performance

### Gerenciamento Térmico

| Ação | Disparador |
|--------|---------|
| Reduzir qualidade | Dispositivo morno |
| Limitar FPS | Dispositivo quente |
| Pausar efeitos | Temperatura crítica |

### Otimização de Bateria

- 30 FPS frequentemente suficiente
- Dormir quando pausado
- Minimizar GPS/rede
- Modo escuro economiza bateria OLED

---

## 4. Requisitos da App Store

### iOS (App Store)

| Requisito | Nota |
|-------------|------|
| Rótulos de privacidade | Obrigatório |
| Exclusão de conta | Se existe criação de conta |
| Screenshots | Para todos os tamanhos de dispositivo |

### Android (Google Play)

| Requisito | Nota |
|-------------|------|
| Target API | SDK do ano atual |
| 64-bit | Obrigatório |
| App bundles | Recomendado |

---

## 5. Modelos de Monetização

| Modelo | Ideal Para |
|-------|----------|
| **Premium** | Jogos de qualidade, audiência fiel |
| **Free + IAP** | Casual, baseado em progressão |
| **Anúncios** | Hyper-casual, alto volume |
| **Subscription** | Atualizações de conteúdo, multiplayer |

---

## 6. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|----------|-------|
| Controles desktop em mobile | Design para toque |
| Ignorar drenagem de bateria | Monitorar térmica |
| Forçar paisagem | Suportar preferência do jogador |
| Rede sempre ligada | Cache e sincronização |

---

> **Lembre-se:** Mobile é a plataforma mais restrita. Respeite bateria e atenção.