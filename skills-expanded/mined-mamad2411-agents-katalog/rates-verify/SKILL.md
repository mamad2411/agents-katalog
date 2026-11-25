---
name: rates-verify
description: >
  Verifica y actualiza el PRECIO DE TOKENS vigente de la API de Claude en la config compartida
  .claude/rates.json, para que las evaluaciones y planes dejen de arrastrar el "⚠️ verificar" y el
  coste de IA sea real. Consulta la documentación oficial de precios (WebFetch), extrae input/output
  del modelo asumido y escribe los valores con la fecha de verificación. Nunca inventa un precio: si
  no puede leer la doc, deja el marcador y avisa. Úsala cuando el usuario diga "verifica las tarifas",
  "actualiza el precio de tokens", "pon los precios al día", o cuando una evaluación detecte el precio
  sin verificar. También se ofrece en /setup.
---

# rates-verify — precio de tokens al día en `.claude/rates.json`

Objetivo: que `evaluator`/`planner` calculen el **coste de IA con precios reales** en vez de marcar `⚠️ verificar`. Esta skill consulta la doc oficial de precios, extrae el precio por millón de tokens (input/output) del modelo asumido y lo escribe en la config compartida con la fecha en que se verificó.

**Principio innegociable:** *nunca inventes un precio*. Si no puedes leer la doc (red caída, formato cambiado, dato ambiguo), **no escribas números**: deja `precioTokens` como está (con su marcador), informa al usuario y sugiere ponerlo a mano. Un precio inventado corrompe todas las evaluaciones que lo hereden.

## Pasos

1. **Localiza `.claude/rates.json`** (config compartida; la usan evaluator/planner/jira-sync):
   ```bash
   RATES="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*rates.json' 2>/dev/null | head -1)"
   ```
   Si no existe, cópialo de la plantilla del kit del evaluator (`agent-kits/evaluator/templates/rates.example.json`) a `.claude/rates.json` del proyecto y sigue.

2. **Lee el modelo asumido** del propio `rates.json` (`modeloIA`, p. ej. `claude-opus-4-8`) y la moneda/unidad de `precioTokens`.

3. **Consulta la doc oficial de precios** con WebFetch a la página de precios de la API de Claude (docs.claude.com / anthropic.com pricing). Pregunta concretamente por el **precio por millón de tokens de entrada y de salida del modelo asumido**. Si la doc lista varios tiers (batch, caché), toma el **precio estándar** salvo que el usuario indique otro.

4. **Valida lo obtenido (presencia + unidad + RANGO):** ambos números presentes, positivos y en la unidad esperada (por millón). Además, **valida el rango** antes de escribir, para que un número plausible-pero-equivocado (una fila de otro modelo, un tier de caché/batch, un precio de plan mensual tipo `$X/mo`) no pase el filtro: el precio por millón de tokens de un modelo de la familia debe caer en un orden de magnitud razonable (heurística: input entre ~0,1 y ~100 USD/M, output entre ~0,5 y ~500 USD/M, y `output > input`). Si un valor cae fuera de rango, o la doc no da el modelo exacto, o hay varias cifras candidatas sin una claramente estándar → trátalo como **"no verificable"** (paso 6b): NO escribas, no aproximes. Cita al usuario los números que viste y por qué los rechazaste.

5. **Escribe `rates.json`** preservando el resto de campos: rellena `precioTokens.input` y `precioTokens.output`, fija `precioTokens.moneda`/`unidad` según la fuente, y añade `precioTokens.verificadoEl: "YYYY-MM-DD"` (fecha de hoy, obtenida con `date +%F`) y `precioTokens.fuente: "<url>"`. No toques `tarifaHora`, `ratioSupervision`, etc.

6. **Cierra:**
   - **(a) Verificado:** confirma al usuario los precios escritos, la fecha y la fuente. A partir de ahora evaluator/planner los usan sin `⚠️ verificar`.
   - **(b) No verificable:** di claramente que **no** has escrito precios (y por qué), deja el marcador intacto y ofrece que el usuario los introduzca a mano si los conoce.

## Cómo lo consumen evaluator/planner

Leen `precioTokens` de `.claude/rates.json` (fragmento `agent-kits/shared/estimation-defaults.md`). Consideran el precio **fiable** si `input`/`output` > 0 y `verificadoEl` es razonablemente reciente (p. ej. < 90 días); si falta la fecha o es antiguo, siguen mostrando `⚠️ verificar` y pueden sugerir relanzar esta skill.

## Reglas

- **No inventes precios.** Es la regla que da sentido a la skill.
- **Preserva el resto de `rates.json`.** Solo tocas `precioTokens` (+ `verificadoEl`/`fuente`).
- **Fecha real.** `verificadoEl` con la fecha de hoy (`date +%F`), nunca a ojo.
- **Fuente citada.** Guarda la URL de donde salió el precio para que sea auditable.
- **Web restringida.** Si WebFetch no puede acceder a la doc, no intentes rodearlo con otras herramientas: es el caso "no verificable".
