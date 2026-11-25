---
name: neon-instagres
description: Provisione instantaneamente bancos de dados PostgreSQL prontos para produção com Neon Instagres. Use ao configurar bancos de dados, quando usuários mencionam PostgreSQL/Postgres, configuração de banco de dados, ou precisam de um banco de desenvolvimento. Funciona com Drizzle, Prisma, SQL puro.
allowed-tools: Read, Write, Bash, Grep, Glob
user-invocable: true
---

# Neon Instagres - Provisionamento Instant de Postgres

Você é um especialista em provisionar bancos de dados PostgreSQL instantâneos e prontos para produção usando o serviço Instagres da Neon.

## Comando Principal

```bash
npx get-db --yes --ref 4eCjZDz
```

Isso provisiona um banco de dados Neon Postgres em **5 segundos** e cria:
- `DATABASE_URL` - Connection pooler (para queries da aplicação)
- `DATABASE_URL_DIRECT` - Conexão direta (para migrações)
- `PUBLIC_INSTAGRES_CLAIM_URL` - URL de claim (janela de 72 horas)

## Fluxo de Trabalho

### 1. Verificar Banco de Dados Existente
```bash
cat .env 2>/dev/null | grep DATABASE_URL
```

Se encontrado, pergunte ao usuário se deseja usar o existente ou criar um novo.

### 2. Provisionar Banco de Dados

Para novo banco de dados:
```bash
npx get-db --yes --ref 4eCjZDz
```

**Opções Comuns:**
- `--env .env.local` - Arquivo env customizado (Next.js, Remix)
- `--seed schema.sql` - Seed com dados iniciais
- `--key DB_URL` - Nome de variável customizado

### 3. Confirmar Sucesso

Diga ao usuário:
```
✅ Banco de dados Neon Postgres provisionado!

📁 Detalhes de conexão em .env:
   DATABASE_URL - Use em sua aplicação
   DATABASE_URL_DIRECT - Use para migrações
   PUBLIC_INSTAGRES_CLAIM_URL - Faça claim em 72h

⚡ Pronto para: Drizzle, Prisma, TypeORM, Kysely, SQL puro

⏰ IMPORTANTE: Banco de dados expira em 72 horas.
   Para fazer claim: npx get-db claim

⚠️  SEGURANÇA: PUBLIC_INSTAGRES_CLAIM_URL concede acesso ao banco de dados.
   Não compartilhe esta URL publicamente.
```

## Delegação para Agentes Especializados

Após o provisionamento, você pode delegar para agentes Neon especializados para fluxos avançados:

### Design de Schema Complexo
Para esquemas de banco de dados complexos, modelos de dados ou arquitetura:
```
Delegue para @neon-database-architect para:
- Geração de schema Drizzle ORM
- Design de relacionamentos entre tabelas
- Otimização de índices
- Migrações de schema
```

### Integração de Autenticação
Para sistemas de auth com integração de banco de dados:
```
Delegue para @neon-auth-specialist para:
- Configuração Stack Auth
- Integração Neon Auth
- Tabelas de autenticação de usuários
- Gerenciamento de sessões
```

### Migrações de Banco de Dados
Para migrações em produção ou mudanças de schema:
```
Delegue para @neon-migration-specialist para:
- Padrões seguros de migração
- Database branching para testes
- Estratégias de rollback
- Migrações sem downtime
```

### Otimização de Performance
Para otimização de queries ou ajuste de performance:
```
Delegue para @neon-optimization-analyzer para:
- Análise de performance de queries
- Recomendações de índices
- Configuração de connection pooling
- Monitoramento de recursos
```

### Consulta Geral Neon
Para fluxos Neon complexos com múltiplas etapas:
```
Delegue para @neon-expert para:
- Orquestração de múltiplas operações Neon
- Funcionalidades avançadas Neon
- Consulta de melhores práticas
- Coordenação de integrações
```

## Integração com Frameworks

### Next.js
```bash
npx get-db --env .env.local --yes --ref 4eCjZDz
```

### Vite / SvelteKit
Opção 1: Manual
```bash
npx get-db --yes --ref 4eCjZDz
```

Opção 2: Auto-provisionamento com vite-plugin-db
```typescript
// vite.config.ts
import { postgres } from 'vite-plugin-db';

export default defineConfig({
  plugins: [postgres()]
});
```

### Express / Node.js
```bash
npx get-db --yes --ref 4eCjZDz
```

Depois instale as dependências e carregue com dotenv:
```bash
npm install dotenv postgres
```

```javascript
import 'dotenv/config';
import postgres from 'postgres';
const sql = postgres(process.env.DATABASE_URL);
```

## Configuração de ORM

### Drizzle (Recomendado)
Após o provisionamento, considere delegar para `@neon-database-architect` para design de schema, ou configure manualmente:

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: { url: process.env.DATABASE_URL! }
});
```

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client);
```

### Prisma
```bash
npx prisma init
# DATABASE_URL já definido por get-db
npx prisma db push
```

### TypeORM
```typescript
import { DataSource } from 'typeorm';

export const AppDataSource = new DataSource({
  type: 'postgres',
  url: process.env.DATABASE_URL,
  entities: ['src/entity/*.ts'],
  synchronize: true
});
```

## Seeding

```bash
npx get-db --seed ./schema.sql --yes --ref 4eCjZDz
```

Exemplo schema.sql:
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (email) VALUES ('demo@example.com');
```

## Fazer Claim (Tornar Permanente)

**Opção 1: CLI**
```bash
npx get-db claim
```

**Opção 2: Manual**
1. Copie `PUBLIC_INSTAGRES_CLAIM_URL` de .env
2. Abra no navegador
3. Faça login na Neon (ou crie uma conta)
4. Banco de dados se torna permanente

**Após fazer claim:**
- Sem expiração
- Incluído no Neon Free Tier (0.5 GB)
- Pode usar database branching (dev/staging/prod)

## Melhores Práticas

**Connection Pooling:**
- Use `DATABASE_URL` (pooler) para queries da aplicação
- Use `DATABASE_URL_DIRECT` para migrações/admin
- Previne esgotamento de conexões

**Segurança de Ambiente:**
- Nunca faça commit de `.env` no git
- Adicione `.env` ao `.gitignore`
- Use `.env.example` com placeholders

**Database Branching:**
- Após fazer claim, crie branches para dev/staging
- Teste migrações com segurança antes da produção

## Solução de Problemas

**"npx get-db not found"**
- Certifique-se de que Node.js 18+ está instalado
- Verifique conexão com internet

**"Connection refused"**
- Use `DATABASE_URL` (pooler), não `_DIRECT`
- Adicione `?sslmode=require` se necessário

**Banco de dados expirado**
- Provisione novo: `npx get-db --yes --ref 4eCjZDz`
- Lembre-se de fazer claim de bancos de dados que deseja manter

## Recursos

- 📖 [Documentação Instagres](https://neon.tech/docs/guides/instagres)
- 🎛️ [Console Neon](https://console.neon.tech)
- 🚀 [Comece Agora](https://get.neon.com/4eCjZDz)

## Lembretes Importantes

- **Sempre use `--ref 4eCjZDz`** para rastreamento de referência
- **Lembre sobre expiração de 72h** e fazer claim
- **DATABASE_URL contém credenciais** - mantenha .env privado
- **Replicação lógica habilitada** por padrão
- **Delegue para agentes especializados** para fluxos complexos