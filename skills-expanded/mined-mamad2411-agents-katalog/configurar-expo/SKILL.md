---
name: configurar-expo
description: "Inicializa um projeto React Native com Expo e toda a stack padrão — Expo Router, NativeWind, TanStack Query, Zustand, Jest e React Native Testing Library. Use quando o dev-mobile vai criar ou padronizar um app mobile."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: configurar-expo

Inicializa um projeto **React Native + Expo** com toda a stack padrão: Expo Router, NativeWind, TanStack Query, Zustand, expo-secure-store, Jest e React Native Testing Library.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §2`, `mobile.md §3`, `mobile.md §7`, `mobile.md §9`, `seguranca.md`  
**Referências rápidas:** `Guidelines/mobile/README.md`, `Guidelines/mobile/expo-config.md`

---

## Quando usar

- Para inicializar um novo projeto mobile do zero
- Para adicionar a stack padrão em um projeto Expo existente que está incompleto
- Para padronizar a configuração de um projeto legado

---

## Pré-requisitos

Antes de executar, confirmar com o usuário:
- Nome do app (exibido nas stores)
- Slug do app (identificador único no Expo, sem espaços)
- Bundle Identifier iOS (ex: `com.empresa.meuapp`)
- Package Android (ex: `com.empresa.meuapp`)
- URL do BFF (ou placeholder para preencher depois)
- EAS Project ID (opcional — pode ser gerado depois com `eas init`)

---

## Processo de execução

### Passo 1 — Criar projeto base

```bash
# Criar com template Expo Router (TypeScript)
npx create-expo-app@latest <nome-do-app> --template blank-typescript

cd <nome-do-app>
```

### Passo 2 — Instalar dependências da stack

```bash
# Expo Router (já incluso no template, confirmar versão)
npx expo install expo-router expo-constants expo-linking expo-status-bar

# Estilos — NativeWind v4
npm install nativewind
npx expo install tailwindcss

# Estado — TanStack Query + Zustand
npm install @tanstack/react-query zustand

# Storage seguro
npx expo install expo-secure-store
npm install @react-native-async-storage/async-storage

# Listas performáticas
npm install @shopify/flash-list

# Gestos e área segura (dependências do Expo Router)
npx expo install react-native-gesture-handler react-native-safe-area-context react-native-screens

# Testes
npm install --save-dev jest jest-expo @testing-library/react-native @testing-library/jest-native

# Axios para HTTP
npm install axios
```

### Passo 3 — Configurar app.config.ts

Substituir `app.json` por `app.config.ts` dinâmico:

```typescript
// app.config.ts
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: process.env.APP_ENV === 'production' ? '<Nome do App>' : '<Nome do App> (Dev)',
  slug: '<slug-do-app>',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  userInterfaceStyle: 'automatic',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#ffffff',
  },
  ios: {
    supportsTablet: false,
    bundleIdentifier: '<bundle.identifier.ios>',
    buildNumber: process.env.BUILD_NUMBER ?? '1',
    config: { usesNonExemptEncryption: false },
  },
  android: {
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#ffffff',
    },
    package: '<com.empresa.app>',
    versionCode: Number(process.env.VERSION_CODE ?? 1),
    permissions: [],
  },
  plugins: ['expo-router', 'expo-secure-store'],
  extra: {
    bffUrl: process.env.BFF_URL ?? 'http://localhost:3000',
    environment: process.env.APP_ENV ?? 'development',
    eas: { projectId: process.env.EAS_PROJECT_ID },
  },
  experiments: { typedRoutes: true },
});
```

### Passo 4 — Configurar NativeWind

```javascript
// babel.config.js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      ['babel-preset-expo', { jsxImportSource: 'nativewind' }],
    ],
    plugins: ['nativewind/babel'],
  };
};
```

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx,ts,tsx}', './src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

```typescript
// global.d.ts
/// <reference types="nativewind/types" />
```

### Passo 5 — Configurar Jest

```json
// package.json — adicionar/atualizar seção jest
{
  "jest": {
    "preset": "jest-expo",
    "setupFilesAfterFramework": ["@testing-library/jest-native/extend-expect"],
    "transformIgnorePatterns": [
      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|@shopify/flash-list|nativewind)"
    ],
    "moduleNameMapper": {
      "^@/(.*)$": "<rootDir>/src/$1"
    },
    "collectCoverageFrom": [
      "src/**/*.{ts,tsx}",
      "app/**/*.{ts,tsx}",
      "!**/*.d.ts",
      "!**/index.ts"
    ]
  }
}
```

### Passo 6 — Configurar alias de paths

```json
// tsconfig.json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

### Passo 7 — Criar estrutura de diretórios

```
src/
├── components/
├── hooks/
├── stores/
├── services/
│   ├── api.ts          ← cliente Axios com interceptor de auth
│   └── queryClient.ts  ← instância do QueryClient
├── types/
│   └── api.ts          ← tipos derivados dos contratos do BFF
└── utils/
```

### Passo 8 — Criar serviços base

```typescript
// src/services/api.ts
import axios from 'axios';
import Constants from 'expo-constants';
import * as SecureStore from 'expo-secure-store';

const api = axios.create({
  baseURL: Constants.expoConfig?.extra?.bffUrl as string,
  timeout: 10_000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Não logar dados da resposta (pode conter PII) — apenas status e URL
    console.error(`[API Error] ${error.response?.status} ${error.config?.url}`);
    return Promise.reject(error);
  }
);

export default api;
```

```typescript
// src/services/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      gcTime: 1000 * 60 * 10,
      retry: 2,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: { retry: 0 },
  },
});
```

### Passo 9 — Criar arquivos de ambiente

```bash
# .env (nunca commitar — adicionar ao .gitignore)
APP_ENV=development
BFF_URL=http://localhost:3000

# .env.staging
APP_ENV=staging
BFF_URL=https://bff-staging.meudominio.com

# .env.production
APP_ENV=production
BFF_URL=https://bff.meudominio.com
```

Adicionar ao `.gitignore`:
```
.env
.env.staging
.env.production
*.keystore
google-play-key.json
```

### Passo 10 — Criar RootLayout inicial

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { queryClient } from '@/services/queryClient';

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <QueryClientProvider client={queryClient}>
          <Stack screenOptions={{ headerShown: false }} />
        </QueryClientProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
```

### Passo 11 — Verificar instalação

```bash
# Iniciar em modo de desenvolvimento
npx expo start

# Rodar testes
npx jest

# Verificar tipos
npx tsc --noEmit
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Posso usar `app.json` estático, é mais simples" | `app.config.ts` é necessário para variáveis de ambiente e configuração dinâmica por ambiente — sem ele o BFF URL fica hardcoded |
| "NativeWind é pesado, vou usar StyleSheet mesmo" | StyleSheet é válido — mas a decisão deve ser tomada agora e padronizada; não misturar os dois no mesmo projeto |
| "Posso instalar o React Navigation manualmente" | Em projetos novos com Expo Router, React Navigation é configurado automaticamente — instalação manual causa conflito de providers |
| "Vou pular a configuração do alias `@/`" | O alias é necessário para que as skills de componente e hook funcionem com imports consistentes |

---

## Checklist de conclusão

- [ ] `app.config.ts` criado com `name`, `slug`, `bundleIdentifier` e `package` corretos
- [ ] NativeWind configurado em `babel.config.js` e `tailwind.config.js`
- [ ] TanStack Query configurado com `QueryClient` e `QueryClientProvider` no `_layout.tsx`
- [ ] Zustand instalado
- [ ] `expo-secure-store` instalado e listado em `plugins`
- [ ] Jest configurado com `jest-expo` e `@testing-library/react-native`
- [ ] Alias `@/` configurado em `tsconfig.json`
- [ ] `src/services/api.ts` com interceptor de auth via `SecureStore`
- [ ] `src/services/queryClient.ts` com configurações padrão
- [ ] Arquivos `.env` criados e adicionados ao `.gitignore`
- [ ] `npx expo start` sobe sem erros
- [ ] `npx jest` roda sem erros
- [ ] `npx tsc --noEmit` passa sem erros
