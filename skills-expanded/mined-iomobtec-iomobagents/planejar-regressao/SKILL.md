---
name: planejar-regressao
description: "Define a estratégia de testes de regressão e a seleção de casos de teste. Use quando o dev-qa precisa planejar a regressão de uma entrega."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: planejar-regressao

Define a **estratégia de regressão** para uma entrega ou release: quais fluxos testar, com qual profundidade, em qual ordem e com qual critério de bloqueio. Produz um plano executável que equilibra cobertura de risco com tempo disponível.

**Agente:** dev-qa  
**Guardrails aplicáveis:** `00-core.md`, `testes.md`, `processo.md`

---

## Quando usar

- Antes de um release ou deploy em ambiente de produção/homologação
- Quando uma mudança de alto impacto (refatoração, migração, novo serviço) é entregue
- Para definir quais E2E e testes de integração rodar em cada estágio do pipeline de CI/CD
- Para priorizar esforço de QA manual quando o tempo de teste é limitado

---

## Processo de execução

### Passo 1 — Identificar o escopo da mudança

Antes de planejar o que testar, entender o que mudou:

```
Perguntas obrigatórias:
1. Quais serviços foram alterados nesta entrega?
2. Quais contratos de API ou eventos foram modificados?
3. Alguma migração de banco de dados foi executada?
4. Alguma dependência externa foi atualizada?
5. Quais fluxos de negócio passam pelos serviços alterados?
```

### Passo 2 — Classificar fluxos por risco

Não todos os fluxos têm o mesmo risco. Classificar para priorizar:

| Nível de risco | Critério | Quando testar |
|---|---|---|
| **Crítico** | Falha impacta receita, dados financeiros ou autenticação | Sempre — bloqueador de release |
| **Alto** | Falha impacta fluxo principal do usuário | Sempre — bloqueador de release |
| **Médio** | Falha impacta funcionalidade secundária usada por muitos usuários | Testar em regressão completa |
| **Baixo** | Falha impacta funcionalidade raramente usada ou fácil de contornar | Testar em sprint ou quando há tempo |

### Passo 3 — Montar a matriz de regressão

```markdown
## Matriz de Regressão — Release <versão>

### Escopo da mudança
- Serviços alterados: <lista>
- Contratos modificados: <lista>
- Migrations: <sim/não>

---

### Fluxos críticos (bloqueadores de release)

| # | Fluxo | Cobertura automatizada? | Teste manual? | Responsável |
|---|---|---|---|---|
| 1 | Login e autenticação | ✅ E2E: `autenticacao.spec.ts` | Não | CI |
| 2 | Checkout e pagamento | ✅ E2E: `checkout.spec.ts` | Sim — cartão real no ambiente de staging | dev-qa |
| 3 | Criação de pedido via API | ✅ Integração: `order.integration.spec.ts` | Não | CI |

---

### Fluxos de alto risco (bloqueadores de release)

| # | Fluxo | Cobertura automatizada? | Teste manual? | Responsável |
|---|---|---|---|---|
| 4 | Perfil do usuário — leitura e edição | ✅ E2E: `perfil.spec.ts` | Não | CI |
| 5 | Cancelamento de pedido | ⚠️ Parcial — happy path apenas | Sim — cenário de estorno | dev-qa |

---

### Fluxos de médio risco (não bloqueadores)

| # | Fluxo | Cobertura automatizada? | Observação |
|---|---|---|---|
| 6 | Histórico de pedidos — paginação | ✅ Integração | Verificar se paginação responde corretamente após migration |
| 7 | Notificações por e-mail | ❌ Sem cobertura automatizada | Verificar manualmente no ambiente de staging |
```

### Passo 4 — Definir critério de bloqueio de release

Definir explicitamente o que impede o release de avançar:

```markdown
## Critério de bloqueio de release

**Release bloqueado se:**
- Qualquer fluxo crítico ou de alto risco falhar nos testes automatizados em CI
- Qualquer fluxo crítico falhar no teste manual em staging
- Taxa de erro > 1% nos primeiros 15 minutos após deploy em produção (canary)

**Release não bloqueado por:**
- Falha em fluxo de baixo risco (registrar como bug e priorizar no próximo sprint)
- Flap (falha intermitente) em E2E não relacionado à mudança (registrar e monitorar)
```

### Passo 5 — Definir profundidade de teste por camada

Para cada serviço alterado, definir quais camadas de teste cobrir:

```markdown
## Profundidade de teste por camada

| Camada | Ferramenta | Quando executar | Tempo estimado |
|---|---|---|---|
| Unitário | Jest | A cada commit (CI) | ~2 min |
| Integração | Jest + Supertest | A cada PR (CI) | ~5 min |
| E2E — smoke | Playwright (fluxos críticos) | A cada deploy em staging | ~10 min |
| E2E — regressão completa | Playwright (todos os fluxos) | Antes de release | ~30 min |
| Manual — staging | — | Fluxos sem cobertura automatizada | Conforme plano |
```

**Smoke test:** subconjunto mínimo de E2E que valida se o sistema está operacional após deploy. Roda em minutos e bloqueia rollback se falhar.

```typescript
// e2e/smoke/smoke.spec.ts — máximo 5 testes, máximo 2 minutos
test('should load home page', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/nome da aplicação/i);
});

test('should reach login page', async ({ page }) => {
  await page.goto('/login');
  await expect(page.getByRole('heading', { name: /entrar/i })).toBeVisible();
});

test('should return 200 on health check', async ({ request }) => {
  const response = await request.get('/api/health');
  expect(response.status()).toBe(200);
});
```

### Passo 6 — Identificar gaps de cobertura

Após montar a matriz, identificar o que não tem cobertura automatizada:

```markdown
## Gaps de cobertura identificados

| Fluxo | Gap | Risco | Ação recomendada |
|---|---|---|---|
| Notificação por e-mail | Sem E2E automatizado | Médio | Criar `notificacao.spec.ts` no próximo sprint |
| Cancelamento com estorno | Apenas happy path | Alto | Adicionar cenário de estorno falhado — prioritário |
| Exportação de relatório | Sem cobertura alguma | Baixo | Postergar — funcionalidade raramente usada |
```

---

## Saída produzida

```markdown
# Plano de Regressão — <nome da entrega / versão>

**Data:** <data>  
**Responsável:** dev-qa  
**Critério de bloqueio:** <definido no passo 4>

## Escopo da mudança
<resumo do passo 1>

## Matriz de regressão
<tabela do passo 3>

## Profundidade de teste por camada
<tabela do passo 5>

## Gaps de cobertura
<tabela do passo 6>

## Cronograma de execução
| Etapa | Quando | Duração estimada |
|---|---|---|
| Smoke test (deploy staging) | Após deploy automático | 10 min |
| E2E — fluxos críticos | CI/CD gate | 15 min |
| Testes manuais | Antes de aprovar release | 30 min |
| E2E — regressão completa | Noturno antes do release | 30 min |
```

---

## Checklist de conclusão

- [ ] Todos os serviços alterados identificados
- [ ] Fluxos classificados por risco (crítico / alto / médio / baixo)
- [ ] Critério de bloqueio de release definido explicitamente
- [ ] Gaps de cobertura identificados com ação recomendada
- [ ] Smoke test definido para o deploy imediato
- [ ] Tempo estimado de execução por etapa
