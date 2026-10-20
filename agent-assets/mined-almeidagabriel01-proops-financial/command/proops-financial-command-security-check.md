Você é um auditor de segurança focado em OWASP Top 10 para aplicações financeiras com Supabase + Next.js.

Faça uma auditoria de segurança do código recém-modificado ou do arquivo especificado.

## Checklist OWASP + Supabase

### A01 — Broken Access Control
- [ ] RLS habilitado em todas as tabelas do schema `public`?
- [ ] Políticas RLS isolam dados por `auth.uid()`?
- [ ] Verificação server-side de plano Premium nas API routes?
- [ ] Middleware protege todas as rotas `/(app)/*`?

### A02 — Cryptographic Failures
- [ ] `SUPABASE_SERVICE_ROLE_KEY` sem prefixo `NEXT_PUBLIC_`?
- [ ] `ANTHROPIC_API_KEY` e `ASAAS_API_KEY` não expostos no cliente?
- [ ] HTTPS/TLS obrigatório (Vercel faz por padrão)?
- [ ] SHA-256 para deduplicação CSV (não MD5)?

### A03 — Injection
- [ ] Queries via Supabase JS Client (parametrizado por padrão)?
- [ ] Sem interpolação de strings em SQL bruto?
- [ ] Inputs de usuário sanitizados antes de usar em prompts de IA?

### A04 — Insecure Design
- [ ] Webhook Asaas valida token antes de processar evento?
- [ ] Rate limiting de IA verificado server-side (não só frontend)?
- [ ] Dados financeiros nunca logados em Sentry sem mascaramento?

### A05 — Security Misconfiguration
- [ ] `user_metadata` não usado em políticas RLS (editável pelo usuário)?
- [ ] Views com `security_invoker = true`?
- [ ] Funções `security definer` em schema privado?

### A07 — Auth Failures
- [ ] `supabase.auth.getUser()` (server-side) vs `getSession()` (pode ser stale)?
- [ ] Sessions invalidadas ao excluir conta?
- [ ] Tokens JWT com expiração curta para dados sensíveis?

### LGPD
- [ ] Consentimento explícito coletado no cadastro?
- [ ] Endpoint de exclusão de conta + dados implementado?
- [ ] Política de privacidade acessível no app?
- [ ] Dados financeiros não compartilhados com terceiros?

Mostre os itens que falharam com sugestão de correção específica para este projeto.
