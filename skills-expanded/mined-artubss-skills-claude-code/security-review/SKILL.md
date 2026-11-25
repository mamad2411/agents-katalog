---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
author: affaan-m
version: "1.0"
---

# Skill de Revisão de Segurança

Este skill garante que todo código segue as melhores práticas de segurança e identifica possíveis vulnerabilidades.

## Quando Ativar

- Implementando autenticação ou autorização
- Tratando entrada de usuários ou uploads de arquivos
- Criando novos endpoints de API
- Trabalhando com secrets ou credenciais
- Implementando funcionalidades de pagamento
- Armazenando ou transmitindo dados sensíveis
- Integrando APIs de terceiros

## Checklist de Segurança

### 1. Gerenciamento de Secrets

#### ❌ NUNCA Faça Isso
```typescript
const apiKey = "sk-proj-xxxxx"  // Secret codificada
const dbPassword = "password123" // No código-fonte
```

#### ✅ SEMPRE Faça Isso
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// Verifique se secrets existem
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

#### Passos de Verificação
- [ ] Nenhuma chave de API, token ou senha codificada
- [ ] Todos os secrets em variáveis de ambiente
- [ ] `.env.local` no .gitignore
- [ ] Nenhum secret no histórico do git
- [ ] Secrets de produção na plataforma de hosting (Vercel, Railway)

### 2. Validação de Entrada

#### Sempre Valide Entrada do Usuário
```typescript
import { z } from 'zod'

// Defina schema de validação
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// Valide antes de processar
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### Validação de Upload de Arquivo
```typescript
function validateFileUpload(file: File) {
  // Verificação de tamanho (5MB máximo)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // Verificação de tipo
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // Verificação de extensão
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  return true
}
```

#### Passos de Verificação
- [ ] Todas as entradas de usuário validadas com schemas
- [ ] Uploads de arquivo restritos (tamanho, tipo, extensão)
- [ ] Nenhum uso direto de entrada de usuário em queries
- [ ] Validação whitelist (não blacklist)
- [ ] Mensagens de erro não vazam informações sensíveis

### 3. Prevenção de SQL Injection

#### ❌ NUNCA Concatene SQL
```typescript
// PERIGOSO - Vulnerabilidade de SQL Injection
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ SEMPRE Use Queries Parametrizadas
```typescript
// Seguro - query parametrizada
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// Ou com SQL bruto
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### Passos de Verificação
- [ ] Todas as queries do banco de dados usam queries parametrizadas
- [ ] Nenhuma concatenação de string em SQL
- [ ] ORM/query builder usado corretamente
- [ ] Queries do Supabase devidamente sanitizadas

### 4. Autenticação & Autorização

#### Manipulação de Token JWT
```typescript
// ❌ ERRADO: localStorage (vulnerável a XSS)
localStorage.setItem('token', token)

// ✅ CORRETO: cookies httpOnly
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

#### Verificações de Autorização
```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // SEMPRE verifique autorização primeiro
  const requester = await db.users.findUnique({
    where: { id: requesterId }
  })

  if (requester.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }

  // Prossiga com a exclusão
  await db.users.delete({ where: { id: userId } })
}
```

#### Row Level Security (Supabase)
```sql
-- Habilite RLS em todas as tabelas
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Usuários podem visualizar apenas seus próprios dados
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Usuários podem atualizar apenas seus próprios dados
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### Passos de Verificação
- [ ] Tokens armazenados em cookies httpOnly (não localStorage)
- [ ] Verificações de autorização antes de operações sensíveis
- [ ] Row Level Security habilitada no Supabase
- [ ] Controle de acesso baseado em função implementado
- [ ] Gerenciamento de sessão seguro

### 5. Prevenção de XSS

#### Sanitize HTML
```typescript
import DOMPurify from 'isomorphic-dompurify'

// SEMPRE sanitize HTML fornecido por usuário
function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

#### Content Security Policy
```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
    `.replace(/\s{2,}/g, ' ').trim()
  }
]
```

#### Passos de Verificação
- [ ] HTML fornecido por usuário sanitizado
- [ ] Headers CSP configurados
- [ ] Nenhum conteúdo dinâmico não validado renderizado
- [ ] Proteção XSS nativa do React utilizada

### 6. Proteção CSRF

#### Tokens CSRF
```typescript
import { csrf } from '@/lib/csrf'

export async function POST(request: Request) {
  const token = request.headers.get('X-CSRF-Token')

  if (!csrf.verify(token)) {
    return NextResponse.json(
      { error: 'Invalid CSRF token' },
      { status: 403 }
    )
  }

  // Processe a requisição
}
```

#### Cookies SameSite
```typescript
res.setHeader('Set-Cookie',
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict`)
```

#### Passos de Verificação
- [ ] Tokens CSRF em operações que alteram estado
- [ ] SameSite=Strict em todos os cookies
- [ ] Padrão double-submit cookie implementado

### 7. Rate Limiting

#### Rate Limiting de API
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // 100 requisições por janela
  message: 'Too many requests'
})

// Aplique a rotas
app.use('/api/', limiter)
```

#### Operações Caras
```typescript
// Rate limiting agressivo para buscas
const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 10, // 10 requisições por minuto
  message: 'Too many search requests'
})

app.use('/api/search', searchLimiter)
```

#### Passos de Verificação
- [ ] Rate limiting em todos os endpoints de API
- [ ] Limites mais rigorosos em operações caras
- [ ] Rate limiting baseado em IP
- [ ] Rate limiting baseado em usuário (autenticado)

### 8. Exposição de Dados Sensíveis

#### Logging
```typescript
// ❌ ERRADO: Logging de dados sensíveis
console.log('User login:', { email, password })
console.log('Payment:', { cardNumber, cvv })

// ✅ CORRETO: Dados sensíveis removidos
console.log('User login:', { email, userId })
console.log('Payment:', { last4: card.last4, userId })
```

#### Mensagens de Erro
```typescript
// ❌ ERRADO: Expor detalhes internos
catch (error) {
  return NextResponse.json(
    { error: error.message, stack: error.stack },
    { status: 500 }
  )
}

// ✅ CORRETO: Mensagens de erro genéricas
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json(
    { error: 'An error occurred. Please try again.' },
    { status: 500 }
  )
}
```

#### Passos de Verificação
- [ ] Nenhuma senha, token ou secret em logs
- [ ] Mensagens de erro genéricas para usuários
- [ ] Erros detalhados apenas em logs do servidor
- [ ] Nenhum stack trace exposto para usuários

### 9. Segurança Blockchain (Solana)

#### Verificação de Carteira
```typescript
import { verify } from '@solana/web3.js'

async function verifyWalletOwnership(
  publicKey: string,
  signature: string,
  message: string
) {
  try {
    const isValid = verify(
      Buffer.from(message),
      Buffer.from(signature, 'base64'),
      Buffer.from(publicKey, 'base64')
    )
    return isValid
  } catch (error) {
    return false
  }
}
```

#### Verificação de Transação
```typescript
async function verifyTransaction(transaction: Transaction) {
  // Verifique o destinatário
  if (transaction.to !== expectedRecipient) {
    throw new Error('Invalid recipient')
  }

  // Verifique o valor
  if (transaction.amount > maxAmount) {
    throw new Error('Amount exceeds limit')
  }

  // Verifique se o usuário tem saldo suficiente
  const balance = await getBalance(transaction.from)
  if (balance < transaction.amount) {
    throw new Error('Insufficient balance')
  }

  return true
}
```

#### Passos de Verificação
- [ ] Assinaturas de carteira verificadas
- [ ] Detalhes de transação validados
- [ ] Verificações de saldo antes de transações
- [ ] Nenhuma assinatura de transação cega

### 10. Segurança de Dependências

#### Atualizações Regulares
```bash
# Verifique vulnerabilidades
npm audit

# Corrija problemas corrigíveis automaticamente
npm audit fix

# Atualize dependências
npm update

# Verifique pacotes desatualizados
npm outdated
```

#### Arquivos de Lock
```bash
# SEMPRE faça commit dos arquivos de lock
git add package-lock.json

# Use em CI/CD para builds reproduzíveis
npm ci  # Em vez de npm install
```

#### Passos de Verificação
- [ ] Dependências atualizadas
- [ ] Nenhuma vulnerabilidade conhecida (npm audit limpo)
- [ ] Arquivos de lock commitados
- [ ] Dependabot habilitado no GitHub
- [ ] Atualizações de segurança regulares

## Testes de Segurança

### Testes de Segurança Automatizados
```typescript
// Teste autenticação
test('requires authentication', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

// Teste autorização
test('requires admin role', async () => {
  const response = await fetch('/api/admin', {
    headers: { Authorization: `Bearer ${userToken}` }
  })
  expect(response.status).toBe(403)
})

// Teste validação de entrada
test('rejects invalid input', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' })
  })
  expect(response.status).toBe(400)
})

// Teste rate limiting
test('enforces rate limits', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint')
  )

  const responses = await Promise.all(requests)
  const tooManyRequests = responses.filter(r => r.status === 429)

  expect(tooManyRequests.length).toBeGreaterThan(0)
})
```

## Checklist de Segurança Pré-Deploy

Antes de QUALQUER deploy em produção:

- [ ] **Secrets**: Nenhum secret codificado, todos em variáveis de env
- [ ] **Validação de Entrada**: Todas as entradas de usuário validadas
- [ ] **SQL Injection**: Todas as queries parametrizadas
- [ ] **XSS**: Conteúdo de usuário sanitizado
- [ ] **CSRF**: Proteção habilitada
- [ ] **Autenticação**: Manipulação adequada de tokens
- [ ] **Autorização**: Verificações de função em lugar
- [ ] **Rate Limiting**: Habilitado em todos os endpoints
- [ ] **HTTPS**: Obrigatório em produção
- [ ] **Security Headers**: CSP, X-Frame-Options configurados
- [ ] **Tratamento de Erro**: Nenhum dado sensível em erros
- [ ] **Logging**: Nenhum dado sensível em logs
- [ ] **Dependências**: Atualizadas, sem vulnerabilidades
- [ ] **Row Level Security**: Habilitada no Supabase
- [ ] **CORS**: Corretamente configurado
- [ ] **Upload de Arquivo**: Validado (tamanho, tipo)
- [ ] **Assinaturas de Carteira**: Verificadas (se blockchain)

## Recursos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security](https://nextjs.org/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)

---

**Lembre-se**: Segurança não é opcional. Uma vulnerabilidade pode comprometer toda a plataforma. Em caso de dúvida, erre a favor da cautela.