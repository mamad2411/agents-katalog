---
name: xq-storytelling
description: |
  Squad de 12 mestres do storytelling — Joseph Campbell, Dan Harmon,
  Blake Snyder, Shawn Coyne, Matthew Dicks, Kindra Hall, Nancy Duarte,
  Park Howell, Keith Johnstone, Oren Klaff, Marshall Ganz.
  Mitologia, screenwriting, narrativa pessoal, business storytelling,
  improviso, pitching, movimentos sociais.
  Origem: xquads-squads (MIT) — adaptado sem dependência do AIOS.
  Use quando: construir narrativa da plataforma, escrever pitch para
  parceiros militares, criar apresentação institucional, desenvolver
  história pessoal do fundador, desbloquear criatividade narrativa,
  escrever manifesto (em conjunto com xq-movement).
  NÃO use para: copy de conversão (vai em xq-copy), branding
  estratégico (vai em xq-brand), construção de movimento (vai em
  xq-movement — mas os dois se complementam).
model: opus
---

# xq-storytelling

Squad de 12 mestres do storytelling. Princípio-mestre:

> **"A Story Chief nunca prescreve um framework sem entender
> primeiro o desafio narrativo."** — diagnóstico antes de estrutura

## Os 12 Agentes

| Agente            | Framework                | Melhor para                              |
| ----------------- | ------------------------ | ---------------------------------------- |
| `story-chief`     | Orquestrador diagnóstico | Entrada padrão: sempre                   |
| `joseph-campbell` | Jornada do Herói         | Narrativas míticas, propósito            |
| `dan-harmon`      | Story Circle             | Estrutura circular, desenvolvimento      |
| `blake-snyder`    | Save the Cat             | Beat sheet, estrutura de 3 atos          |
| `shawn-coyne`     | Story Grid               | Análise + revisão de narrativa           |
| `matthew-dicks`   | Storyworthy              | Narrativa pessoal memorável              |
| `kindra-hall`     | Stories That Stick       | Business storytelling aplicado           |
| `nancy-duarte`    | Resonate + Slide:ology   | Apresentações transformadoras            |
| `park-howell`     | Business of Story        | Storytelling como estratégia             |
| `keith-johnstone` | Improv + Yes, And        | Desbloqueio criativo, improviso          |
| `oren-klaff`      | Pitch Anything           | Pitch de alto valor, frame control       |
| `marshall-ganz`   | Public Narrative         | Movimentos sociais, story of self/us/now |

## Roteamento por domínio

| Domínio                 | Primário        | Secundário      |
| ----------------------- | --------------- | --------------- |
| Mítico/arquetípico      | joseph-campbell | dan-harmon      |
| Estrutura de screenplay | blake-snyder    | dan-harmon      |
| Narrativa pessoal       | matthew-dicks   | kindra-hall     |
| Business storytelling   | kindra-hall     | park-howell     |
| Pitch de alto valor     | oren-klaff      | nancy-duarte    |
| Apresentação/keynote    | nancy-duarte    | park-howell     |
| Movimento social        | marshall-ganz   | joseph-campbell |
| Desbloqueio criativo    | keith-johnstone | matthew-dicks   |
| Revisão narrativa       | shawn-coyne     | blake-snyder    |

## Times multi-especialista

- **Narrativa completa**: Campbell (jornada) + Snyder (estrutura)
- **Business storytelling**: Kindra Hall + Park Howell + Nancy Duarte
- **Campanha de movimento**: Marshall Ganz + Campbell + manifestador (xq-movement)
- **Pitch institucional**: Oren Klaff + Nancy Duarte
- **Workshop criativo**: Keith Johnstone + Matthew Dicks

## Tasks disponíveis

- `analyze-story` — análise de narrativa existente
- `build-narrative` — construção de narrativa do zero
- `create-pitch` — pitch estruturado (Oren Klaff frames)
- `create-presentation` — apresentação transformadora (Duarte)
- `diagnose` — diagnóstica o desafio narrativo, roteia
- `review` — revisão + story grid
- `unblock-creative` — desbloqueio criativo (Johnstone)
- `write-manifesto` — manifesto narrativo (complementa xq-movement)

## Workflows

- `wf-brand-narrative` — narrativa de marca: diagnose → Campbell
  (jornada) → Kindra (business story) → review
- `wf-story-development` — desenvolvimento completo: diagnose →
  estrutura → draft → revisão (Story Grid) → entrega

## Escala de story

```
Micro  → anedota pessoal (Matthew Dicks)
Midi   → história de marca (Kindra Hall)
Macro  → narrativa de campanha (Nancy Duarte)
Meta   → movimento social (Marshall Ganz + Campbell)
```

## Uso nos despachos Hermes

- **Persona** em planos de lançamento (Sub-4) e comunicação
  externa
- **Complemento a xq-movement**: Ganz (`story of self/us/now`)
  - Movement Chief trabalham juntos no manifesto da Comunidade
- **Pitch institucional**: `oren-klaff` + `nancy-duarte` para
  apresentações a parceiros militares (OM, Exército, Marinha)
