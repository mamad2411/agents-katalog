---
name: brain
description: 🧠 Orquestrador de Inteligências Múltiplas — dispara uma pergunta para 9 agentes especializados (Gardner) e sintetiza um conceito único e integrado
category: cognitive
tags: [inteligências-múltiplas, gardner, multi-agente, síntese, brain]
---

# 🧠 Brain — Sistema de Inteligências Múltiplas

## O que faz

O **Brain** é um orquestrador multi-agente baseado na **Teoria das Inteligências Múltiplas de Howard Gardner**. Quando você faz uma pergunta, o Brain:

1. ⚡ Dispara a **mesma pergunta** para 9 agentes especialistas em paralelo
2. 🧠 Cada agente interpreta a pergunta **exclusivamente através da lente da sua inteligência** (Linguística, Lógico-Matemática, Espacial, Corporal-Cinestésica, Musical, Interpessoal, Intrapessoal, Naturalista, Existencial)
3. 🔄 Coleta todas as respostas
4. 🪄 **Sintetiza um conceito NOVO** — não um resumo, mas uma compreensão integrada que emerge do conjunto

## Como usar

```
@brain <sua pergunta>
```

### Exemplos

```
@brain Como funciona uma sinapse?
```

```
@brain O que é consciência?
```

```
@brain Como a matemática descreve a realidade?
```

```
@brain Qual o sentido da vida?
```

```
@brain Como funciona a gravidade?
```

## Procedimento para Zivy

Quando o usuário invocar `@brain <pergunta>`, siga estes passos:

### Passo 1: Executar o orchestrator
Execute o orchestrator.py com a pergunta do usuário:

```bash
cd /root/.hermes/skills/brain && python3 orchestrator.py "<pergunta>"
```

**Importante:** Preserve a pergunta exata do usuário, incluindo pontuação e acentos.

### Passo 2: Coletar resultado
O orchestrator imprime:
1. ✅ Status de cada inteligência (ok/erro/timeout) + tamanho em chars + flag de truncamento
2. 🧠 Síntese final do Brain
3. 💾 Caminho do arquivo de sessão salvo

### Passo 3: Retornar ao usuário
Apresente a **síntese final** de forma limpa, com um breve resumo do processo:

```
🧠 SÍNTESE DO BRAIN

[conteúdo da síntese]

---
⚡ 9 inteligências consultadas • Processado em X.Xs
💾 Sessão salva em: /root/.hermes/skills/brain/responses/session_XXXXXX.json
```

### ⚠️ Pitfalls

1. **Timeout:** Se alguma inteligência exceder 90s, o sistema retorna timeout parcial. A síntese ainda será feita com as respostas disponíveis. Isso é raro — o modelo deepseek-v4-flash é rápido.

2. **Perguntas muito curtas/triviais:** O sistema funciona melhor com perguntas conceituais ("que horas são?" não é ideal). Se o usuário insistir em perguntas triviais, a síntese ainda pode surpreender pelas metáforas.

3. **Tempo total:** Cada execução leva ~1-2 minutos (9 chamadas paralelas). Informe o usuário se ele estiver com pressa.

4. **Modelo de raciocínio (deepseek-v4-flash):** O modelo gasta tokens em raciocínio interno ANTES de gerar a resposta. Isso já foi corrigido no orchestrator com `max_tokens: 16000`, `extract_content()` com fallback, e stripping de CoT vazado. **Se aparecerem respostas vazias ou truncadas:**
   - Verificar o campo `truncated` no JSON de sessão
   - Consultar `references/deepseek-reasoning-model-behavior.md` para diagnóstico completo

5. **CoT vazado:** Respostas começando com "Thinking..." ou "Analyze..." são automaticamente limpas por `_strip_cot_from_content()`. Se ainda assim aparecerem, o system prompt pode precisar de reforço na instrução de não vazar raciocínio.

## Arquitetura

```
                    ┌─────────────────┐
                    │   USUÁRIO        │
                    │  "pergunta"      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   BRAIN (Zivy)  │
                    │  Orchestrator   │
                    │  + Síntese      │
                    └───┬────┬────┬───┘
                        │    │    │
         ┌──────────────┼────┼────┼──────────────┐
         │              │    │    │              │
  ┌──────▼─────┐ ┌──────▼──┐ ┌──▼──────┐ ┌──────▼──────┐
  │ Linguística │ │ Lógico  │ │ Espacial │ │ Cinestésica │ ...
  │ soul.md     │ │ soul.md │ │ soul.md │ │ soul.md     │
  │ agent.md    │ │ agent.md│ │ agent.md│ │ agent.md    │
  └─────────────┘ └─────────┘ └─────────┘ └─────────────┘
                        │    │    │
         ┌──────────────┼────┼────┼──────────────┐
         │              │    │    │              │
  ┌──────▼──────────────▼────▼────▼──────────────▼──────┐
  │           BRAIN — SÍNTESE FINAL                     │
  │  Conceito novo, integrado, claro e estabelecido     │
  └─────────────────────────────────────────────────────┘
```

## Inteligências

| # | Inteligência | Temperatura | Estilo |
|---|-------------|-------------|--------|
| 1 | 🧠 **Linguística** | 0.7 | Narrativo, metafórico, etimológico |
| 2 | 🔢 **Lógico-Matemática** | 0.3 | Analítico, preciso, estruturado |
| 3 | 🌌 **Espacial** | 0.6 | Visual, geométrico, arquitetônico |
| 4 | 🏃 **Corporal-Cinestésica** | 0.8 | Visceral, tátil, movimento |
| 5 | 🎵 **Musical** | 0.9 | Rítmico, harmônico, frequência |
| 6 | 👥 **Interpessoal** | 0.7 | Relacional, comunicação, rede |
| 7 | 🧘 **Intrapessoal** | 0.7 | Reflexivo, subjetivo, self |
| 8 | 🌿 **Naturalista** | 0.6 | Orgânico, evolutivo, ecológico |
| 9 | 🌌 **Existencial** | 0.8 | Contemplativo, transcendente |

## Estrutura de Arquivos

```
~/.hermes/skills/brain/
├── SKILL.md                          ← Esta skill
├── orchestrator.py                   ← Orquestrador principal
├── references/
│   └── deepseek-reasoning-model-behavior.md  ← Comportamento de modelos de raciocínio
├── intelligences/
│   ├── linguistic/soul.md + agent.md
│   ├── logical-mathematical/soul.md + agent.md
│   ├── spatial/soul.md + agent.md
│   ├── bodily-kinesthetic/soul.md + agent.md
│   ├── musical/soul.md + agent.md
│   ├── interpersonal/soul.md + agent.md
│   ├── intrapersonal/soul.md + agent.md
│   ├── naturalistic/soul.md + agent.md
│   └── existential/soul.md + agent.md
└── responses/                        ← Sessões salvas (JSON)
```

---

## 🌍 Versão Pública

Este projeto está disponível no GitHub: **https://github.com/tiagovficagna/Hbrain**

Lá você encontra:
- README completo com instruções de instalação
- Exemplos de saída com sínteses reais
- Arquitetura detalhada
- MIT License
