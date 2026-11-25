---
name: spec-modulo
description: "Desarrollo guiado por especificación para módulos de PrestaShop, adaptado de GitHub Spec Kit. Seis fases: especificar, aclarar, planificar, tareas, implementar y converger. Usar SIEMPRE que se vaya a crear un módulo NUEVO o a meter un cambio GRANDE (una funcionalidad entera, un rediseño, una migración de versión). Se invoca como /spec-modulo <fase> <lo que se quiere>. NO usar para arreglos pequeños: para dos líneas, se arregla y ya."
risk: low
source: "adaptado de https://github.com/github/spec-kit"
date_added: "2026-09-02"
---

# Especificar antes de picar código

Adaptación de **GitHub Spec Kit** (desarrollo guiado por especificación) a los módulos de
PrestaShop de este usuario. La idea de fondo es la del original: **primero se escribe qué
tiene que hacer y por qué, y solo después el cómo**; la especificación deja de ser
documentación que se tira y pasa a ser lo que dirige el trabajo.

Lo que NO se ha traído del original, y por qué:

| Del original | Aquí | Por qué |
|---|---|---|
| CLI `specify` por `uv` | nada | El CLAUDE.md prohíbe dependencias. Esto son plantillas y una forma de trabajar, no un programa. |
| Carpeta `.specify/` en el proyecto | nada | Acabaría dentro del ZIP que se le manda al cliente. |
| `memory/constitution.md` | **el CLAUDE.md** | REGLA 0: nada gana al CLAUDE.md. Un segundo fichero de principios es una segunda verdad, y entonces no hay ninguna. |
| Comandos `/speckit.*` en inglés | fases en castellano | Todo el trabajo del usuario está en castellano. |

## Cuándo se usa y cuándo NO (BLOQUEANTE)

**SÍ:** módulo nuevo · una funcionalidad entera dentro de un módulo que ya existe ·
rediseñar una pantalla completa · migrar de 8.x a 9.x · algo que va a tocar más de cinco
ficheros o que hay que dejar por escrito para el cliente.

**NO:** un arreglo de dos líneas · una cadena que falta en el `.xlf` · una tilde · un
`LIMIT 1` de más · cambiar un texto. **Para eso se arregla y ya.** Escribir tres documentos
para cambiar una línea es exactamente el derroche contra el que avisa el apartado «Gasto»
del CLAUDE.md.

**Ante la duda: se pregunta al usuario si quiere spec o si va directo.**

## Dónde viven las especificaciones

```
<carpeta de trabajo>\_specs\<modulo>\NNN-<nombre-corto>\
    spec.md      qué y por qué        (fase 1)
    plan.md      cómo                 (fase 3)
    tareas.md    en qué orden         (fase 4)
    notas.md     lo que se aprendió   (al converger)
```

**FUERA de la carpeta del módulo, a propósito**: lo que va dentro del módulo acaba en el
ZIP del cliente, y las notas internas no son suyas. `NNN` es un número de tres cifras
correlativo dentro de ese módulo (`001`, `002`…).

---

## Fase 1 — ESPECIFICAR  (`/spec-modulo especificar <lo que se quiere>`)

Se escribe `spec.md` a partir de `plantillas/spec.md`.

**Solo el QUÉ y el PARA QUIÉN. Ni una decisión técnica.** Nada de nombres de hook, de
tablas ni de ficheros: eso es la fase 3.

Cinco cosas que en un módulo de PrestaShop hay que dejar cerradas aquí y que casi nunca
vienen en el encargo:

1. **Versiones objetivo.** ¿8.x, 9.x, o las dos? Decide toda la arquitectura: sin un «solo
   PrestaShop 9.1» explícito, el CLAUDE.md obliga a estructura legacy sin `src/`.
2. **Quién lo usa.** Comerciante en el back-office, cliente en el front, un cron, el
   webservice, o varios. Cada uno es un controlador distinto.
3. **Multitienda.** ¿La configuración es global o por tienda? Hay que decidirlo ahora y
   escribirlo, no descubrirlo al final.
4. **Idiomas.** Qué idiomas hay que entregar traducidos.
5. **Datos que ya existen.** Si toca `orders`, `customers` o cualquier tabla con
   histórico: decirlo aquí, porque activa la REGLA 0 de scans masivos.

Todo lo que no esté claro se marca **`[FALTA ACLARAR: la pregunta]`**. No se inventa.

## Fase 2 — ACLARAR  (`/spec-modulo aclarar`)

Se leen los `[FALTA ACLARAR:]` y se le hacen al usuario **como mucho cinco preguntas**, las
que de verdad cambian el diseño. Las demás se resuelven con un valor por defecto razonable
y se anotan en «Suposiciones».

Las respuestas se meten en `spec.md` y desaparece el marcador. Sin marcadores no se pasa a
la fase 3.

## Fase 3 — PLANIFICAR  (`/spec-modulo plan`)

Se escribe `plan.md` a partir de `plantillas/plan.md`. Aquí sí va el cómo.

**La comprobación contra el CLAUDE.md es una puerta, no una formalidad.** Antes de escribir
una sola tarea hay que responder a esto por escrito, con SÍ o con el motivo:

- ¿Estructura legacy, sin `src/`, sin `config/`, sin `composer.json`, sin `vendor/`, sin
  `upgrade/`? (Única excepción: destino EXCLUSIVO PrestaShop 9.1, confirmado por el usuario.)
- ¿La clase principal coincide con la carpeta y va sin `namespace`?
- ¿`index.php` en TODAS las carpetas, recursivo? ¿Cabeceras en todos los ficheros?
- ¿Las migraciones van en `addnewfeatures()` con `try{}`, y no en ficheros `upgrade/`?
- ¿La configuración es UN solo `HelperForm` con **pestañas** y un único botón de guardar?
- ¿`isUsingNewTranslationSystem()` a true y TODAS las cadenas con
  `d='Modules.<Studly>.<Admin|Shop>'`? (Nunca `mod=`: no lee los `.xlf`.)
- ¿Los `.xlf` van en `translations/<locale>/Modules<Nombre><Dominio>.<locale>.xlf`?
- ¿Multitienda decidido y escrito: global o por tienda?
- ¿Algún endpoint AJAX? Entonces las TRES cabeceras anti-caché, y **sin** `Content-Type`.
- ¿Se recorre alguna tabla con histórico? Entonces ventana de 24 h como mucho, seed previo
  y kill switch.
- ¿Se toca la ficha de producto del back-office? Entonces **invocar antes el skill
  `prestashop-admin-product`**, que no es opcional.

Si algo se salta una de estas reglas, va a la tabla «Lo que nos saltamos y por qué», con el
motivo escrito. Si no hay motivo que se pueda escribir en una frase, no se salta.

## Fase 4 — TAREAS  (`/spec-modulo tareas`)

Se escribe `tareas.md` a partir de `plantillas/tareas.md`: tareas numeradas `T001…`,
**agrupadas por historia de usuario**, cada grupo entregable y probable por su cuenta.

Las que tocan ficheros distintos se marcan `[P]` (se pueden hacer a la vez). Las que tocan
el mismo fichero, en fila.

Y al final de todo, las tareas que el CLAUDE.md exige siempre y que siempre se olvidan:
`index.php` en cada carpeta nueva · cabeceras · `php -l` en todos los `.php` ·
`addnewfeatures()` al día · los `.xlf` de cada idioma · los tres documentos `.md` ·
la pasada de ortografía · registrar el módulo con `prestashop_connect_gmartos`.

## Fase 5 — IMPLEMENTAR  (`/spec-modulo implementar`)

Se ejecutan las tareas **por orden y por historia**, no todas a la vez. Al terminar cada
historia se para y se dice al usuario qué se puede probar ya.

Se marca cada tarea `[x]` en `tareas.md` según se hace. Si aparece algo que no estaba
previsto, se añade como tarea nueva en vez de hacerlo por lo bajo.

## Fase 6 — CONVERGER  (`/spec-modulo converger`)

Comparar lo que hay con `spec.md` y `tareas.md`, y **apuntar lo que falte como tareas
nuevas** en vez de dar por bueno lo que hay.

Comprobaciones que se pasan aquí, en este orden:

1. `php -l` en todos los `.php`.
2. `index.php` en todas las carpetas, recursivo.
3. Cadenas: que no quede ningún `{l s='...' mod='...'}`, y que cada cadena esté en el `.xlf`.
4. Ortografía: `python <herramientas>/ortografia/revisar_ortografia.py <carpeta>` — es la
   tercera y última pasada de las tres del CLAUDE.md, y **hay que preguntar al usuario**
   si está todo correcto y si quiere que se revise.
5. **Preguntar al usuario si instala en las tiendas locales** (máximo dos preguntas por
   tarea; dicho que sí, ya no se vuelve a preguntar). Autorizado: `8.2b` por defecto.
6. Los tres documentos `.md` al día, en `manuales/<modulo>/`.
7. Las capturas, en `capturas/<modulo>/`. Nada de esto va dentro del módulo.

Lo aprendido por el camino se escribe en `notas.md`, y si vale para cualquier proyecto,
también en la memoria y en el CLAUDE.md.

---

## Manual por tipo de proyecto

`MANUAL.md` (copia en `modulos IA/_specs/MANUAL.md`) explica cómo se aplica esto a
cada tipo de trabajo, con la **puerta propia** de cada uno: módulo de PrestaShop,
importación de datos, migración de tiendas, herramienta de escritorio, WooCommerce,
integración con IA y Odoo. Leerlo antes de empezar uno de esos.

## Plantillas

`plantillas/spec.md` · `plantillas/plan.md` · `plantillas/tareas.md`

Se copian a la carpeta de la especificación y se rellenan. Los comentarios `<!-- -->`
explican qué va en cada hueco y se borran al rellenar.

**Why:** 2026-09-02. El método viene de github/spec-kit; la adaptación es para que no choque
con el CLAUDE.md. Lo importante que trae el original y aquí se conserva: escribir el qué
antes que el cómo, marcar lo que no está claro en vez de inventarlo, y trocear en historias
que se puedan entregar y probar de una en una.
