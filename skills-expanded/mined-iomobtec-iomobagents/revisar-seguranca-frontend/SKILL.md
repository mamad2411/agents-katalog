---
name: revisar-seguranca-frontend
description: "Checklist shift-left de segurança para React — XSS, tokens em storage, CSRF e atributo rel noopener — como parte do DoD do dev. Use quando o dev-frontend ou o dev-security valida segurança antes do merge."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-seguranca-frontend

Checklist shift-left de segurança para aplicações React, executado pelo próprio dev-frontend como parte do DoD antes de abrir o PR.

**Agente:** `dev-frontend`, `dev-security`  
**Output:** Checklist preenchido + lista de itens a corrigir antes do PR (se houver).  
**Referências rápidas:** `References/security-checklist.md`

---

## Quando usar

Antes de abrir PR de frontend. O próprio `dev-frontend` executa este checklist como parte do DoD — não precisa esperar o `dev-security` para validar o básico.

---

## Contexto

Esta skill cobre os vetores de ataque mais comuns em aplicações React: XSS, exposição de dados sensíveis em storage e logs, e CSRF em aplicações com autenticação por cookie. O `dev-security` audita vetores mais complexos — esta skill é a responsabilidade mínima do próprio dev-frontend.

---

## Checklist

Execute cada item e marque: ✅ Conforme | ⛔ Violação (corrija antes de PR)

### §6 — XSS (Cross-Site Scripting)

- [ ] **Sem `dangerouslySetInnerHTML` sem sanitização:** Toda ocorrência de `dangerouslySetInnerHTML` usa `DOMPurify.sanitize()` com allowlist de tags explícita.
- [ ] **Links com href dinâmico validam protocolo:** URLs vindas de dados externos verificam `startsWith('https://')` antes de usar em `href`.
- [ ] **Sem `innerHTML` manual:** Não usar `element.innerHTML`, `document.write()` ou `insertAdjacentHTML()` com conteúdo do usuário.
- [ ] **Sem `eval()` ou `Function()` com dados externos:** Conteúdo de usuário nunca é executado como código.

```tsx
// ✅ Correto — React escapa por padrão
<p>{userDescription}</p>

// ✅ Correto — HTML necessário com sanitização
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(richText, { ALLOWED_TAGS: ['b', 'i', 'em', 'p', 'ul', 'li'] })
}} />

// ✅ Correto — href validado
const safeUrl = externalUrl?.startsWith('https://') ? externalUrl : '#';
<a href={safeUrl} rel="noopener noreferrer">Link</a>

// ⛔ Violação
<div dangerouslySetInnerHTML={{ __html: userInput }} />
<a href={user.website}>site</a>  // website pode ser javascript:alert(1)
```

### §3 — Exposição de dados sensíveis no cliente

- [ ] **Tokens não em localStorage/sessionStorage:** Access tokens ficam em memória (variável de estado ou closure). Refresh token fica em cookie httpOnly gerenciado pelo servidor — nunca no browser storage.
- [ ] **Dados sensíveis não persistidos desnecessariamente:** CPF, número de cartão, senha não ficam em `useState` além do formulário. Limpar após submit.
- [ ] **Sem `console.log` com PII ou tokens:** Nenhum log de debug com dados pessoais, tokens de autenticação ou campos de cartão.
- [ ] **Campos de formulário sensíveis sem autocomplete inadequado:** Campos de senha usam `autoComplete="current-password"` ou `"new-password"`. Campos de cartão usam `autoComplete="cc-number"`.

```tsx
// ✅ Correto — token em memória (React Query / SWR gerenciam)
const { data: user } = useQuery({ queryKey: ['me'], queryFn: fetchCurrentUser });

// ⛔ Violação
localStorage.setItem('access_token', token);
sessionStorage.setItem('user_cpf', cpf);
console.log('user data', { cpf, cartao, senha });
```

### §7 — CSRF

- [ ] **Se autenticação é via JWT no header `Authorization`:** Nenhuma ação necessária — JWT no header é naturalmente protegido contra CSRF.
- [ ] **Se autenticação é via cookie de sessão:** Verificar que o backend configurou `SameSite=strict` ou `SameSite=lax` no cookie. Se não, reportar ao `dev-backend`.
- [ ] **Links externos com `rel="noopener noreferrer"`:** Todo `<a target="_blank">` tem `rel="noopener noreferrer"` para evitar tabnapping.

```tsx
// ✅ Correto
<a href="https://externo.com" target="_blank" rel="noopener noreferrer">
  Ver mais
</a>

// ⛔ Violação
<a href={externalLink} target="_blank">Ver mais</a>  // sem rel — tabnapping possível
```

### §3 — Dados sensíveis em requisições

- [ ] **Sem dados sensíveis em query string:** CPF, tokens, dados de cartão nunca são passados como parâmetros de URL (`?cpf=123`). Usar body de POST.
- [ ] **Sem dados sensíveis em logs de erro:** Handlers de erro não logam o request completo se ele contém dados sensíveis.
- [ ] **Headers Authorization não logados:** Interceptors de HTTP client não logam headers de autenticação.

```tsx
// ✅ Correto
const { data } = await api.post('/validate', { cpf });

// ⛔ Violação
const { data } = await api.get(`/validate?cpf=${cpf}`);  // CPF em URL → logs, history, referer
```

### Segurança de dependências de UI

- [ ] **DOMPurify instalado se usar `dangerouslySetInnerHTML`:** `npm list dompurify` confirma instalação.
- [ ] **Sem bibliotecas de UI que injetam HTML sem sanitização:** Verificar se bibliotecas de rich text editor ou markdown renderer sanitizam output.

---

## Como usar o resultado

**Todos os itens ✅:** Registrar no checklist de DoD e abrir PR.

**Algum item ⛔:** Corrigir antes de abrir PR. O `dev-security` vai identificar os mesmos itens na auditoria pré-merge.

**Dúvida sobre um item:** Consultar `Guardrails/appsec.md §6` (XSS) ou `§3` (exposição de dados) para exemplos detalhados.

---

## Formato de inclusão no DoD

Adicionar ao checklist de conclusão do `dev-frontend`:

```markdown
### Checklist de segurança (revisar-seguranca-frontend)
- [x] §6 XSS — sem dangerouslySetInnerHTML sem DOMPurify, href validados
- [x] §3 Exposição — tokens em memória (não em storage), sem PII em logs
- [x] §7 CSRF — links externos com rel="noopener noreferrer"
- [x] §3 Requisições — dados sensíveis no body, nunca em query string
```
