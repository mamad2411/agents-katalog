# AGENTS.md — Punto de entrada para agentes de IA

## Lectura de arranque (obligatoria, ~35 KB)

1. `ESTADO-ACTUAL.md` — qué es verdad hoy
2. `docs/normativo/REGLAS_NO_HACER.md` — R1–R8, las prohibiciones permanentes
3. `docs/normativo/GLOSARIO.md` — los términos donde el sistema ya se rompió
4. `docs/00-INDICE.md` — qué leer después, según la tarea

**No leas más que eso al arrancar.** `docs/00-INDICE.md` tiene un presupuesto de
lectura por tipo de tarea; síguelo. Cargar documentación «por si acaso» consume la
mitad de la ventana antes de escribir una línea, y en este repo hay ~500 KB de docs.

Antes de **crear** un archivo, funcion, script o SQL: leer `docs/normativo/ORDEN.md`.
Dice donde va cada cosa y que puede importar que.

Antes de ejecutar cualquier cosa de `scripts/`: leer `scripts/README.md`.
Hay scripts que borran tablas en producción y no lo dice su nombre.

## Orden de autoridad

1. código y estado real del repositorio
2. reglas arquitectónicas permanentes (`filosofia.estructural`)
3. reglas de no hacer (`docs/normativo/REGLAS_NO_HACER.md`)
4. contexto funcional (`ESTADO-ACTUAL.md`)
5. historial y documentación técnica (`docs/historial/` — **nunca como estado actual**)
6. prompt actual

## Reglas de trabajo

- **Medir antes de modificar.** Consultas de solo lectura (`scripts/`, columna LEE) antes
  de cualquier cambio importante, y otra vez al terminar para comparar.
- **No asumir que la documentación histórica describe el presente.** `contexto.feliz`
  (ahora `docs/historial/contexto.feliz.md`) y
  todo `docs/historial/` fueron ciertos el día que se escribieron.
- **No crear sistemas paralelos** cuando ya existe una fuente de verdad
  (`periodos` para ciclo; `inscripciones_alumno` para alumno→grupo).
- **No ejecutar migraciones destructivas sin autorización explícita.** Los cambios de
  datos deben ser mínimos, reversibles, explicados y verificables.
- **La lógica va en `lib/`.** `app/actions/` valida sesión y delega. La decisión que se
  pueda probar sin base de datos va en un módulo puro.
- Al terminar: `npx tsc --noEmit`, la suite pura del módulo, `next build`, y documentar
  cualquier cambio arquitectónico relevante en `ESTADO-ACTUAL.md`.

## Antes de dar un cambio por bueno

`docs/normativo/CONTRATO-DE-CAMBIO.md` — checklist de aceptación, y en su §1 el bloque
de 12 líneas que se pega al final de cada prompt para Cline.

## Reparto

Claude diagnostica, mide, redacta el prompt **y revisa lo entregado**.
Cline (DeepSeek) implementa. Cómo se redacta un prompt: `criterios.prompts`.

```
Claude    diagnostica → decide arquitectura → redacta el prompt
              ↓
Cline     implementa → corre suites → corrige lo suyo
              ↓
CI        tsc · suites · test-orden · permisos · build      ← árbitro objetivo
              ↓
Claude    revisa: ¿funciona Y respeta la arquitectura?
              ↓                         ↓
            acepta                   nuevo prompt → Cline
```

**La revisión no es opcional, y no pregunta solo «¿funciona?».** Un
implementador puede entregar algo que compila, pasa las suites y aun así
duplicó lógica, creó una segunda fuente de verdad, subió I/O a la action o se
saltó una capa. Eso el CI no lo ve entero y `tsc` no lo ve en absoluto — por
eso existe `scripts/test-orden.mjs`, que convierte la mitad comprobable de
`ORDEN.md` en una suite. Lo que el script no alcanza, lo revisa Claude contra
el checklist de `CONTRATO-DE-CAMBIO.md` §2.

### Presupuesto de contexto por agente

No es el mismo, y confundirlos es lo que hace caro el reparto:

| Agente | Recibe | Por qué |
|---|---|---|
| Claude | el repo: puede investigar a fondo | diagnosticar exige ver relaciones que no están en ningún archivo |
| Cline | **solo el paquete del prompt** | con 500 KB de docs gasta la ventana antes de escribir una línea, y no necesita decidir nada: la decisión ya está tomada |

El paquete de Cline se genera, no se escribe a mano:

```bash
node scripts/gen-contexto-cline.mjs --tarea=crear <archivos que se van a tocar>
```

Devuelve el presupuesto de lectura que corresponde (de `docs/00-INDICE.md`), la
capa de cada archivo y qué exige, las suites que lo cubren, los términos del
glosario que de verdad aparecen, y el bloque del CONTRATO. A mano se olvida
alguno y el prompt acaba diciendo «lee el repo», que es lo contrario del
presupuesto.

### Qué nunca se delega sin revisión

Decidir el esquema · elegir la fuente de verdad de un dominio · tocar
`lib/auth/` · retirar legacy o un fallback · bajar un umbral de
`test-orden.mjs`. Un umbral que baja para que el CI pase apaga el guardián, y
apagarlo es una decisión de arquitectura disfrazada de arreglo.
