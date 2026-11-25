---
name: embebidos3-nano
description: Trabaja con la Jetson Nano del proyecto embebidos-3 — verificar estado antes de cualquier cambio, exponer endpoints HTTP/WS, evitar incompatibilidades de plataforma (Python 3.6 / TRT 8.2 / sm_53 Maxwell).
---

# embebidos3-nano

Convenciones, endpoints y verificaciones para interactuar con el Jetson Nano B01 que sirve el modelo de detección de residuos (glass/paper/plastic).

**Regla fundamental: verificá el estado actual del Nano ANTES de implementar o decidir.** La plataforma es restrictiva (Python 3.6.9, TensorRT 8.2.1.8, JetPack 4.6.1, Maxwell sm_53) y cualquier suposición no verificada cuesta tiempo de iteración.

## Conexión

| Variable | Valor |
|---|---|
| SSH alias | `nano` (definido en `~/.ssh/config`) |
| IP Headscale | `100.64.0.2` |
| Usuario | `jetson` |
| Sudo password | `IAEmbebidos` |
| Server FastAPI/WS | `http://100.64.0.2:8000` |
| ROOT del proyecto | `/home/jetson/embebidos-3` |

> **Control plane propio (migración 2026-05-23):** el Nano ya NO usa Tailscale Inc. (`controlplane.tailscale.com`, bloqueado por el FortiGate de UAO). Ahora se registra contra un **Headscale self-hosted** en `https://80-241-217-130.nip.io` (VPS Contabo de Frevalle). La IP vieja `100.100.166.120` quedó obsoleta. El acceso SSH es **por llave `~/.ssh/id_ed25519`** (ya no por Tailscale SSH). Detalle del deploy: `investigaciones/2026-05-23-headscale-deploy.md`.

Para sudo en SSH, usá `ssh -tt nano "echo 'IAEmbebidos' | sudo -S -p '' COMMAND"` (TTY forzado evita "sudo: a password is required").

## Verificá ANTES de cambiar — comandos canon

```bash
# Servicios systemd
ssh nano "systemctl is-active embebidos3-server.service"
ssh nano "echo 'IAEmbebidos' | sudo -S -p '' systemctl list-units 'embebidos3-builder@*.service' --all --no-pager"

# Estado del modelo
curl -s http://100.64.0.2:8000/model/state | python -m json.tool
curl -s -X POST http://100.64.0.2:8000/model/check-updates | python -m json.tool

# Filesystem (engine y meta)
ssh nano "ls -la /home/jetson/embebidos-3/engines/ /run/embebidos3/ 2>&1"

# Logs server (último minuto)
ssh nano "echo 'IAEmbebidos' | sudo -S -p '' journalctl -u embebidos3-server.service --since '1 minute ago' --no-pager"

# Sudoers cargado (verificar paths absolutos correctos)
ssh nano "sudo -nl 2>&1 | grep -v 'Matching\|User\|may run'"

# Binarios del sistema (paths varían entre Ubuntu 18.04 ARM y x86)
ssh nano "for cmd in fallocate swapoff swapon sysctl mkswap chmod tee; do echo -n \"\$cmd → \"; which \$cmd; done"
```

## Endpoints HTTP del server

| Endpoint | Método | Uso |
|---|---|---|
| `/health` | GET | liveness |
| `/ws` | WS | inferencia binario (JPEG frame → JSON detecciones) |
| `/model/state` | GET | `no_model` / `ready` / `degraded` / `building` + `engine_binary_present` |
| `/model/check-updates` | POST | compara `hf_revision` + `onnx_sha256` local vs HF Hub (LFS oid sin descargar) |
| `/model/build` | POST | `{ "force": bool, "workspace_mb": int? }` → 202 con `job_id` |
| `/model/rollback` | POST | swap inverso con `.previous` |
| `/model/adopt` | POST | crea meta retroactivo para engine huérfano (binario sin meta) |
| `/jobs/active` | GET | job en curso o `null` |
| `/jobs/<id>` | GET | estado del job |
| `/jobs/<id>/logs` | GET | SSE stream de logs en vivo |
| `/jobs/<id>` | DELETE | cancela job activo (SIGTERM al builder) |

Todos los endpoints HTTP soportan CORS (`allow_origins=["*"]`) — el dashboard local en `localhost:8001` puede consumirlos directamente.

## Modelo + tracking de identidad

El sistema rastrea CADA engine compilado con un `.meta.json` paralelo:

```json
{
  "hf_revision": "b93964f9e4f9464cfe55b13ca5a577ba383a4dd5",
  "hf_commit_date": "2026-05-16T14:47:01.000Z",
  "onnx_sha256": "223f1a71...",      // SHA256 del ONNX que se compiló
  "engine_sha256": "a30f8f5f...",    // SHA256 del .engine resultante
  "build_completed_at": "2026-05-16T18:30:18Z",
  "build_duration_s": 1820,
  "trtexec_args": ["--fp16", "--workspace=512"],
  "validation": { "passed": 3, "failed": 0, ... },
  "adopted": false                    // true si vino de /model/adopt
}
```

Sin meta → estado `no_model` aunque haya binario en disco. Para registrar un binario huérfano:
- `POST /model/adopt` hashea el `.engine` + consulta HF (head + LFS oid de `exports/best.onnx`) + crea meta con `adopted: true`.
- O recompilar de cero: `POST /model/build {"force": true}`.

## Filesystem del Nano

```
/home/jetson/embebidos-3/
├── scripts/
│   ├── server/
│   │   ├── nano_server.py          FastAPI/WS server (uvicorn foreground via systemd)
│   │   ├── nano_start_server.sh    exec uvicorn (sin nohup, systemd Type=simple)
│   │   ├── nano_server_constants.py
│   │   ├── pid_utils.py
│   │   └── recover_job_state.py
│   ├── builder/
│   │   ├── nano_build_engine.sh    12 fases (download → trtexec → validate → swap)
│   │   ├── embebidos3-builder-launch wrapper sudoers-safe
│   │   ├── builder_state.py        helper para escribir job.json
│   │   ├── parse_trtexec_progress.py
│   │   ├── validate_engine.py      importa nano_correctness
│   │   ├── nano_correctness.py     letterbox + NMS V0 sm_53
│   │   ├── write_archive_manifest.py
│   │   └── write_engine_meta.py
│   ├── hub/
│   │   └── hf_rest.py              cliente HF (sin huggingface_hub SDK, compat Py3.6)
│   ├── install/
│   │   ├── nano_install_systemd.sh idempotente: units + sudoers + daemon-reload
│   │   └── nano_install_inference.sh
│   ├── training/
│   │   └── bootstrap.sh            provisioning Vast.ai (Track B)
│   └── dashboard/                  UI estática consumida en localhost
├── engines/
│   ├── best_fp16.engine            engine TRT activo
│   ├── best_fp16.engine.meta.json  tracking del engine activo
│   ├── .previous/                  backup para rollback
│   └── .staging/                   en compilación
├── onnx/                           descargas temporales del ONNX
└── logs/                           tegrastats por job

/run/embebidos3/                    runtime tmpfs (RuntimeDirectoryPreserve=yes)
├── job.json                        estado del job activo (fcntl.lockf + heartbeat)
└── builder.lock                    lock exclusivo del builder

/etc/systemd/system/
├── embebidos3-server.service       Type=simple, Restart=on-failure
└── embebidos3-builder@.service     templated oneshot, TimeoutStartSec=2700

/etc/sudoers.d/embebidos3           granular NOPASSWD (15 reglas, mode 0440)
/etc/embebidos3/secrets.env         HF_TOKEN, EMBEBIDOS3_TRTEXEC_WORKSPACE
/usr/local/bin/embebidos3-builder-launch   wrapper con regex validation defense-in-depth
```

## Restricciones de plataforma (Python 3.6.9)

NO usar (sintaxis post-3.7):
- Walrus operator `:=` (3.8+)
- `match`/`case` (3.10+)
- `dict | dict` merge (3.9+)
- F-string `=` debug (`f"{x=}"`, 3.8+)
- `subprocess.run(capture_output=True)` (3.7+) → usar `stdout=PIPE, stderr=PIPE`
- `subprocess.run(..., text=True)` (3.7+) → usar `universal_newlines=True`
- `argparse.add_subparsers(required=True)` (3.7+) → validar manualmente con `if not args.cmd: parser.error(...)`
- `Path.replace()` está OK en 3.6
- Pydantic 1.9.2 (NO 2.x) — usa `regex=` (NO `pattern=`). El campo `pattern=` se ignora SILENCIOSAMENTE y permite valores inválidos. Para validación estricta, hacer match manual con `re.compile(...)`.

NO disponibles en JetPack 4.6.1:
- `huggingface_hub` SDK (incompat Py3.6) — usar cliente custom `hf_rest.py`
- systemd directives v240+ (Nano tiene v237):
  - `StandardOutput=append:` → usar `file:`
  - `RuntimeDirectoryPreserve=restart` → usar `yes`

## Sudoers granular — 14 reglas (mode 0440)

```
jetson ALL=(root) NOPASSWD: /usr/local/bin/embebidos3-builder-launch *
jetson ALL=(root) NOPASSWD: /bin/systemctl stop|start embebidos3-server.service
jetson ALL=(root) NOPASSWD: /bin/systemctl stop embebidos3-builder@*.service
jetson ALL=(root) NOPASSWD: /bin/systemctl stop|start lightdm.service
jetson ALL=(root) NOPASSWD: /bin/systemctl disable nvzramconfig
jetson ALL=(root) NOPASSWD: /sbin/swapoff -a
jetson ALL=(root) NOPASSWD: /sbin/swapon /mnt/swap.img
jetson ALL=(root) NOPASSWD: /sbin/sysctl vm.swappiness=*
jetson ALL=(root) NOPASSWD: /usr/bin/fallocate -l 8G /mnt/swap.img    # OJO: NO /sbin/fallocate
jetson ALL=(root) NOPASSWD: /bin/chmod 600 /mnt/swap.img
jetson ALL=(root) NOPASSWD: /sbin/mkswap /mnt/swap.img
jetson ALL=(root) NOPASSWD: /usr/bin/tee /proc/sys/vm/drop_caches
```

**Verificá los paths de binarios con `which` ANTES de añadir reglas** — varían entre distros. Caso real: `fallocate` está en `/usr/bin/`, no en `/sbin/` (la convención GNU coreutils).

## Build de engine (15-40 min)

Durante el build:
- El server **se DETIENE** (libera GPU). Tus polls al server fallarán.
- Monitoreo: `ssh nano "cat /run/embebidos3/job.json"` o `journalctl -u embebidos3-builder@<id>.service -f`.
- Si necesitás cancelar: `DELETE /jobs/<id>` (cuando server esté arriba) o `sudo systemctl stop embebidos3-builder@<id>.service`.

Al terminar el build:
- Trap EXIT del script restaura: lightdm, swappiness, server.
- Swap atómico de engine via `Path.replace`.
- Worker recarga engine vía `request_swap`.

## Errores recurrentes (negativos aprendidos)

- "launch_failed" con stderr vacío en `POST /model/build` → casi siempre es sudoers mal configurado (path incorrecto) o `subprocess.run(capture_output=True)` que no existe en Py3.6.
- SIGSEGV durante shutdown del server → orden de destrucción del TRT context. Debe ser: `stream → outputs → inputs → bindings → trt_ctx → engine → runtime`.
- `pip3: command not found` → usar `python3 -m pip` en el Nano.
- WS `ConnectionClosedOK` durante envío de error → silenciar con try/except (es esperado, el peer cerró).
- `/dev/null` en bash funciona, pero en PowerShell usar `$null`.
