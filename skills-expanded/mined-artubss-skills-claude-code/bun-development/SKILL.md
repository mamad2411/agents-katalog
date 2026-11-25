---
name: bun-development
description: "Desenvolvimento moderno de JavaScript/TypeScript com runtime Bun. Cobre gerenciamento de pacotes, bundling, testes e migração do Node.js. Use quando trabalhar com Bun, otimizar velocidade de desenvolvimento JS/TS ou migrar do Node.js para Bun."
---

# ⚡ Desenvolvimento com Bun

> Desenvolvimento rápido e moderno de JavaScript/TypeScript com o runtime Bun, inspirado em [oven-sh/bun](https://github.com/oven-sh/bun).

## Quando Usar Esta Skill

Use esta skill quando:

- Iniciar novos projetos JS/TS com Bun
- Migrar do Node.js para Bun
- Otimizar velocidade de desenvolvimento
- Usar ferramentas nativas do Bun (bundler, test runner)
- Resolver problemas específicos do Bun

---

## 1. Primeiros Passos

### 1.1 Instalação

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"

# Homebrew
brew tap oven-sh/bun
brew install bun

# npm (se necessário)
npm install -g bun

# Upgrade
bun upgrade
```

### 1.2 Por Que Bun?

| Recurso              | Bun            | Node.js                          |
| :------------------ | :------------- | :------------------------------- |
| Tempo de inicialização | ~25ms        | ~100ms+                          |
| Instalação de pacotes | 10-100x mais rápido | Baseline                    |
| TypeScript           | Nativo         | Requer transpilador              |
| JSX                  | Nativo         | Requer transpilador              |
| Test runner          | Nativo         | Externo (Jest, Vitest)          |
| Bundler              | Nativo         | Externo (Webpack, esbuild)      |

---

## 2. Configuração do Projeto

### 2.1 Criar Novo Projeto

```bash
# Inicializar projeto
bun init

# Cria:
# ├── package.json
# ├── tsconfig.json
# ├── index.ts
# └── README.md

# Com template específico
bun create <template> <project-name>

# Exemplos
bun create react my-app        # App React
bun create next my-app         # App Next.js
bun create vite my-app         # App Vite
bun create elysia my-api       # API Elysia
```

### 2.2 package.json

```json
{
  "name": "my-bun-project",
  "version": "1.0.0",
  "module": "index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun run --watch index.ts",
    "start": "bun run index.ts",
    "test": "bun test",
    "build": "bun build ./index.ts --outdir ./dist",
    "lint": "bunx eslint ."
  },
  "devDependencies": {
    "@types/bun": "latest"
  },
  "peerDependencies": {
    "typescript": "^5.0.0"
  }
}
```

### 2.3 tsconfig.json (Otimizado para Bun)

```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "module": "esnext",
    "target": "esnext",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "composite": true,
    "strict": true,
    "downlevelIteration": true,
    "skipLibCheck": true,
    "jsx": "react-jsx",
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "allowJs": true,
    "types": ["bun-types"]
  }
}
```

---

## 3. Gerenciamento de Pacotes

### 3.1 Instalando Pacotes

```bash
# Instalar do package.json
bun install              # ou 'bun i'

# Adicionar dependências
bun add express          # Dependência regular
bun add -d typescript    # Dependência de desenvolvimento
bun add -D @types/node   # Dependência de desenvolvimento (alias)
bun add --optional pkg   # Dependência opcional

# De registro específico
bun add lodash --registry https://registry.npmmirror.com

# Instalar versão específica
bun add react@18.2.0
bun add react@latest
bun add react@next

# Do Git
bun add github:user/repo
bun add git+https://github.com/user/repo.git
```

### 3.2 Removendo & Atualizando

```bash
# Remover pacote
bun remove lodash

# Atualizar pacotes
bun update              # Atualizar todos
bun update lodash       # Atualizar específico
bun update --latest     # Atualizar para latest (ignora ranges)

# Verificar desatualizados
bun outdated
```

### 3.3 bunx (equivalente a npx)

```bash
# Executar binários de pacotes
bunx prettier --write .
bunx tsc --init
bunx create-react-app my-app

# Com versão específica
bunx -p typescript@4.9 tsc --version

# Executar sem instalar
bunx cowsay "Hello from Bun!"
```

### 3.4 Lockfile

```bash
# bun.lockb é um lockfile binário (parsing mais rápido)
# Para gerar lockfile de texto para debugging:
bun install --yarn    # Cria yarn.lock

# Confiar em lockfile existente
bun install --frozen-lockfile
```

---

## 4. Executando Código

### 4.1 Execução Básica

```bash
# Executar TypeScript diretamente (sem build!)
bun run index.ts

# Executar JavaScript
bun run index.js

# Executar com argumentos
bun run server.ts --port 3000

# Executar script do package.json
bun run dev
bun run build

# Forma curta (para scripts)
bun dev
bun build
```

### 4.2 Modo Watch

```bash
# Auto-reiniciar em mudanças de arquivo
bun --watch run index.ts

# Com hot reloading
bun --hot run server.ts
```

### 4.3 Variáveis de Ambiente

```typescript
// Arquivo .env é carregado automaticamente!

// Acessar variáveis de ambiente
const apiKey = Bun.env.API_KEY;
const port = Bun.env.PORT ?? "3000";

// Ou usar process.env (compatível com Node.js)
const dbUrl = process.env.DATABASE_URL;
```

```bash
# Executar com arquivo .env específico
bun --env-file=.env.production run index.ts
```

---

## 5. APIs Nativas

### 5.1 Sistema de Arquivos (Bun.file)

```typescript
// Ler arquivo
const file = Bun.file("./data.json");
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();

// Informações do arquivo
console.log(file.size); // bytes
console.log(file.type); // tipo MIME

// Escrever arquivo
await Bun.write("./output.txt", "Hello, Bun!");
await Bun.write("./data.json", JSON.stringify({ foo: "bar" }));

// Stream para arquivos grandes
const reader = file.stream();
for await (const chunk of reader) {
  console.log(chunk);
}
```

### 5.2 Servidor HTTP (Bun.serve)

```typescript
const server = Bun.serve({
  port: 3000,

  fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/") {
      return new Response("Hello World!");
    }

    if (url.pathname === "/api/users") {
      return Response.json([
        { id: 1, name: "Alice" },
        { id: 2, name: "Bob" },
      ]);
    }

    return new Response("Not Found", { status: 404 });
  },

  error(error) {
    return new Response(`Error: ${error.message}`, { status: 500 });
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

### 5.3 Servidor WebSocket

```typescript
const server = Bun.serve({
  port: 3000,

  fetch(req, server) {
    // Fazer upgrade para WebSocket
    if (server.upgrade(req)) {
      return; // Upgraded
    }
    return new Response("Upgrade failed", { status: 500 });
  },

  websocket: {
    open(ws) {
      console.log("Client connected");
      ws.send("Welcome!");
    },

    message(ws, message) {
      console.log(`Received: ${message}`);
      ws.send(`Echo: ${message}`);
    },

    close(ws) {
      console.log("Client disconnected");
    },
  },
});
```

### 5.4 SQLite (Bun.sql)

```typescript
import { Database } from "bun:sqlite";

const db = new Database("mydb.sqlite");

// Criar tabela
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

// Inserir
const insert = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
insert.run("Alice", "alice@example.com");

// Consultar
const query = db.prepare("SELECT * FROM users WHERE name = ?");
const user = query.get("Alice");
console.log(user); // { id: 1, name: "Alice", email: "alice@example.com" }

// Consultar todos
const allUsers = db.query("SELECT * FROM users").all();
```

### 5.5 Hash de Senha

```typescript
// Hash de senha
const password = "super-secret";
const hash = await Bun.password.hash(password);

// Verificar senha
const isValid = await Bun.password.verify(password, hash);
console.log(isValid); // true

// Com opções de algoritmo
const bcryptHash = await Bun.password.hash(password, {
  algorithm: "bcrypt",
  cost: 12,
});
```

---

## 6. Testes

### 6.1 Testes Básicos

```typescript
// math.test.ts
import { describe, it, expect, beforeAll, afterAll } from "bun:test";

describe("Math operations", () => {
  it("adds two numbers", () => {
    expect(1 + 1).toBe(2);
  });

  it("subtracts two numbers", () => {
    expect(5 - 3).toBe(2);
  });
});
```

### 6.2 Executando Testes

```bash
# Executar todos os testes
bun test

# Executar arquivo específico
bun test math.test.ts

# Executar com padrão correspondente
bun test --grep "adds"

# Modo watch
bun test --watch

# Com cobertura
bun test --coverage

# Timeout
bun test --timeout 5000
```

### 6.3 Matchers

```typescript
import { expect, test } from "bun:test";

test("matchers", () => {
  // Igualdade
  expect(1).toBe(1);
  expect({ a: 1 }).toEqual({ a: 1 });
  expect([1, 2]).toContain(1);

  // Comparações
  expect(10).toBeGreaterThan(5);
  expect(5).toBeLessThanOrEqual(5);

  // Veracidade
  expect(true).toBeTruthy();
  expect(null).toBeNull();
  expect(undefined).toBeUndefined();

  // Strings
  expect("hello").toMatch(/ell/);
  expect("hello").toContain("ell");

  // Arrays
  expect([1, 2, 3]).toHaveLength(3);

  // Exceções
  expect(() => {
    throw new Error("fail");
  }).toThrow("fail");

  // Async
  await expect(Promise.resolve(1)).resolves.toBe(1);
  await expect(Promise.reject("err")).rejects.toBe("err");
});
```

### 6.4 Mocking

```typescript
import { mock, spyOn } from "bun:test";

// Mock de função
const mockFn = mock((x: number) => x * 2);
mockFn(5);
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith(5);
expect(mockFn.mock.results[0].value).toBe(10);

// Espiar em método
const obj = {
  method: () => "original",
};
const spy = spyOn(obj, "method").mockReturnValue("mocked");
expect(obj.method()).toBe("mocked");
expect(spy).toHaveBeenCalled();
```

---

## 7. Bundling

### 7.1 Build Básico

```bash
# Fazer bundle para produção
bun build ./src/index.ts --outdir ./dist

# Com opções
bun build ./src/index.ts \
  --outdir ./dist \
  --target browser \
  --minify \
  --sourcemap
```

### 7.2 Build API

```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "browser", // ou "bun", "node"
  minify: true,
  sourcemap: "external",
  splitting: true,
  format: "esm",

  // Pacotes externos (não bundled)
  external: ["react", "react-dom"],

  // Definir globais
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },

  // Nomeação
  naming: {
    entry: "[name].[hash].js",
    chunk: "chunks/[name].[hash].js",
    asset: "assets/[name].[hash][ext]",
  },
});

if (!result.success) {
  console.error(result.logs);
}
```

### 7.3 Compilar para Executável

```bash
# Criar executável standalone
bun build ./src/cli.ts --compile --outfile myapp

# Compilação cruzada
bun build ./src/cli.ts --compile --target=bun-linux-x64 --outfile myapp-linux
bun build ./src/cli.ts --compile --target=bun-darwin-arm64 --outfile myapp-mac

# Com assets embutidos
bun build ./src/cli.ts --compile --outfile myapp --embed ./assets
```

---

## 8. Migração do Node.js

### 8.1 Compatibilidade

```typescript
// A maioria das APIs do Node.js funciona fora da caixa
import fs from "fs";
import path from "path";
import crypto from "crypto";

// process é global
console.log(process.cwd());
console.log(process.env.HOME);

// Buffer é global
const buf = Buffer.from("hello");

// __dirname e __filename funcionam
console.log(__dirname);
console.log(__filename);
```

### 8.2 Passos Comuns de Migração

```bash
# 1. Instalar Bun
curl -fsSL https://bun.sh/install | bash

# 2. Substituir gerenciador de pacotes
rm -rf node_modules package-lock.json
bun install

# 3. Atualizar scripts em package.json
# "start": "node index.js" → "start": "bun run index.ts"
# "test": "jest" → "test": "bun test"

# 4. Adicionar tipos do Bun
bun add -d @types/bun
```

### 8.3 Diferenças do Node.js

```typescript
// ❌ Específico do Node.js (pode não funcionar)
require("module")             // Use import em vez disso
require.resolve("pkg")        // Use import.meta.resolve
__non_webpack_require__       // Não suportado

// ✅ Equivalentes do Bun
import pkg from "pkg";
const resolved = import.meta.resolve("pkg");
Bun.resolveSync("pkg", process.cwd());

// ❌ Essas globais diferem
process.hrtime()              // Use Bun.nanoseconds()
setImmediate()                // Use queueMicrotask()

// ✅ Recursos específicos do Bun
const file = Bun.file("./data.txt");  // API rápida de arquivo
Bun.serve({ port: 3000, fetch: ... }); // Servidor HTTP rápido
Bun.password.hash(password);           // Hash nativo
```

---

## 9. Dicas de Performance

### 9.1 Use APIs Nativas do Bun

```typescript
// Lento (compatibilidade com Node.js)
import fs from "fs/promises";
const content = await fs.readFile("./data.txt", "utf-8");

// Rápido (nativo do Bun)
const file = Bun.file("./data.txt");
const content = await file.text();
```

### 9.2 Use Bun.serve para HTTP

```typescript
// Não faça: Express/Fastify (overhead)
import express from "express";
const app = express();

// Faça: Bun.serve (nativo, 4-10x mais rápido)
Bun.serve({
  fetch(req) {
    return new Response("Hello!");
  },
});

// Ou use Elysia (framework otimizado para Bun)
import { Elysia } from "elysia";
new Elysia().get("/", () => "Hello!").listen(3000);
```

### 9.3 Fazer Bundle para Produção

```bash
# Sempre fazer bundle e minificar para produção
bun build ./src/index.ts --outdir ./dist --minify --target node

# Depois executar o bundle
bun run ./dist/index.js
```

---

## Referência Rápida

| Tarefa       | Comando                                    |
| :----------- | :----------------------------------------- |
| Inicializar projeto | `bun init`                         |
| Instalar dependências | `bun install`                  |
| Adicionar pacote | `bun add <pkg>`                     |
| Executar script | `bun run <script>`                  |
| Executar arquivo | `bun run file.ts`                   |
| Modo watch | `bun --watch run file.ts`               |
| Executar testes | `bun test`                          |
| Build | `bun build ./src/index.ts --outdir ./dist` |
| Executar pacote | `bunx <pkg>`                         |

---

## Recursos

- [Bun Documentation](https://bun.sh/docs)
- [Bun GitHub](https://github.com/oven-sh/bun)
- [Elysia Framework](https://elysiajs.com/)
- [Bun Discord](https://bun.sh/discord)