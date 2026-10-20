---
name: python-tooling-standards
description: Estándar de la casa para scripts y generadores Python de tooling (generación de DDL y entidades desde el modelo, seeds, validaciones, hooks) — salida determinista byte a byte, idempotencia, CLI con argparse y códigos de salida, abortar ante entrada inválida en vez de adivinar, flags explícitos para acciones destructivas, type hints, entorno virtual con dependencias fijadas, portabilidad Windows (python, pathlib, UTF-8 explícito) y tests con pytest. Usar al crear o modificar cualquier script Python del repo, un generador, un cargador de datos o un hook, y al revisar por qué dos corridas dan salidas distintas.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Scripts y generadores Python

Los scripts de tooling son infraestructura: un generador que emite DDL distinto en cada
corrida hace imposible detectar deriva (`model-driven-schema`); un cargador que "arregla" lo
que no entiende siembra datos inventados (`seed-data-catalogs`). Estas reglas hacen que un
script sea confiable como un test.

## 1. Determinismo: misma entrada → mismos bytes

- **Ordená todo lo que iterás**: `sorted(path.glob(...))`, `sorted(d.items())`,
  `json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2)`. `glob` y los `set` no tienen
  orden garantizado; los `dict` conservan inserción, que depende del orden de lectura.
- Nada de timestamps, rutas absolutas, nombres de máquina o usuario dentro de la salida
  generada. Si necesitás marcar procedencia, usá el hash del insumo o la versión del modelo.
- Aleatoriedad solo con semilla explícita y declarada; IDs derivados de la clave natural
  (`uuid.uuid5`), no `uuid4()` (`seed-data-catalogs` §3).
- Saltos de línea fijos: `open(..., "w", encoding="utf-8", newline="\n")`. Con `newline=None`,
  Python traduce `\n` a `os.linesep` y en Windows genera `\r\n`: el mismo generador produce
  diffs distintos según la máquina.
- **Prueba de determinismo en CI**: correr el generador dos veces sobre el mismo insumo y
  comparar directorios; o una vez sobre el árbol limpio y `git diff --exit-code`.

## 2. Idempotencia y seguridad de ejecución

- Correr N veces deja el mismo estado que correr una. El script reporta qué hizo
  (`creados: 3, actualizados: 0, sin cambios: 128`); una corrida muda no se puede verificar.
- **Acciones destructivas (borrar, truncar, sobrescribir, reconstruir) exigen un flag explícito**
  (`--yes`, `--force`) y sin él corren en modo `--dry-run` o abortan. Nunca dependen de un prompt
  interactivo: en CI y en un hook no hay quién conteste.
- Escritura atómica: generar a un archivo temporal en el mismo directorio y renombrar; un
  corte a mitad no deja salida a medias.
- Antes de un cambio grande: un modo `--dry` que muestre el diff o el plan sin tocar nada.

## 3. Abortar en vez de adivinar

- Entrada inválida, ambigua o fuera de vocabulario ⇒ **mensaje accionable** (archivo, línea, qué
  se esperaba) y **código de salida distinto de cero**. Nunca un default silencioso ni un
  "warning" que nadie lee. Ver `data-modeling-plantuml` §9.
- Acumulá todos los errores de validación de una pasada y reportalos juntos; abortar en el
  primero obliga a diez corridas para ver diez errores.
- Guardas de entorno: un cargador de datos de demo aborta si detecta un entorno productivo
  (variable de entorno, nombre de base, host).
- Un sub-proceso (`subprocess.run(..., check=True)`) que falla propaga el fallo; no lo envuelvas
  en `try/except: pass`.

## 4. CLI

```python
import argparse, sys
from pathlib import Path

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Genera DDL desde el modelo.")
    p.add_argument("module", nargs="?", default="all", help="módulo o 'all'")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true", help="confirma acciones destructivas")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = generate(args.module, args.out, dry_run=args.dry_run)
    for e in errors:
        print(f"ERROR {e.file}:{e.line}: {e.message}", file=sys.stderr)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
```

- `main(argv)` devuelve el código de salida y recibe `argv` opcional: así se testea sin
  `subprocess`. `argparse` sale con **2** ante argumentos inválidos; reservá **1** para errores
  de validación/ejecución y **0** para éxito.
- `--help` útil, `choices=` para valores cerrados, `add_subparsers(dest=..., required=True)` si
  hay varios comandos, `add_mutually_exclusive_group` para flags incompatibles.
- Errores y diagnóstico a `stderr`; solo el resultado a `stdout` (para poder redirigirlo).
- Sin `input()`, sin `os.system`, sin `print` de depuración que quede.

## 5. Portabilidad Windows / Linux

- Invocación como `python` y `python -m modulo`; no asumas `python3` ni `#!/usr/bin/env` en
  Windows. Documentá la versión mínima soportada.
- `pathlib.Path` siempre; nunca concatenar strings con `/` o `\\`. Cuidado con
  mayúsculas/minúsculas: NTFS no distingue, Linux sí — dos archivos que difieren solo en caso
  rompen en un sistema y no en el otro.
- **Encoding explícito en cada `open()`**: sin `encoding=`, Python usa la codificación de la
  configuración regional (en Windows suele no ser UTF-8) y un acento rompe la corrida. Lo mismo
  al leer `stdout` de un subproceso (`text=True, encoding="utf-8"`).
- No dependas de herramientas externas (`sed`, `grep`, `sh`) desde Python; hacelo en Python.
- Rutas largas, permisos y `os.symlink` se comportan distinto en Windows: evitalos o probalos.
- Consola de Windows: si imprimís caracteres no ASCII y falla, reconfigurá
  `sys.stdout.reconfigure(encoding="utf-8")` al inicio, no cambies el contenido.

## 6. Calidad de código

- Type hints en toda función pública; verificación estática (`mypy` o `pyright`) en CI.
- Formato y lint automáticos (`ruff` cubre ambos); sin discusiones de estilo en review.
- Funciones puras para la lógica (parsear, transformar, validar) separadas de la E/S
  (leer, escribir, ejecutar): lo puro se testea sin disco. Aplica `clean-code`.
- `dataclasses`/`TypedDict` para las estructuras que cruzan funciones; no dicts anónimos.
- Sin estado global mutable; configuración por argumentos o variables de entorno leídas en
  un solo lugar. Secretos nunca en el código (`environment-secrets-config`).
- Logging con `logging`, no `print`, cuando el script corre como servicio o hook.

## 7. Dependencias y entorno

- Un entorno virtual por repo (`python -m venv .venv`), ignorado por git, con activación
  documentada para PowerShell, cmd y bash.
- Dependencias **fijadas** (`==`) en un archivo de lock generado por herramienta; para tooling
  crítico, hashes con `--require-hashes` (`pip-compile --generate-hashes` o equivalente).
- Preferí la biblioteca estándar: cada dependencia es superficie de ataque y de rotura
  (`dependency-management`).
- El script declara y verifica su versión mínima de Python al inicio si usa sintaxis nueva.

## 8. Tests con pytest

- La lógica pura se testea con entradas mínimas y salida esperada exacta (comparación de
  strings/bytes, no "contiene").
- E/S con `tmp_path`; salida de consola con `capsys`; entorno con `monkeypatch`.
- `main([...])` se invoca directo y se afirma el código de retorno y `stderr`.
- **Golden tests** para generadores: insumo pequeño versionado → salida esperada versionada;
  un cambio intencional actualiza el golden en el mismo PR, con revisión del diff.
- Test de determinismo (dos corridas iguales) y de idempotencia (segunda corrida: 0 cambios).
- Test de guardas: entrada inválida ⇒ código ≠ 0 y mensaje con archivo y línea; acción
  destructiva sin `--yes` ⇒ no toca nada.

## Anti-patrones

- Iterar un `glob` sin ordenar y confiar en que "siempre sale igual".
- `open(path)` sin `encoding`; `newline` por defecto en salida versionada.
- `except Exception: pass` alrededor de un subproceso o una escritura.
- Default silencioso ante un valor desconocido ("si no está en el vocabulario, uso `text`").
- Script que borra o trunca sin flag, o que pregunta por consola.
- Corregir la salida generada a mano en vez del generador.

## Checklist

- [ ] Salida determinista: iteraciones ordenadas, sin timestamps ni rutas, `newline="\n"`, UTF-8.
- [ ] Idempotente y con reporte de conteos; escritura atómica.
- [ ] Toda entrada inválida aborta con archivo/línea y código ≠ 0; errores agrupados.
- [ ] Acciones destructivas detrás de `--yes`/`--force`, con `--dry-run` disponible.
- [ ] `main(argv) -> int`, `sys.exit(main())`, diagnóstico a `stderr`.
- [ ] `pathlib`, `encoding=` explícito, sin dependencias de shell; probado en Windows y Linux.
- [ ] Type hints, lint y verificación estática en CI.
- [ ] Entorno virtual y dependencias fijadas.
- [ ] Tests: goldens, determinismo, idempotencia, guardas.
