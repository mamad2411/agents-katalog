---
name: windows-dev-environment
description: Entorno de desarrollo en Windows 11 (el de la casa) — PowerShell vs Git Bash, `python` en vez de `python3`, rutas y encoding UTF-8, CRLF/LF con `.gitattributes`, Corepack y yarn 4, puertos ocupados, y trampas de portabilidad frente a Linux (`/proc`, `os.getloadavg`, shebangs, permisos). Usar al escribir un script o comando que otro correrá en Windows, al configurar la máquina de un dev nuevo, cuando algo "anda en Linux y falla en Windows", o al escribir un hook que debe correr en Windows.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Entorno de desarrollo en Windows 11

La casa desarrolla en Windows 11. Los ejemplos y scripts de las skills deben correr acá, no solo
en Linux. Verificado: Corepack contra el repo oficial de Node; el resto son comportamientos
estables de Windows/Git.

## 1. PowerShell vs Git Bash — cuándo cada uno

| Usá | Para |
|---|---|
| PowerShell | Herramientas nativas de Windows, `git`, `npm`/`yarn`, `docker`, cmdlets, la mayoría del día a día |
| Git Bash | Scripts POSIX (`.sh`), pipelines con utilidades unix (`grep`, `sed`), un `Makefile` |

- No asumas que un one-liner de bash corre en PowerShell y viceversa: distinta sintaxis de
  variables (`$env:VAR` vs `$VAR`), redirección (`2>$null` vs `2>/dev/null`), y operadores.
- Al documentar un comando en una skill o README, decí en qué shell corre, o dá las dos
  variantes si es un paso obligatorio para todos.
- Evitá comandos que abren editores interactivos (`git rebase -i`) en scripts.

## 2. Python: `python`, no `python3`

En esta máquina el intérprete es **`python`**; `python3` no existe (es la convención de
Linux/macOS). Todo script, hook, comando de README y ejemplo de skill que invoque Python usa
`python`. Un `python3 script.py` falla con "command not found". Ver `python-tooling-standards`
para el estándar de los propios scripts.

## 3. Encoding y rutas

- **UTF-8 explícito** al leer/escribir archivos desde Python: `open(path, encoding="utf-8")`.
  El default de Windows puede ser una codepage ANSI y romper acentos y caracteres del dominio.
- En PowerShell, `Set-Content`/`Add-Content` default a ANSI: pasá `-Encoding utf8` cuando otro
  lea el archivo.
- Rutas: usá `pathlib.Path` en Python (nada de concatenar con `/` ni `\` a mano); en scripts
  portables no hardcodees separadores. Cuidado con el límite de longitud de ruta de Windows en
  árboles profundos de `node_modules`.

## 4. Saltos de línea: CRLF vs LF

Windows usa CRLF; los scripts y las herramientas unix esperan LF. Un `.sh` con CRLF falla con un
error críptico (el shebang queda `#!/bin/sh\r`). Controlalo con **`.gitattributes`** en la raíz,
para que no dependa de la config de cada máquina:

```gitattributes
* text=auto eol=lf
*.sh   text eol=lf
*.ps1  text eol=crlf
*.cmd  text eol=crlf
*.png binary
```

Así el repo guarda LF y cada quien lo ve como corresponde. Un archivo montado en un contenedor
desde Windows conserva sus saltos: si un script de arranque tiene CRLF, el contenedor lo rechaza
(ver `docker-local-stack`).

## 5. Corepack y yarn 4

La casa usa **yarn 4**, activado con Corepack y fijado por el campo `packageManager` de
`package.json`:

```json
{ "packageManager": "yarn@4.x.x" }
```

- `corepack enable` crea los shims; la versión la manda `packageManager`, no la global instalada.
- **Corepack viene con Node hasta la 24.x y se quita en Node 25.0.0**. Si el dev usa Node ≥ 25,
  hay que instalarlo aparte (`npm install -g corepack`) antes de `corepack enable`. Documentá la
  versión de Node soportada en el `.nvmrc`/`engines` del proyecto.
- No mezcles `npm install` en un proyecto yarn: rompe el lockfile.

## 6. Puertos ocupados

Un `EADDRINUSE` al levantar la API o el front suele ser un proceso anterior colgado. Para ver y
matar quién ocupa un puerto:

```powershell
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess
Stop-Process -Id <pid>            # confirmá antes de matar
```
```bash
netstat -ano | grep :3000         # Git Bash; la última columna es el PID
```
Antes de matar, confirmá que es tuyo (ver `agent-resource-control` para no dejar procesos
huérfanos al cerrar).

## 7. Hooks y portabilidad — lo que NO existe en Windows

Al escribir un hook o script que debe correr acá (ver `hooks-and-guardrails`), no asumas Linux:

- **`/proc` no existe**: nada de leer `/proc/meminfo`. **`os.getloadavg()` lanza** en Windows.
  Un guard de recursos basado en eso queda inerte y no protege — usá APIs multiplataforma
  (`psutil`) o marcá el chequeo como no soportado explícitamente, no silenciosamente.
- **Permisos POSIX (`chmod`, bit de ejecución)** no aplican; no dependas de ellos.
- **Shebangs** no se respetan al invocar directo: llamá `python script.py`, no `./script.py`.
- Rutas absolutas de Linux (`/tmp`, `/usr/...`) no existen: usá el temp del sistema vía la API
  del lenguaje, no rutas hardcodeadas.
- Probá el hook **en Windows** antes de confiar en él; un hook que "anda en el CI Linux" puede no
  hacer nada en la máquina del dev.

## Checklist

- [ ] Comandos de scripts/README dicen su shell (PowerShell o Git Bash) o dan ambas variantes.
- [ ] `python`, nunca `python3`; archivos leídos/escritos con UTF-8 explícito; rutas con `pathlib`.
- [ ] `.gitattributes` fija LF para `.sh` y binarios marcados; nada de CRLF en scripts unix.
- [ ] yarn 4 vía `packageManager` + Corepack; versión de Node soportada documentada (Corepack ≤ 24.x).
- [ ] Los hooks no dependen de `/proc`, `getloadavg`, permisos POSIX ni shebangs; probados en Windows.
