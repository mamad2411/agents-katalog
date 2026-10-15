---
name: init-store-io
description: "Inicializa una tienda VTEX IO basada en Fast Template LATAM. Ejecuta el orquestador init.js que tiene 11 pasos. Diagnostica y resuelve errores en cada paso. Usar cuando el usuario dice /init-store-io, 'inicializar tienda vtex io', 'levantar tienda io', 'setup store io', 'correr init', 'ejecutar init'."
---

# Skill: Init Store IO — Fast Template LATAM

Orquesta la inicializacion de tienda VTEX IO ejecutando `init.js` y sus 11 pasos. Diagnostica y resuelve errores automaticamente.

**Directorio de scripts**: `init-ftlat-v2/` (dentro del repo fasttemplate)

---

## Los 11 Pasos del Orquestador

```
 1. Login y workspace VTEX         → login-workspace.js
 2. Easy Setup - Instalar app      → easy-setup-populate.js
 3. Clonar repositorios            → clone-repos.js
 4. Instalar peer dependencies     → install-apps.js
 5. Configuracion inicial (setup)  → setup.js config.json
 6. Linkear aplicaciones           → vtex-link.js
 7. Subir fuentes                  → upload-fonts.js
 8. Subir imagenes                 → upload-images-vtex.js
 9. Config post-imagenes (setup)   → setup.js config.json
10. Subir emails                   → upload-emails.js
11. Pasos manuales                 → manual-steps.js
```

---

## Prerequisitos

Verificar antes de arrancar:

```bash
node --version && yarn --version && vtex --version && ssh -T git@bitbucket.org
```

- **Node.js** >= 14
- **Yarn** global
- **VTEX CLI** instalado y funcionando
- **Acceso SSH a Bitbucket** (workspace vtex-infralatam)
- **node-fetch** y **form-data** instalados en init-ftlat-v2 (`cd init-ftlat-v2 && yarn`)

---

## Paso 0: Clonar el repo init-ftlat

Antes de ejecutar cualquier paso, clonar el repo base en la rama `process`:

```bash
git clone --branch process git@bitbucket.org:vtex-infralatam/init-ftlat.git
cd init-ftlat/init-ftlat-v2
yarn
```

**IMPORTANTE**: Siempre clonar desde la rama `process`. Esta rama contiene la version actualizada de los scripts de inicializacion.

### Limpieza post-ejecucion

Al terminar todos los pasos (1-11), eliminar el repo clonado `init-ftlat/`. Solo sirve para ejecutar los scripts — los repos de la tienda ya quedaron clonados aparte.

```bash
rm -rf init-ftlat
```

---

## Como Ejecutar

### Orquestador completo

```bash
cd init-ftlat-v2
node init.js --yes --output json
```

### Desde un paso especifico (resume)

```bash
node init.js --from-step 5 --yes --output json
```

### Un solo paso

```bash
node init.js --only-step 3 --yes --output json
```

### Paso individual directo (sin orquestador)

```bash
node login-workspace.js --vendor mitienda --workspace easysetup --yes --output json
node clone-repos.js --proyecto ATKAR --vendor mitienda --yes --output json
```

---

## Estado Persistente: init-state.json

El orquestador mantiene estado en `init-ftlat-v2/init-state.json`:

```json
{
  "vendor": "mitienda",
  "proyecto": "ATKAR",
  "workspace": "easysetup",
  "paso_actual": 1,
  "easy_setup_ok": null,
  "completed_steps": []
}
```

**Campos clave**:
- `paso_actual`: Ultimo paso ejecutado. `--from-step` usa este valor si no se pasa argumento.
- `completed_steps`: Array de IDs de pasos completados.
- `vendor` / `proyecto`: Usados por scripts que necesitan estos valores.

**Para resetear**: borrar `init-state.json` o editarlo manualmente.

---

## Configuracion: config.json

Archivo de variables para reemplazo masivo en repos. `setup.js` busca cada KEY en todos los archivos del proyecto y reemplaza por su VALUE.

Variables importantes que se llenan automaticamente:
- `VENDOR` — lo llena `clone-repos.js`
- `PRIMARY_FONT` / `SECONDARY_FONT` — lo llena `upload-fonts.js`
- `LOGO_IMAGE`, `LOGO_BLANCO`, etc. — lo llena `upload-images-vtex.js`

Variables que requieren input del usuario:
- `MARCA`, `PRIMARY_COLOR`, `SECONDARY_COLOR`, todos los colores
- `PHONE_MARCA`, `MAIL_TO`, tokens de integracion

---

# CATALOGO DE ERRORES POR PASO

## Paso 1: Login y Workspace (`login-workspace.js`)

### Que hace
1. Verifica VTEX CLI instalado (`vtex --version`)
2. Obtiene vendor (args, state, o prompt)
3. Verifica login actual (`vtex whoami`)
4. Si no logueado → ejecuta `vtex login {vendor}`
5. Cambia a workspace (`vtex use {workspace}`)
6. Guarda vendor/workspace en state

### Errores y soluciones

| Error JSON | Mensaje | Causa | Solucion |
|---|---|---|---|
| `vtex_cli_not_installed` | VTEX CLI no esta instalado | `vtex --version` fallo | Instalar: `yarn global add vtex` o `npm i -g vtex` |
| `vendor_required` | --vendor requerido con --yes | Modo --yes sin vendor en args ni state | Pasar `--vendor mitienda` o escribir vendor en init-state.json |
| `not_logged_in` | No hay sesion activa para {vendor} | En modo --yes no puede abrir browser | El usuario debe ejecutar `vtex login {vendor}` manualmente antes |
| `login_failed` | Error durante vtex login | Login interactivo fallo (browser no abrio, timeout) | Usuario ejecuta `vtex login {vendor}` en otra terminal |
| `login_verification_failed` | No se pudo verificar login | `vtex whoami` no retorna account correcto despues de 60s | Verificar que el login completo OK: `vtex whoami`. Si no → `vtex login {vendor}` |
| `workspace_failed` | Error al cambiar a workspace | `vtex use {workspace}` fallo | Verificar: `vtex workspace list`. Crear workspace: `vtex workspace create {ws}` |

### Diagnostico automatico

```bash
# Verificar estado actual
vtex whoami
# Si no hay sesion → el usuario debe hacer login manual
vtex login {vendor}
# Verificar workspace
vtex workspace list
```

---

## Paso 2: Easy Setup (`easy-setup-populate.js`)

### Que hace
1. Instala app `infralatam.easy-setup@0.x` via `vtex install`
2. Lee sesion VTEX de `~/.vtex/session/session.json`
3. POST a `https://{account}.myvtex.com/_v/api/easy-setup/populate`
4. Pobla catalogo, logistica, pagos del account

### Validacion previa — OBLIGATORIA

Antes de ejecutar este paso, verificar si la tienda ya tiene datos. Easy Setup sobreescribe catalogo, logistica y pagos. **No ejecutar si la tienda ya tiene informacion.**

```bash
# Verificar si hay productos en catalogo
curl -s "https://{vendor}.myvtex.com/api/catalog_system/pvt/products/GetProductAndSkuIds?_from=0&_to=1" \
  -H "VtexIdclientAutCookie: {token}" | node -e "
const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
const total=d.range?.total || Object.keys(d.data||{}).length;
console.log(JSON.stringify({has_products: total > 0, total}))
"
```

**Regla para el agente**:
1. Ejecutar la verificacion de productos
2. Si `has_products: true` → **PREGUNTAR al usuario** antes de continuar. Mostrar cantidad de productos encontrados y advertir que Easy Setup puede sobreescribir datos existentes
3. Si `has_products: false` → tienda vacia, ejecutar Easy Setup normalmente
4. Si el usuario confirma que quiere saltear → marcar paso 2 como completado y continuar con paso 3

### Errores y soluciones

| Error JSON | Mensaje | Causa | Solucion |
|---|---|---|---|
| `easy_setup_install_failed` | Error instalando Easy Setup | `vtex install` fallo (permisos, app no encontrada) | Manual: `vtex install infralatam.easy-setup@0.x -f`. Si persiste → verificar que la app existe en el registry |
| `no_vtex_session` | No se encontro sesion VTEX CLI | `~/.vtex/session/session.json` no existe o token expirado | `vtex login {vendor}` para crear/renovar sesion |
| `api_error` | Error {status}: {body} | API rechazo el request (401=token expirado, 404=app no instalada, 500=error server) | **401/403**: `vtex login {vendor}`. **404**: verificar app instalada `vtex list`. **500**: reintentar, es idempotente |
| `connection_error` | Error de conexion: {message} | Red, DNS, o timeout | Verificar internet. Reintentar. Si `ECONNREFUSED` → el account no existe o dominio mal |

### Bug conocido en este script

**Linea 33** usa `isJsonMode()` pero NO lo importa de output.js (solo importa `parseOutputFlag, log, logError, jsonOut`). En modo JSON, el `vtex install` mostrara output en consola igualmente. No causa crash porque `isJsonMode` no esta definido y la expresion se evalua como falsy.

### Diagnostico automatico

```bash
# Verificar sesion
cat ~/.vtex/session/session.json | node -e "const s=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); console.log('account:', s.account, 'token length:', s.token?.length)"

# Verificar app instalada
vtex list | grep easy-setup

# Test manual del endpoint
curl -s -w "\n%{http_code}" -X POST \
  "https://{vendor}.myvtex.com/_v/api/easy-setup/populate" \
  -H "Content-Type: application/json" \
  -H "VtexIdclientAutCookie: $(cat ~/.vtex/session/session.json | node -e "process.stdout.write(JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).token)")" \
  -d '{}'
```

---

## Paso 3: Clonar Repositorios (`clone-repos.js`)

### Que hace
1. Obtiene proyecto/vendor (args, state, o prompt)
2. Clona 10 repos de Bitbucket (vtex-infralatam)
3. Elimina `.git/` de cada repo clonado
4. Actualiza `manifest.json`: vendor, title, name, dependencies
5. Reemplaza acronimo `FTLAT` → `{proyecto}` en contenido y nombres de archivos
6. Actualiza VENDOR en config.json

### Los 10 repos

```
captation-modal-FTLAT → captation-modal-{PROYECTO}
newsletter-FTLAT      → newsletter-{PROYECTO}
checkout-ui-FTLAT     → checkout-ui-{PROYECTO}
checkout-summary-FTLAT→ checkout-summary-{PROYECTO}
footer-FTLAT          → footer-{PROYECTO}
minicart-FTLAT        → minicart-{PROYECTO}
fast-template-FTLAT   → store-theme-{PROYECTO}  (renombrado!)
menu-basic-FTLAT      → menu-basic-{PROYECTO}
store-components-FTLAT→ store-components-{PROYECTO}
mails-backup-FTLAT    → mails-backup-{PROYECTO}
```

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| `missing_args` (proyecto/vendor) | Modo --yes sin proyecto o vendor | Pasar `--proyecto ATKAR --vendor mitienda` |
| `git clone` falla para un repo | SSH sin acceso, repo no existe, red | Verificar SSH: `ssh -T git@bitbucket.org`. Verificar repo existe en vtex-infralatam. Clonar manual: `git clone git@bitbucket.org:vtex-infralatam/{repo}-FTLAT.git {target}` |
| Directorio destino ya existe | Re-ejecucion sin limpiar | Borrar directorio existente: `rm -rf ../{target}` |
| Error reemplazando acronimo | Archivo binario mal detectado | Normalmente silencioso. Si corrompe archivo → re-clonar ese repo |

### Diagnostico automatico

```bash
# Verificar acceso SSH
ssh -T git@bitbucket.org

# Verificar que repos existen
for repo in captation-modal newsletter checkout-ui checkout-summary footer minicart fast-template menu-basic store-components mails-backup; do
  git ls-remote git@bitbucket.org:vtex-infralatam/${repo}-FTLAT.git HEAD 2>/dev/null && echo "OK: $repo" || echo "FAIL: $repo"
done

# Verificar repos ya clonados
ls -d ../*-{PROYECTO} 2>/dev/null

# Limpiar para re-clonar
rm -rf ../*-{PROYECTO}
```

### Post-verificacion

Despues de clonar, verificar:
1. 10 directorios existen en directorio padre
2. Cada uno tiene `manifest.json` con vendor correcto
3. No hay referencias a `FTLAT` (salvo si el proyecto ES "FTLAT")

---

## Paso 4: Instalar Peer Dependencies (`install-apps.js`)

### Que hace
1. Verifica login VTEX via `vtex whoami`
2. Busca store-theme por `manifest.json` name match en directorio padre
3. Lee `peerDependencies` del manifest
4. Agrega `vtex.wish-list@1.x` si no esta
5. Ejecuta `vtex install {dep}@{version} -f` para cada una

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| `not_logged_in` | `vtex whoami` fallo | `vtex login {vendor}` |
| Store-theme no encontrado | Repos no clonados o manifest.json no tiene "store-theme" en name | Verificar paso 3 completado. Buscar: `grep -r "store-theme" ../*/manifest.json` |
| `vtex install` falla para una dep | App no existe en registry, version no disponible, permisos | Individual: `vtex install {dep}@{version} -f`. Si la app no existe → verificar nombre exacto. Algunas apps requieren billing aprobado |
| Todas las deps fallan | Token expirado | `vtex login {vendor}` y reintentar |
| Billing required / Terms of service | App requiere aprobacion manual en VTEX Admin | Ver seccion "Apps que requieren aprobacion" abajo |

### Apps que requieren aprobacion de billing

Algunas peer dependencies necesitan que el usuario apruebe terminos/billing manualmente en VTEX Admin. `vtex install -f` falla silenciosamente o muestra error de billing para estas apps.

**Regla para el agente — OBLIGATORIA**:

1. Despues de ejecutar `install-apps.js`, parsear output y listar TODAS las deps que fallaron
2. Para cada dep fallida, verificar si es error de billing ejecutando: `vtex install {dep}@{version}` (sin -f) y buscar mensajes como "billing", "terms", "subscribe", "pricing" en output
3. Si hay apps pendientes de billing:
   - Generar URL de aprobacion: `https://{vendor}.myvtex.com/admin/apps/{vendor-app}/{version}/setup` (o la URL que VTEX CLI muestre en el error)
   - **MOSTRAR AL USUARIO** la lista de apps pendientes con sus URLs de aprobacion
   - **ESPERAR** a que el usuario confirme que aprobo cada una
   - Reintentar `vtex install {dep}@{version} -f` despues de aprobacion
4. **NO continuar al paso 5/6** hasta que TODAS las peer dependencies esten instaladas. Componentes fallan en `vtex link` si faltan peers (ej: `vtex.wish-list@1.x`)

### Diagnostico automatico

```bash
# Verificar login
vtex whoami

# Verificar store-theme existe
find .. -name "manifest.json" -maxdepth 2 -exec grep -l "store-theme" {} \;

# Instalar dep individual que fallo
vtex install vtex.store@2.x -f

# Verificar que deps estan instaladas
vtex list | grep -E "wish-list|store-sitemap|reviews-and-ratings"
```

---

## Paso 5 y 9: Setup / Reemplazo de Variables (`setup.js config.json`)

### Que hace
1. Lee config.json (keys = variables, values = reemplazos)
2. Recorre TODOS los archivos del directorio padre (raiz del proyecto)
3. Busca cada KEY como palabra completa (regex `\b`) en contenido
4. Reemplaza con VALUE
5. Renombra archivos que contengan KEY en nombre

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| `Error: Debes pasar un archivo JSON` | Falta argumento | Ejecutar: `node setup.js config.json` |
| `Error: El archivo config.json no existe` | config.json no encontrado en CWD | Verificar CWD es `init-ftlat-v2/`. El archivo debe existir ahi |
| `SyntaxError: Unexpected token` | config.json malformado | Validar JSON: `node -e "JSON.parse(require('fs').readFileSync('config.json','utf8'))"` |
| No reemplaza nada (`No se encontraron archivos`) | Variable no existe en ningun archivo, o ya fue reemplazada | Normal si es segunda ejecucion. Verificar que repos existen en directorio padre |
| Corrompe archivos binarios | Intenta leer binario como UTF-8 | El script ignora errores de lectura. Si detectas corrupcion → re-clonar repo afectado |

### Importante

- **Paso 5** se ejecuta ANTES de subir fuentes/imagenes → las variables `PRIMARY_FONT`, `SECONDARY_FONT`, `LOGO_IMAGE`, etc. todavia estan vacias o con valores placeholder
- **Paso 9** se ejecuta DESPUES de subir imagenes → config.json ya tiene URLs de imagenes
- setup.js busca "word boundary" (`\b`), asi que `VENDOR` no matchea dentro de `myVENDOR` ni `VENDOR_ID`

### Diagnostico automatico

```bash
# Validar config.json
node -e "const c=JSON.parse(require('fs').readFileSync('config.json','utf8')); console.log(Object.keys(c).length, 'variables'); Object.entries(c).filter(([k,v])=>!v||v===k).forEach(([k])=>console.log('  VACIA:', k))"

# Verificar que directorio padre tiene repos
ls -d ../*/manifest.json 2>/dev/null | wc -l
```

---

## Paso 6: Linkear Aplicaciones (`vtex-link.js`)

### Que hace
1. Verifica VTEX CLI instalado
2. Busca directorios que matcheen patrones (9 para vtex link + 2 para yarn dev)
3. Ordena por dependencias (topological sort) — store-theme al final
4. Para cada directorio:
   - `yarn` si falta `node_modules/`
   - `yarn run sass` si tiene script sass (proceso background)
   - `vtex link` como proceso background, espera "successfully" (timeout 300s)
5. Para checkout: `yarn run dev` (proceso background)
6. Muestra PIDs activos al final

### Patrones de directorio (vtex link)

```
checkout-summary, footer, menu-basic, newsletter,
store-components, captation-modal, minicart,
fast-template, store-theme
```

### Patrones de directorio (yarn dev)

```
checkout-io, checkout-ui
```

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| VTEX CLI no instalado | `vtex --version` fallo | `yarn global add vtex` |
| No se encontraron directorios | Repos no clonados | Verificar paso 3 |
| `vtex link` timeout (300s) | Build tarda mucho, o error silencioso | Revisar output. Reintentar manual: `cd ../{repo} && vtex link`. Si TypeScript error → fix error en codigo |
| `vtex link` falla (exit code != 0) | Error de build, dependencia faltante, app ya linkeada, conflict | Leer output del error. Causas comunes abajo |
| `yarn` falla en un repo | Dependencias rotas, package.json invalido | `cd ../{repo} && rm -rf node_modules && yarn` |
| Sass no arranca | Script sass no existe o sass no instalado | Verificar `package.json` del repo tiene script "sass" |

### Errores comunes de `vtex link`

**1. TypeScript errors**
```
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'
```
→ Fix: corregir el archivo TypeScript indicado

**2. Dependency not found**
```
Could not resolve dependency: {vendor}.{app}@{version}
```
→ Fix: `vtex install {vendor}.{app}@{version} -f` o verificar que la app dependency esta linkeada/instalada

**3. Builder error**
```
Error in builder react: Build failed
```
→ Fix: revisar errores de React/TypeScript en el output. Usualmente imports faltantes o tipos incorrectos

**4. App already linked**
```
The app is already linked
```
→ No es error real. La app ya esta corriendo

**5. Manifest validation**
```
Invalid manifest.json
```
→ Fix: verificar manifest.json del repo tiene vendor, name, version validos

### Regla para el agente — Reintentar componentes fallidos

El script `vtex-link.js` NO reintenta componentes que fallan (timeout u otro error). **El agente DEBE reintentar manualmente**:

1. Parsear output JSON e identificar componentes fallidos (campo `failed` o mensaje "Fallaron")
2. Por cada componente fallido:
   - Matar proceso colgado si existe: `kill {pid}` (usar PIDs del output)
   - Reintentar manual: `cd ../{repo} && vtex link` (esperar "successfully" en output, timeout 300s)
3. Maximo 2 reintentos por componente
4. Si falla despues de 2 reintentos → informar al usuario con error exacto y pedir intervencion

**Orden de reintento importa**: si `store-theme` fallo, reintentar ULTIMO (depende de otros componentes).

### Diagnostico automatico

```bash
# Verificar que repos existen
ls -d ../*-{PROYECTO}/ 2>/dev/null

# Verificar login y workspace
vtex whoami

# Matar links anteriores
node kill-vtex-links.js --yes

# Re-linkear un repo especifico
cd ../{repo} && vtex link

# Ver procesos vtex link activos
ps aux | grep "vtex link" | grep -v grep
```

---

## Paso 7: Subir Fuentes (`upload-fonts.js`)

### Que hace
1. Busca store-theme y checkout por `manifest.json` name en directorio padre
2. Escanea `init-ftlat-v2/fonts/` buscando subcarpetas con fuentes (.otf, .ttf, .woff, .woff2, .eot)
3. Detecta font-family (nombre carpeta), weight (nombre archivo), style (italic/normal)
4. Copia fuentes a `{store-theme}/assets/fonts/`
5. Genera `{store-theme}/styles/configs/font-faces.css`
6. Actualiza `config.json` con PRIMARY_FONT y SECONDARY_FONT
7. Si checkout existe → genera `_fonts.scss` con URLs absolutas del workspace

### Estructura esperada de fonts/

```
fonts/
├── futura-std/
│   ├── FuturaStd-Bold.otf
│   ├── FuturaStd-Regular.otf
│   └── FuturaStd-Light.otf
└── neue-montreal/
    ├── NeueMontreal-Regular.woff2
    └── NeueMontreal-Bold.woff2
```

- Primera carpeta = PRIMARY_FONT
- Segunda carpeta = SECONDARY_FONT
- Si solo 1 carpeta → ambas iguales

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| `No se encontro store-theme` | Repos no clonados o manifest.json no matchea | Verificar: `find .. -name manifest.json -exec grep -l store-theme {} \;` |
| `No se encontraron carpetas dentro de fonts/` | Directorio `fonts/` vacio | Crear subcarpetas con archivos de fuente dentro de `init-ftlat-v2/fonts/`. Estructura: `fonts/{familia}/{archivo.ext}` |
| `No se encontraron archivos de fuentes` | Carpetas existen pero no tienen .otf/.ttf/.woff/.woff2/.eot | Verificar extensiones de archivos en `fonts/` |
| `No se pudo obtener workspace` | `vtex whoami` fallo (solo afecta checkout _fonts.scss) | `vtex login {vendor}`. Sin esto, no genera _fonts.scss para checkout pero fuentes del store-theme SI se suben |

### Diagnostico automatico

```bash
# Verificar fuentes
find fonts/ -type f \( -name "*.otf" -o -name "*.ttf" -o -name "*.woff" -o -name "*.woff2" \)

# Verificar que se copiaron
ls -la ../store-theme-*/assets/fonts/

# Verificar font-faces.css generado
cat ../store-theme-*/styles/configs/font-faces.css

# Verificar config.json actualizado
node -e "const c=JSON.parse(require('fs').readFileSync('config.json','utf8')); console.log('PRIMARY:', c.PRIMARY_FONT, 'SECONDARY:', c.SECONDARY_FONT)"
```

---

## Paso 8: Subir Imagenes (`upload-images-vtex.js`)

### Que hace
1. Lee sesion VTEX de `~/.vtex/session/session.json`
2. Lee imagenes de `init-ftlat-v2/images/`
3. Salta imagenes que ya tienen URL en config.json (idempotente)
4. Sube cada imagen via GraphQL (file-manager-graphql mutation)
5. Actualiza config.json con URL de cada imagen cuyo nombre (sin ext) matchee una KEY

### Errores y soluciones

| Error | Causa | Solucion |
|---|---|---|
| No se encontro sesion VTEX CLI | `~/.vtex/session/session.json` no existe | `vtex login {vendor}` |
| Sesion incompleta/expirada | Token vacio o expirado | `vtex login {vendor}` para renovar |
| `La carpeta images no existe` | `init-ftlat-v2/images/` no existe | Crear la carpeta y agregar imagenes: `mkdir -p images` |
| `Error 401` | Token expirado durante upload | `vtex login {vendor}` y reintentar. El script es idempotente (salta imagenes ya subidas) |
| `Error 413` | Imagen demasiado grande | Comprimir la imagen. VTEX tiene limite de ~4MB por archivo |
| `Error 500` en GraphQL | Error interno de VTEX file-manager | Reintentar. Si persiste → usar metodo alternativo catalog-images (cambiar en codigo linea 303) |
| `Respuesta sin URL` | GraphQL retorno datos pero sin fileUrl | Posible error de permisos. Verificar que el workspace tiene permisos de escritura |
| `No se encontro la key "{name}" en config.json` | Nombre de imagen no matchea ninguna key | Normal si la imagen es extra. Para que auto-actualice config.json, el nombre del archivo (sin ext) debe ser exactamente igual a la KEY |

### Diagnostico automatico

```bash
# Verificar imagenes disponibles
ls -la images/

# Verificar sesion
node -e "const s=JSON.parse(require('fs').readFileSync(require('os').homedir()+'/.vtex/session/session.json','utf8')); console.log('account:', s.account, 'token:', s.token?.substring(0,20)+'...')"

# Verificar que keys de config matchean nombres de imagenes
node -e "
const fs=require('fs'), path=require('path');
const config=JSON.parse(fs.readFileSync('config.json','utf8'));
const imgs=fs.readdirSync('images').map(f=>path.basename(f,path.extname(f)));
imgs.forEach(i => {
  if(config[i]!==undefined) console.log('MATCH:', i, config[i]?'(ya tiene URL)':'(vacia)');
  else console.log('NO MATCH:', i);
});
"

# Re-ejecutar (idempotente, salta imagenes ya subidas)
node upload-images-vtex.js --yes
```

---

## Paso 10: Subir Emails (`upload-emails.js`)

### Que hace
1. Busca directorio `mails-backup-*` en directorio padre
2. Verifica que existe `upload-templates.js` dentro
3. Instala dependencias si faltan (`yarn`)
4. Ejecuta `node upload-templates.js` dentro del directorio mails-backup

### Errores y soluciones

| Error JSON | Causa | Solucion |
|---|---|---|
| `mails_backup_not_found` | No existe directorio mails-backup | Verificar paso 3 (clonar repos). Buscar: `ls -d ../mails-backup-*` |
| `upload_script_not_found` | `upload-templates.js` no existe dentro del directorio | El repo de mails-backup esta incompleto. Re-clonar: `git clone git@bitbucket.org:vtex-infralatam/mails-backup-FTLAT.git mails-backup-{PROYECTO}` |
| `upload_failed` | `node upload-templates.js` fallo | Ejecutar manual: `cd ../mails-backup-{PROYECTO} && node upload-templates.js`. Causas comunes: token expirado, templates malformados |
| Yarn falla | Dependencias rotas | `cd ../mails-backup-{PROYECTO} && rm -rf node_modules && yarn` |

### Diagnostico automatico

```bash
# Verificar directorio
ls -d ../mails-backup-*/

# Verificar script existe
ls ../mails-backup-*/upload-templates.js

# Ejecutar manual
cd ../mails-backup-* && node upload-templates.js
```

---

## Paso 11: Pasos Manuales (`manual-steps.js`)

### Que hace
Solo muestra un checklist de pasos que requieren accion manual del usuario. No ejecuta nada. No puede fallar.

### Pasos manuales que lista:
1. Subir favicon (CMS > Configuracion > General)
2. HTML header/footer en checkout (Portal > Code)
3. Entidad Newsletter en MasterData (NL)
4. Trigger newsletter
5. Indexar Intelligent Search
6. Crear archivo monto-envio.json en checkout
7. Configurar Mascara Simple

---

# SCRIPTS AUXILIARES (no en el orquestador)

## configure-repo.js

Ejecuta `yarn` en init-ftlat-v2 y en todos los repos clonados. Equivale a instalar dependencias de todos los repos.

### Errores:
- `yarn no esta instalado` → `npm install -g yarn`
- `No se encontraron directorios` → Repos no clonados (paso 3)
- `yarn` falla en un repo → `cd ../{repo} && rm -rf node_modules yarn.lock && yarn`

## install-peer-deps.js

Busca store-theme, lee peerDependencies, y ejecuta `vtex install` para cada una.

### Errores:
- Store-theme no encontrado → verificar paso 3
- `vtex whoami` falla → `vtex login {vendor}`
- `vtex install` falla → verificar app existe, billing aprobado

## kill-vtex-links.js

Busca procesos `vtex link` y `yarn run sass` y los mata.

### Errores:
- Proceso no se puede matar → `kill -9 {PID}`
- Ningun proceso encontrado → normal, no hay links corriendo

---

# ERRORES TRANSVERSALES

Estos errores pueden ocurrir en multiples pasos:

## Token VTEX expirado

**Sintoma**: 401/403 en API calls, "not logged in", sesion incompleta
**Afecta**: pasos 1, 2, 4, 6, 7, 8, 10
**Solucion**:
```bash
vtex login {vendor}
# Luego resumir desde el paso que fallo:
node init.js --from-step {N} --yes --output json
```

## SSH a Bitbucket falla

**Sintoma**: `Permission denied (publickey)`, `Could not resolve hostname`
**Afecta**: paso 3
**Solucion**:
```bash
# Verificar SSH key
ssh -T git@bitbucket.org

# Si falla, verificar key configurada
cat ~/.ssh/id_rsa.pub  # o id_ed25519.pub

# Agregar key a Bitbucket: Settings > SSH Keys
```

## node-fetch no instalado

**Sintoma**: `Cannot find module 'node-fetch'`
**Afecta**: pasos 2, 8
**Solucion**:
```bash
cd init-ftlat-v2 && yarn
# o
npm install node-fetch form-data
```

## Directorio padre no tiene repos

**Sintoma**: "No se encontro store-theme", "No se encontraron directorios"
**Afecta**: pasos 4, 5, 6, 7, 8, 9, 10
**Solucion**: Verificar paso 3 completo. `ls -d ../*-{PROYECTO}`

## ENOENT (archivo/carpeta no existe)

**Sintoma**: `Error: ENOENT: no such file or directory`
**Diagnostico**: Leer la ruta del error. Determinar que archivo/carpeta falta.
**Solucion**: Crear la carpeta/archivo faltante, o ejecutar el paso previo que lo genera.

## Regex lastIndex bug

Varios scripts usan regex con flag `g` y llaman `.test()` seguido de `.replace()`. El `lastIndex` puede causar matcheos inconsistentes. Los scripts hacen `regex.lastIndex = 0` para mitigar, pero si ves reemplazos parciales, ejecutar el paso de nuevo suele resolver.

---

# FLUJO DE EJECUCION RECOMENDADO

## Para agente AI

1. **Verificar prerequisitos**: node, yarn, vtex, ssh
2. **Verificar login**: `vtex whoami` — si no esta logueado, pedir al usuario que ejecute `vtex login`
3. **Ejecutar orquestador**: `node init.js --yes --output json`
4. **Si falla un paso**:
   a. Parsear JSON output para identificar paso y error
   b. Consultar seccion de errores del paso en esta skill
   c. Aplicar solucion
   d. Resumir: `node init.js --from-step {N} --yes --output json`
5. **Despues de paso 7 (fuentes)**: verificar config.json tiene PRIMARY_FONT/SECONDARY_FONT correctos
6. **Despues de paso 8 (imagenes)**: verificar config.json tiene URLs de imagenes
7. **Paso 11**: mostrar checklist al usuario para acciones manuales

## Cuando el orquestador no funciona

Ejecutar pasos individuales:

```bash
cd init-ftlat-v2

# Paso 1
node login-workspace.js --vendor {VENDOR} --workspace easysetup --yes --output json

# Paso 2
node easy-setup-populate.js --yes --output json

# Paso 3
node clone-repos.js --proyecto {PROYECTO} --vendor {VENDOR} --yes --output json

# Paso 4
node install-apps.js --yes --output json

# Paso 5
node setup.js config.json

# Paso 6
node vtex-link.js

# Paso 7
node upload-fonts.js

# Paso 8
node upload-images-vtex.js --yes

# Paso 9
node setup.js config.json

# Paso 10
node upload-emails.js --yes --output json

# Paso 11
node manual-steps.js --output json
```

---

# REGLAS PARA EL AGENTE

1. **SIEMPRE usar `--yes --output json`** al ejecutar scripts (evitar prompts interactivos)
2. **PARSEAR JSON** del output para detectar errores programaticamente
3. **NUNCA saltear pasos** — el orden importa (excepto paso 11 que es informativo)
4. **Token expirado es la causa #1** — si algo falla con 401/403, renovar token primero
5. **Re-ejecucion es segura** — la mayoria de scripts son idempotentes (clone-repos es la excepcion: borrar dirs antes de re-clonar)
6. **CWD debe ser `init-ftlat-v2/`** para todos los scripts
7. **config.json se va llenando** progresivamente: paso 3 pone VENDOR, paso 7 pone fuentes, paso 8 pone imagenes, paso 5/9 reemplaza variables
8. **No modificar config.json manualmente** entre pasos 5 y 9 (setup.js busca keys como strings, si ya fueron reemplazadas no las encuentra de nuevo)
9. **Verificar estado**: leer `init-state.json` para saber en que paso quedo
10. **Informar progreso** al usuario despues de cada paso completado
11. **Limpieza final**: al terminar todos los pasos, eliminar el directorio `init-ftlat/` clonado en paso 0 — solo contiene scripts, no es parte de la tienda
