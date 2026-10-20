---
name: hr-interview-prep
description: Cria planos de entrevista estruturados com perguntas baseadas em competências e scorecards. Use quando preparando entrevistas de candidatos para a Evolution. Gatilhos: "plano de entrevista para", "perguntas de entrevista para", "como devemos entrevistar", "scorecard para", "preparar entrevista".
argument-hint: "<cargo ou role>"
---

# HR — Interview Prep

Crie planos de entrevista estruturados para avaliar candidatos de forma consistente e justa.

## Princípios de Design de Entrevista

1. **Estruturado**: Mesmas perguntas para todos os candidatos ao cargo
2. **Baseado em competências**: Perguntas mapeadas para habilidades e comportamentos específicos
3. **Baseado em evidências**: Use perguntas comportamentais e situacionais
4. **Painel diverso**: Múltiplas perspectivas reduzem viés
5. **Pontuado**: Use rubricas, não intuição

## Componentes do Plano de Entrevista

### Competências do Cargo
Defina 4-6 competências-chave para o cargo (ex: habilidades técnicas, comunicação, liderança, resolução de problemas, adaptabilidade, orientação a produto).

### Banco de Perguntas
Para cada competência:
- 2-3 perguntas comportamentais ("Me fale sobre uma vez que...")
- 1-2 perguntas situacionais ("Como você lidaria com...")
- Sondagens de follow-up

### Scorecard
Avalie cada competência em uma escala consistente (1-4) com descrições claras de cada nível.

### Template de Debrief
Formato estruturado para os entrevistadores compartilharem os resultados e tomar uma decisão.

## Output — Kit Completo de Entrevista

```markdown
## Kit de Entrevista: [Cargo] — [Nível]
**Preparado por:** [Nome] | **Data:** [Data]

---

### Competências Avaliadas

| Competência | Peso | Entrevistador |
|-------------|------|---------------|
| [Competência 1 — ex: Expertise Técnica] | Alta | [Nome] |
| [Competência 2 — ex: Comunicação] | Média | [Nome] |
| [Competência 3 — ex: Ownership / Autonomia] | Alta | [Nome] |
| [Competência 4 — ex: Colaboração] | Média | [Nome] |
| [Competência 5 — ex: Alinhamento com missão open source] | Alta | Davidson |

---

### Estrutura do Painel

| Etapa | Entrevistador | Foco | Duração |
|-------|--------------|------|---------|
| Triagem | [Danilo / Gui] | Fit técnico básico, motivações | 30min |
| Técnica | [Danilo + Gui] | Expertise técnica, raciocínio | 60min |
| Cultural | Davidson | Missão, valores, ambição | 30min |
| Projeto Prático | [Time técnico] | Resolução de problema real | Assíncrono / 2h |

---

### Banco de Perguntas por Competência

#### Competência: Expertise Técnica
**Comportamentais:**
1. "Me fale sobre o sistema mais complexo que você construiu. Quais foram os maiores desafios técnicos e como os resolveu?"
2. "Descreva uma vez que você teve que aprender uma tecnologia nova rapidamente para entregar um projeto. Como foi o processo?"
3. "Me conte sobre um bug crítico que você encontrou em produção. Como você diagnosticou e resolveu?"

**Situacionais:**
1. "Se você descobrisse que uma decisão técnica passada está causando problemas de escalabilidade agora, como abordaria a situação?"
2. "Como você avaliaria adotar uma nova biblioteca open source em um projeto crítico?"

**Follow-ups:**
- "Qual foi especificamente sua contribuição vs. do time?"
- "O que você faria diferente hoje?"
- "Como você mediu o sucesso?"

---

#### Competência: Ownership / Autonomia
**Comportamentais:**
1. "Me fale sobre uma vez que você identificou um problema que ninguém tinha pedido para você resolver. O que fez?"
2. "Descreva uma situação em que você teve que tomar uma decisão importante sem ter todas as informações. Como agiu?"

**Situacionais:**
1. "Se você recebesse uma issue no Linear sem muito contexto e sem ninguém disponível para explicar, o que faria?"
2. "Você está trabalhando em uma feature quando percebe que a abordagem planejada não vai funcionar. Como procede?"

---

#### Competência: Alinhamento com Open Source / Missão Evolution
**Comportamentais:**
1. "Você já contribuiu com projetos open source? Me conte sobre essa experiência."
2. "Por que você se interessa especificamente pela Evolution API? O que te atraiu?"
3. "Como você lida com o fato de que parte do seu trabalho será público e usado por milhares de devs?"

**Situacionais:**
1. "Um usuário abre uma issue no GitHub relatando um bug crítico às 23h. Você vê. O que faz?"

---

### Rubrica de Pontuação (Scorecard)

**Escala:**
| Nota | Descrição |
|------|-----------|
| 4 — Excepcional | Evidência forte e consistente da competência. Muito acima do esperado para o nível. |
| 3 — Atende | Evidência clara e sólida. Atende plenamente o esperado para o nível. |
| 2 — Parcial | Alguma evidência, mas com lacunas. Atende parcialmente. Precisará de desenvolvimento. |
| 1 — Não atende | Pouca ou nenhuma evidência. Não atende o mínimo esperado. |

**Scorecard por Candidato:**

| Competência | Peso | Nota (1-4) | Evidências Coletadas |
|-------------|------|-----------|----------------------|
| Expertise Técnica | Alta | [ ] | |
| Comunicação | Média | [ ] | |
| Ownership / Autonomia | Alta | [ ] | |
| Colaboração | Média | [ ] | |
| Alinhamento com missão | Alta | [ ] | |
| **TOTAL PONDERADO** | | [ ] | |

**Recomendação do Entrevistador:** [ ] Forte SIM / [ ] SIM / [ ] NÃO / [ ] Forte NÃO

---

### Template de Debrief

```
## Debrief: [Nome do Candidato] — [Cargo]
**Data:** [Data] | **Participantes:** [Nomes]

### Pontuações
| Entrevistador | Competência | Nota | Resumo |
|---------------|------------|------|--------|
| [Nome] | [Competência] | [1-4] | [Evidência] |

### Forças Identificadas
- [Ponto forte com evidência específica]

### Preocupações / Lacunas
- [Preocupação com evidência específica]

### Pontos de Divergência entre Entrevistadores
- [Onde vocês discordaram e por quê]

### Decisão
[ ] CONTRATAR — Próximos passos: [oferta / aprovação de headcount / etc.]
[ ] NÃO CONTRATAR — Razão: [específica]
[ ] AGUARDAR — Por quê: [outros candidatos, mais tempo para decidir]

### Notas para a Oferta
- [Aspirações de carreira mencionadas]
- [Fatores de motivação relevantes para personalizar a proposta]
- [Pontos de atenção para o onboarding]
```

---

## Dicas para Entrevistas na Evolution

1. **Foco em exemplos reais** — Peça situações específicas. "O que você faria?" é mais fraco que "O que você fez?".
2. **Contexto open source é diferencial** — Candidatos familiarizados com WhatsApp API, bots, ou contribuição open source têm vantagem de ramp-up real.
3. **Time pequeno, alto impacto** — Avalie autonomia pesada. Com ~10 pessoas, não há espaço para quem precisa de muita estrutura.
4. **Processo rápido** — Tome decisão em até 48h após o último round. Candidatos bons têm outras ofertas.
5. **Bias mitigation** — Comece avaliando competências antes de comparar candidatos entre si. Evite "me lembrou de [pessoa X]" como critério.
