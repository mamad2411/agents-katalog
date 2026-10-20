---
name: resilient-build
version: 1.0.0
description: >
  Pipeline de geração de artefatos com resiliência em cada etapa.
  Checkpoint por etapa, validação multicamada, e relatório obrigatório.
triggers:
  - "build pipeline"
  - "gerar artefato"
  - "resilient build"
  - "/resilient-build"
---

# RESILIENT BUILD — Pipeline de build que não falha silenciosamente

> **Propósito**: Executar builds como transações — ou entrega completa e validada, ou relatório claro de onde e por que parou.

## 7 Etapas do Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1.PARSE  │──▶│ 2.VALID  │──▶│ 3.ENV    │──▶│ 4.DEPEND │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │
  CKPT 1         CKPT 2        CKPT 3         CKPT 4
     │              │              │              │
┌──────────┐   ┌──────────┐   ┌──────────┐
│ 7.DELIV  │◀──│ 6.VALOUT │◀──│ 5.BUILD  │◀────┘
└──────────┘   └──────────┘   └──────────┘
     │              │              │
  CKPT 7         CKPT 6        CKPT 5
```

## Uso Básico

```typescript
import { runBuildPipeline, BuildEventFactory } from './infrastructure/build/index.js';

const report = await runBuildPipeline(
  { input: 'data.json' },
  {
    PARSE: async (ctx) => ({ success: true, data: parse(ctx.intent) }),
    VALIDATE: async (ctx) => validateInput(ctx.data.get('parsed')),
    BUILD: async (ctx) => generateArtifact(ctx.data.get('validated')),
    OUTPUT_VALIDATION: async (ctx) => validateArtifact(ctx.data.get('tempPath')),
    DELIVER: async (ctx) => deliverToDestination(ctx.data.get('validatedPath')),
  },
  { timeoutPerStepMs: 30000 }
);

console.log(report.status); // 'SUCCESS' | 'PARTIAL' | 'FAILED'
console.log(report.steps);  // Checkpoints de cada etapa
```

## Validação de Input

```typescript
import { validate, assertValid } from './infrastructure/validation/index.js';

const schema = {
  name: { type: 'string', required: true },
  age: { type: 'number', coerce: true, min: 0, max: 150 },
  email: { type: 'string', pattern: /^[^@]+@[^@]+$/ },
} as const;

const result = validate(input, schema);

if (!result.valid) {
  console.log(result.errors[0].code); // 'required.missing' | 'type.invalid' | 'domain.outOfRange'
}

// Ou fail-fast
const validData = assertValid(result);
```

## Escrita Atômica

```typescript
import { generateInTemp, validateOutput, atomicMove } from './infrastructure/atomic-io/index.js';

const tempPath = await generateInTemp(data, async (data, path) => {
  await writeFile(path, JSON.stringify(data));
});

const validation = await validateOutput(tempPath, {
  minSize: 100,
  magicBytes: Buffer.from([0x89, 0x50, 0x4E, 0x47]), // PNG
  validator: (path) => validateJson(path),
});

if (validation.valid) {
  const result = await atomicMove(tempPath, '/output/file.png', 'version');
  console.log(result.finalPath); // /output/file_v2.png se já existia
}
```

## Resiliência

### Retry com backoff

```typescript
import { withRetry, isRetryableError } from './infrastructure/resilience/index.js';

const result = await withRetry(
  () => fetchDataFromAPI(),
  { maxAttempts: 3, baseDelayMs: 1000, maxDelayMs: 30000 }
);
```

### Chunk Isolation

```typescript
import { processChunks } from './infrastructure/resilience/index.js';

const { results, failed, events } = await processChunks(
  items,
  async (item) => processItem(item),
  { maxConcurrency: 4, timeoutPerChunkMs: 30000 }
);

// Se 1 chunk falha, outros 19 continuam
console.log(`${results.length} succeeded, ${failed.length} failed`);
```

### Fallback por Criticidade

```typescript
import { withFallback } from './infrastructure/resilience/index.js';

// P0: Não tem fallback, falha crítica
// P1: Usa fallback com warning
// P2: Fallback silencioso

const data = await withFallback(
  () => fetchCriticalData(),
  { criticality: 'P1', fallback: cachedData }
);
```

## Contratos de Erro

```typescript
interface BuildError {
  step: number;           // 1-7
  stepName: string;       // 'Parse' | 'Validate' | ...
  errorType: 'PARSE' | 'VALIDATION' | 'ENV' | 'DEPENDENCY' | 'BUILD' | 'OUTPUT' | 'DELIVERY' | 'TIMEOUT' | 'IO';
  message: string;
  inputSnapshot: string;  // 200 chars do input
  attemptedFix?: string;
  nextStep: string;       // Instrução acionável
}
```

## Anti-Patterns Proibidos

| ❌ Anti-pattern | ✅ Correto |
|-----------------|----------|
| Escrever direto no destino | Temp → validação → move |
| `catch (e) { console.log(e) }` | Erros estruturados com next_step |
| Retry em ValidationError | Classificar: retryable vs não-retryable |
| Abortar tudo por falha em 1 chunk | Chunk isolation + partial delivery |
| Timeout infinito | Timeout por etapa + kill + report |

## Referências

- Pipeline: `src/infrastructure/build/pipeline.ts`
- Validação: `src/infrastructure/validation/validator.ts`
- Atomic IO: `src/infrastructure/atomic-io/atomic-writes.ts`
- Resiliência: `src/infrastructure/resilience/`