---
name: code-truth-validation
description: Validação obrigatória de documentação contra código real. Previne inconsistências doc-vs-code em integrações, gateways, enums e arquivos referenciados.
---

# Code-Truth Validation

> **Toda afirmação técnica em documentação DEVE ser verificada contra o código real.**

---

## 🎯 PROPÓSITO

Garantir que documentação gerada (flow docs, TDD, handover) reflita o estado **real** do código — não o estado planejado, assumido, ou desatualizado.

---

## 🔴 REGRAS OBRIGATÓRIAS

> [!CAUTION]
> **ANTES de salvar qualquer doc técnico**, o agente DEVE executar a validação abaixo.
> Documentação sem verificação contra código real gera inconsistências graves.

### 1. Checklist de Validação por Tipo

#### Integrações / Gateways / APIs externas

- [ ] Arquivo/classe mencionado **existe** no codebase (`find_by_name` / `grep_search`)
- [ ] Está **registrado** no enum/config correspondente
- [ ] Se doc diz "ativo/implementado" → confirmar que código NÃO é stub/mock/placeholder
- [ ] Se doc diz "será implementado" / "planejado" → marcar com `⏳ PLANEJADO` visível

#### Componentes / Arquivos referenciados

- [ ] CADA arquivo referenciado existe no path indicado
- [ ] Funções/métodos citados existem na assinatura real

#### Enums / Constantes / Configs

- [ ] Valores referenciados confirmados contra o fonte real

---

### 2. Separação Estado Atual vs Estado Planejado

**Se divergência detectada** — NÃO documentar o estado planejado como se fosse atual. Separar:

```markdown
## Estado Atual (verificado no código)

[O que realmente existe — com referências a arquivos]

## Estado Planejado / Decisão de Projeto

> ⏳ **Ainda não implementado no código**
> [O que deveria existir — com justificativa e referência à decisão]
```

- Registrar divergência como débito técnico na seção de débitos do doc

---

### 3. Cross-Scope Doc-vs-Code (para escopos anteriores)

> [!WARNING]
> Documentação de escopos anteriores pode conter **afirmações desatualizadas**
> (ex: flow doc do `shop/` dizendo "gateway = Pagar.me" quando o código tem `Cielo.php`).

Para cada **integração ou componente cross-scope** identificado:

1. Verificar se o arquivo/classe referenciado **existe** no codebase do novo escopo
2. Se doc anterior diz "ativo" → confirmar no código (não é stub?)
3. Se doc anterior diz "planejado" → verificar se foi implementado
4. Registrar divergências:

```markdown
### ⚠️ Divergências Doc → Código

| Doc Fonte | Afirmação | Realidade no Código | Ação |
|-----------|-----------|---------------------|------|
| {arquivo.md} | {o que o doc diz} | {o que o código tem} | Corrigir doc / Registrar débito |
```

---

### 4. Doc Impact Check (Pós-Implementação)

> [!CAUTION]
> **GATE POR TASK:** Após implementar e testar cada task que modifica código,
> verificar se os arquivos modificados são referenciados em documentação existente.

**Ações:**

1. Listar os arquivos modificados pela task
2. Buscar referências em `docs/flows/` e `docs/design/TDD-*.md`:
   ```bash
   grep -rl "{nome_do_arquivo}" docs/flows/ docs/design/ 2>/dev/null
   ```
3. Se **referências encontradas** → Abrir e verificar se descrição corresponde ao estado real
4. Se **divergência** → Atualizar doc seguindo regras da seção 2
5. Registrar:

```markdown
📄 DOC IMPACT — Task #{id}
- Arquivos modificados: {lista}
- Docs afetados: {lista ou "Nenhum"}
- Docs atualizados: {lista ou "N/A"}
```

---

### 5. Doc Freshness Gate (Pré-Publicação)

> [!CAUTION]
> **GATE BLOQUEANTE:** Antes de publicar documentação (Flyee ou entrega),
> re-validar TODOS os docs gerados contra o código atual.
> Fases de implementação podem ter alterado comportamento documentado.

```markdown
⚠️ DOC FRESHNESS GATE

[ ] Re-executar CODE-TRUTH VALIDATION em CADA doc de `docs/flows/`
[ ] Re-executar CODE-TRUTH VALIDATION em `docs/design/TDD-*.md`
[ ] Divergências encontradas? → Docs atualizados com estado real
[ ] Divergências registradas no arquivo de progresso
[ ] Se nenhuma divergência → Registrar: "✅ Docs validados"

❌ Se QUALQUER item desmarcado → NÃO publicar
✅ TODOS marcados → Prosseguir
```

---

#### Historical Lesson — Code-Truth Validation

> 🔴 **FALHA (shop/ gateway):** Flow doc documentou "gateway = Pagar.me" quando o código
> implementava `Cielo.php`. Divergência descoberta apenas na fase cross-scope seguinte.
> **Causa raiz:** Agente documentou sem verificar enum `PaymentGatewayType.php`.

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Quando usar |
|----------|-------------|
| `/legacy-project` | Phase 4 (flow docs), Phase 2.5 (cross-scope), Gate 7B→8 (freshness) |
| `/document` | Antes de salvar qualquer flow doc |
| `/new-task` | Quando modificando código documentado |
| `/new-project` | Phase 5 (implementação com docs) |
