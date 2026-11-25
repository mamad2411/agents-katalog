---
name: nodejs-best-practices
description: Princípios de desenvolvimento Node.js e tomada de decisão. Seleção de framework, padrões assíncronos, segurança e arquitetura. Ensina pensamento, não cópia.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Node.js Best Practices

> Princípios e tomada de decisão para desenvolvimento Node.js em 2025.
> **Aprenda a PENSAR, não memorize padrões de código.**

---

## ⚠️ Como Usar Esta Habilidade

Esta habilidade ensina **princípios de tomada de decisão**, não código fixo para copiar.

- PERGUNTE ao usuário sobre preferências quando não estiverem claras
- Escolha framework/padrão baseado no CONTEXTO
- Não use a mesma solução padrão toda vez

---

## 1. Seleção de Framework (2025)

### Árvore de Decisão

```
O que você está construindo?
│
├── Edge/Serverless (Cloudflare, Vercel)
│   └── Hono (zero-dependency, cold starts ultra-rápidos)
│
├── API de Alta Performance
│   └── Fastify (2-3x mais rápido que Express)
│
├── Enterprise/Familiaridade da equipe
│   └── NestJS (estruturado, DI, decoradores)
│
├── Legado/Estável/Ecossistema máximo
│   └── Express (maduro, mais middleware)
│
└── Full-stack com frontend
    └── Next.js API Routes ou tRPC
```

### Princípios de Comparação

| Fator | Hono | Fastify | Express |
|-------|------|---------|---------|
| **Melhor para** | Edge, serverless | Performance | Legado, aprendizado |
| **Cold start** | Mais rápido | Rápido | Moderado |
| **Ecossistema** | Em crescimento | Bom | Maior |
| **TypeScript** | Nativo | Excelente | Bom |
| **Curva de aprendizado** | Baixa | Média | Baixa |

### Perguntas para Seleção:
1. Qual é o alvo de deployment?
2. O tempo de cold start é crítico?
3. A equipe tem experiência prévia?
4. Há código legado para manter?

---

## 2. Considerações de Runtime (2025)

### TypeScript Nativo

```
Node.js 22+: --experimental-strip-types
├── Executa arquivos .ts diretamente
├── Sem etapa de build para projetos simples
└── Considere para: scripts, APIs simples
```

### Decisão do Sistema de Módulos

```
ESM (import/export)
├── Padrão moderno
├── Melhor tree-shaking
├── Carregamento assíncrono de módulos
└── Use para: projetos novos

CommonJS (require)
├── Compatibilidade legada
├── Mais pacotes npm suportam
└── Use para: codebases existentes, alguns casos especiais
```

### Seleção de Runtime

| Runtime | Melhor Para |
|---------|----------|
| **Node.js** | Propósito geral, maior ecossistema |
| **Bun** | Performance, bundler integrado |
| **Deno** | Segurança em primeiro lugar, TypeScript integrado |

---

## 3. Princípios de Arquitetura

### Conceito de Estrutura em Camadas

```
Fluxo de Requisição:
│
├── Camada Controller/Route
│   ├── Manipula especificidades HTTP
│   ├── Validação de entrada na fronteira
│   └── Chama camada de serviço
│
├── Camada Service
│   ├── Lógica de negócio
│   ├── Agnóstica de framework
│   └── Chama camada de repositório
│
└── Camada Repository
    ├── Apenas acesso a dados
    ├── Queries de banco de dados
    └── Interações com ORM
```

### Por Que Isso Importa:
- **Testabilidade**: Mock de camadas independentemente
- **Flexibilidade**: Trocar banco de dados sem tocar lógica de negócio
- **Clareza**: Cada camada tem responsabilidade única

### Quando Simplificar:
- Scripts pequenos → Um arquivo OK
- Protótipos → Menos estrutura aceitável
- Sempre pergunte: "Isso vai crescer?"

---

## 4. Princípios de Tratamento de Erros

### Tratamento de Erros Centralizado

```
Padrão:
├── Crie classes de erro customizadas
├── Lance de qualquer camada
├── Capture no nível superior (middleware)
└── Formate resposta consistente
```

### Filosofia de Resposta de Erro

```
Cliente recebe:
├── Status HTTP apropriado
├── Código de erro para manipulação programática
├── Mensagem amigável ao usuário
└── SEM detalhes internos (segurança!)

Logs recebem:
├── Stack trace completo
├── Contexto da requisição
├── ID do usuário (se aplicável)
└── Timestamp
```

### Seleção de Código de Status

| Situação | Status | Quando |
|----------|--------|--------|
| Entrada inválida | 400 | Cliente enviou dados inválidos |
| Sem autenticação | 401 | Credenciais ausentes ou inválidas |
| Sem permissão | 403 | Autenticação válida, mas não permitido |
| Não encontrado | 404 | Recurso não existe |
| Conflito | 409 | Duplicado ou conflito de estado |
| Validação | 422 | Schema válido mas regras de negócio falham |
| Erro de servidor | 500 | Culpa nossa, registre tudo |

---

## 5. Princípios de Padrões Assíncronos

### Quando Usar Cada Um

| Padrão | Use Quando |
|--------|-----------|
| `async/await` | Operações assíncronas sequenciais |
| `Promise.all` | Operações paralelas independentes |
| `Promise.allSettled` | Paralelo onde algumas podem falhar |
| `Promise.race` | Timeout ou primeira resposta vence |

### Conscientização do Event Loop

```
I/O-bound (async ajuda):
├── Queries de banco de dados
├── Requisições HTTP
├── Sistema de arquivos
└── Operações de rede

CPU-bound (async não ajuda):
├── Operações criptográficas
├── Processamento de imagem
├── Cálculos complexos
└── → Use worker threads ou offload
```

### Evitar Bloqueio do Event Loop

- Nunca use métodos síncronos em produção (fs.readFileSync, etc.)
- Offload de trabalho CPU-intensivo
- Use streaming para dados grandes

---

## 6. Princípios de Validação

### Valide nas Fronteiras

```
Onde validar:
├── Ponto de entrada da API (corpo/params da requisição)
├── Antes de operações de banco de dados
├── Dados externos (respostas de API, uploads de arquivo)
└── Variáveis de ambiente (startup)
```

### Seleção de Biblioteca de Validação

| Biblioteca | Melhor Para |
|-----------|-----------|
| **Zod** | TypeScript first, inferência |
| **Valibot** | Bundle menor (tree-shakeable) |
| **ArkType** | Performance crítica |
| **Yup** | Uso existente com React Form |

### Filosofia de Validação

- Falhe rápido: Valide cedo
- Seja específico: Mensagens de erro claras
- Não confie: Mesmo em dados "internos"

---

## 7. Princípios de Segurança

### Checklist de Segurança (Não Código)

- [ ] **Validação de entrada**: Todas as entradas validadas
- [ ] **Queries parametrizadas**: Sem concatenação de string para SQL
- [ ] **Hash de senha**: bcrypt ou argon2
- [ ] **Verificação JWT**: Sempre verifique assinatura e expiração
- [ ] **Rate limiting**: Proteção contra abuso
- [ ] **Security headers**: Helmet.js ou equivalente
- [ ] **HTTPS**: Em produção
- [ ] **CORS**: Propriamente configurado
- [ ] **Secrets**: Apenas variáveis de ambiente
- [ ] **Dependências**: Auditadas regularmente

### Mentalidade de Segurança

```
Não confie em nada:
├── Query params → valide
├── Corpo da requisição → valide
├── Headers → verifique
├── Cookies → valide
├── Uploads de arquivo → escaneie
└── APIs externas → valide resposta
```

---

## 8. Princípios de Testes

### Seleção de Estratégia de Teste

| Tipo | Propósito | Ferramentas |
|------|----------|-----------|
| **Unitário** | Lógica de negócio | node:test, Vitest |
| **Integração** | Endpoints de API | Supertest |
| **E2E** | Fluxos completos | Playwright |

### O Que Testar (Prioridades)

1. **Caminhos críticos**: Autenticação, pagamentos, negócio principal
2. **Casos extremos**: Entradas vazias, limites
3. **Tratamento de erros**: O que acontece quando falha?
4. **Não vale a pena testar**: Código do framework, getters triviais

### Test Runner Integrado (Node.js 22+)

```
node --test src/**/*.test.ts
├── Sem dependência externa
├── Boa cobertura de reportagem
└── Modo watch disponível
```

---

## 10. Anti-padrões para Evitar

### ❌ NÃO FAÇA:
- Use Express para novos projetos edge (use Hono)
- Use métodos síncronos em código de produção
- Coloque lógica de negócio em controllers
- Pule validação de entrada
- Hardcode secrets
- Confie em dados externos sem validação
- Bloqueie event loop com trabalho CPU

### ✅ FAÇA:
- Escolha framework baseado no contexto
- Pergunte ao usuário sobre preferências quando não estiverem claras
- Use arquitetura em camadas para projetos em crescimento
- Valide todas as entradas
- Use variáveis de ambiente para secrets
- Faça profile antes de otimizar

---

## 11. Checklist de Decisão

Antes de implementar:

- [ ] **Perguntou ao usuário sobre preferência de stack?**
- [ ] **Escolheu framework para ESTE contexto?** (não só padrão)
- [ ] **Considerou alvo de deployment?**
- [ ] **Planejou estratégia de tratamento de erros?**
- [ ] **Identificou pontos de validação?**
- [ ] **Considerou requisitos de segurança?**

---

> **Lembre-se**: Node.js best practices são sobre tomada de decisão, não memorizar padrões. Todo projeto merece consideração fresca baseada em seus requisitos.