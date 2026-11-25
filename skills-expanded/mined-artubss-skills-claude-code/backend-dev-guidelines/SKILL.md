---
name: backend-dev-guidelines
description: Guia completo de desenvolvimento backend para microserviços Node.js/Express/TypeScript. Use ao criar routes, controllers, services, repositories, middleware ou trabalhar com Express APIs, acesso a banco de dados com Prisma, rastreamento de erros com Sentry, validação com Zod, unifiedConfig, injeção de dependências ou padrões assíncronos. Cobre arquitetura em camadas (routes → controllers → services → repositories), padrão BaseController, tratamento de erros, monitoramento de performance, estratégias de testes e migração de padrões legados.
---

# Diretrizes de Desenvolvimento Backend

## Propósito

Estabelecer consistência e boas práticas em microserviços backend (blog-api, auth-service, notifications-service) usando padrões modernos de Node.js/Express/TypeScript.

## Quando Usar Esta Skill

Ativa automaticamente ao trabalhar em:
- Criar ou modificar routes, endpoints, APIs
- Construir controllers, services, repositories
- Implementar middleware (auth, validação, tratamento de erros)
- Operações de banco de dados com Prisma
- Rastreamento de erros com Sentry
- Validação de entrada com Zod
- Gerenciamento de configuração
- Testes e refatoração backend

---

## Início Rápido

### Checklist de Nova Feature Backend

- [ ] **Route**: Definição limpa, delegue ao controller
- [ ] **Controller**: Estenda BaseController
- [ ] **Service**: Lógica de negócio com DI
- [ ] **Repository**: Acesso a dados (se complexo)
- [ ] **Validation**: Schema Zod
- [ ] **Sentry**: Rastreamento de erros
- [ ] **Tests**: Testes unitários + integração
- [ ] **Config**: Use unifiedConfig

### Checklist de Novo Microserviço

- [ ] Estrutura de diretórios (veja [architecture-overview.md](architecture-overview.md))
- [ ] instrument.ts para Sentry
- [ ] Setup unifiedConfig
- [ ] Classe BaseController
- [ ] Stack de middleware
- [ ] Error boundary
- [ ] Framework de testes

---

## Visão Geral da Arquitetura

### Arquitetura em Camadas

```
Requisição HTTP
    ↓
Routes (roteamento apenas)
    ↓
Controllers (manipulação de requisição)
    ↓
Services (lógica de negócio)
    ↓
Repositories (acesso a dados)
    ↓
Banco de Dados (Prisma)
```

**Princípio Chave:** Cada camada tem UMA responsabilidade.

Veja [architecture-overview.md](architecture-overview.md) para detalhes completos.

---

## Estrutura de Diretórios

```
service/src/
├── config/              # UnifiedConfig
├── controllers/         # Manipuladores de requisição
├── services/            # Lógica de negócio
├── repositories/        # Acesso a dados
├── routes/              # Definições de rota
├── middleware/          # Middleware Express
├── types/               # Tipos TypeScript
├── validators/          # Schemas Zod
├── utils/               # Utilitários
├── tests/               # Testes
├── instrument.ts        # Sentry (PRIMEIRA IMPORTAÇÃO)
├── app.ts               # Setup Express
└── server.ts            # Servidor HTTP
```

**Convenções de Nomenclatura:**
- Controllers: `PascalCase` - `UserController.ts`
- Services: `camelCase` - `userService.ts`
- Routes: `camelCase + Routes` - `userRoutes.ts`
- Repositories: `PascalCase + Repository` - `UserRepository.ts`

---

## Princípios Principais (7 Regras-Chave)

### 1. Routes Apenas Roteia, Controllers Controlam

```typescript
// ❌ NUNCA: Lógica de negócio em routes
router.post('/submit', async (req, res) => {
    // 200 linhas de lógica
});

// ✅ SEMPRE: Delegue ao controller
router.post('/submit', (req, res) => controller.submit(req, res));
```

### 2. Todos os Controllers Estendem BaseController

```typescript
export class UserController extends BaseController {
    async getUser(req: Request, res: Response): Promise<void> {
        try {
            const user = await this.userService.findById(req.params.id);
            this.handleSuccess(res, user);
        } catch (error) {
            this.handleError(error, res, 'getUser');
        }
    }
}
```

### 3. Todos os Erros para Sentry

```typescript
try {
    await operation();
} catch (error) {
    Sentry.captureException(error);
    throw error;
}
```

### 4. Use unifiedConfig, NUNCA process.env

```typescript
// ❌ NUNCA
const timeout = process.env.TIMEOUT_MS;

// ✅ SEMPRE
import { config } from './config/unifiedConfig';
const timeout = config.timeouts.default;
```

### 5. Valide Toda Entrada com Zod

```typescript
const schema = z.object({ email: z.string().email() });
const validated = schema.parse(req.body);
```

### 6. Use Padrão Repository para Acesso a Dados

```typescript
// Service → Repository → Database
const users = await userRepository.findActive();
```

### 7. Testes Abrangentes Obrigatórios

```typescript
describe('UserService', () => {
    it('should create user', async () => {
        expect(user).toBeDefined();
    });
});
```

---

## Importações Comuns

```typescript
// Express
import express, { Request, Response, NextFunction, Router } from 'express';

// Validação
import { z } from 'zod';

// Banco de Dados
import { PrismaClient } from '@prisma/client';
import type { Prisma } from '@prisma/client';

// Sentry
import * as Sentry from '@sentry/node';

// Config
import { config } from './config/unifiedConfig';

// Middleware
import { SSOMiddlewareClient } from './middleware/SSOMiddleware';
import { asyncErrorWrapper } from './middleware/errorBoundary';
```

---

## Referência Rápida

### Códigos de Status HTTP

| Código | Caso de Uso |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado |
| 400 | Requisição Inválida |
| 401 | Não Autorizado |
| 403 | Proibido |
| 404 | Não Encontrado |
| 500 | Erro no Servidor |

### Templates de Service

**Blog API** (✅ Matura) - Use como template para REST APIs
**Auth Service** (✅ Matura) - Use como template para padrões de autenticação

---

## Antipadrões a Evitar

❌ Lógica de negócio em routes
❌ Uso direto de process.env
❌ Tratamento de erro faltando
❌ Sem validação de entrada
❌ Prisma direto em todo lugar
❌ console.log em vez de Sentry

---

## Guia de Navegação

| Preciso... | Leia isto |
|------------|-----------|
| Entender arquitetura | [architecture-overview.md](architecture-overview.md) |
| Criar routes/controllers | [routing-and-controllers.md](routing-and-controllers.md) |
| Organizar lógica de negócio | [services-and-repositories.md](services-and-repositories.md) |
| Validar entrada | [validation-patterns.md](validation-patterns.md) |
| Adicionar rastreamento de erros | [sentry-and-monitoring.md](sentry-and-monitoring.md) |
| Criar middleware | [middleware-guide.md](middleware-guide.md) |
| Acesso ao banco de dados | [database-patterns.md](database-patterns.md) |
| Gerenciar config | [configuration.md](configuration.md) |
| Lidar com async/erros | [async-and-errors.md](async-and-errors.md) |
| Escrever testes | [testing-guide.md](testing-guide.md) |
| Ver exemplos | [complete-examples.md](complete-examples.md) |

---

## Arquivos de Recurso

### [architecture-overview.md](architecture-overview.md)
Arquitetura em camadas, ciclo de vida de requisição, separação de responsabilidades

### [routing-and-controllers.md](routing-and-controllers.md)
Definições de route, BaseController, tratamento de erros, exemplos

### [services-and-repositories.md](services-and-repositories.md)
Padrões de service, DI, padrão repository, cache

### [validation-patterns.md](validation-patterns.md)
Schemas Zod, validação, padrão DTO

### [sentry-and-monitoring.md](sentry-and-monitoring.md)
Inicialização Sentry, captura de erros, monitoramento de performance

### [middleware-guide.md](middleware-guide.md)
Auth, auditoria, error boundaries, AsyncLocalStorage

### [database-patterns.md](database-patterns.md)
PrismaService, repositories, transações, otimização

### [configuration.md](configuration.md)
UnifiedConfig, configs de ambiente, secrets

### [async-and-errors.md](async-and-errors.md)
Padrões assíncronos, erros customizados, asyncErrorWrapper

### [testing-guide.md](testing-guide.md)
Testes unitários/integração, mocking, cobertura

### [complete-examples.md](complete-examples.md)
Exemplos completos, guia de refatoração

---

## Skills Relacionadas

- **database-verification** - Verificar nomes de coluna e consistência de schema
- **error-tracking** - Padrões de integração Sentry
- **skill-developer** - Meta-skill para criar e gerenciar skills

---

**Status da Skill**: COMPLETA ✅
**Contagem de Linhas**: < 500 ✅
**Divulgação Progressiva**: 11 arquivos de recurso ✅