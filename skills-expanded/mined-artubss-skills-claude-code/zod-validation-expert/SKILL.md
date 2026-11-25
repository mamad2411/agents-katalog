---
name: zod-validation-expert
description: "Especialista em Zod — validação de schemas em TypeScript. Aborda parsing, erros customizados, refinamentos, inferência de tipos e integração com React Hook Form, Next.js e tRPC."
risk: safe
source: community
date_added: "2026-03-05"
---

# Especialista em Validação Zod

Você é um especialista Zod em nível de produção. Você ajuda desenvolvedores a construir definições de schema type-safe e lógica de validação. Você domina os fundamentos do Zod (primitivos, objetos, arrays, records), inferência de tipos (`z.infer`), validações complexas (`.refine`, `.superRefine`), transformações (`.transform`) e integrações no ecossistema moderno de TypeScript (React Hook Form, Next.js API Routes / App Router Actions, tRPC e variáveis de ambiente).

## Quando Usar Essa Skill

- Use ao definir schemas de validação TypeScript para inputs de API ou formulários
- Use ao configurar validação de variáveis de ambiente (`process.env`)
- Use ao integrar Zod com React Hook Form (`@hookform/resolvers/zod`)
- Use ao extrair ou inferir tipos TypeScript de schemas de validação em runtime
- Use ao escrever regras de validação complexas (ex: validação entre campos, validação assíncrona)
- Use ao transformar dados de entrada (ex: string para Date, coerção de string para número)
- Use ao padronizar formatação de mensagens de erro

## Conceitos Fundamentais

### Por Que Zod?

Zod elimina a duplicação de escrever uma interface TypeScript *e* um schema de validação em runtime. Você define o schema uma vez, e Zod infere o tipo TypeScript estático. Note que Zod é para **parsing, não apenas validação**. `safeParse` e `parse` retornam dados limpos e tipados, removendo chaves desconhecidas por padrão.

## Definição de Schema e Inferência de Tipos

### Primitivos e Coerção

```typescript
import { z } from "zod";

// Primitivos básicos
const stringSchema = z.string().min(3).max(255);
const numberSchema = z.number().int().positive();
const dateSchema = z.date();

// Coerção (casting automático de inputs antes da validação)
// Muito útil para FormData em Next.js Server Actions ou queries de URL
const ageSchema = z.coerce.number().min(18); // "18" -> 18
const activeSchema = z.coerce.boolean(); // "true" -> true
const dobSchema = z.coerce.date(); // "2020-01-01" -> Date object
```

### Objetos e Inferência de Tipos

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  username: z.string().min(3).max(20),
  email: z.string().email(),
  role: z.enum(["ADMIN", "USER", "GUEST"]).default("USER"),
  age: z.number().min(18).optional(), // Pode ser omitido
  website: z.string().url().nullable(), // Pode ser null
  tags: z.array(z.string()).min(1), // Array com pelo menos 1 item
});

// Infira o tipo TypeScript diretamente do schema
// Sem necessidade de escrever uma `interface User { ... }` separada
export type User = z.infer<typeof UserSchema>;
```

### Tipos Avançados

```typescript
// Records (Objetos com chaves dinâmicas mas tipos de valor específicos)
const envSchema = z.record(z.string(), z.string()); // Record<string, string>

// Unions (OU)
const idSchema = z.union([z.string(), z.number()]); // string | number
// Ou mais simples:
const idSchema2 = z.string().or(z.number());

// Discriminated Unions (Cases switch type-safe)
const ActionSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("create"), id: z.string() }),
  z.object({ type: z.literal("update"), id: z.string(), data: z.any() }),
  z.object({ type: z.literal("delete"), id: z.string() }),
]);
```

## Parsing e Validação

### parse vs safeParse

```typescript
const schema = z.string().email();

// ❌ parse: Lança um ZodError se a validação falhar
try {
  const email = schema.parse("invalid-email");
} catch (err) {
  if (err instanceof z.ZodError) {
    console.error(err.issues);
  }
}

// ✅ safeParse: Retorna um objeto de resultado (Sem necessidade de try/catch)
const result = schema.safeParse("user@example.com");

if (!result.success) {
  // TypeScript reduz result para SafeParseError
  console.log(result.error.format()); 
  // Early return ou lance erro de domínio
} else {
  // TypeScript reduz result para SafeParseSuccess
  const validEmail = result.data; // Type é `string`
}
```

## Customizando Validação

### Mensagens de Erro Customizadas

```typescript
const passwordSchema = z.string()
  .min(8, { message: "Senha deve ter pelo menos 8 caracteres" })
  .max(100, { message: "Senha é muito longa" })
  .regex(/[A-Z]/, { message: "Senha deve conter pelo menos uma letra maiúscula" })
  .regex(/[0-9]/, { message: "Senha deve conter pelo menos um número" });

// Mapa de erros global (útil para i18n)
z.setErrorMap((issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === "string") return { message: "Este campo deve ser texto" };
  }
  return { message: ctx.defaultError };
});
```

### Refinamentos (Lógica Customizada)

```typescript
// Refinamento básico
const passwordCheck = z.string().refine((val) => val !== "password123", {
  message: "Senha muito fraca",
});

// Validação entre campos (ex: confirmar senha)
const formSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Senhas não correspondem",
  path: ["confirmPassword"], // Define o erro no campo específico
});
```

### Transformações

```typescript
// Altere dados durante o parsing
const stringToNumber = z.string()
  .transform((val) => parseInt(val, 10))
  .refine((val) => !isNaN(val), { message: "Não é um inteiro válido" });

// Agora o tipo inferido é `number`, não `string`!
type TransformedResult = z.infer<typeof stringToNumber>; // number
```

## Padrões de Integração

### React Hook Form

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("Endereço de email inválido"),
  password: z.string().min(6, "Senha deve ter 6+ caracteres"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = (data: LoginFormValues) => {
    // data é totalmente tipado e validado
    console.log(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      {/* ... */}
    </form>
  );
}
```

### Next.js Server Actions

```typescript
"use server";
import { z } from "zod";

// Coerção é crítica aqui porque valores de FormData são sempre strings
const createPostSchema = z.object({
  title: z.string().min(3),
  content: z.string().optional(),
  published: z.coerce.boolean().default(false), // checkbox -> "on" -> true
});

export async function createPost(prevState: any, formData: FormData) {
  // Converta FormData para objeto padrão usando Object.fromEntries
  const rawData = Object.fromEntries(formData.entries());
  
  const validatedFields = createPostSchema.safeParse(rawData);
  
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }
  
  // Prossiga com operação de banco de dados validada
  const { title, content, published } = validatedFields.data;
  // ...
  return { success: true };
}
```

### Variáveis de Ambiente

```typescript
// Torne variáveis de ambiente estritamente tipadas e falhe rápido
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().default(3000),
  API_KEY: z.string().min(10),
});

// Falha o build imediatamente se variáveis de env estão faltando ou inválidas
const env = envSchema.parse(process.env);

export default env;
```

## Melhores Práticas

- ✅ **Faça:** Co-localize schemas junto aos componentes ou rotas de API que os usam para manter separação de responsabilidades.
- ✅ **Faça:** Use `z.infer<typeof Schema>` em todos os lugares em vez de manter interfaces TypeScript duplicadas manualmente.
- ✅ **Faça:** Prefira `safeParse` sobre `parse` para evitar blocos `try/catch` espalhados e aproveite o type narrowing do TypeScript para tratamento robusto de erros.
- ✅ **Faça:** Use `z.coerce` ao aceitar dados de `URLSearchParams` ou `FormData`, e esteja ciente que `z.coerce.boolean()` converte strings `"false"`/`"off"` de forma inesperada sem pré-processamento customizado.
- ✅ **Faça:** Use `.flatten()` ou `.format()` em objetos `ZodError` para extrair facilmente erros serializáveis e legíveis para consumo no frontend.
- ❌ **Não:** Confie exclusivamente em `.partial()` para schemas de atualização se tipos de campo ou restrições diferirem entre operações de criação e atualização; defina schemas distintos.
- ❌ **Não:** Esqueça de passar a opção `path` em `.refine()` ou `.superRefine()` ao realizar validações entre campos de nível de objeto, senão o erro não será anexado ao campo de input correto.

## Resolução de Problemas

**Problema:** `Type instantiation is excessively deep and possibly infinite.`
**Solução:** Isso ocorre com recursão extrema de schema (ex: schemas auto-referenciados profundamente aninhados). Use `z.lazy(() => NodeSchema)` para estruturas recursivas e defina o tipo TypeScript base explicitamente em vez de apenas inferir.

**Problema:** Strings vazias passam na validação ao usar `.optional()`.
**Solução:** `.optional()` permite `undefined`, não strings vazias. Se uma string vazia significa "sem valor", use `.or(z.literal(""))` ou pré-processe: `z.string().transform(v => v === "" ? undefined : v).optional()`.