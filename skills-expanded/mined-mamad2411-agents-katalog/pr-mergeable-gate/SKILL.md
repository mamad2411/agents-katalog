---
name: pr-mergeable-gate
description: Gate OBLIGATORIO de entrega de un pull request — ningún PR se deja sin demostrar con la salida literal de `gh` que es mergeable — sin conflictos (`mergeable = MERGEABLE`), `mergeStateStatus` limpio, fuera de draft y con los checks en verde — y cómo destrabar cada estado (`BEHIND`, `DIRTY`, `UNSTABLE`, `BLOCKED`, `UNKNOWN`) sin atajos. Usar SIEMPRE al abrir un PR, después de cada push a su rama, después de que se mergee algo en la base, y antes de cerrar el turno con un PR abierto.
effort: high
---

# PR siempre mergeable

Un PR abierto no es una entrega. Un PR que **se puede mergear ahora mismo** sí. La diferencia la
decide GitHub, no la sensación de quien lo abrió: por eso se consulta y se pega la salida.

> ## ⛔ No negociable (regla 35)
> Ningún turno se cierra con un PR propio sin su estado mergeable demostrado. Si no se logra, la
> microtarea que lo entrega queda `A MEDIAS` con la causa exacta. Nunca `HECHO`.

Comandos verificados contra `gh` 2.97.0 (`gh pr view --help`, `gh pr checks --help`).

## 1. Cuándo se consulta

1. Inmediatamente después de abrir el PR.
2. Después de **cada** push a la rama del PR.
3. Después de que se mergee algo en la rama base (otro PR, un hotfix): el estado de ayer venció.
4. Antes de cerrar el turno, siempre, aunque nada haya cambiado.

## 2. La consulta

```bash
gh pr view <n> --json number,url,isDraft,mergeable,mergeStateStatus,reviewDecision,baseRefName,headRefName
gh pr checks <n> --watch --fail-fast
```

- `gh pr checks --watch` espera a que terminen los checks; `--fail-fast` corta al primer fallo.
  Correlo en primer plano: su resultado decide el siguiente paso (regla 70.2.2).
- Si el repo no tiene checks configurados, `gh pr checks` lo informa; se pega esa salida igual.
- Tras un push, GitHub puede tardar en recalcular: si `mergeable` sale `UNKNOWN`, se vuelve a
  consultar. **Nunca se asume** el valor.

## 3. Condición de entrega

Todas a la vez:

| Campo | Valor exigido |
|---|---|
| `isDraft` | `false` |
| `mergeable` | `MERGEABLE` |
| `mergeStateStatus` | `CLEAN` o `HAS_HOOKS` (o `BLOCKED` solo por review humana pendiente, ver §4) |
| `gh pr checks` | Ningún check en `fail`; ninguno pendiente al momento de entregar |

## 4. Cómo destrabar cada estado

| Estado | Significa | Qué se hace |
|---|---|---|
| `mergeable: CONFLICTING` / `DIRTY` | Conflicto con la base | Traer la base (`git fetch origin` + merge o rebase según el método del repo, ver `github-pull-requests` §8), resolver **entendiendo ambos lados**, correr la verificación de la microtarea otra vez, pushear y re-consultar |
| `BEHIND` | La rama quedó atrás y la protección exige estar al día | Actualizar la rama (`gh pr update-branch <n>`, o merge/rebase local), re-verificar y re-consultar |
| `UNSTABLE` | Un check falla | Abrir el log del check, clasificar (regla 80.4), corregir la causa. `PRODUCT_BUG`/`TEST_BUG` se corrigen en el PR |
| `BLOCKED` | Falta un requisito de protección | Identificar cuál. Si **lo único** que falta es la aprobación humana, se declara en el reporte con a quién se pidió. Cualquier otro motivo se destraba |
| `DRAFT` | Está en borrador | `gh pr ready <n>` cuando el trabajo esté en condición de review; si no lo está, no es entrega |
| `UNKNOWN` | GitHub no terminó de calcular | Re-consultar. No se entrega con `UNKNOWN` |


## 5. Prohibiciones

1. Mergear o destrabar con privilegios de administrador salteando la protección.
2. Deshabilitar, saltear o marcar como no requerido un check para que el PR quede verde.
3. `skip`, `only`, borrar o debilitar tests para que el check pase (regla 80.5).
4. `git push --force` sobre una rama con commits de otra persona. Sobre la propia, solo
   `--force-with-lease` y declarado.
5. Resolver un conflicto quedándose "con lo mío" sin leer el cambio de la base.
6. Entregar con `UNKNOWN`, con checks pendientes o con un "seguro pasa".
7. Declarar mergeable sin la salida pegada.

## 6. Qué va al reporte

En `evidencia/pr-<n>-mergeable.txt`, la salida literal de ambos comandos (sin tokens ni datos de
personas). En el `REPORTE.md`, una línea:

> `PR #<n>` — `MERGEABLE` · `CLEAN` · checks N/N verdes · consultado <fecha y hora> tras el
> último push `<sha corto>`.

Si no quedó mergeable: `A MEDIAS` con el estado exacto, qué se intentó y qué falta.

## Checklist

- [ ] Consulta hecha después del último push y antes de cerrar el turno.
- [ ] `isDraft=false`, `mergeable=MERGEABLE`, `mergeStateStatus` aceptado.
- [ ] `gh pr checks` sin fallos ni pendientes.
- [ ] Conflictos resueltos entendiendo ambos lados y re-verificados.
- [ ] Ningún atajo de §5.
- [ ] Salida literal en `evidencia/` y línea de estado en el `REPORTE.md`.
- [ ] Si hay UI: `critical-double-review` hecha antes de entregar el PR.

Relacionadas: `github-pull-requests` (forma del PR) · `github-branch-protection-rulesets` ·
`github-cli-automation` · `e2e-failure-triage` · `critical-double-review`.
