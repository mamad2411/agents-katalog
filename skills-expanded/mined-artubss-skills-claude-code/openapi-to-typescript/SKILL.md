---
name: openapi-to-typescript
description: Converte OpenAPI 3.0 JSON/YAML para interfaces TypeScript e type guards. Esta skill deve ser usada quando o usuário solicita gerar tipos a partir de OpenAPI, converter schema para TS, criar interfaces de API ou gerar tipos TypeScript a partir de uma especificação de API.
---

# OpenAPI para TypeScript

Converte especificações OpenAPI 3.0 para interfaces TypeScript e type guards.

**Entrada:** Arquivo OpenAPI (JSON ou YAML)
**Saída:** Arquivo TypeScript com interfaces e type guards

## Quando Usar

- "gerar tipos a partir de openapi"
- "converter openapi para typescript"
- "criar interfaces de API"
- "gerar tipos a partir de spec"

## Fluxo de Trabalho

1. Solicitar o caminho do arquivo OpenAPI (se não fornecido)
2. Ler e validar o arquivo (deve ser OpenAPI 3.0.x)
3. Extrair schemas de `components/schemas`
4. Extrair endpoints de `paths` (tipos de requisição/resposta)
5. Gerar TypeScript (interfaces + type guards)
6. Perguntar onde salvar (padrão: `types/api.ts` no diretório atual)
7. Escrever o arquivo

## Validação OpenAPI

Verificar antes de processar:

```
- Campo "openapi" deve existir e começar com "3.0"
- Campo "paths" deve existir
- Campo "components.schemas" deve existir (se houver tipos)
```

Se inválido, reportar o erro e parar.

## Mapeamento de Tipos

### Primitivos

| OpenAPI     | TypeScript   |
|-------------|--------------|
| `string`    | `string`     |
| `number`    | `number`     |
| `integer`   | `number`     |
| `boolean`   | `boolean`    |
| `null`      | `null`       |

### Modificadores de Formato

| Formato       | TypeScript              |
|---------------|-------------------------|
| `uuid`        | `string` (comentário UUID) |
| `date`        | `string` (comentário data) |
| `date-time`   | `string` (comentário ISO)  |
| `email`       | `string` (comentário email)|
| `uri`         | `string` (comentário URI)  |

### Tipos Complexos

**Object:**
```typescript
// OpenAPI: type: object, properties: {id, name}, required: [id]
interface Example {
  id: string;      // required: sem ?
  name?: string;   // optional: com ?
}
```

**Array:**
```typescript
// OpenAPI: type: array, items: {type: string}
type Names = string[];
```

**Enum:**
```typescript
// OpenAPI: type: string, enum: [active, draft]
type Status = "active" | "draft";
```

**oneOf (Union):**
```typescript
// OpenAPI: oneOf: [{$ref: Cat}, {$ref: Dog}]
type Pet = Cat | Dog;
```

**allOf (Intersection/Extends):**
```typescript
// OpenAPI: allOf: [{$ref: Base}, {type: object, properties: ...}]
interface Extended extends Base {
  extraField: string;
}
```

## Geração de Código

### Cabeçalho do Arquivo

```typescript
/**
 * Auto-gerado de: {source_file}
 * Gerado em: {timestamp}
 *
 * NÃO EDITAR MANUALMENTE - Regenerar a partir do schema OpenAPI
 */
```

### Interfaces (de components/schemas)

Para cada schema em `components/schemas`:

```typescript
export interface Product {
  /** Identificador único do produto */
  id: string;

  /** Título do produto */
  title: string;

  /** Preço do produto */
  price: number;

  /** Timestamp de criação */
  created_at?: string;
}
```

- Usar descrição OpenAPI como JSDoc
- Campos em `required[]` não têm `?`
- Campos fora de `required[]` têm `?`

### Tipos de Requisição/Resposta (de paths)

Para cada endpoint em `paths`:

```typescript
// GET /products - parâmetros de query
export interface GetProductsRequest {
  page?: number;
  limit?: number;
}

// GET /products - resposta 200
export type GetProductsResponse = ProductList;

// POST /products - corpo da requisição
export interface CreateProductRequest {
  title: string;
  price: number;
}

// POST /products - resposta 201
export type CreateProductResponse = Product;
```

Convenção de nomenclatura:
- `{Method}{Path}Request` para params/body
- `{Method}{Path}Response` para resposta

### Type Guards

Para cada interface principal, gerar um type guard:

```typescript
export function isProduct(value: unknown): value is Product {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof (value as any).id === 'string' &&
    'title' in value &&
    typeof (value as any).title === 'string' &&
    'price' in value &&
    typeof (value as any).price === 'number'
  );
}
```

Regras de type guard:
- Verificar `typeof value === 'object' && value !== null`
- Para cada campo obrigatório: verificar `'field' in value`
- Para campos primitivos: verificar `typeof`
- Para arrays: verificar `Array.isArray()`
- Para enums: verificar `.includes()`

### Tipo de Erro (sempre incluir)

```typescript
export interface ApiError {
  status: number;
  error: string;
  detail?: string;
}

export function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    typeof (value as any).status === 'number' &&
    'error' in value &&
    typeof (value as any).error === 'string'
  );
}
```

## Resolução de $ref

Ao encontrar `{"$ref": "#/components/schemas/Product"}`:
1. Extrair o nome do schema (`Product`)
2. Usar o tipo diretamente (não resolver inline)

```typescript
// OpenAPI: items: {$ref: "#/components/schemas/Product"}
// TypeScript:
items: Product[]  // referência, não inline
```

## Exemplo Completo

**Entrada (OpenAPI):**
```json
{
  "openapi": "3.0.0",
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "format": "uuid"},
          "email": {"type": "string", "format": "email"},
          "role": {"type": "string", "enum": ["admin", "user"]}
        },
        "required": ["id", "email", "role"]
      }
    }
  },
  "paths": {
    "/users/{id}": {
      "get": {
        "parameters": [{"name": "id", "in": "path", "required": true}],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/User"}
              }
            }
          }
        }
      }
    }
  }
}
```

**Saída (TypeScript):**
```typescript
/**
 * Auto-gerado de: api.openapi.json
 * Gerado em: 2025-01-15T10:30:00Z
 *
 * NÃO EDITAR MANUALMENTE - Regenerar a partir do schema OpenAPI
 */

// ============================================================================
// Types
// ============================================================================

export type UserRole = "admin" | "user";

export interface User {
  /** UUID */
  id: string;

  /** Email */
  email: string;

  role: UserRole;
}

// ============================================================================
// Request/Response Types
// ============================================================================

export interface GetUserByIdRequest {
  id: string;
}

export type GetUserByIdResponse = User;

// ============================================================================
// Type Guards
// ============================================================================

export function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof (value as any).id === 'string' &&
    'email' in value &&
    typeof (value as any).email === 'string' &&
    'role' in value &&
    ['admin', 'user'].includes((value as any).role)
  );
}

// ============================================================================
// Error Types
// ============================================================================

export interface ApiError {
  status: number;
  error: string;
  detail?: string;
}

export function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    typeof (value as any).status === 'number' &&
    'error' in value &&
    typeof (value as any).error === 'string'
  );
}
```

## Erros Comuns

| Erro | Ação |
|------|------|
| Versão OpenAPI != 3.0.x | Reportar que apenas 3.0 é suportada |
| $ref não encontrado | Listar refs ausentes |
| Tipo desconhecido | Usar `unknown` e avisar |
| Referência circular | Usar type alias com referência lazy |