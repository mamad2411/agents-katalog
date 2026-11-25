---
name: clerk-auth
description: "Padrões especializados para implementação de autenticação Clerk, middleware, organizações, webhooks e sincronização de usuários. Use quando: adicionar autenticação, auth do Clerk, autenticação de usuário, sign in, sign up."
source: vibeship-spawner-skills (Apache 2.0)
---

# Autenticação Clerk

## Padrões

### Configuração Next.js App Router

Configuração completa do Clerk para Next.js 14/15 App Router.

Inclui ClerkProvider, variáveis de ambiente e componentes
básicos de sign-in/sign-up.

Componentes-chave:
- ClerkProvider: Envolve o app fornecendo contexto de autenticação
- <SignIn />, <SignUp />: Formulários de autenticação pré-construídos
- <UserButton />: Menu de usuário com gerenciamento de sessão


### Proteção de Rotas com Middleware

Proteja rotas usando clerkMiddleware e createRouteMatcher.

Melhores práticas:
- Arquivo middleware.ts único na raiz do projeto
- Use createRouteMatcher para grupos de rotas
- auth.protect() para proteção explícita
- Centralize toda lógica de autenticação no middleware


### Autenticação em Server Components

Acesse o estado de autenticação em Server Components usando auth() e currentUser().

Funções-chave:
- auth(): Retorna userId, sessionId, orgId, claims
- currentUser(): Retorna objeto User completo
- Ambas requerem clerkMiddleware configurado


## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | crítica | Veja documentação |
| Problema | alta | Veja documentação |
| Problema | alta | Veja documentação |
| Problema | alta | Veja documentação |
| Problema | média | Veja documentação |
| Problema | média | Veja documentação |
| Problema | média | Veja documentação |
| Problema | média | Veja documentação |