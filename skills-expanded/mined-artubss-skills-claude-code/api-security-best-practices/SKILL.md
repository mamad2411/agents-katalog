---
name: api-security-best-practices
description: "Implemente padrões seguros de design de API, incluindo autenticação, autorização, validação de entrada, rate limiting e proteção contra vulnerabilidades comuns de API"
---

# Práticas de Segurança em APIs

## Visão Geral

Guia para desenvolvedores construírem APIs seguras implementando autenticação, autorização, validação de entrada, rate limiting e proteção contra vulnerabilidades comuns. Esta skill abrange padrões de segurança para APIs REST, GraphQL e WebSocket.

## Quando Usar Esta Skill

- Use ao projetar novos endpoints de API
- Use ao proteger APIs existentes
- Use ao implementar autenticação e autorização
- Use ao proteger contra ataques em APIs (injection, DDoS, etc.)
- Use ao realizar auditorias de segurança em APIs
- Use ao se preparar para auditorias de segurança
- Use ao implementar rate limiting e throttling
- Use ao lidar com dados sensíveis em APIs

## Como Funciona

### Etapa 1: Autenticação e Autorização

Vou ajudá-lo a implementar autenticação segura:
- Escolha o método de autenticação (JWT, OAuth 2.0, API keys)
- Implemente autenticação baseada em tokens
- Configure controle de acesso baseado em funções (RBAC)
- Proteja o gerenciamento de sessões
- Implemente autenticação multifatorial (MFA)

### Etapa 2: Validação e Sanitização de Entrada

Proteja contra ataques de injection:
- Valide todos os dados de entrada
- Sanitize as entradas do usuário
- Use queries parametrizadas
- Implemente validação de schema de requisição
- Previna SQL injection, XSS e command injection

### Etapa 3: Rate Limiting e Throttling

Previna abuso e ataques DDoS:
- Implemente rate limiting por usuário/IP
- Configure throttling de API
- Configure quotas de requisição
- Trate erros de rate limit adequadamente
- Monitore atividades suspeitas

### Etapa 4: Proteção de Dados

Proteja dados sensíveis:
- Criptografe dados em trânsito (HTTPS/TLS)
- Criptografe dados sensíveis em repouso
- Implemente tratamento de erros adequado (sem vazamento de dados)
- Sanitize mensagens de erro
- Use headers seguros

### Etapa 5: Testes de Segurança em APIs

Verifique a implementação de segurança:
- Teste autenticação e autorização
- Realize testes de penetração
- Verifique vulnerabilidades comuns (OWASP API Top 10)
- Valide o tratamento de entrada
- Teste rate limiting


## Exemplos

### Exemplo 1: Implementando Autenticação JWT

```markdown
## Implementação Segura de Autenticação JWT

### Fluxo de Autenticação

1. Usuário faz login com credenciais
2. Servidor valida credenciais
3. Servidor gera token JWT
4. Cliente armazena token com segurança
5. Cliente envia token com cada requisição
6. Servidor valida o token

### Implementação

#### 1. Gere Tokens JWT Seguros

\`\`\`javascript
// auth.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Endpoint de login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Valide entrada
    if (!email || !password) {
      return res.status(400).json({ 
        error: 'Email and password are required' 
      });
    }
    
    // Encontre o usuário
    const user = await db.user.findUnique({ 
      where: { email } 
    });
    
    if (!user) {
      // Não revele se o usuário existe
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // Verifique a senha
    const validPassword = await bcrypt.compare(
      password, 
      user.passwordHash
    );
    
    if (!validPassword) {
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // Gere token JWT
    const token = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { 
        expiresIn: '1h',
        issuer: 'your-app',
        audience: 'your-app-users'
      }
    );
    
    // Gere refresh token
    const refreshToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    // Armazene refresh token no banco de dados
    await db.refreshToken.create({
      data: {
        token: refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });
    
    res.json({
      token,
      refreshToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      error: 'An error occurred during login' 
    });
  }
});
\`\`\`

#### 2. Verifique Tokens JWT (Middleware)

\`\`\`javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  // Obtenha token do header
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required' 
    });
  }
  
  // Verifique token
  jwt.verify(
    token, 
    process.env.JWT_SECRET,
    { 
      issuer: 'your-app',
      audience: 'your-app-users'
    },
    (err, user) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          return res.status(401).json({ 
            error: 'Token expired' 
          });
        }
        return res.status(403).json({ 
          error: 'Invalid token' 
        });
      }
      
      // Anexe usuário à requisição
      req.user = user;
      next();
    }
  );
}

module.exports = { authenticateToken };
\`\`\`

#### 3. Proteja Rotas

\`\`\`javascript
const { authenticateToken } = require('./middleware/auth');

// Rota protegida
app.get('/api/user/profile', authenticateToken, async (req, res) => {
  try {
    const user = await db.user.findUnique({
      where: { id: req.user.userId },
      select: {
        id: true,
        email: true,
        name: true,
        // Não retorne passwordHash
      }
    });
    
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});
\`\`\`

#### 4. Implemente Refresh de Token

\`\`\`javascript
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(401).json({ 
      error: 'Refresh token required' 
    });
  }
  
  try {
    // Verifique refresh token
    const decoded = jwt.verify(
      refreshToken, 
      process.env.JWT_REFRESH_SECRET
    );
    
    // Verifique se refresh token existe no banco de dados
    const storedToken = await db.refreshToken.findFirst({
      where: {
        token: refreshToken,
        userId: decoded.userId,
        expiresAt: { gt: new Date() }
      }
    });
    
    if (!storedToken) {
      return res.status(403).json({ 
        error: 'Invalid refresh token' 
      });
    }
    
    // Gere novo token de acesso
    const user = await db.user.findUnique({
      where: { id: decoded.userId }
    });
    
    const newToken = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    res.json({
      token: newToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    res.status(403).json({ 
      error: 'Invalid refresh token' 
    });
  }
});
\`\`\`

### Práticas de Segurança

- ✅ Use secrets JWT fortes (mínimo 256-bit)
- ✅ Defina tempos de expiração curtos (1 hora para tokens de acesso)
- ✅ Implemente refresh tokens para sessões de longa duração
- ✅ Armazene refresh tokens no banco de dados (podem ser revogados)
- ✅ Use apenas HTTPS
- ✅ Não armazene dados sensíveis no payload JWT
- ✅ Valide issuer e audience do token
- ✅ Implemente blacklist de tokens para logout
```


### Exemplo 2: Validação de Entrada e Prevenção de SQL Injection

```markdown
## Prevenção de SQL Injection e Validação de Entrada

### O Problema

**❌ Código Vulnerável:**
\`\`\`javascript
// NUNCA FAÇA ISSO - Vulnerabilidade de SQL Injection
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // Perigoso: Entrada do usuário diretamente na query
  const query = \`SELECT * FROM users WHERE id = '\${userId}'\`;
  const user = await db.query(query);
  
  res.json(user);
});

// Exemplo de ataque:
// GET /api/users/1' OR '1'='1
// Retorna todos os usuários!
\`\`\`

### A Solução

#### 1. Use Queries Parametrizadas

\`\`\`javascript
// ✅ Seguro: Query parametrizada
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // Valide entrada primeiro
  if (!userId || !/^\d+$/.test(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  // Use query parametrizada
  const user = await db.query(
    'SELECT id, email, name FROM users WHERE id = $1',
    [userId]
  );
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 2. Use ORM com Escape Adequado

\`\`\`javascript
// ✅ Seguro: Usando Prisma ORM
app.get('/api/users/:id', async (req, res) => {
  const userId = parseInt(req.params.id);
  
  if (isNaN(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      email: true,
      name: true,
      // Não selecione campos sensíveis
    }
  });
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 3. Implemente Validação de Requisição com Zod

\`\`\`javascript
const { z } = require('zod');

// Defina schema de validação
const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name too long'),
  age: z.number()
    .int('Age must be an integer')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age')
    .optional()
});

// Middleware de validação
function validateRequest(schema) {
  return (req, res, next) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
  };
}

// Use validação
app.post('/api/users', 
  validateRequest(createUserSchema),
  async (req, res) => {
    // Entrada é validada neste ponto
    const { email, password, name, age } = req.body;
    
    // Hash da senha
    const passwordHash = await bcrypt.hash(password, 10);
    
    // Crie usuário
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
        age
      }
    });
    
    // Não retorne hash da senha
    const { passwordHash: _, ...userWithoutPassword } = user;
    res.status(201).json(userWithoutPassword);
  }
);
\`\`\`

#### 4. Sanitize Saída para Prevenir XSS

\`\`\`javascript
const DOMPurify = require('isomorphic-dompurify');

app.post('/api/comments', authenticateToken, async (req, res) => {
  const { content } = req.body;
  
  // Valide
  if (!content || content.length > 1000) {
    return res.status(400).json({ 
      error: 'Invalid comment content' 
    });
  }
  
  // Sanitize HTML para prevenir XSS
  const sanitizedContent = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
  
  const comment = await prisma.comment.create({
    data: {
      content: sanitizedContent,
      userId: req.user.userId
    }
  });
  
  res.status(201).json(comment);
});
\`\`\`

### Checklist de Validação

- [ ] Valide todas as entradas do usuário
- [ ] Use queries parametrizadas ou ORM
- [ ] Valide tipos de dados (string, number, email, etc.)
- [ ] Valide ranges de dados (comprimento mín/máx, ranges de valor)
- [ ] Sanitize conteúdo HTML
- [ ] Escape caracteres especiais
- [ ] Valide uploads de arquivo (tipo, tamanho, conteúdo)
- [ ] Use allowlists, não blocklists
```


### Exemplo 3: Rate Limiting e Proteção contra DDoS

```markdown
## Implementando Rate Limiting

### Por Que Rate Limiting?

- Previna ataques de brute force
- Proteja contra DDoS
- Previna abuso de API
- Garanta uso justo
- Reduza custos de servidor

### Implementação com Express Rate Limit

\`\`\`javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

// Crie cliente Redis
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// Rate limit geral de API
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // 100 requisições por janela
  message: {
    error: 'Too many requests, please try again later',
    retryAfter: 900 // segundos
  },
  standardHeaders: true, // Retorne info de rate limit nos headers
  legacyHeaders: false,
  // Gerador de chave customizado (por ID de usuário ou IP)
  keyGenerator: (req) => {
    return req.user?.userId || req.ip;
  }
});

// Rate limit rígido para endpoints de autenticação
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // Apenas 5 tentativas de login por 15 minutos
  skipSuccessfulRequests: true, // Não conte logins bem-sucedidos
  message: {
    error: 'Too many login attempts, please try again later',
    retryAfter: 900
  }
});

// Aplique rate limiters
app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);

// Rate limiter customizado para operações custosas
const expensiveLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hora
  max: 10, // 10 requisições por hora
  message: {
    error: 'Rate limit exceeded for this operation'
  }
});

app.post('/api/reports/generate', 
  authenticateToken,
  expensiveLimiter,
  async (req, res) => {
    // Operação custosa
  }
);
\`\`\`

### Avançado: Rate Limiting por Usuário

\`\`\`javascript
// Limites diferentes baseado em tier de usuário
function createTieredRateLimiter() {
  const limits = {
    free: { windowMs: 60 * 60 * 1000, max: 100 },
    pro: { windowMs: 60 * 60 * 1000, max: 1000 },
    enterprise: { windowMs: 60 * 60 * 1000, max: 10000 }
  };
  
  return async (req, res, next) => {
    const user = req.user;
    const tier = user?.tier || 'free';
    const limit = limits[tier];
    
    const key = \`rl:user:\${user.userId}\`;
    const current = await redis.incr(key);
    
    if (current === 1) {
      await redis.expire(key, limit.windowMs / 1000);
    }
    
    if (current > limit.max) {
      return res.status(429).json({
        error: 'Rate limit exceeded',
        limit: limit.max,
        remaining: 0,
        reset: await redis.ttl(key)
      });
    }
    
    // Defina headers de rate limit
    res.set({
      'X-RateLimit-Limit': limit.max,
      'X-RateLimit-Remaining': limit.max - current,
      'X-RateLimit-Reset': await redis.ttl(key)
    });
    
    next();
  };
}

app.use('/api/', authenticateToken, createTieredRateLimiter());
\`\`\`

### Proteção DDoS com Helmet

\`\`\`javascript
const helmet = require('helmet');

app.use(helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  // Previna clickjacking
  frameguard: { action: 'deny' },
  // Oculte header X-Powered-By
  hidePoweredBy: true,
  // Previna MIME type sniffing
  noSniff: true,
  // Ative HSTS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
\`\`\`

### Headers de Resposta de Rate Limit

\`\`\`
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
Retry-After: 900
\`\`\`
```

## Práticas Recomendadas

### ✅ Faça Isso

- **Use HTTPS em Todo Lugar** - Nunca envie dados sensíveis sobre HTTP
- **Implemente Autenticação** - Requeira autenticação para endpoints protegidos
- **Valide Todas as Entradas** - Nunca confie em entrada do usuário
- **Use Queries Parametrizadas** - Previna SQL injection
- **Implemente Rate Limiting** - Proteja contra brute force e DDoS
- **Hash Senhas** - Use bcrypt com salt rounds >= 10
- **Use Tokens de Curta Duração** - Tokens de acesso JWT devem expirar rapidamente
- **Implemente CORS Adequadamente** - Permita apenas origens confiáveis
- **Registre Eventos de Segurança** - Monitore atividades suspeitas
- **Mantenha Dependências Atualizadas** - Atualize pacotes regularmente
- **Use Security Headers** - Implemente Helmet.js
- **Sanitize Mensagens de Erro** - Não vaze informações sensíveis

### ❌ Não Faça Isso

- **Não Armazene Senhas em Texto Plano** - Sempre hash senhas
- **Não Use Secrets Fracos** - Use secrets JWT fortes e aleatórios
- **Não Confie em Entrada do Usuário** - Sempre valide e sanitize
- **Não Exponha Stack Traces** - Oculte detalhes de erro em produção
- **Não Use Concatenação de String para SQL** - Use queries parametrizadas
- **Não Armazene Dados Sensíveis em JWT** - JWTs não são criptografados
- **Não Ignore Updates de Segurança** - Atualize dependências regularmente
- **Não Use Credenciais Padrão** - Altere todas as senhas padrão
- **Não Desabilite CORS Completamente** - Configure adequadamente
- **Não Registre Dados Sensíveis** - Sanitize logs

## Armadilhas Comuns

### Problema: Secret JWT Exposto no Código
**Sintomas:** Secret JWT hardcoded ou commitado no Git
**Solução:**
\`\`\`javascript
// ❌ Ruim
const JWT_SECRET = 'my-secret-key';

// ✅ Bom
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required');
}

// Gere secret forte
// node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
\`\`\`

### Problema: Requisitos de Senha Fracos
**Sintomas:** Usuários podem definir senhas fracas como "password123"
**Solução:**
\`\`\`javascript
const passwordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

// Ou use uma biblioteca de força de senha
const zxcvbn = require('zxcvbn');
const result = zxcvbn(password);
if (result.score < 3) {
  return res.status(400).json({
    error: 'Password too weak',
    suggestions: result.feedback.suggestions
  });
}
\`\`\`

### Problema: Verificações de Autorização Faltando
**Sintomas:** Usuários podem acessar recursos que não deveriam
**Solução:**
\`\`\`javascript
// ❌ Ruim: Apenas verifica autenticação
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});

// ✅ Bom: Verifica autenticação e autorização
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  const post = await prisma.post.findUnique({
    where: { id: req.params.id }
  });
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  // Verifique se o usuário é dono do post ou é admin
  if (post.userId !== req.user.userId && req.user.role !== 'admin') {
    return res.status(403).json({ 
      error: 'Not authorized to delete this post' 
    });
  }
  
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
\`\`\`

### Problema: Mensagens de Erro Verbosas
**Sintomas:** Mensagens de erro revelam detalhes do sistema
**Solução:**
\`\`\`javascript
// ❌ Ruim: Expõe detalhes do banco de dados
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
    // Error: "Unique constraint failed on the fields: (`email`)"
  }
});

// ✅ Bom: Mensagem de erro genérica
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    console.error('User creation error:', error); // Registre erro completo
    
    if (error.code === 'P2002') {
      return res.status(400).json({ 
        error: 'Email already exists' 
      });
    }
    
    res.status(500).json({ 
      error: 'An error occurred while creating user' 
    });
  }
});
\`\`\`

## Checklist de Segurança

### Autenticação e Autorização
- [ ] Implemente autenticação forte (JWT, OAuth 2.0)
- [ ] Use HTTPS para todos os endpoints
- [ ] Hash senhas com bcrypt (salt rounds >= 10)
- [ ] Implemente expiração de token
- [ ] Adicione mecanismo de refresh token
- [ ] Verifique autorização do usuário para cada requisição
- [ ] Implemente controle de acesso baseado em funções (RBAC)

### Validação de Entrada
- [ ] Valide todas as entradas do usuário
- [ ] Use queries parametrizadas ou ORM
- [ ] Sanitize conteúdo HTML
- [ ] Valide uploads de arquivo
- [ ] Implemente validação de schema de requisição
- [ ] Use allowlists, não blocklists

### Rate Limiting e Proteção DDoS
- [ ] Implemente rate limiting por usuário/IP
- [ ] Adicione limites mais rígidos para endpoints de autenticação
- [ ] Use Redis para rate limiting distribuído
- [ ] Retorne headers apropriados de rate limit
- [ ] Implemente throttling de requisição

### Proteção de Dados
- [ ] Use HTTPS/TLS para todo o tráfego
- [ ] Criptografe dados sensíveis em repouso
- [ ] Não armazene dados sensíveis em JWT
- [ ] Sanitize mensagens de erro
- [ ] Implemente configuração apropriada de CORS
- [ ] Use security headers (Helmet.js)

### Monitoramento e Registro
- [ ] Registre eventos de segurança
- [ ] Monitore atividades suspeitas
- [ ] Configure alertas para tentativas de autenticação falhadas
- [ ] Rastreie padrões de uso de API
- [ ] Não registre dados sensíveis

## OWASP API Security Top 10

1. **Broken Object Level Authorization** - Sempre verifique se o usuário pode acessar recurso
2. **Broken Authentication** - Implemente mecanismos de autenticação forte
3. **Broken Object Property Level Authorization** - Valide quais propriedades o usuário pode acessar
4. **Unrestricted Resource Consumption** - Implemente rate limiting e quotas
5. **Broken Function Level Authorization** - Verifique role do usuário para cada função
6. **Unrestricted Access to Sensitive Business Flows** - Proteja workflows críticos
7. **Server Side Request Forgery (SSRF)** - Valide e sanitize URLs
8. **Security Misconfiguration** - Use práticas recomendadas e headers de segurança
9. **Improper Inventory Management** - Documente e proteja todos os endpoints de API