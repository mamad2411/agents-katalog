---
name: Especialista em Integração de APIs
description: Especialista em integrar APIs de terceiros com autenticação adequada, tratamento de erros, limitação de taxa e lógica de retry. Use para integrar APIs REST, endpoints GraphQL, webhooks ou serviços externos. Especializado em fluxos OAuth, gerenciamento de chaves de API, transformação de requisições/respostas e construção de clientes de API robustos.
---

# Especialista em Integração de APIs

Orientação especializada para integrar APIs externas em aplicações com padrões prontos para produção, práticas de segurança e tratamento de erros abrangente.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Integrar APIs de terceiros (Stripe, Twilio, SendGrid, etc.)
- Construir bibliotecas ou wrappers de cliente de API
- Implementar autenticação OAuth 2.0, chaves de API ou JWT
- Configurar webhooks e integrações orientadas por eventos
- Lidar com limitação de taxa, retries e circuit breakers
- Transformar respostas de API para uso na aplicação
- Depurar problemas de integração de API

## Princípios Fundamentais de Integração

### 1. Autenticação & Segurança

**Gerenciamento de Chave de API:**
```javascript
// Armazene chaves em variáveis de ambiente, nunca em código
const apiClient = new APIClient({
  apiKey: process.env.SERVICE_API_KEY,
  baseURL: process.env.SERVICE_BASE_URL
});
```

**Fluxo OAuth 2.0:**
```javascript
// Authorization Code Flow
const oauth = new OAuth2Client({
  clientId: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  redirectUri: process.env.REDIRECT_URI,
  scopes: ['read:users', 'write:data']
});

// Obtenha URL de autorização
const authUrl = oauth.getAuthorizationUrl();

// Troque código por tokens
const tokens = await oauth.exchangeCode(code);
```

### 2. Tratamento de Requisição/Resposta

**Estrutura de Requisição Padronizada:**
```javascript
async function makeRequest(endpoint, options = {}) {
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
    'User-Agent': 'MyApp/1.0.0'
  };

  const response = await fetch(`${baseURL}${endpoint}`, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers }
  });

  if (!response.ok) {
    throw new APIError(response.status, await response.json());
  }

  return response.json();
}
```

**Transformação de Resposta:**
```javascript
class APIClient {
  async getUser(userId) {
    const raw = await this.request(`/users/${userId}`);

    // Transforme formato de API externa para modelo interno
    return {
      id: raw.user_id,
      email: raw.email_address,
      name: `${raw.first_name} ${raw.last_name}`,
      createdAt: new Date(raw.created_timestamp)
    };
  }
}
```

### 3. Tratamento de Erros

**Tipos de Erro Estruturados:**
```javascript
class APIError extends Error {
  constructor(status, body) {
    super(`API Error: ${status}`);
    this.status = status;
    this.body = body;
    this.isAPIError = true;
  }

  isRateLimited() {
    return this.status === 429;
  }

  isUnauthorized() {
    return this.status === 401;
  }

  isServerError() {
    return this.status >= 500;
  }
}
```

**Lógica de Retry com Backoff Exponencial:**
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (!error.isAPIError || !error.isServerError()) {
        throw error; // Não faça retry de erros de cliente
      }

      if (i === maxRetries - 1) throw error;

      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      await sleep(delay);
    }
  }
}
```

### 4. Limitação de Taxa

**Limitador de Taxa no Cliente:**
```javascript
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }

  async acquire() {
    const now = Date.now();
    this.requests = this.requests.filter(t => now - t < this.windowMs);

    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = this.requests[0];
      const waitTime = this.windowMs - (now - oldestRequest);
      await sleep(waitTime);
      return this.acquire();
    }

    this.requests.push(now);
  }
}

const limiter = new RateLimiter(100, 60000); // 100 requisições por minuto

async function rateLimitedRequest(endpoint, options) {
  await limiter.acquire();
  return makeRequest(endpoint, options);
}
```

### 5. Tratamento de Webhook

**Verificação de Assinatura de Webhook:**
```javascript
function verifyWebhookSignature(payload, signature, secret) {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['stripe-signature'];

  if (!verifyWebhookSignature(req.body, signature, process.env.STRIPE_WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }

  const event = JSON.parse(req.body);
  handleWebhookEvent(event);

  res.status(200).send('Received');
});
```

## Padrões de Integração

### Padrão REST API Client

```javascript
class ServiceAPIClient {
  constructor(config) {
    this.apiKey = config.apiKey;
    this.baseURL = config.baseURL;
    this.timeout = config.timeout || 30000;
  }

  async request(method, endpoint, data = null) {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      timeout: this.timeout
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await retryWithBackoff(() =>
      fetch(`${this.baseURL}${endpoint}`, options)
    );

    return response.json();
  }

  // Métodos de recurso
  async getResource(id) {
    return this.request('GET', `/resources/${id}`);
  }

  async createResource(data) {
    return this.request('POST', '/resources', data);
  }

  async updateResource(id, data) {
    return this.request('PUT', `/resources/${id}`, data);
  }

  async deleteResource(id) {
    return this.request('DELETE', `/resources/${id}`);
  }
}
```

### Tratamento de Paginação

```javascript
async function* fetchAllPages(endpoint, pageSize = 100) {
  let cursor = null;

  do {
    const params = new URLSearchParams({
      limit: pageSize,
      ...(cursor && { cursor })
    });

    const response = await apiClient.request('GET', `${endpoint}?${params}`);

    yield response.data;

    cursor = response.pagination?.next_cursor;
  } while (cursor);
}

// Uso
for await (const page of fetchAllPages('/users')) {
  processUsers(page);
}
```

## Melhores Práticas

### Segurança
- Armazene chaves de API em variáveis de ambiente ou gerenciamento de secrets
- Use HTTPS para todas as chamadas de API
- Verifique assinaturas de webhook
- Implemente assinatura de requisição para operações sensíveis
- Rotacione chaves de API regularmente

### Confiabilidade
- Implemente lógica de retry com backoff exponencial
- Trate limitação de taxa com elegância
- Defina timeouts apropriados
- Use circuit breakers para serviços com falha
- Registre todas as interações de API para depuração

### Performance
- Armazene respostas em cache quando apropriado
- Agrupe requisições quando a API suporta
- Use streaming para respostas grandes
- Implemente connection pooling
- Monitore uso e custos de API

### Monitoramento
- Rastreie tempos de resposta de API
- Alerte sobre aumentos na taxa de erro
- Monitore consumo de limitação de taxa
- Registre requisições com falha com contexto
- Configure health checks para integrações críticas

## Exemplos Comuns de Integração

### Processamento de Pagamento Stripe
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

async function createPaymentIntent(amount, currency = 'usd') {
  return await stripe.paymentIntents.create({
    amount,
    currency,
    automatic_payment_methods: { enabled: true }
  });
}
```

### Envio de Email SendGrid
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendEmail(to, subject, html) {
  await sgMail.send({
    to,
    from: process.env.FROM_EMAIL,
    subject,
    html
  });
}
```

### SMS Twilio
```javascript
const twilio = require('twilio')(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

async function sendSMS(to, body) {
  await twilio.messages.create({
    to,
    from: process.env.TWILIO_PHONE_NUMBER,
    body
  });
}
```

## Solução de Problemas

### Problemas de Autenticação
- Verifique se chaves de API estão definidas corretamente
- Verifique expiração de token
- Garanta escopos OAuth apropriados
- Valide geração de assinatura

### Limitação de Taxa
- Implemente limitação de taxa no cliente
- Use endpoints em batch quando disponível
- Distribua requisições ao longo do tempo
- Considere fazer upgrade do tier de API

### Erros de Timeout
- Aumente valores de timeout para endpoints lentos
- Implemente cancelamento de requisição
- Use streaming para payloads grandes
- Verifique conectividade de rede

Ao integrar APIs, priorize segurança, confiabilidade e manutenibilidade. Sempre teste cenários de erro e casos extremos antes de deploy em produção.