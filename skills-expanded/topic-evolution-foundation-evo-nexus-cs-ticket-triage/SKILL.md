---
name: cs-ticket-triage
description: Triagem e priorização de ticket ou problema de suporte. Use ao receber um novo ticket que precisa de categorização, atribuição de prioridade P1-P4, decisão sobre qual time deve tratar, ou verificação de duplicidade antes de encaminhar. / Triage and prioritize a support ticket or customer issue. Use when a new ticket comes in and needs categorization, assigning P1-P4 priority, deciding which team should handle it, or checking whether it's a duplicate or known issue before routing.
argument-hint: "<texto do ticket ou descrição do problema>"
---

# /cs-ticket-triage

> Se encontrar integrações não configuradas, verifique [CONNECTORS.md](../../CONNECTORS.md).

Categorize, priorize e encaminhe um ticket de suporte ou problema de cliente. Produz uma avaliação de triagem estruturada com uma resposta inicial sugerida.

## Usage

```
/cs-ticket-triage <texto do ticket, mensagem do cliente ou descrição do problema>
```

Exemplos:
- `/cs-ticket-triage Cliente diz que o dashboard está em branco desde esta manhã`
- `/cs-ticket-triage "Fui cobrado duas vezes na minha assinatura este mês"`
- `/cs-ticket-triage Usuário não consegue conectar SSO — erro 403 na callback URL`
- `/cs-ticket-triage Solicitação de feature: exportar relatórios em PDF`

## Workflow

### 1. Parse do Problema

Leia o input e extraia:

- **Problema central**: O que o cliente está realmente vivenciando?
- **Sintomas**: Qual comportamento ou erro específico está vendo?
- **Contexto do cliente**: Quem é? Há detalhes de conta, plano ou histórico disponíveis?
- **Sinais de urgência**: Está bloqueado? É produção? Quantos usuários afetados?
- **Estado emocional**: Frustrado, confuso, neutro, escalando?

### 2. Categorizar e Priorizar

Usando a taxonomia de categorias e o framework de prioridade abaixo:

- Atribuir uma **categoria primária** (bug, how-to, feature request, billing, conta, integração, segurança, dados, performance) e uma secundária opcional
- Atribuir uma **prioridade** (P1–P4) com base em impacto e urgência
- Identificar a **área de produto** a que o problema se refere

### 3. Verificar Duplicatas e Problemas Conhecidos

Antes de encaminhar, verificar nas fontes disponíveis:

- **int-evo-crm** (`/int-evo-crm`): Buscar tickets similares abertos ou resolvidos recentemente
- **Notion MCP**: Verificar problemas conhecidos ou documentação existente
- **int-linear-review** (`/int-linear-review`) ou **Linear MCP**: Verificar se há bug report ou feature request existente

Aplicar o processo de detecção de duplicatas abaixo.

### 4. Determinar Encaminhamento

Usando as regras de routing abaixo, recomendar qual time ou fila deve tratar com base na categoria e complexidade.

### 5. Gerar Output de Triagem

```
## Triagem: [Resumo em uma linha do problema]

**Categoria:** [Primária] / [Secundária se aplicável]
**Prioridade:** [P1-P4] — [Breve justificativa]
**Área de produto:** [Área/time]

### Resumo do Problema
[Resumo em 2-3 frases do que o cliente está vivenciando]

### Detalhes Chave
- **Cliente:** [Nome/conta se conhecido]
- **Impacto:** [Quem e o que está afetado]
- **Workaround:** [Disponível / Não disponível / Desconhecido]
- **Tickets relacionados:** [Links para problemas similares se encontrados]
- **Problema conhecido:** [Sim — link / Não / Verificando]

### Recomendação de Encaminhamento
**Encaminhar para:** [Time ou fila]
**Por quê:** [Breve raciocínio]

### Resposta Inicial Sugerida
[Rascunho da primeira resposta ao cliente — reconhecer o problema,
definir expectativas, fornecer workaround se disponível.
Usar os templates de auto-resposta abaixo como ponto de partida.]

### Notas Internas
- [Contexto adicional para o agente que pegar o ticket]
- [Dicas de reprodução se for um bug]
- [Gatilhos de escalação a observar]
```

### 6. Oferecer Próximos Passos

Após apresentar a triagem:
- "Quer que eu redija uma resposta completa para o cliente?"
- "Devo buscar mais contexto sobre esse problema?"
- "Quer que eu verifique se é um bug conhecido no Linear?"
- "Devo escalar? Posso montar o pacote com /cs-customer-escalation."

---

## Taxonomia de Categorias

Atribuir a cada ticket uma **categoria primária** e opcionalmente uma **secundária**:

| Categoria | Descrição | Palavras-Sinal |
|----------|-------------|-------------|
| **Bug** | Produto se comportando incorretamente ou inesperadamente | Erro, quebrado, crash, não funciona, inesperado, errado, falhando |
| **How-to** | Cliente precisa de orientação sobre como usar o produto | Como faço, posso, onde fica, configurar, ajuda com |
| **Feature request** | Cliente quer uma capacidade que não existe | Seria ótimo se, gostaria de poder, há planos para, solicitando |
| **Billing** | Pagamento, assinatura, fatura ou problemas de preço | Cobrança, fatura, pagamento, assinatura, reembolso, upgrade, downgrade |
| **Conta** | Acesso à conta, permissões, configurações ou gerenciamento de usuários | Login, senha, acesso, permissão, SSO, bloqueado, não consigo entrar |
| **Integração** | Problemas ao conectar com ferramentas de terceiros ou APIs | API, webhook, integração, conectar, OAuth, sync, terceiros |
| **Segurança** | Preocupações de segurança, acesso a dados ou perguntas de compliance | Violação de dados, acesso não autorizado, compliance, LGPD, vulnerabilidade |
| **Dados** | Qualidade de dados, migração, problemas de importação/exportação | Dados faltando, exportar, importar, migração, dados incorretos, duplicatas |
| **Performance** | Velocidade, confiabilidade ou problemas de disponibilidade | Lento, timeout, latência, fora do ar, indisponível, degradado |

### Dicas para Determinação de Categoria

- Se o cliente reportar **tanto** um bug quanto um feature request, o bug é primário
- Se não consegue logar por causa de um bug, a categoria é **Bug** (não Conta) — a causa raiz define a categoria
- "Funcionava antes e agora não funciona" = **Bug**
- "Quero que funcione de forma diferente" = **Feature request**
- "Como faço para funcionar?" = **How-to**
- Em caso de dúvida, optar por **Bug** — é melhor investigar do que descartar

## Framework de Prioridade

### P1 — Crítico
**Critérios:** Sistema em produção fora do ar, perda ou corrupção de dados, brecha de segurança, todos ou a maioria dos usuários afetados.

- O cliente não consegue usar o produto de forma alguma
- Dados estão sendo perdidos, corrompidos ou expostos
- Um incidente de segurança está em andamento
- O problema está piorando ou expandindo em escopo

**SLA esperado:** Responder em até 1 hora. Trabalho contínuo até resolver ou mitigar. Atualizações a cada 1-2 horas.

### P2 — Alto
**Critérios:** Feature principal quebrado, workflow significativo bloqueado, muitos usuários afetados, sem workaround.

- Um workflow central está quebrado mas o produto é parcialmente utilizável
- Vários usuários são afetados ou uma conta-chave está impactada
- O problema está bloqueando trabalho sensível ao tempo
- Nenhum workaround razoável existe

**SLA esperado:** Responder em até 4 horas. Investigação ativa no mesmo dia. Atualizações a cada 4 horas.

### P3 — Médio
**Critérios:** Feature parcialmente quebrado, workaround disponível, usuário único ou equipe pequena afetada.

- Uma feature não está funcionando corretamente mas existe um workaround
- O problema é inconveniente mas não bloqueia trabalho crítico
- Um usuário único ou equipe pequena é afetada
- O cliente não está escalando urgentemente

**SLA esperado:** Responder em até 1 dia útil. Resolução ou atualização em até 3 dias úteis.

### P4 — Baixo
**Critérios:** Inconveniência menor, problema cosmético, pergunta geral, feature request.

- Problemas cosméticos ou de UI que não afetam funcionalidade
- Feature requests e ideias de melhoria
- Perguntas gerais ou de how-to
- Problemas com soluções simples e documentadas

**SLA esperado:** Responder em até 2 dias úteis. Resolução em ritmo normal.

### Gatilhos de Escalação de Prioridade

Elevar prioridade automaticamente quando:
- Cliente esperou mais do que o SLA permite
- Vários clientes reportam o mesmo problema (padrão detectado)
- O cliente escalou explicitamente ou mencionou envolvimento de executivo
- Um workaround que estava em vigor para de funcionar
- O problema se expande em escopo (mais usuários, mais dados, novos sintomas)

## Regras de Routing

Encaminhar tickets com base em categoria e complexidade:

| Encaminhar para | Quando |
|----------|------|
| **Suporte Tier 1 (frontline)** | Perguntas de how-to, problemas conhecidos com soluções documentadas, dúvidas de billing, resets de senha |
| **Suporte Tier 2 (sênior)** | Bugs que requerem investigação, configuração complexa, troubleshooting de integração, problemas de conta |
| **Devs (Engineering)** | Bugs confirmados que precisam de correção de código, problemas de infraestrutura, degradação de performance |
| **Produto** | Feature requests com demanda significativa, decisões de design, gaps de workflow |
| **Segurança** | Preocupações de acesso a dados, relatórios de vulnerabilidade, questões de compliance |
| **Davidson (Liderança)** | Clientes de alto valor em risco, breach de SLA, cliente solicitando envolvimento executivo, exceções de política |

## Detecção de Duplicatas

Antes de criar um novo ticket ou encaminhar, verificar duplicatas:

1. **Buscar por sintoma**: Procurar tickets com mensagens de erro ou descrições similares
2. **Buscar por cliente**: Verificar se esse cliente tem um ticket aberto para o mesmo problema
3. **Buscar por área de produto**: Procurar tickets recentes na mesma área de feature
4. **Verificar problemas conhecidos**: Comparar com problemas conhecidos documentados

**Se uma duplicata for encontrada:**
- Linkar o novo ticket ao existente
- Notificar o cliente que é um problema conhecido sendo rastreado
- Adicionar novas informações do novo relato ao ticket existente
- Elevar prioridade se o novo relato adiciona urgência (mais clientes afetados, etc.)

## Templates de Auto-Resposta por Categoria

### Bug — Resposta Inicial
```
Obrigado por reportar isso. Entendo como [impacto específico]
pode ser disruptivo para o seu trabalho.

Registrei isso como um problema [prioridade] e nossa equipe está
investigando. [Se houver workaround: "Enquanto isso, você pode
[workaround]."]

Vou te atualizar em até [prazo SLA] com o que encontrarmos.
```

### How-to — Resposta Inicial
```
Boa pergunta! [Resposta direta ou link para documentação]

[Se mais complexo: "Deixa eu te guiar pelos passos:"]
[Passos ou orientações]

Me avise se isso ajudou, ou se tiver perguntas de acompanhamento.
```

### Feature Request — Resposta Inicial
```
Obrigado pela sugestão — entendo por que [capacidade]
seria valioso para o seu workflow.

Documentei isso e compartilhei com nosso time de produto.
Embora não possa me comprometer com um prazo específico, seu feedback
informa diretamente as prioridades do nosso roadmap.

[Se houver alternativa: "Enquanto isso, você pode achar
[alternativa] útil para alcançar algo similar."]
```

### Billing — Resposta Inicial
```
Entendo que problemas de billing precisam de atenção imediata. Deixa
eu verificar isso para você.

[Se simples: detalhes da resolução]
[Se complexo: "Estou revisando sua conta agora e terei
uma resposta em até [prazo]."]
```

### Segurança — Resposta Inicial
```
Obrigado por sinalizar isso — levamos questões de segurança
a sério e estamos revisando imediatamente.

Escalei isso para nossa equipe de segurança para investigação.
Vou te retornar em até [prazo] com nossos achados.

[Se ação for necessária: "Enquanto isso, recomendamos
[ação protetora]."]
```

## Boas Práticas de Triagem

1. Leia o ticket completo antes de categorizar — contexto em mensagens posteriores frequentemente muda a avaliação
2. Categorize pela **causa raiz**, não apenas pelo sintoma descrito
3. Em caso de dúvida na prioridade, errar para o lado mais alto — é mais fácil de-escalar do que recuperar de um SLA perdido
4. Sempre verificar duplicatas e problemas conhecidos antes de encaminhar
5. Escrever notas internas que ajudem a próxima pessoa a pegar contexto rapidamente
6. Incluir o que você já verificou ou descartou para evitar investigação duplicada
7. Sinalizar padrões — se estiver vendo o mesmo problema repetidamente, escalar o padrão mesmo que os tickets individuais sejam de baixa prioridade
