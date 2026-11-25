---
name: dead-code-duplication
description: Detección y eliminación de código muerto y duplicación — archivos, exports, imports y dependencias sin uso con knip, duplicación con jscpd, dependencias circulares con madge, feature flags viejos y ramas muertas, con la regla de buscar usos dinámicos antes de borrar. Usar al limpiar un módulo, al bajar el tamaño del bundle o del árbol de dependencias, después de quitar una feature, al configurar la etapa de duplicación del gate, o cuando "no sé si esto se usa todavía".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Código muerto y duplicación — borrar es una feature

El código que nadie ejecuta no es neutro: se compila, se testea, confunde al que lee,
esconde bugs y agranda el bundle. La duplicación multiplica el costo de cada cambio.
Ambos se miden con herramientas y se eliminan con cuidado — el control de versiones
recuerda lo borrado (`clean-code`: nada de código comentado "por las dudas").

## 1. Código muerto: knip

knip detecta **archivos, exports y dependencias sin uso** (verificado en knip.dev).
Es el sucesor práctico de ts-prune (solo exports) y depcheck (solo deps):

```bash
yarn knip                 # reporte de lo no usado
yarn knip --production     # solo el grafo de producción (ignora tests/tooling)
yarn knip --fix            # aplica remociones seguras (revisá el diff)
```

Config en `knip.json` / `knip.ts` declarando entry points reales (mains, `main.ts`,
rutas, workers, hooks) para que no marque como muerto lo que entra por un camino que no
ve. `--fix` no es magia: revisá cada borrado como cualquier cambio.

## 2. Dependencias circulares: madge

```bash
npx madge --circular --extensions ts src/    # ✅ lista los ciclos; idealmente vacío
```

Un ciclo de imports es acoplamiento que rompe orden de carga, tree-shaking y tests.
En CI, `--circular` puede fallar el build si aparece uno nuevo.

## 3. Duplicación: jscpd

```bash
npx jscpd src/ --min-tokens 50 --threshold 5   # falla si el % duplicado supera el umbral
```

`--min-tokens` fija el tamaño mínimo del bloque para contar como clon; `--threshold` es
el % que bloquea (ver `code-quality-gates`). Ajustá ambos en el CLAUDE.md del proyecto.

## 4. Duplicación: ¿siempre abstraer? No

Duplicación no es lo mismo que repetición incidental. Antes de crear una abstracción
compartida, preguntá si los dos usos **cambian por la misma razón**:

- ✅ Abstraé: la misma regla de negocio copiada en tres servicios; si cambia, cambia en los tres.
- ❌ No abstraigás (todavía): dos bloques que hoy se parecen pero pertenecen a dominios
  distintos que evolucionan aparte. Una abstracción prematura acopla lo que debía estar
  separado y es más cara de deshacer que la duplicación (regla del "duplicá antes de
  abstraer" / WET vs DRY). Ver `solid-principles`.

## 5. Antes de borrar: buscá el uso que la herramienta no ve

El riesgo real de eliminar es el **uso dinámico** que el análisis estático no rastrea:

```bash
# ✅ antes de borrar `computeRiskScore`, buscá referencias por string y reflexión
grep -rn "computeRiskScore" src/            # llamadas normales + strings
grep -rn "\['computeRiskScore'\]\|\[\`" src/  # acceso dinámico por índice
```

Sospechá de: acceso por string (`obj[name]`), inyección de dependencias por token,
plantillas HTML de Angular (knip cubre TS, no siempre el binding del template), reflexión,
endpoints llamados solo por el front o por un cron externo, migraciones/seeds referenciados
por nombre. Si hay duda, deprecá primero (log de "esto todavía se usa") y borrá después.

## 6. Feature flags y ramas muertas

- Un flag que ya está 100% activado (o 100% apagado hace meses) es código muerto en las
  dos ramas del `if`: quitá el flag y la rama perdedora. Los flags viejos son deuda
  (`technical-debt-management`).
- Ramas de git abandonadas: se borran tras mergear (auto-delete, ver `github-repo-standards`).

## Anti-patrones
- Borrar lo que knip marca sin buscar usos dinámicos → rompés algo en runtime.
- Dejar `--fix` a ciegas sin revisar el diff.
- Abstraer al segundo uso por reflejo y acoplar dominios distintos.
- Comentar el código en vez de borrarlo.
- Flags "temporales" que llevan un año prendidos.

## Checklist
- [ ] knip corre con entry points bien declarados; el reporte está limpio o justificado.
- [ ] `madge --circular` sin ciclos nuevos.
- [ ] jscpd por debajo del umbral acordado.
- [ ] Antes de cada borrado se buscaron usos dinámicos (grep por string, DI, templates).
- [ ] No quedaron flags ni ramas muertas de features ya decididas.
