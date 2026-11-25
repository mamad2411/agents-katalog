---
name: tpl-dominio-autenticacao-enterprise
description: Template do pack (dominio/04-autenticacao-enterprise.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/04-autenticacao-enterprise.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Autenticação Enterprise (OAuth2, SSO, MFA)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/04-autenticacao-enterprise.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Auth enterprise vai muito além de username/password com bcrypt. SAML SSO para clientes
corporativos, WebAuthn para segurança alta, TOTP como segundo fator — cada um tem fluxo
específico com armadilhas próprias. A maioria dos bugs de segurança em auth não é
sofisticada: é token não expirado, state CSRF não validado, session não invalidada no logout.

## STACK ASSUMPTIONS
- Identity: Auth0, Keycloak, Okta, ou implementação própria via Passport.js / Spring Security
- Token: JWT (RS256 preferivelmente, não HS256)
- Session: Redis com TTL (não JWT stateless puro para apps que precisam de revogação)
- MFA: speakeasy/otplib para TOTP; @simplewebauthn para WebAuthn
- DB: PostgreSQL para user store, refresh tokens, device sessions

## CORE CONCEPTS
- **OAuth2 Authorization Code + PKCE**: flow recomendado para SPAs e mobile
- **SAML 2.0**: protocolo XML usado por enterprise SSO (Okta, Azure AD, Google Workspace)
- **TOTP**: Time-based One-Time Password (Google Authenticator, Authy)
- **WebAuthn / FIDO2**: autenticação por biometria ou hardware key (sem senha)
- **JWT Rotation**: access token de vida curta (15min) + refresh token de vida longa
- **Device Fingerprint**: hash de user-agent, screen, timezone para detectar novo dispositivo
- **Account Lockout**: bloqueio após N tentativas falhas com backoff exponencial
- **PKCE**: Proof Key for Code Exchange — previne auth code interception attack

## ARCHITECTURE RULES

### JWT Strategy
- Access token: RS256, expiry 15 minutos, payload mínimo (sub, roles, iat, exp)
- Refresh token: opaco (UUID v4), armazenado em DB, expiry 30 dias, rotacionado a cada uso
- Nunca armazenar access token em localStorage — usar httpOnly cookie ou memory
- Refresh token em httpOnly cookie + CSRF token em header
- Manter blacklist de revogados em Redis (para logout forçado)

### OAuth2 / SAML SSO
- SEMPRE validar `state` parameter em callback OAuth2 (previne CSRF)
- PKCE obrigatório para public clients (SPA, mobile)
- SAML: validar assinatura do IdP, validar `NotBefore`/`NotOnOrAfter`, validar `Audience`
- Mapear claims externos para roles internos via mapeamento configurável (não hardcoded)
- Armazenar `provider` + `provider_user_id` na tabela de users para SSO linking

### MFA Flow
- TOTP setup: gerar secret → exibir QR → exigir verificação antes de ativar
- Recovery codes: gerar 10 no setup, armazenar com hash (bcrypt), uso único
- WebAuthn: armazenar `credentialId`, `publicKey`, `counter` no banco
- Verificar `counter` no WebAuthn para detectar clonagem de authenticator
- MFA bypass de emergência: requer aprovação de admin com audit log

### Session Management
- Session ID: 32 bytes aleatórios, armazenar hash no servidor
- Redis com TTL: renovar TTL a cada request ativo
- Logout: deletar session do Redis + invalidar refresh tokens do device
- Logout global: invalidar TODAS as sessions do usuário (campo `sessions_invalidated_at`)
- Device sessions: listar dispositivos ativos, permitir revogar individualmente

### Account Security
- Lockout: 5 tentativas falhas → bloqueio 15min (backoff: 2x a cada nova falha)
- Lockout em Redis por `userId` E por `IP` (previne user enumeration via timing)
- Notificar por email: novo dispositivo, login em país diferente, MFA desativado
- Senhas: min 12 chars, breached password check (Have I Been Pwned API)
- Password history: não permitir reusar últimas 5 senhas

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /auth/login | Verificar credenciais → checar lockout → emitir tokens → criar session |
| POST /auth/refresh | Validar refresh token → rotacionar → emitir novo access token |
| POST /auth/logout | Invalidar session → revogar refresh token → limpar cookies |
| GET /auth/oauth/:provider | Gerar state + PKCE verifier → redirect ao IdP |
| GET /auth/oauth/:provider/callback | Validar state → trocar code por tokens → mapear user → emitir JWT |
| POST /auth/mfa/totp/setup | Gerar secret → retornar QR URL (não ativar ainda) |
| POST /auth/mfa/totp/verify-setup | Verificar TOTP de confirmação → ativar MFA → gerar recovery codes |
| POST /auth/mfa/totp/challenge | Verificar TOTP no login step-up → emitir token com MFA claim |
| POST /auth/mfa/webauthn/register | Gerar challenge → retornar PublicKeyCredentialCreationOptions |
| POST /auth/mfa/webauthn/verify-register | Verificar credential → armazenar publicKey + counter |
| POST /auth/mfa/webauthn/challenge | Gerar assertion challenge para login |
| POST /auth/password/reset-request | Rate limit → enviar magic link (não expor se email existe) |
| GET /sessions | Listar devices ativos do usuário com last_seen |
| DELETE /sessions/:id | Revogar session específica (logout remoto) |

## CRITICAL RULES
1. Nunca logar passwords, tokens ou secrets — nem em debug
2. `state` OAuth2 obrigatório e verificado no callback (CSRF protection)
3. Refresh token rotacionado a cada uso — detectar reuse → invalidar toda família
4. Respostas de auth não devem diferenciar "usuário não existe" de "senha incorreta"
5. Lockout por IP E por userId — não apenas um deles
6. TOTP não ativar sem verificação confirmada pelo usuário
7. WebAuthn counter: rejeitar se counter novo ≤ counter armazenado (clone detection)
8. RS256 para JWT em vez de HS256 (chave assimétrica — serviços validam sem ter signing key)
9. Session invalidada no backend ao logout — JWT expirado não é logout
10. Recovery codes: hash com bcrypt, marcar como usados, nunca exibir após setup

## COMMON PITFALLS

### ❌ State OAuth2 ignorado
```javascript
// ERRADO: vulnerável a CSRF
app.get('/oauth/callback', async (req) => {
  const { code } = req.query; // ignora state
  const tokens = await exchangeCode(code);
});

// CORRETO
app.get('/oauth/callback', async (req) => {
  const { code, state } = req.query;
  const storedState = await redis.get(`oauth_state:${req.session.id}`);
  if (state !== storedState) throw new Error('CSRF detected');
  const tokens = await exchangeCode(code);
});
```

### ❌ JWT stateless sem revogação
```javascript
// ERRADO: logout apenas no client — token ainda válido por 8h
res.clearCookie('token'); // no servidor, token ainda aceito

// CORRETO: session + JWT de vida curta
await redis.del(`session:${sessionId}`); // logout real
// Access token expira em 15min (dano limitado)
```

### ❌ Diferenciar erros de auth
```javascript
// ERRADO: user enumeration vulnerability
if (!user) return res.status(404).json({ error: 'User not found' });
if (!validPassword) return res.status(401).json({ error: 'Wrong password' });

// CORRETO: mensagem genérica + timing constante
await bcrypt.compare(password, user?.hash ?? '$2b$10$invalidhashtopreventtiming');
return res.status(401).json({ error: 'Invalid credentials' });
```

## QUALITY GATES
- [ ] State CSRF validado em todo callback OAuth2
- [ ] Refresh token rotacionado a cada uso com detecção de reuse
- [ ] Access token com vida ≤ 15 minutos
- [ ] Logout invalida session no servidor (não apenas no cliente)
- [ ] MFA exige verificação antes de ativar
- [ ] WebAuthn verifica counter para detectar clonagem
- [ ] Lockout por userId + IP com backoff exponencial
- [ ] Recovery codes com hash no banco, uso único
- [ ] Respostas de auth não diferenciam tipo de erro (user enumeration)
- [ ] Nenhum secret ou token em logs

## FORBIDDEN
- HS256 para JWT em sistemas com múltiplos serviços
- localStorage para armazenar access tokens (XSS risk)
- State OAuth2 omitido ou não verificado
- Logout apenas client-side com JWT de longa duração
- Mensagens de erro diferenciando "usuário não existe" de "senha incorreta"
- Ativar TOTP/WebAuthn sem step de verificação
- Refresh token de uso único sem detecção de replaying
