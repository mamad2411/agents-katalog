---
name: kali
description: Enciende la VM KaliLab (UTM) si esta apagada, verifica que responde por SSH y la deja lista como entorno aislado para investigacion pasiva (analisis de archivos sospechosos, OSINT sobre casos de trabajo) o como lugar de ejecucion de /pentest contra activos propios. Invocacion manual con /kali; /kali down la apaga.
disable-model-invocation: true
---

# /kali: KaliLab como entorno aislado

KaliLab es una VM de UTM en esta Mac (backend Apple, arm64). Todo lo que corre ahi queda fuera
del sistema de Karen: la Mac entra a Kali por SSH con una llave propia y Kali no tiene acceso
de vuelta (sin carpetas compartidas, sin reenvio de agente).

## Arrancar

```bash
bash ~/.claude/skills/kali/scripts/kali-up.sh
```

Idempotente: si Kali ya responde no hace nada; si esta apagada o suspendida la arranca y espera
el SSH (120 s por defecto, `KALI_BOOT_TIMEOUT`). Imprime host, usuario e IP.

Si falla por tiempo, casi siempre es que la VM quedo en GRUB o en una pantalla de la consola:
pide a Karen que mire la ventana de UTM. No intentes manejar la VM con Companion (no puede
escribir dentro de ella).

## Apagar (`/kali down`)

```bash
bash ~/.claude/skills/kali/scripts/kali-down.sh
```

Pide el apagado al sistema invitado y solo fuerza si no responde en 60 s.

## Datos fijos

- Alias SSH: `kalilab` (usuario `k`, llave `~/.ssh/kalilab_ed25519`, solo llave, sin root por SSH).
- `sudo` dentro de Kali pide la contrasena de Karen: nunca la pidas ni la guardes. Si un paso
  necesita sudo, dale a Karen el comando para que lo corra ella con `ssh -t kalilab '...'`.
- Teclado: la consola de Kali esta en US y el teclado fisico es latinoamericano.

## Modo 1: investigacion (casos de trabajo)

Para analizar material hostil (adjuntos, PDFs, correos) y hacer OSINT pasivo, como el caso de
suplantacion de ATFX.

1. Carpeta por caso en Kali: `~/casos/<caso>/`. Copia con `scp`, nunca montando carpetas.
2. Registra el SHA-256 de cada archivo original al recibirlo (cadena de custodia).
3. Analiza sin abrir: `exiftool`, `pdfid`, `pdf-parser`, `pdftotext`, `pdfimages`, cabeceras de
   correo con Python `email`.
4. OSINT solo pasivo: whois/RDAP, DNS, crt.sh, Wayback, geolocalizacion por IP, blockchain
   publica. **Nunca** escanear, autenticarse ni explotar infraestructura de terceros, aunque
   sea de estafadores: es acceso no autorizado y contamina la evidencia.
5. Las listas de "username checkers" dan falsos positivos: verifica con un usuario inventado
   antes de citar cualquier perfil.
6. Personas: un nombre en un whois o una foto de perfil no identifican a nadie. En los reportes
   se escribe "registrante declarado", no "responsable". Sin reconocimiento facial.
7. Reporte a Desktop, en el idioma que pida Karen, sin datos personales innecesarios de victimas.

El guard `pentest-scope.mjs` cubre `ssh/scp/sftp/rsync/mosh/utmctl` hacia KaliLab y pide
confirmacion en cada uno si la carpeta de trabajo no tiene un `.pentest-scope.json` vigente cuyo
alcance liste un target `kalilab:` (un alcance escrito para otro objetivo no basta). Para un caso
largo, crea uno con Karen con `targets: ["kalilab:~/casos/<caso>"]` y una regla "solo analisis
local y consultas pasivas".

`kali-up.sh` y `kali-down.sh` no pasan por el guard a proposito: solo encienden o apagan la VM y
corren un `ssh true` fijo. `~/.claude/skills/kali` es un symlink a este directorio del plugin.

## Modo 2: probar sistemas propios

Esto lo conduce `/pentest`, no esta skill: `/kali` solo deja el entorno listo. El alcance es el
`.pentest-scope.json` del proyecto; sin uno vigente y aprobado por Karen no se ejecuta nada
ofensivo desde Kali. Produccion de Atom/ATFX y terceros quedan fuera aunque Karen trabaje ahi,
salvo autorizacion escrita del dueno del sistema anadida al alcance.
