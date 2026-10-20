# ElderTech — Instrucciones para Claude

## ¿Qué es este proyecto?
Aplicación móvil para adultos mayores en residencias geriátricas.
Stack: **React Native + Expo SDK 54 + TypeScript + Supabase**.

## Carpeta de skills
Toda la documentación del proyecto para Claude está en `.claude/`:
- `CONTEXT.md` — visión general, decisiones de arquitectura
- `DATABASE.md` — schema completo de Supabase
- `DESIGN.md` — sistema de diseño, colores, tipografía
- `SCREENS.md` — especificación pantalla por pantalla

**Leer siempre `.claude/CONTEXT.md` al inicio de cada sesión.**

## Alias de paths
`@/*` → `./src/*` (configurado en tsconfig.json y babel.config.js)

## Comandos útiles

**El backend (`backend/`) tiene que estar corriendo siempre** — la app y el
backoffice ya no hablan con Supabase directo para la mayoría de los módulos,
sino con este BFF (`http://localhost:3001` en dev). Si no está levantado, el
dashboard del backoffice y las pantallas de la app quedan sin datos (todo en 0
o "sin datos aún"), sin ningún error visible.

```bash
# Backend (BFF) — dejarlo corriendo en su propia terminal
cd backend && npm install   # solo la primera vez (o si package.json cambió)
cd backend && npm run dev   # queda escuchando en :3001

# App móvil
npx expo start          # Iniciar en modo desarrollo
npx expo start --android
npx expo start --ios

# Backoffice
cd backoffice && npm run dev   # Vite, queda en :5173
```

Si en Windows ves `SELF_SIGNED_CERT_IN_CHAIN` en los logs del backend (típico
en redes corporativas/escolares con inspección TLS), corré
`cd backend && npm run setup:certs` — también se corre solo antes de cada
`npm run dev` (`predev`), así que normalmente no hace falta a mano.

## Versión web / PWA
`npm run build:web` (build) · `npm run serve:web` (prueba local con las cabeceras de Vercel).
Adaptadores por plataforma (`*.web.ts(x)`), arquitectura, limitaciones de Safari/iOS, DNS de DonWeb,
variables y matriz de funcionalidades: **`docs/WEB_PWA.md`**. El backend necesita `CORS_ALLOWED_ORIGINS`
con el dominio web y las claves `VAPID_*` para Web Push.

## Reglas de desarrollo
1. **Accesibilidad primero**: botones mínimo 48×48pt, texto mínimo 17px body
2. **Sin tabs**: la navegación es Stack (Expo Router), no bottom tabs
3. **TypeScript estricto**: sin `any`, tipado explícito siempre
4. **Supabase real**: no mockear servicios — usar fallback solo para dev sin credenciales
5. **Open-Meteo**: API de clima gratuita, sin API key (ver `climaService.ts`)
6. **expo-av**: para streaming de radio (ver `RadioContext.tsx`)
7. **expo-speech**: para TTS en español AR (ver `tts.ts`)

## Variables de entorno necesarias
Ver `.env.example` — copiar a `.env` y completar con datos de Supabase.

## APK/OTA sin datos de la base — causa raíz recurrente (ya resuelta, 4 capas)
Si la app funciona bien con `expo start` pero el **APK instalado o una
actualización OTA en un celular real** no carga nada (todo vacío o pantalla
roja de error), la causa histórica siempre fue la misma: el build/`eas
update` se publicó con `EXPO_PUBLIC_API_URL=http://localhost:3001` (el valor
de `.env` local, pensado solo para la PC del developer) o con una URL
efímera/mal escrita. En el celular "localhost" es el celular mismo — no hay
backend ahí. Pasó varias veces incluso con las variables de EAS ya
"arregladas" porque `eas update` **no** usa las variables alojadas en EAS a
menos que se le pase `--environment <nombre>` explícitamente — sin ese flag,
cae de nuevo al `.env` local.

Esto ya no depende de acordarse de ningún flag — hay 4 capas independientes,
de la más a la menos importante:

1. **`.env.production`** (raíz del repo, SÍ versionado a propósito — ver
   `.gitignore`, tiene una excepción explícita para este archivo). Expo
   (`@expo/env`) lo carga automáticamente con prioridad sobre `.env` en
   *cualquier* build/export que corra con `NODE_ENV=production` — que es el
   default tanto para `eas build --profile preview|production` como para
   `eas update` sin flags. Esta es la fuente de verdad real de la URL del
   backend en producción; para cambiarla, editar este archivo y commitear.
2. **Variables de entorno alojadas en EAS** (`environment: preview` /
   `production` en `eas.json`) — se usan solo si a `eas update`/`eas build`
   se les pasa `--environment preview|production`. Redundante con el punto 1
   pero no está de más tenerlas bien:
   ```bash
   eas env:set --environment preview    --name EXPO_PUBLIC_API_URL --value <URL-real-del-backend> --visibility plaintext
   eas env:set --environment production --name EXPO_PUBLIC_API_URL --value <URL-real-del-backend> --visibility plaintext
   ```
3. **`app.config.js`** — corta el build/export (lanza una excepción) si
   `EXPO_PUBLIC_API_URL` sigue siendo localhost/vacía en un contexto de
   build real (perfiles `preview`/`production` o `NODE_ENV=production`). El
   perfil `development` (dev client) queda explícitamente afuera — ahí
   localhost es intencional.
4. **`src/utils/apiUrlGuard.ts` + pantalla de error en `app/_layout.tsx`** —
   si por lo que sea igual se coló un build/OTA roto, la app muestra un
   error rojo explícito en vez de quedarse "sin datos" en silencio.

**Para cambiar la URL del backend de producción:** editar `.env.production`
(punto 1) y correr `eas update`/`eas build` de nuevo — con eso alcanza, las
capas 2-4 son red de seguridad, no la fuente de verdad.
