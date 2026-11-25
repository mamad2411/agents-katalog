---
name: configurar-auth
description: "Configura autenticação JWT com guards do Passport e validação de token. Use quando um serviço precisa proteger rotas com autenticação."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: configurar-auth

Adiciona **autenticação JWT** a um serviço NestJS existente: guard global, estratégia Passport, extração e validação do token, decorators de acesso público e tipagem do usuário autenticado no contexto da request.

**Agente:** dev-backend  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`

---

## Quando usar

- Ao adicionar proteção de endpoints em serviço que ainda não tem auth
- Ao integrar validação de JWT emitido por serviço de identidade externo
- Para adicionar controle de acesso por role após autenticação básica

---

## Pré-requisitos

- Serviço NestJS inicializado
- Estratégia de auth definida pelo arquiteto (JWT, API Key, OAuth)
- `JWT_SECRET` ou URL do JWKS definida

Esta skill cobre o padrão **JWT Bearer** — o mais comum entre serviços internos. Para OAuth/OIDC externo, adaptar o passo de validação do payload.

---

## Processo de execução

### Passo 1 — Instalar dependências

```bash
npm install @nestjs/passport @nestjs/jwt passport passport-jwt
npm install --save-dev @types/passport-jwt
```

### Passo 2 — Configurar JwtModule

`src/modules/auth/auth.module.ts`:
```typescript
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { JwtStrategy } from './strategies/jwt.strategy';
import { env } from '../../config/env.config';

@Module({
  imports: [
    PassportModule,
    JwtModule.register({
      secret: env.JWT_SECRET,
      signOptions: { expiresIn: '1h' },
    }),
  ],
  providers: [JwtStrategy],
  exports: [JwtModule],
})
export class AuthModule {}
```

### Passo 3 — Criar a estratégia JWT

`src/modules/auth/strategies/jwt.strategy.ts`:
```typescript
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { env } from '../../../config/env.config';

export interface JwtPayload {
  sub: string;       // userId
  email: string;
  roles: string[];
  iat: number;
  exp: number;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: env.JWT_SECRET,
    });
  }

  async validate(payload: JwtPayload) {
    if (!payload.sub) throw new UnauthorizedException();
    // Retorno é injetado em req.user
    return { userId: payload.sub, email: payload.email, roles: payload.roles };
  }
}
```

### Passo 4 — Criar JwtAuthGuard global

`src/common/guards/jwt-auth.guard.ts`:
```typescript
import { Injectable, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) return true;
    return super.canActivate(context);
  }
}
```

### Passo 5 — Criar decorator @Public()

`src/common/decorators/public.decorator.ts`:
```typescript
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

Uso:
```typescript
@Public()
@Get('health')
healthCheck() { return { status: 'ok' }; }
```

### Passo 6 — Criar decorator @CurrentUser()

`src/common/decorators/current-user.decorator.ts`:
```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export interface AuthenticatedUser {
  userId: string;
  email: string;
  roles: string[];
}

export const CurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext): AuthenticatedUser => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

Uso no controller:
```typescript
@Get('me')
getProfile(@CurrentUser() user: AuthenticatedUser) {
  return this.service.findById(user.userId);
}
```

### Passo 7 — Registrar guard globalmente no AppModule

```typescript
import { APP_GUARD } from '@nestjs/core';
import { JwtAuthGuard } from './common/guards/jwt-auth.guard';

@Module({
  imports: [AuthModule, ...],
  providers: [
    {
      provide: APP_GUARD,
      useClass: JwtAuthGuard,
    },
  ],
})
export class AppModule {}
```

Registrar globalmente significa que **todos os endpoints exigem token por padrão**. Endpoints públicos usam `@Public()`.

### Passo 8 — Adicionar JWT_SECRET ao env.config.ts

```typescript
const envSchema = z.object({
  // ...existente
  JWT_SECRET: z.string().min(32, 'JWT_SECRET deve ter pelo menos 32 caracteres'),
});
```

### Passo 9 — Adicionar guards de role (opcional)

`src/common/guards/roles.guard.ts`:
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

---

## Regras de segurança obrigatórias

- `JWT_SECRET` nunca em código-fonte — sempre via `process.env` validado (`seguranca.md §2`)
- `JWT_SECRET` mínimo 32 caracteres — validado no schema de env (`backend.md §6`)
- `ignoreExpiration: false` — nunca aceitar token expirado
- Nunca logar o token JWT completo — logar apenas `userId` do payload (`seguranca.md §2` + `backend.md §5`)
- Tokens não são armazenados em banco por este serviço — emissão é responsabilidade do serviço de identidade

---

## Checklist de conclusão

- [ ] `JwtStrategy` valida token e retorna `{ userId, email, roles }`
- [ ] `JwtAuthGuard` registrado globalmente no `AppModule`
- [ ] Decorator `@Public()` funciona em endpoints de saúde e auth
- [ ] Decorator `@CurrentUser()` disponível nos controllers
- [ ] `JWT_SECRET` validado no `env.config.ts` com mínimo de 32 chars
- [ ] Nenhum secret de token em código-fonte ou log
- [ ] Testes unitários do guard e da estratégia escritos
