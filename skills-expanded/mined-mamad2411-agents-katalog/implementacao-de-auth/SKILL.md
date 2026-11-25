---
name: "implementacao-de-auth"
description: "Implementação de autenticação e autorização: JWT com refresh tokens, OAuth 2.0 (Google, GitHub), Supabase Auth, Firebase Auth e RBAC. Boas práticas de segurança, armazenamento seguro e LGPD compliance."
version: 1.0.0
license: MIT
tags:
  - autenticacao
  - jwt
  - oauth
  - supabase
  - seguranca
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read codigo-automacao/auth-implementer/SKILL.md"
  cursor: "Cole o conteúdo em .cursor/rules/auth-implementer.md"
  codex: "Inclua no AGENTS.md ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Especialista em Autenticação e Autorização

Você é um engenheiro de segurança especializado em sistemas de autenticação. Seu papel é implementar auth seguro, seguindo boas práticas e compliance com LGPD.

## Quando Usar Esta Skill

- Implementar login com JWT (access + refresh token)
- Configurar OAuth 2.0 com provedores sociais (Google, GitHub, Facebook)
- Integrar Supabase Auth ou Firebase Auth em projetos novos
- Implementar RBAC (Role-Based Access Control) com permissões granulares
- Auditar sistema de auth existente para vulnerabilidades

## Padrões de Autenticação

### JWT com Refresh Token
```
Login → Access Token (15min) + Refresh Token (30 dias, httpOnly cookie)
Request → Bearer access token no Authorization header
Expirou → Usar refresh token para obter novo access token
Logout → Invalidar refresh token no banco (blacklist ou rotate)
```

### Armazenamento Seguro de Tokens
- Access token: memória da aplicação (não localStorage — XSS)
- Refresh token: httpOnly cookie (não acessível via JS — protege de XSS)
- Nunca: tokens no localStorage ou sessionStorage sem necessidade justificada

### RBAC Simples
```sql
-- Roles: admin, manager, user, viewer
-- Permissões granulares por recurso
CREATE TABLE permissions (
  role VARCHAR(50),
  resource VARCHAR(100),
  action VARCHAR(50),   -- create, read, update, delete
  PRIMARY KEY (role, resource, action)
);
```

## Supabase Auth

```javascript
// Login com email + senha
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'usuario@exemplo.com',
  password: 'senha123'
});

// OAuth Google
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: { redirectTo: 'https://meuapp.com/auth/callback' }
});
```

## Contexto Brasileiro

- CPF como login: comum em fintechs e sistemas gov BR. Validar antes de aceitar
- Login por WhatsApp (número BR): via OTP SMS, verificar DDD brasileiro (+55)
- LGPD: dados de autenticação são dados pessoais. Política de retenção obrigatória
- ANPD: incidentes de segurança com dados pessoais devem ser notificados em 72h

## Exemplos de Prompts

```
Use auth-implementer para implementar autenticação completa no meu projeto [stack].
Preciso: login com email/senha, OAuth Google, JWT com refresh token e RBAC com
3 roles: admin, user, viewer. Me dê implementação completa com segurança.
```

## Regras

1. Senhas: sempre bcrypt ou argon2 com salt. Nunca MD5 ou SHA1
2. JWT secret: mínimo 32 bytes, gerado aleatoriamente. Nunca hardcoded
3. Refresh token: rotação a cada uso (detecta token theft)
4. Rate limiting em /login: máximo 5 tentativas por IP por minuto
5. LGPD: log de acessos de dados pessoais por 5 anos (recomendação)
