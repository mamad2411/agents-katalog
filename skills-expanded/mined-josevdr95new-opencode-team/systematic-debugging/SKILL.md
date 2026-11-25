---
name: Systematic Debugging
description: Método de depuración de causa raíz en 4 fases — reproducir, aislar, corregir al mínimo y verificar con regresión. Para cualquier bug, antes de tocar código.
---

## Fases (en orden, sin saltarte ninguna)

### 1. Reproducir
- Consigue un reproducible confiable (comando, pasos en el navegador con la skill `browser`, o test que falle) ANTES de tocar nada.
- Si no reproduces, no puedes verificar el fix: decláralo y trabaja con la mejor hipótesis evidenciada.

### 2. Aislar
- Lee el error completo y los logs antes de hipotetizar.
- Formula UNA hipótesis concreta y diseña la prueba más barata que la confirme o refute (log puntual, breakpoint, test mínimo).
- Acota por bisección: comenta/deshabilita mitades del flujo, compara con un commit que funcionaba (`git log`, `git bisect` si procede).
- Cambia UNA cosa a la vez. Si necesitas cambiar cinco cosas, no tienes hipótesis: tienes especulación.

### 3. Corregir al mínimo
- Arregla la causa raíz, no el síntoma. Si tu fix necesita reescribir mucho, vuelve a la fase 2.
- Prohibido el fix de escopeta: nada de cambios "por si acaso" ni refactors no relacionados.
- Revisa el código vecino: el mismo defecto suele estar repetido cerca.

### 4. Verificar
- Añade un test de regresión que falle sin el fix y pase con él.
- Ejecuta la suite completa: el fix no puede romper nada más.
- Reproduce de nuevo el escenario original (pasos o navegador) para confirmar.

## Reporte

- Causa raíz en una frase clara.
- Fix y archivos tocados.
- Evidencia: test de regresión + resultado de suite + repro original verificado.
- Bugs vecinos detectados y riesgo residual.
