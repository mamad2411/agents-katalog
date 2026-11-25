---
name: mobile-state-data
description: "Estado y datos en apps Expo: TanStack Query, Zustand, almacenamiento (expo-secure-store para tokens, AsyncStorage/MMKV), offline, variables EXPO_PUBLIC_ y consumo de APIs NestJS/FastAPI. Usar al traer datos, manejar estado global, sesión, caché o persistencia."
---

# mobile-state-data

## Objetivo
Separar claramente **estado de servidor** (TanStack Query), **estado de cliente** (Zustand / estado local) y **persistencia** (SecureStore, AsyncStorage/MMKV), con un cliente HTTP tipado y un comportamiento correcto sin red.

## Cuándo aplicarla
- Consumir un endpoint (listar, detalle, crear, actualizar).
- Guardar tokens, preferencias o caché local.
- Añadir estado global (sesión, carrito, filtros).
- Soportar offline, reintentos o refresco al volver a la app.
- Configurar URLs de API y variables por entorno.

Complementos: `mobile:expo-router-navigation` (guards de auth), `mobile:mobile-testing` (mocks de red y stores). Si está instalado, `expo:expo-data-fetching`.

## Paso 0: detectar
1. `package.json`: ¿`@tanstack/react-query`, `zustand`, `jotai`, `redux`, `swr`, `axios`, `ky`, `zod`, `react-native-mmkv`, `@react-native-async-storage/async-storage`, `expo-sqlite`? **Usa lo que ya hay**; no introduzcas otra librería para lo mismo.
2. ¿Existe ya un cliente HTTP (`lib/api.ts`, `services/http.ts`)? Extiéndelo.
3. ¿Tipos generados del backend (OpenAPI de NestJS `@nestjs/swagger` o de FastAPI `/openapi.json`)? Prefiere generarlos a escribirlos a mano.
4. `.env*`, `app.config.ts` (`extra`) y `eas.json` (`env`/`environment`) para URLs por entorno.

## Qué va dónde
| Dato | Dónde | Por qué |
|---|---|---|
| Respuestas del API (listas, detalle) | TanStack Query | Caché, dedupe, reintentos, invalidación |
| Sesión en memoria (usuario, rol) | Zustand o contexto | Leído en muchas pantallas |
| Token de acceso / refresh | `expo-secure-store` | Cifrado por Keychain/Keystore |
| Preferencias (tema, idioma, onboarding visto) | MMKV o AsyncStorage (vía `persist` de Zustand) | No sensible, persistente |
| Estado de formulario | Local (`useState` / `react-hook-form`) | No es global |
| Filtros de una pantalla | Params de ruta o estado local | Enlazable y efímero |
| Datos offline estructurados | `expo-sqlite` (u ORM como Drizzle) | Consultas y volumen |

Regla: **nunca copies datos de TanStack Query a Zustand**. Si varias pantallas necesitan el mismo dato de servidor, usan el mismo `queryKey`.

## Estructura
```
src/
  lib/
    env.ts              # lectura y validación de EXPO_PUBLIC_*
    api/
      client.ts         # fetch tipado, auth header, errores
      errors.ts         # ApiError
    query-client.ts     # QueryClient + focus/online managers
    storage.ts          # wrappers de SecureStore / MMKV
  features/orders/api/
    orders.api.ts       # funciones HTTP (getOrders, createOrder)
    orders.queries.ts   # queryOptions, useOrders, useCreateOrder
    orders.schemas.ts   # Zod schemas + tipos inferidos
  stores/
    auth.store.ts       # Zustand
```

## Variables de entorno
```ts
// src/lib/env.ts
import { z } from 'zod';

const schema = z.object({
  EXPO_PUBLIC_API_URL: z.string().url(),
  EXPO_PUBLIC_SENTRY_DSN: z.string().optional(),
});

export const env = schema.parse({
  EXPO_PUBLIC_API_URL: process.env.EXPO_PUBLIC_API_URL,
  EXPO_PUBLIC_SENTRY_DSN: process.env.EXPO_PUBLIC_SENTRY_DSN,
});
```
- Solo se inlinean las variables con prefijo `EXPO_PUBLIC_` y con acceso estático `process.env.EXPO_PUBLIC_X` (no `process.env[key]` ni destructuring).
- **Son públicas**: quedan en texto plano en el bundle. Nunca API keys privadas, secretos de backend ni credenciales. Si necesitas un secreto, el backend hace la llamada.
- Local: `.env` / `.env.local` (añade `.env*.local` a `.gitignore`). En EAS: variables de entorno por `environment` (`development`, `preview`, `production`) y `eas env:pull` para traerlas a local.
- Cambiar una `EXPO_PUBLIC_` requiere nuevo bundle (reinicia Metro con `-c`; en producción, nuevo build o update).
- En el emulador Android, `localhost` es el emulador: usa `10.0.2.2` o la IP LAN de tu máquina; en dispositivo físico, la IP LAN.

## Cliente HTTP y TanStack Query
Lee `references/api-client.md` para el cliente completo (auth header, refresh de token, errores de NestJS/FastAPI, validación con Zod, paginación e infinite queries).

Setup mínimo en React Native:
```ts
// src/lib/query-client.ts
import { QueryClient, focusManager, onlineManager } from '@tanstack/react-query';
import { AppState, Platform } from 'react-native';
import NetInfo from '@react-native-community/netinfo';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, retry: 2 },
    mutations: { retry: 0 },
  },
});

// Refetch al volver a primer plano (no hay "window focus" en RN)
AppState.addEventListener('change', (status) => {
  if (Platform.OS !== 'web') focusManager.setFocused(status === 'active');
});

// Pausa queries/mutations sin red y reanuda al reconectar
onlineManager.setEventListener((setOnline) =>
  NetInfo.addEventListener((state) => setOnline(!!state.isConnected)),
);
```
Queries y mutations por feature:
```ts
// src/features/orders/api/orders.queries.ts
import { queryOptions, useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

export const orderKeys = {
  all: ['orders'] as const,
  list: (filters: OrderFilters) => [...orderKeys.all, 'list', filters] as const,
  detail: (id: string) => [...orderKeys.all, 'detail', id] as const,
};

export const orderDetailQuery = (id: string) =>
  queryOptions({ queryKey: orderKeys.detail(id), queryFn: () => getOrder(id), enabled: !!id });

export const useOrder = (id: string) => useQuery(orderDetailQuery(id));

export function useCreateOrder() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createOrder,
    onSuccess: () => qc.invalidateQueries({ queryKey: orderKeys.all }),
  });
}
```
- Query keys con factory por feature; nada de strings sueltos repetidos.
- Refetch al enfocar pantalla si hace falta: `useFocusEffect` + `refetch()` (o `refetchOnMount`), no `setInterval`.
- Pull-to-refresh: `refreshing={isRefetching}` y `onRefresh={refetch}`.
- Estados en UI: `isPending` (primera carga), `isError` + `error`, `data` vacío, `isRefetching`. Toda pantalla maneja los cuatro.
- Updates optimistas solo cuando la UX lo pide; con rollback en `onError`.

## Zustand
```ts
// src/stores/preferences.store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

type PreferencesState = {
  theme: 'system' | 'light' | 'dark';
  hasSeenOnboarding: boolean;
  setTheme: (theme: PreferencesState['theme']) => void;
  completeOnboarding: () => void;
};

export const usePreferences = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'system',
      hasSeenOnboarding: false,
      setTheme: (theme) => set({ theme }),
      completeOnboarding: () => set({ hasSeenOnboarding: true }),
    }),
    { name: 'preferences', storage: createJSONStorage(() => AsyncStorage), version: 1 },
  ),
);
```
- Consume con selectores: `usePreferences((s) => s.theme)`. Para varios campos, `useShallow` de `zustand/react/shallow`.
- Acciones dentro del store; nada de `setState` desde componentes arbitrarios.
- `persist` con `version` y `migrate` cuando cambie la forma del estado.
- Tokens **no** van en `persist` con AsyncStorage/MMKV sin cifrar.

## Almacenamiento
- **Tokens**: `expo-secure-store` (`setItemAsync`, `getItemAsync`, `deleteItemAsync`). Valores pequeños (algunos iOS rechazan ~2 KB); en iOS persiste tras desinstalar (limpia en primer arranque si es un requisito). No disponible en web: usa otra estrategia en web.
- **Clave-valor rápido**: `react-native-mmkv` (v4 usa `createMMKV()` y Nitro Modules; requiere dev build). Síncrono, ideal para `persist` de Zustand con un adaptador `getItem/setItem/removeItem`.
- **AsyncStorage**: funciona en Expo Go; asíncrono; suficiente para preferencias.
- **Alternativa Expo**: `expo-sqlite/kv-store` ofrece una API compatible con AsyncStorage sobre SQLite.
- **Datos estructurados offline**: `expo-sqlite`.
- Envuelve el almacenamiento en `lib/storage.ts` para poder cambiar la implementación y mockearla en tests.

## Offline
- Mínimo: `onlineManager` + banner "Sin conexión" + no disparar mutaciones que fallarán.
- Caché persistente de queries: `PersistQueryClientProvider` (`@tanstack/react-query-persist-client`) con `@tanstack/query-async-storage-persister`; define `gcTime` alto y `buster` con la versión de la app.
- Mutaciones offline: `networkMode` por defecto (`online`) las pausa sin red y las reanuda; si deben sobrevivir a un cierre de app, persístelas y registra `setMutationDefaults` para poder reanudarlas.
- Sincronización compleja (edición offline con conflictos): diseña con backend (timestamps/versiones) antes de codificar.

## Antipatrones
- `useEffect` + `fetch` + `useState` para datos de servidor cuando el proyecto ya tiene TanStack Query.
- Guardar tokens en AsyncStorage/MMKV sin cifrar o en Zustand persistido.
- Secretos en `EXPO_PUBLIC_*` o en `app.config.ts` `extra`.
- Leer todo el store: `const store = useStore()` (re-render en cada cambio).
- Duplicar datos del servidor en estado global.
- `queryKey` que no incluye todas las variables que usa `queryFn`.
- Ignorar errores de validación de respuesta (usa Zod en los bordes).

## Checklist final
- [ ] Datos de servidor en TanStack Query con key factory; estado cliente en Zustand/local.
- [ ] Tokens solo en SecureStore; nada sensible en `EXPO_PUBLIC_`.
- [ ] Respuestas validadas/tipadas; errores del backend mapeados a `ApiError`.
- [ ] Pantallas con estados de carga, error (con reintento), vacío y datos.
- [ ] Comportamiento sin red probado (modo avión).
- [ ] Refetch al volver a primer plano configurado.
- [ ] Mocks de red/stores en tests (`mobile:mobile-testing`).
