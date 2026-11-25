---
name: integration-completeness
description: Valida que componentes interativos (botões, forms) estão conectados às funções. Previne gaps UI→Function.
---

# Integration Completeness Validation

> Garantir que componentes interativos estão **conectados** às funções, não apenas existem.

---

## 🎯 PROBLEMA

Testes podem passar verificando:
- ✅ Botão existe na tela
- ✅ Função funciona isoladamente

Mas **FALHAM** em verificar:
- ❌ Clicar no botão chama a função

---

## 🔗 QUANDO USAR?

| Workflow | Fase | Trigger |
|----------|------|---------|
| `/new-project` | Phase 5.2 | Após criar componentes UI |
| `/new-task` | Phase 3.7 | Se feature tem UI interativa |
| `/execute` | Durante implementação | Para cada componente |

---

## ✅ CHECKLIST DE VALIDAÇÃO

Para **CADA componente interativo**, verificar:

### Botões e Links
```markdown
[ ] onClick definido?
[ ] onClick chama função correta?
[ ] Função está importada?
[ ] Teste verifica clique → ação?
```

### Forms
```markdown
[ ] onSubmit definido?
[ ] onSubmit chama handler?
[ ] preventDefault chamado?
[ ] Teste verifica submit → ação?
```

### Inputs Controlados
```markdown
[ ] value ligado a state?
[ ] onChange atualiza state?
[ ] Teste verifica input → state?
```

---

## 🧪 TEMPLATE DE TESTE DE INTEGRAÇÃO

### Botão que chama função

```typescript
// ❌ INCOMPLETO - só verifica existência
it('should have a login button', () => {
    render(<LoginPage />);
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
});

// ✅ COMPLETO - verifica conexão
it('should call signIn when login button is clicked', async () => {
    const mockSignIn = vi.fn();
    render(<LoginPage onSignIn={mockSignIn} />);
    
    await userEvent.click(screen.getByRole('button', { name: /login/i }));
    
    expect(mockSignIn).toHaveBeenCalled();
});
```

### Form que submete dados

```typescript
// ❌ INCOMPLETO
it('should have a submit button', () => {
    render(<ContactForm />);
    expect(screen.getByRole('button', { name: /enviar/i })).toBeInTheDocument();
});

// ✅ COMPLETO
it('should call onSubmit with form data', async () => {
    const mockSubmit = vi.fn();
    render(<ContactForm onSubmit={mockSubmit} />);
    
    await userEvent.type(screen.getByLabelText(/email/i), 'test@test.com');
    await userEvent.click(screen.getByRole('button', { name: /enviar/i }));
    
    expect(mockSubmit).toHaveBeenCalledWith({ email: 'test@test.com' });
});
```

---

## 🚨 REGRAS CRÍTICAS

### Para Testes

| Tipo de Teste | O que verificar |
|---------------|-----------------|
| Existência | Componente renderiza |
| **Interação** | Clique/submit dispara ação |
| **Integração** | Ação produz efeito correto |

### Para Implementação

| Componente | Obrigatório |
|------------|-------------|
| `<button>` | `onClick` definido |
| `<a>` | `href` ou `onClick` |
| `<form>` | `onSubmit` definido |
| `<input>` | `onChange` se controlado |

---

## 📋 GATE DE VERIFICAÇÃO

Antes de marcar UI como completa:

```markdown
## Verificação de Integração

### Componentes Interativos
| Componente | Handler | Função | Teste |
|------------|---------|--------|-------|
| Botão Login Google | onClick | signInWithGoogle | ✅/❌ |
| Botão Login GitHub | onClick | signInWithGitHub | ✅/❌ |
| Form Newsletter | onSubmit | subscribeNewsletter | ✅/❌ |

### Checklist
- [ ] TODOS os handlers definidos?
- [ ] TODOS os handlers têm testes de clique?
- [ ] ZERO handlers vazios/placeholder?
```

---

## ⚠️ ANTI-PATTERNS

| ❌ Errado | ✅ Correto |
|-----------|-----------|
| `<button>Login</button>` | `<button onClick={handleLogin}>Login</button>` |
| `onClick={() => {}}` | `onClick={signIn}` |
| Teste só de existência | Teste de existência + interação |
| Handler sem importar função | Handler importa e chama função |

---

## 🔍 DETECÇÃO RÁPIDA

Buscar no código por componentes potencialmente desconectados:

```bash
# Botões sem onClick
grep -r "<button" --include="*.tsx" | grep -v "onClick"

# Forms sem onSubmit  
grep -r "<form" --include="*.tsx" | grep -v "onSubmit"

# Handlers vazios
grep -r "onClick={() => {}}" --include="*.tsx"
grep -r 'onClick={() => ""}' --include="*.tsx"
```

---

## 🔍 Production Mock Detection (DATA INTEGRATION SCAN)

> [!CAUTION]
> Before marking implementation as complete, the agent MUST verify that NO production
> page/route contains mock data.

**Mandatory scan (run for EACH page/route in production path):**

```markdown
⚠️ DATA INTEGRATION SCAN — Implementation Complete?

For EACH file in src/app/ (pages and routes):
[ ] Pattern: `mock` (case insensitive) — ZERO occurrences?
[ ] Pattern: `() => {}` or `() => { }` — ZERO noop callbacks?
[ ] Pattern: `// TODO` in business logic — ZERO placeholders?
[ ] Pattern: `// MVP:` — ZERO MVP flags?

If ANY pattern found:
→ LIST affected files
→ FIX before marking implementation as complete
→ Connect to database / implement real logic

✅ ZERO mock patterns in production → CLEARED
```

**Recommended scan commands:**

```bash
grep -rn "mock" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "() => {}" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "// TODO" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "// MVP" src/app/ --include="*.tsx" --include="*.ts" -l
```

> **Historical Lesson:** Phase 5.2 had a gate "Components connected to backend" but no verification
> mechanism. The agent marked it ✅ without checking. 7 files had `mockData`, `// MVP: mock response`,
> and `onApprove={() => {}}` in production code.

---

> **Regra de Ouro:** Se o usuário pode clicar, o teste deve clicar.
