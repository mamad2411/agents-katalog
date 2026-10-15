---
name: nodejs-security
description: "Seguridad en aplicaciones Node.js. Cubre Helmet 8, CORS, rate limiting, JWT/OAuth2, validación de input, SQL injection, CSRF, dependency audit (npm audit), secrets management (.env + Zod), Node.js security releases y hardening. Actívala al asegurar APIs, implementar autenticación, o auditar dependencias."
disable-model-invocation: true
---

# Node.js Security

Guía de seguridad para aplicaciones Node.js. Defensa en profundidad: cada capa valida, nada confía en la anterior.

---

## HTTP Security Headers — Helmet 8

```typescript
import helmet from 'helmet';

// Configuración recomendada para API REST (sin CSP para UIs)
app.use(helmet());

// Equivale a:
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:'],
  },
}));
app.use(helmet.crossOriginEmbedderPolicy());
app.use(helmet.crossOriginOpenerPolicy());
app.use(helmet.crossOriginResourcePolicy({ policy: 'same-origin' }));
app.use(helmet.referrerPolicy({ policy: 'strict-origin-when-cross-origin' }));
app.use(helmet.strictTransportSecurity());
app.use(helmet.xContentTypeOptions());
app.use(helmet.xFrameOptions({ action: 'deny' }));
app.use(helmet.xPermittedCrossDomainPolicies());
app.use(helmet.dnsPrefetchControl({ allow: false }));
```

---

## CORS

```typescript
import cors from 'cors';

// ✅ Explícito — nunca '*'
app.use(cors({
  origin: process.env.CORS_ORIGIN?.split(',') ?? ['http://localhost:5173'],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

---

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// General
app.use(rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: { message: 'Too many requests', code: 'RATE_LIMIT' } },
}));

// Auth endpoints más restrictivos
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true, // Solo fallos consumen el límite
});

app.post('/api/auth/login', authLimiter, loginHandler);
```

---

## JWT — Autenticación

```typescript
import jwt from 'jsonwebtoken';
import { z } from 'zod';

// ✅ Claims tipados
const TokenPayloadSchema = z.object({
  sub: z.string(),       // subject (userId)
  role: z.string(),
  iat: z.number(),
  exp: z.number(),
});

type TokenPayload = z.infer<typeof TokenPayloadSchema>;

// Generar
function signToken(userId: string, role: string): string {
  return jwt.sign(
    { sub: userId, role },
    process.env.JWT_SECRET!,
    {
      expiresIn: '15m',
      algorithm: 'HS256',
      issuer: 'miapp-api',
    },
  );
}

// Refresh token (más larga duración, almacenar en httpOnly cookie)
function signRefreshToken(userId: string): string {
  return jwt.sign(
    { sub: userId, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d', algorithm: 'HS256' },
  );
}

// Verificar
function verifyToken(token: string): TokenPayload {
  const decoded = jwt.verify(token, process.env.JWT_SECRET!, {
    algorithms: ['HS256'],
    issuer: 'miapp-api',
  });
  return TokenPayloadSchema.parse(decoded);
}

// Auth middleware
export async function auth(req: Request, res: Response, next: NextFunction) {
  try {
    const header = req.headers.authorization;
    if (!header?.startsWith('Bearer ')) {
      throw new AppError('Missing token', 401, 'UNAUTHORIZED');
    }

    const payload = verifyToken(header.slice(7));
    req.user = { id: payload.sub, role: payload.role };
    next();
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      next(new AppError('Token expired', 401, 'TOKEN_EXPIRED'));
    } else {
      next(new AppError('Invalid token', 401, 'UNAUTHORIZED'));
    }
  }
}
```

---

## Input Validation — Zod en todas las fronteras

```typescript
// Body, query params, path params — todo validado
const CreateOrderSchema = z.object({
  customerId: z.string().min(1).max(50),
  amount: z.number().positive().max(9_999_999),
  status: z.enum(['pending', 'confirmed']).optional(),
});

// Zod refine para validaciones cross-field
const TransferSchema = z.object({
  fromAccount: z.string(),
  toAccount: z.string(),
  amount: z.number().positive(),
}).refine(data => data.fromAccount !== data.toAccount, {
  message: 'Cannot transfer to the same account',
  path: ['toAccount'],
});

// Sanitizar strings
const SafeStringSchema = z.string()
  .trim()
  .min(1)
  .max(1000)
  .transform(s => s.replace(/<[^>]*>/g, '')); // Strip HTML tags
```

---

## SQL Injection

```typescript
// ❌ NUNCA concatenar input en SQL
const query = `SELECT * FROM orders WHERE customer_id = '${customerId}'`;

// ✅ Siempre parametrizado
// Con Prisma
const orders = await prisma.order.findMany({
  where: { customerId },
});

// Con Drizzle
const orders = await db.select().from(ordersTable)
  .where(eq(ordersTable.customerId, customerId));

// Con raw SQL parametrizado
import { sql } from 'drizzle-orm';
const orders = await db.execute(sql`
  SELECT * FROM orders WHERE customer_id = ${customerId}
`); // Drizzle parametriza automáticamente
```

---

## CSRF Protection

```typescript
import csrf from 'csurf';
import cookieParser from 'cookie-parser';

// Para apps con cookies (no APIs stateless con JWT Bearer)
app.use(cookieParser());

const csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
  },
});

// Ruta que expone el token
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Proteger mutaciones
app.post('/api/orders', csrfProtection, createOrder);
```

---

## Dependency Audit

```bash
# Auditar vulnerabilidades
npm audit

# Actualizar dependencias vulnerables
npm audit fix

# CI: fallar si hay vulnerabilidades altas o críticas
npm audit --audit-level=high

# Snyk (análisis más profundo)
npx snyk test
npx snyk monitor
```

```yaml
# GitHub Actions: audit automático
- name: npm audit
  run: npm audit --audit-level=high
```

---

## Secrets Management

```typescript
import { z } from 'zod';
import 'dotenv/config';

// ✅ Validar todas las env vars al inicio
const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),
  CORS_ORIGIN: z.string(),
  STRIPE_API_KEY: z.string().startsWith('sk_'),
});

export const env = EnvSchema.parse(process.env);
// Si falta alguna variable → la app no arranca.

// Nunca loguear secretos
console.log({ dbUrl: env.DATABASE_URL }); // ❌
```

---

## Node.js Security Releases

```bash
# Mantenerse actualizado con releases de seguridad
# Node.js publica security releases para CVEs.

# Verificar versión actual vs última segura
node --version
# Node 24.16.0+ LTS, Node 26.3.1+ Current (Jun 2026)

# npm-check-updates para actualizar dependencias
npx npm-check-updates -u
npm install
```

---

## Checklist de seguridad

- [ ] Helmet configurado con headers de seguridad
- [ ] CORS con orígenes explícitos
- [ ] Rate limiting en todos los endpoints (auth más restrictivo)
- [ ] JWT con secret fuerte (≥32 chars), algoritmo HS256 mínimo, expiración corta
- [ ] Refresh tokens en httpOnly cookies, no en localStorage
- [ ] Zod validación en todas las fronteras (body, query, params)
- [ ] SQL parametrizado siempre (nunca string concatenation)
- [ ] CSRF protection para apps con cookies
- [ ] `npm audit` en CI, sin vulnerabilidades altas/críticas
- [ ] Secrets en variables de entorno, validados con Zod al inicio
- [ ] No loguear secretos, tokens, ni datos personales
- [ ] Node.js actualizado al último security release
- [ ] Dependencias actualizadas periódicamente
- [ ] `helmet.contentSecurityPolicy` si sirves HTML
