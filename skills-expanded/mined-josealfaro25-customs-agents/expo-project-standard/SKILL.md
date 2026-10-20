---
name: expo-project-standard
description: "Estándar para crear apps móviles nuevas con React Native + Expo (SDK 56), Expo Router, NativeWind v5, Zustand, TanStack Query, react-hook-form + zod, deep linking y EAS. Usar al crear un proyecto Expo desde cero, al decidir dónde va un archivo o al revisar que un proyecto cumple el estándar antes de entregar."
---

# expo-project-standard

Guía para crear apps móviles nuevas con React Native + Expo. Es la contraparte móvil de `frontend:nextjs-project-standard`: mismo stack de estado, formularios y validación, y misma estructura por vertical slices.

> **Proyectos existentes**: si el proyecto ya tiene convenciones (`CLAUDE.md`, estructura, librerías), **síguelas**. Este estándar aplica a proyectos nuevos y a lo que no esté definido. Verifica siempre la versión de `expo` en `package.json` (= SDK) y consulta la documentación de ese SDK antes de afirmar compatibilidades.

---

## 📁 1. Project Setup

### Tecnologías base

- **Expo SDK 56** (React Native 0.85, React 19.2), New Architecture por defecto
- **TypeScript** con `strict: true`
- **Expo Router** para navegación file-based
- **NativeWind v5 + Tailwind v4** para estilos (sin CSS-in-JS ad-hoc)
- **Zustand** (estado) + **TanStack Query** (datos remotos)
- **react-hook-form + zod** para formularios y validación
- **ESLint + Prettier** para formato

### Creación del proyecto

```bash
# Crea el proyecto con la plantilla de TypeScript + Expo Router
npx create-expo-app@latest my-app

# Regla de oro: instalar dependencias con expo install para asegurar
# compatibilidad con el SDK (no usar npm/pnpm install directo para libs nativas)
cd my-app
npx expo install nativewind tailwindcss@^4 zustand @tanstack/react-query
npx expo install react-hook-form @hookform/resolvers zod expo-secure-store expo-linking expo-image
npx expo install @shopify/flash-list react-native-reanimated react-native-worklets
```

Sigue la guía de instalación de NativeWind v5 para el SDK instalado (dependencias peer, `postcss.config.mjs` y `metro.config.js`); cambia entre versiones mayores.

### Archivos de configuración mínimos

```
app.config.ts        # Configuración de la app (scheme, plugins, deep linking)
tsconfig.json        # strict: true, alias @/*
metro.config.js      # withNativewind aplicado
eslint.config.js     # config de Expo
.prettierrc          # formato consistente con el repo
global.css           # capa base de Tailwind para NativeWind
eas.json             # perfiles development / preview / production
```

---

## 🗂️ 2. Folder Structure

Estructura por **vertical slices** (si el proyecto tiene un ADR de arquitectura, ese manda): la navegación vive en `app/` (Expo Router) y cada dominio agrupa todo lo suyo en `features/<dominio>/`. Las pantallas son delgadas: componen piezas de las features.

```
my-app/
├── app/                          # Expo Router (rutas = archivos)
│   ├── _layout.tsx               # Layout raíz (providers globales)
│   ├── index.tsx                 # Ruta inicial
│   ├── (tabs)/                   # Grupo de tabs
│   │   ├── _layout.tsx           # Configuración de tabs
│   │   └── home.tsx
│   └── +not-found.tsx            # Ruta 404 / fallback
├── features/                     # Vertical slices por dominio
│   └── auth/                     # Ejemplo: dominio de autenticación
│       ├── components/           # UI propia del dominio
│       ├── hooks/                # Lógica (useLogin, etc.)
│       ├── store.ts              # Estado Zustand del dominio
│       ├── api.ts                # Llamadas a datos (TanStack Query)
│       ├── schema.ts             # Esquemas zod
│       └── types.ts              # Tipos del dominio
├── components/                   # UI compartida y reutilizable
│   └── Button/
│       ├── Button.tsx
│       └── index.ts
├── lib/                          # Configuración y clientes (query client, cn, etc.)
├── hooks/                        # Hooks globales
├── stores/                       # Stores Zustand globales
├── types/                        # Tipos compartidos
├── assets/                       # Imágenes, fuentes, íconos
├── global.css                    # Capa base de Tailwind
└── app.config.ts                 # Config de Expo
```

Reglas:

- Una feature **no importa** internals de otra feature; si algo se comparte, sube a `components/`, `lib/` o `types/`.
- `app/` no contiene lógica de negocio: solo rutas, layouts y composición.

---

## 📝 3. Naming Conventions

### Carpetas y archivos

- **Componentes**: PascalCase → `Button`, `UserCard`
- **Hooks**: camelCase con prefijo `use` → `useLogin.ts`
- **Rutas (Expo Router)**: siempre lowercase → `home.tsx`, `_layout.tsx`, `[id].tsx`
- **Features**: lowercase por dominio → `features/auth/`
- **Tipos/Interfaces**: en `types/` o colocados por feature

```
✅ Correcto:
- components/UserCard/UserCard.tsx
- features/auth/hooks/useLogin.ts
- app/(tabs)/home.tsx

❌ Incorrecto:
- components/user-card/user-card.tsx
- features/Auth/hooks/Login.ts
- app/(tabs)/Home.tsx
```

---

## 🧩 4. Component Rules

### Estructura

- **UI con clases de NativeWind** (prop `className`), no `StyleSheet` disperso
- **Separar lógica de UI**: un hook (`useX`) por componente cuando haya lógica
- Mantener componentes pequeños (<150 líneas)
- Preferir **composición** sobre herencia
- Tipar siempre las props con `interface` o `type`

### Patrón recomendado

```tsx
// UserCard.tsx
import { View, Text } from 'react-native';
import { useUserCard } from './useUserCard';

interface UserCardProps {
  userId: string;
  onPress?: () => void;
}

export function UserCard({ userId, onPress }: UserCardProps) {
  const { user, isLoading } = useUserCard({ userId });

  if (isLoading) return null;

  return (
    <View className="p-4 bg-white rounded-lg shadow">
      <Text className="text-lg font-semibold">{user.name}</Text>
    </View>
  );
}
```

---

## 🧭 5. Navigation & Deep Linking (Expo Router)

### Navegación

- **Expo Router** (file-based) como sistema único; rutas = archivos en `app/`
- Layouts con `_layout.tsx`, grupos con `(group)/`, rutas dinámicas con `[id].tsx`
- Habilitar **typed routes** y navegar con `<Link>` o `router.push()`
- En SDK 56+, importar siempre desde `expo-router` (no desde `@react-navigation/*`)

### Deep linking (requisito de primera clase)

Toda pantalla a la que se pueda llegar desde fuera de la app (web, email, push, redes) debe tener deep link:

- Definir `scheme` en `app.config.ts` y configurar **Universal Links (iOS)** con `apple-app-site-association` y **App Links (Android)** con `assetlinks.json` (los sirve el web; ver `frontend:nextjs-project-standard`, sección 5)
- Mapear rutas de entrada desde web a pantallas de la app, con la **misma ruta** en ambos lados (`/profile/123`)
- Si hay web, implementar **smart app banner** y un camino claro a la instalación
- (Opcional) evaluar **App Clips (iOS)** / **Instant Apps (Android)** para reducir fricción de entrada

Detalle de configuración y auth en `mobile:expo-router-navigation`.

```tsx
import { Link, router } from 'expo-router';

<Link href="/profile/123">Ver perfil</Link>;
// o imperativo
router.push({ pathname: '/profile/[id]', params: { id: '123' } });
```

---

## 📊 6. State & Data Management

### Estrategia

- **Estado global de UI/cliente**: Zustand (consistente con el web)
- **Datos remotos**: TanStack Query para caché, revalidación y estados de red
- **Estado local**: `useState` / `useContext` cuando sea suficiente
- **Evitar**: Redux y librerías de estado complejas como default; duplicar en Zustand datos que ya cachea TanStack Query

### Ejemplo con TanStack Query

```tsx
// features/users/api.ts
import { useQuery } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/users`);
      if (!res.ok) throw new Error('Error de red');
      return res.json();
    },
  });
}
```

Cliente HTTP, refresco de tokens y estado offline en `mobile:mobile-state-data`.

---

## 📋 7. Forms & Validation

- **react-hook-form** para manejo de formularios
- **zod** para esquemas de validación (mismo patrón que el web; los esquemas pueden compartirse en un paquete si hay monorepo)
- Validación en cliente para feedback inmediato; el backend valida de nuevo

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});
type LoginInput = z.infer<typeof schema>;

export function useLoginForm() {
  return useForm<LoginInput>({ resolver: zodResolver(schema) });
}
```

---

## 🎨 8. Styling (NativeWind)

- Usar **clases utilitarias** vía `className` directamente en los componentes
- Reutilizar los **tokens del design system** del proyecto configurados en Tailwind (si hay web, mismos nombres en ambos)
- Combinar clases dinámicas con `cn()` (clsx + tailwind-merge)
- **No** mezclar `StyleSheet` y NativeWind para lo mismo; estilos dinámicos puntuales (p. ej. valores animados) solo cuando sea imprescindible

```tsx
import { Pressable, Text } from 'react-native';
import { cn } from '@/lib/cn';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onPress?: () => void;
}

export function Button({ variant = 'primary', children, onPress }: ButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      className={cn('px-4 py-2 rounded-lg', variant === 'primary' ? 'bg-primary' : 'bg-gray-200')}
    >
      <Text className={cn('font-medium', variant === 'primary' ? 'text-white' : 'text-gray-900')}>{children}</Text>
    </Pressable>
  );
}
```

---

## ⚠️ 9. Error Handling

- Usar **error boundaries** de Expo Router (`ErrorBoundary` exportado desde un layout o pantalla)
- Envolver llamadas async en `try...catch` y manejar el estado de error de TanStack Query
- Mostrar mensajes amigables al usuario (no errores crudos)
- **Sin `console.error` residual** en el proyecto final

```tsx
// app/_layout.tsx
import { Pressable, Text, View } from 'react-native';
import type { ErrorBoundaryProps } from 'expo-router';

export function ErrorBoundary({ retry }: ErrorBoundaryProps) {
  return (
    <View className="flex-1 items-center justify-center">
      <Text className="text-lg font-bold text-red-600">Algo salió mal</Text>
      <Pressable onPress={retry} className="mt-4 px-4 py-2 bg-primary rounded">
        <Text className="text-white">Reintentar</Text>
      </Pressable>
    </View>
  );
}
```

---

## ⚡ 10. Performance Rules

- Usar **FlashList** (o `FlatList`) para listas largas; nunca `.map()` dentro de un `ScrollView` con datos ilimitados
- Aprovechar **React Compiler** (estable en SDK 54+); evitar memoización manual innecesaria
- Animaciones con **Reanimated** (requiere `react-native-worklets` en SDK 54+)
- Cargar pantallas/recursos pesados de forma diferida
- Optimizar imágenes con `expo-image`
- **Limpiar** timers/listeners en `useEffect`

```tsx
import { FlashList } from '@shopify/flash-list';

// FlashList v2 (New Architecture) ya no usa estimatedItemSize; en v1 es obligatorio
<FlashList
  data={users}
  renderItem={({ item }) => <UserCard userId={item.id} />}
  keyExtractor={(item) => item.id}
/>;
```

Más reglas de rendimiento y animación en `mobile:react-native-components`.

---

## 🔒 11. Security Rules

- **Secretos y tokens** en `expo-secure-store` (Keychain/Keystore); **nunca** en AsyncStorage
- Variables de entorno: solo `EXPO_PUBLIC_*` para valores seguros de exponer (quedan embebidos en el bundle)
- Todas las llamadas de red vía **HTTPS**
- **Validar siempre** la entrada con `zod`
- No registrar datos sensibles en logs

```bash
# ✅ Seguro de exponer
EXPO_PUBLIC_API_URL=https://api.example.com

# ❌ Nunca exponer (va en secure-store o backend)
API_SECRET=...
```

---

## 🧱 12. Native Modules & Config Plugins

- Preferir paquetes del ecosistema Expo y **config plugins** sobre código nativo a mano
- Para funcionalidad nativa propia, usar la **Expo Modules API** (Swift/Kotlin/TS)
- **No hacer `eject`** ni mantener `ios/`/`android/` manualmente sin justificación documentada
- La configuración nativa se genera vía CNG a partir de `app.config.ts` + plugins
- Todo cambio nativo (dependencia nativa, plugin, permisos) requiere **nuevo build**; no llega por EAS Update

---

## 🧪 13. Testing Rules

- **Unit**: Jest (`jest-expo`) + React Native Testing Library
- **E2E**: Maestro (recomendado) o Detox
- **QA de deep links** en los navegadores y WebViews in-app desde los que llega el tráfico: los in-app browsers pueden interceptar enlaces, así que el flujo web → app debe probarse ahí

Detalle de configuración y mocks nativos en `mobile:mobile-testing`.

```tsx
// UserCard.test.tsx
import { render, screen } from '@testing-library/react-native';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  it('renderiza el nombre', () => {
    render(<UserCard userId="1" />);
    expect(screen.getByText('Ada')).toBeTruthy();
  });
});
```

---

## 📈 14. Observability & Analytics

- Capturar **SO, versión y modelo de dispositivo** de forma fiable (lo que el User-Agent web no da)
- Registrar **atribución de origen** (web, campaña, push → app) para medir la adquisición
- **Crash reporting** con Sentry o EAS Observe (incluir source maps)
- Definir eventos de producto clave; evitar registrar datos sensibles

---

## ♿ 15. Accessibility Rules

- Usar `accessibilityRole`, `accessibilityLabel` y `accessibilityHint` en componentes interactivos
- Garantizar contraste de color accesible (tokens del design system)
- Tamaños táctiles adecuados (mín. 44x44 pt)
- Soportar lectores de pantalla (VoiceOver / TalkBack)

```tsx
<Pressable accessibilityRole="button" accessibilityLabel="Cerrar" onPress={onClose}>
  <Icon name="close" />
</Pressable>
```

---

## 🎨 16. Code Style Rules

- **TypeScript estricto** y componentes funcionales (sin clases)
- Tipar props con `interface` o `type`
- Imports absolutos con alias `@/*`
- Orden de imports: librerías externas → módulos internos (`@/`) → relativos
- Archivos terminan con newline

```tsx
// 1. Externas
import { View, Text } from 'react-native';
import { useQuery } from '@tanstack/react-query';

// 2. Internas
import { Button } from '@/components/Button';
import { useAuth } from '@/features/auth/hooks/useAuth';

// 3. Relativas
import { helper } from '../utils/helper';
```

---

## 🚀 17. Build & Deployment (EAS)

- Build con **EAS Build** y perfiles `development`, `preview`, `production`
- Publicación en tiendas con **EAS Submit**
- Updates OTA con **EAS Update** (canales por perfil, `runtimeVersion` con política)
- `eas build`, `eas submit` y `eas update` **solo con confirmación explícita** (coste y usuarios reales); ver `mobile:expo-developer`
- El detalle de integración DevOps (canales, invalidaciones, secretos de CI) queda **por documentar**

```bash
eas build --profile preview --platform all
eas submit --platform ios
eas update --branch production --message "fix: ..."
```

---

## 📋 18. Final Checklist

Antes de entregar / publicar:

- [ ] Estructura por vertical slices (`app/` + `features/`) respetada
- [ ] Todos los componentes en TypeScript estricto, sin errores (`tsc --noEmit`)
- [ ] Estilos solo con NativeWind (tokens del design system)
- [ ] Navegación con Expo Router y rutas tipadas
- [ ] Deep linking configurado (Universal Links + App Links) y probado en los WebViews in-app relevantes
- [ ] Estado con Zustand y datos con TanStack Query
- [ ] Manejo de errores y sin `console.error` residual
- [ ] Secretos en `expo-secure-store`
- [ ] Accesibilidad básica implementada
- [ ] Tests pasan (`jest`) y lint limpio (`eslint`)
- [ ] `npx expo-doctor` sin errores
- [ ] Build de EAS válido para iOS y Android
