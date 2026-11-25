---
name: cerrar
description: Cierra la sesión dejando todo guardado — commitea lo que vale, escribe la nota de traspaso en SESIONES/ y actualiza el índice, para retomar mañana sin reexplicar nada. Usar con /cerrar, "cerremos", "me voy", "dejá todo guardado".
disable-model-invocation: true
---

# /cerrar — que mañana arranques en 15 segundos

En orden, sin pedir permiso para cada paso:

1. **Lo aprendido, a su lugar.** Si en la sesión hubo una decisión, va al tema de `WIKI/` que corresponde. Si hubo una corrección que vale para siempre, `/recordar`. Si hubo un entregable, a `OUTPUTS/`. Entrada arriba en `changelog/AAAA-MM.md`.
2. **Git.** `git status --short`. Lo que vale se commitea con un mensaje en una línea. La basura (temporales, logs sueltos) no: avisá qué es. Si hay remoto, push.
3. **Nota de traspaso** en `SESIONES/AAAA-MM-DD-<tema-corto>.md`, con exactamente esto:

```markdown
# <tema>
<fecha y hora>

## Qué quedó hecho
- (concreto, con archivos)

## Qué quedó a medias
- (o "nada")

## El próximo paso exacto
- (una sola acción, escrita para pegarla como prompt)

## Contexto que no está escrito en otro lado
- (qué se decidió y por qué, qué se probó y no funcionó)
```

4. **Índice:** línea **arriba** en `SESIONES/index.md` con el link.
5. Cerrá con una línea: *"Mañana: `/retomar <tema>`."*

La nota es para tu yo de mañana, no para lucirse. Corta.
