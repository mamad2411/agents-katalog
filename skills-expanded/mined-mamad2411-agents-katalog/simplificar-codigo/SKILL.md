---
name: simplificar-codigo
description: "Refactoring com preservação de comportamento — Chesterton's Fence, complexidade essencial versus acidental e clareza acima de esperteza. Use quando um dev ou o tech-lead vai simplificar código sem mudar comportamento."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: simplificar-codigo

Refatorar código para reduzir complexidade acidental, preservando o comportamento exato. Baseado no Princípio de Chesterton's Fence: entender o propósito de algo antes de modificá-lo.

**Agente:** `dev-backend`, `dev-bff`, `dev-frontend`, `dev-mobile`, `tech-lead`  

---

## Quando usar

- Ao fazer code review e encontrar complexidade desnecessária
- Antes de adicionar feature em área com débito técnico
- Quando um PR de simplificação é explicitamente solicitado

---

## Processo

### Passo 1 — Entender antes de tocar (Chesterton's Fence)
Ler o código completo e responder por escrito: "por que este código existe dessa forma?" Antes de remover ou simplificar qualquer coisa, documentar a intenção original. Se não consegue responder, aplicar a regra de Chesterton's Fence: não remova o que não entende. Investigue primeiro.

Chesterton's Fence aplicado ao código: se existe uma construção aparentemente estranha no meio do código, não a remova antes de entender por que ela foi colocada ali. Pode haver uma razão não óbvia — workaround de bug, requisito de compliance, edge case raro documentado só em Slack.

### Passo 2 — Separar complexidade essencial de complexidade acidental
Antes de qualquer modificação, classificar cada trecho candidato à simplificação:

| Tipo | Definição | Ação |
|---|---|---|
| Complexidade essencial | Regra de negócio genuinamente complexa, requisito não negociável | Não simplificar — preserve e documente |
| Complexidade acidental | Abstração desnecessária, indireção sem motivo, nesting evitável | Candidata a simplificação |

Se não consegue distinguir, perguntar ao dono do código ou ao tech-lead antes de prosseguir.

### Passo 3 — Garantir cobertura de testes
Verificar que existe cobertura de testes automáticos para o comportamento atual do trecho que será simplificado. Se não existe, escrever os testes primeiro. Nunca simplificar código sem rede de segurança — a simplificação pode introduzir regressão silenciosa.

### Passo 4 — Aplicar uma simplificação por vez
Executar exatamente uma simplificação, rodar todos os testes, verificar que passam, e só então aplicar a próxima. Nunca agrupar múltiplas simplificações sem verificar entre elas — isso torna impossível identificar qual simplificação introduziu uma regressão.

Candidatos válidos para simplificação:
- Abstração usada em apenas um lugar (abstração prematura — inline)
- Variável intermediária usada exatamente uma vez sem ganho real de clareza
- Comentário que descreve o "o quê" (o código já diz isso) em vez do "por quê" — remover ou converter em comentário de intenção
- Nesting de 4 ou mais níveis que pode ser achatado com early return
- Condição negativa dupla (`!isNotValid`) que pode ser invertida (`isValid`)

### Passo 5 — Verificar que o diff é apenas estrutural
Revisar o diff completo e confirmar que nenhuma mudança de comportamento foi introduzida — apenas mudança estrutural. Casos onde isso falha silenciosamente: renomear variável que shadeia outra, remover null-check considerado "óbvio", inline de função com side-effect.

### Passo 6 — Documentar no PR
Descrever no PR o que foi simplificado, por que era complexidade acidental (não essencial), e qual alternativa foi usada. Isso previne reverter a simplificação sem entender o motivo.

---

## O que NÃO simplificar

- **Código já limpo** — "simplificação" de código legível e bem estruturado gera ruído sem valor e sinaliza preferência pessoal de estilo, não melhoria objetiva
- **Implementações que você não entende completamente** — aplica Chesterton's Fence; investigue antes de tocar
- **Seções críticas de performance** — otimizações às vezes parecem complexas por razão válida (cache manual, loop desenrolado, evitar alocação); verifique com benchmarks antes de simplificar
- **Código que outros times consomem** — mudança de interface sem coordenação quebra contratos; use a skill `migrar-deprecar` nesses casos
- **Workarounds com comentário explicativo** — se há um comentário dizendo "necessário por causa de X", investigue X antes de remover o workaround

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "O código está funcionando, não vale mexer" | Código difícil de entender vai introduzir bugs na próxima modificação. Simplificar agora é mais barato do que debugar depois. |
| "Vou refatorar tudo enquanto estou aqui" | Scope creep em refactoring é o maior risco. Escopo ao necessário — o resto vira issue separada. |
| "Essa abstração pode ser útil no futuro" | YAGNI. Abstração sem uso atual é complexidade sem benefício. Se precisar no futuro, extrai no futuro com o contexto correto. |
| "Código 'inteligente' é sinal de competência" | Código que exige esforço para entender é código ruim, independentemente de ser "elegante". Clareza supera esperteza. |
| "Não preciso de testes para uma simplificação simples" | Simplificações "simples" são a principal fonte de regressões silenciosas. Se é simples, escrever o teste é rápido. |

---

## Anti-padrões bloqueados

- Simplificar código sem ler e entender a intenção original primeiro
- Agrupar simplificação + mudança de comportamento no mesmo commit
- Remover tratamento de erro "redundante" sem confirmar que o erro nunca ocorre em produção
- Refatorar código de outro time sem comunicação prévia
- Usar simplificação como veículo para introduzir novo padrão sem aprovação do tech-lead
- Simplificar além do escopo do PR original ("limpeza oportunista" não solicitada)

---

## Checklist de conclusão

- [ ] A intenção original do código foi documentada antes de qualquer modificação
- [ ] A complexidade identificada é acidental (não essencial)
- [ ] Existem testes cobrindo o comportamento atual antes da simplificação
- [ ] Cada simplificação foi aplicada e testada individualmente
- [ ] O diff não contém nenhuma mudança de comportamento — apenas mudança estrutural
- [ ] Código de outros times não foi modificado sem comunicação
- [ ] Workarounds com comentário explicativo foram investigados antes de qualquer remoção
- [ ] O PR documenta o que foi simplificado e por quê era complexidade acidental
