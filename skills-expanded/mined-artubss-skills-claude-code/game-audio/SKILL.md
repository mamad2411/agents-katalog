---
name: game-audio
description: Princípios de áudio em jogos. Design de som, integração de música, sistemas de áudio adaptativo.
allowed-tools: Read, Glob, Grep
---

# Princípios de Áudio em Jogos

> Design de som e integração de música para experiências imersivas em jogos.

---

## 1. Sistema de Categorias de Áudio

### Definições de Categorias

| Categoria | Comportamento | Exemplos |
|----------|----------|----------|
| **Música** | Loop, crossfade, ducking | BGM, música de combate |
| **SFX** | One-shot, posicionado em 3D | Passos, impactos |
| **Ambiente** | Loop, camada de fundo | Vento, multidão, floresta |
| **UI** | Imediato, não-3D | Cliques de botão, notificações |
| **Voz** | Prioridade, trigger de ducking | Diálogos, narrador |

### Hierarquia de Prioridade

```
Quando sons competem por canais:

1. Voz (maior - sempre audível)
2. SFX do jogador (feedback crítico)
3. SFX de inimigos (importante para gameplay)
4. Música (mood, mas duckável)
5. Ambiente (menor - pode ser dropado)
```

---

## 2. Decisões de Design de Som

### Abordagem de Criação de SFX

| Abordagem | Quando Usar | Trade-offs |
|----------|-------------|------------|
| **Gravação** | Realismo necessário | Alta qualidade, intensivo em tempo |
| **Síntese** | Sci-fi, retrô, UI | Único, requer habilidade |
| **Amostras de biblioteca** | Produção rápida | Sons comuns, licenciamento |
| **Layering** | Sons complexos | Melhores resultados, mais trabalho |

### Estrutura de Layering

| Camada | Propósito | Exemplo: Tiro |
|-------|---------|------------------|
| **Attack** | Transiente inicial | Click, snap |
| **Body** | Caráter principal | Boom, blast |
| **Tail** | Decay, ambiente | Reverb, eco |
| **Sweetener** | Toque especial | Casca do cartucho, mecânico |

---

## 3. Integração de Música

### Sistema de Estados de Música

```
Estado do Jogo → Resposta de Música
│
├── Menu → Tema calmo, loopável
├── Exploração → Atmosférico, ambiental
├── Combate detectado → Transição para tensão
├── Combate ativo → Música de batalha completa
├── Vitória → Stinger + transição calma
├── Derrota → Stinger sombrio
└── Boss → Track única, multi-fase
```

### Técnicas de Transição

| Técnica | Usar Quando | Sensação |
|-----------|----------|------|
| **Crossfade** | Mudança de mood suave | Gradual |
| **Stinger** | Evento imediato | Dramático |
| **Stem mixing** | Intensidade dinâmica | Sem emendas |
| **Beat-synced** | Gameplay rítmico | Musical |
| **Queue point** | Próxima pausa natural | Limpo |

---

## 4. Decisões de Áudio Adaptativo

### Parâmetros de Intensidade

| Parâmetro | Afeta | Exemplo |
|-----------|---------|---------|
| **Nível de ameaça** | Intensidade da música | Contagem de inimigos |
| **Vida** | Filter, reverb | Vida baixa = abafado |
| **Velocidade** | Tempo, energia | Velocidade de corrida |
| **Ambiente** | Reverb, EQ | Caverna vs exterior |
| **Hora do dia** | Mood, volume | Noite = mais quieto |

### Vertical vs Horizontal

| Sistema | O que Muda | Melhor Para |
|--------|--------------|----------|
| **Vertical (camadas)** | Adiciona/remove camadas de instrumentos | Escala de intensidade |
| **Horizontal (segmentos)** | Diferentes seções de música | Mudanças de estado |
| **Combinado** | Ambos | Trilhas sonoras adaptativas AAA |

---

## 5. Decisões de Áudio 3D

### Espacialização

| Elemento | Posicionado em 3D? | Motivo |
|---------|----------------|--------|
| Passos do jogador | Não (ou sutil) | Sempre audível |
| Passos do inimigo | Sim | Consciência direcional |
| Gunfire | Sim | Consciência de combate |
| Música | Não | Mood, não-diegética |
| Zona de ambiente | Sim (área) | Ambiental |
| Sons de UI | Não | Feedback de interface |

### Comportamento por Distância

| Distância | Comportamento do Som |
|----------|----------------|
| **Próximo** | Volume total, frequência completa |
| **Médio** | Falloff de volume, rolloff de alta frequência |
| **Distante** | Baixo volume, filtro passa-baixa |
| **Máximo** | Silencioso ou sugestão ambiental |

---

## 6. Considerações de Plataforma

### Seleção de Formato

| Plataforma | Formato Recomendado | Motivo |
|----------|-------------------|--------|
| PC | OGG Vorbis, WAV | Qualidade, sem licença |
| Console | Específico da plataforma | Certificação |
| Mobile | MP3, AAC | Tamanho, compatibilidade |
| Web | WebM/Opus, fallback MP3 | Suporte de navegador |

### Orçamento de Memória

| Tipo de Jogo | Orçamento de Áudio | Estratégia |
|-----------|--------------|----------|
| Mobile casual | 10-50 MB | Comprimido, menos variantes |
| PC indie | 100-500 MB | Foco em qualidade |
| AAA | 1+ GB | Qualidade total, muitas variantes |

---

## 7. Hierarquia de Mix

### Referência de Equilíbrio de Volume

| Categoria | Nível Relativo | Notas |
|----------|----------------|-------|
| **Voz** | 0 dB (referência) | Sempre clara |
| **SFX do Jogador** | -3 a -6 dB | Proeminente mas não agressivo |
| **Música** | -6 a -12 dB | Fundação, faz ducking para voz |
| **SFX de Inimigos** | -6 a -9 dB | Importante mas não dominante |
| **Ambiente** | -12 a -18 dB | Fundo sutil |

### Regras de Ducking

| Quando | Fazer Ducking De | Quantidade |
|------|-----------|--------|
| Voz toca | Música, Ambiente | -6 a -9 dB |
| Explosão | Tudo exceto explosão | Duck breve |
| Menu abre | Áudio de gameplay | -3 a -6 dB |

---

## 8. Anti-padrões

| Não Faça | Faça |
|-------|-----|
| Toque o mesmo som repetidamente | Use variações (3-5 por som) |
| Volume máximo em tudo | Use hierarquia de mix apropriada |
| Ignore o silêncio | Silêncio cria contraste |
| Uma música loop infinita | Forneça variedade, transições |
| Pule áudio no protótipo | Áudio placeholder importa |

---

> **Lembre-se:** 50% da experiência do jogo é áudio. Um jogo mutado perde metade de sua alma.