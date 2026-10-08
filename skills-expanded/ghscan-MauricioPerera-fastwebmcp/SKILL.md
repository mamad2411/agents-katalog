---
type: 'Task Contract'
title: 'Exportar un DefinedTool como fuente de skill mcpwasm (solo schema, no runtime)'
description: 'toMcpwasmSkillSource(tool) reusa el name/description/inputSchema ya derivados por defineTool() para emitir el registerTool({...}) que mcpwasm/llms-txt-skills espera en un tool.js; el handler del sandbox no se auto-genera.'
tags: ['webmcp', 'mcpwasm', 'interop', 'core']

task: to-mcpwasm-skill
intent: "Generar el texto fuente de un tool.js de mcpwasm a partir de un DefinedTool, sin intentar portar el execute (imposible: DOM vs sandbox QuickJS sin DOM)."
target: src_ts/to-mcpwasm-skill.ts
signature: "function toMcpwasmSkillSource(tool: DefinedTool, options?: McpwasmSkillOptions): string"
test_command: "node --test tests_ts/to-mcpwasm-skill.test.ts"
budget:
  cyclomatic_max: 4
  nesting_max: 2
  lines_max: 25
  params_max: 2
tests: "tests_ts/to-mcpwasm-skill.test.ts"
tests_sha256: "b3f0f93fa16587b89e270efda6ed785c2ed6b9f4b70132321f73d1fd801db47c"
touch_only: ['src_ts/to-mcpwasm-skill.ts']
deps_allowed: []
forbids: ['network', 'subprocess', 'llm']
---

# Contract: Exportar un DefinedTool como fuente de skill mcpwasm

## Intent
El usuario pidio soporte para `mcpwasm` (github.com/MauricioPerera/mcpwasm), un
proyecto DISTINTO del mismo autor: "Static MCP" — tools publicadas como archivos
estaticos (`llms.txt` + `tool.js` por skill), ejecutadas sandboxeadas en QuickJS-wasm
(Cloudflare Workers), sin DOM ni `fetch` — solo `registerTool`, `host.fetchOrigin`
(restringido al origin), `host.memorySearch` opcional, y ECMAScript puro. Investigado
contra el codigo real de `mcpwasm` y `llms-txt-skills` (no solo el README) antes de
diseñar esto.

**Limite real, verificado, no adivinado:** el `execute` de una tool WebMCP existe para
tocar el DOM de una pagina real — no tiene sentido dentro del sandbox (no hay DOM). El
`handler` de mcpwasm corre aislado con capacidades inyectadas (`host.*`) que no tienen
equivalente en el navegador. Ningun documento de ninguno de los dos proyectos describe
un mecanismo para compartir esa logica, y este contrato NO inventa uno. Lo unico
compartible es la capa de schema: `name`/`description`/`inputSchema` (JSON Schema), que
`defineTool()` ya deriva de Zod. `toMcpwasmSkillSource()` reusa ESE schema ya calculado
para emitir el `registerTool({...})` que mcpwasm espera en su `tool.js`, con el
`handler` como placeholder — quien publique escribe la logica del sandbox aparte,
porque no hay forma honesta de generarla automaticamente.

mcpwasm ya tiene su propio CLI oficial (`@rckflr/llms-skills`, `init --tool` +
`publish`) para scaffolding completo y sellado de hash — este contrato NO lo
reimplementa; solo evita que el autor tenga que re-escribir a mano el mismo schema que
`fastwebmcp` ya calculo para el navegador.

## Interface
```
interface McpwasmSkillOptions {
  handlerBody?: string; // texto JS crudo para el cuerpo de handler(args); default: stub TODO
}

function toMcpwasmSkillSource(tool: DefinedTool, options?: McpwasmSkillOptions): string
```

## Invariants
- El output SIEMPRE es un unico `registerTool({ name, description, inputSchema, handler
  }); ` sintacticamente valido como cuerpo de funcion (verificable con
  `new Function(output)` sin lanzar).
- `name` y `description` se serializan con `JSON.stringify` (nunca interpolacion cruda)
  — a salvo de comillas, backslashes y saltos de linea en el valor original.
- `inputSchema` en el output es el `tool.inputSchema` YA derivado por `defineTool()` —
  esta funcion no vuelve a inferir ni transformar el schema.
- Si `options.handlerBody` no se provee, el `handler` generado es un stub que lanza y
  menciona "TODO" y "mcpwasm" (para que sea imposible publicarlo sin querer sin
  completarlo). Si se provee, su texto se inserta verbatim dentro de
  `handler(args) { ... }`.
- No hace red, `subprocess`/`child_process`, ni llama a un LLM — es generacion de texto
  pura, sin tocar el CLI real de mcpwasm ni publicar nada.

## Examples
- `toMcpwasmSkillSource(defineTool({ name: 'sum_numbers', ... }))` -> string que empieza
  con `registerTool({` y contiene `name: "sum_numbers"`.
- Con `{ handlerBody: 'return args.a + args.b;' }` -> ese texto aparece verbatim dentro
  de `handler(args) { ... }`, sin el stub TODO.
- `defineTool({ name: 'weird_"tool"', ... })` -> `toMcpwasmSkillSource` produce una
  fuente igual sintacticamente valida (comillas escapadas correctamente).

## Do / Don't
- DO: reusar `tool.inputSchema` tal cual — es el contrato con `defineTool()`, ya
  verificado end-to-end contra un `document.modelContext` real (CONTRACT-40).
- DO: dejar el `handler` como responsabilidad explicita del usuario — nunca intentar
  traducir automaticamente el `execute` original.
- DON'T: importar ni invocar `@rckflr/llms-skills` (el CLI real de mcpwasm) — esta
  funcion solo genera el texto del `tool.js`, no publica ni sella hashes.
- DON'T: agregar red, `subprocess`/`child_process`, ni ninguna llamada a un LLM.

## Tests
(Los tests estan en `tests_ts/to-mcpwasm-skill.test.ts` — escritos ANTES de la
implementación; oráculo congelado, sellado por `tests_sha256`.)

## Constraints
- PARAR y reportar si el `intent` resulta imposible de cumplir sin violar `touch_only` o
  `forbids`.
