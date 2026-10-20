---
name: build-publicacao
description: "Gera builds iOS e Android via EAS Build, publica nas stores via EAS Submit e configura OTA updates. Use quando o dev-mobile ou o dev-devops vai distribuir uma versão do app."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: build-publicacao

Gera builds iOS e Android via **EAS Build** e publica nas stores via **EAS Submit**. Cobre configuração de certificados, keystores, OTA updates e automação via GitHub Actions.

**Agente:** `dev-mobile`, `dev-devops`  
**Guardrails aplicáveis:** `mobile.md`, `seguranca.md`, `operacional.md`  
**Referências rápidas:** `Guidelines/mobile/eas-build.md`

---

## Quando usar

- Para gerar o primeiro build do projeto (configuração inicial de EAS)
- Para publicar uma nova versão nas stores (App Store e Google Play)
- Para gerar build de preview para distribuição interna (TestFlight / Firebase App Distribution)
- Para publicar OTA update sem passar pelas stores
- Para configurar automação de build em GitHub Actions

---

## Pré-requisitos

Confirmar antes de iniciar:

- [ ] `eas.json` configurado com perfis `development`, `preview` e `production`
- [ ] `app.config.ts` com `bundleIdentifier` (iOS) e `package` (Android) corretos
- [ ] Conta Expo autenticada (`eas login`)
- [ ] Para iOS: conta Apple Developer ativa com permissões de build
- [ ] Para Android: conta Google Play Console ativa
- [ ] Todos os testes passando (`npx jest`)
- [ ] `npx tsc --noEmit` sem erros
- [ ] `revisar-seguranca-mobile` executado e aprovado

---

## Processo de execução

### Fase 1 — Configuração inicial (apenas na primeira vez)

#### 1.1 — Inicializar EAS no projeto

```bash
# Instalar CLI global
npm install -g eas-cli

# Autenticar
eas login

# Inicializar projeto (vincula ao Expo Application Services)
eas init

# Confirmar que o projectId foi adicionado ao app.config.ts
```

#### 1.2 — Criar eas.json

```json
{
  "cli": {
    "version": ">= 12.0.0",
    "requireCommit": true
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": { "APP_ENV": "development" }
    },
    "preview": {
      "distribution": "internal",
      "env": {
        "APP_ENV": "staging",
        "BFF_URL": "https://bff-staging.meudominio.com"
      }
    },
    "production": {
      "autoIncrement": true,
      "env": {
        "APP_ENV": "production",
        "BFF_URL": "https://bff.meudominio.com"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "dev@empresa.com",
        "ascAppId": "<id-do-app-no-app-store-connect>",
        "appleTeamId": "<TEAM-ID>"
      },
      "android": {
        "serviceAccountKeyPath": "./google-play-key.json",
        "track": "internal"
      }
    }
  }
}
```

#### 1.3 — Configurar credenciais

```bash
# iOS — EAS gerencia automaticamente (recomendado)
eas credentials --platform ios
# Selecionar: "Let EAS handle it"

# Android — EAS gera e armazena keystore
eas credentials --platform android
# Selecionar: "Generate new keystore"
# ⚠️ Fazer backup do keystore no painel EAS imediatamente
```

---

### Fase 2 — Build de preview (distribuição interna)

```bash
# Build para ambas as plataformas
eas build --profile preview --platform all

# Resultado:
# - iOS: link para download do .ipa via expo.dev
# - Android: link para download do .apk/.aab
```

**Distribuição do preview:**
- iOS: distribuição via TestFlight (recomendado) ou direta com UDID do dispositivo
- Android: distribuição via link direto ou Firebase App Distribution

**Verificar antes de prosseguir para produção:**
- [ ] Fluxo de autenticação funciona
- [ ] Todas as telas carregam sem crash
- [ ] Deep linking funciona (testar com URL real)
- [ ] Permissões solicitadas no momento correto
- [ ] Performance aceitável em dispositivo real (não apenas simulador)

---

### Fase 3 — Build de produção

#### 3.1 — Incrementar versão

Antes do build de produção, atualizar `version` e os números de build:

```typescript
// app.config.ts — com autoIncrement: true no eas.json, o buildNumber/versionCode
// são incrementados automaticamente pelo EAS. Só incrementar `version` manualmente.
version: '1.1.0',   // Semantic versioning — visível nas stores
```

#### 3.2 — Executar build de produção

```bash
# Ambas as plataformas em paralelo
eas build --profile production --platform all

# Monitorar progresso
eas build:list --limit 5
```

#### 3.3 — Verificar o build antes de submeter

```bash
# Ver detalhes do build
eas build:view <build-id>

# Instalar em dispositivo para smoke test final
# iOS: via TestFlight internal testing
# Android: baixar APK/AAB e instalar via adb
adb install <arquivo.apk>
```

---

### Fase 4 — Submissão nas stores

#### 4.1 — App Store (iOS)

```bash
# Submete o build mais recente de produção
eas submit --platform ios --latest

# Ou especificar build ID
eas submit --platform ios --id <build-id>
```

**Após a submissão no App Store Connect:**
1. Acessar App Store Connect → TestFlight → Adicionar notas de release
2. Submeter para revisão: App Store → versão → Submit for Review
3. Preencher export compliance (usesNonExemptEncryption)
4. Aguardar revisão (24-48h em média)

**Pré-requisitos no App Store Connect:**
- Screenshots obrigatórias: iPhone 6.7" (2796x1290) e iPhone 6.1" (2532x1170)
- Screenshots de iPad se `supportsTablet: true`
- Descrição, palavras-chave e notas de privacidade atualizadas
- Rating e classificação etária configurados

#### 4.2 — Google Play (Android)

```bash
# Submete o build mais recente de produção para a faixa "internal"
eas submit --platform android --latest
```

**Após a submissão no Google Play Console:**
1. Acessar Google Play Console → Testes internos → promover para Closed Testing (alpha)
2. Closed Testing → promover para Open Testing (beta) após validação
3. Beta → produção após aprovação

**Pré-requisitos no Google Play Console:**
- Screenshots: phone (1080x1920), tablet 7" e 10" (opcionais mas recomendados)
- Ícone de alta resolução: 512x512
- Feature graphic: 1024x500
- Política de privacidade URL configurada
- Service Account JSON com permissão de publicação

---

### Fase 5 — OTA Update (sem build nativo)

Usar apenas quando **não há mudança de código nativo**:

```bash
# Publicar update para o canal de produção
eas update --branch production --message "Corrige layout da tela de pedidos"

# Preview do que será publicado antes de confirmar
eas update --branch production --dry-run
```

**Quando OTA é suficiente:**
- Correções de bug em TypeScript/React Native
- Mudanças de UI sem novos módulos nativos
- Atualização de strings, textos, cores

**Quando OTA não é suficiente (requer novo build):**
- Adição de novo Config Plugin ou módulo nativo
- Mudança de versão nativa de biblioteca Expo
- Alteração em `app.config.ts` que afeta código nativo

---

### Fase 6 — Automação via GitHub Actions (opcional)

```yaml
# .github/workflows/eas-build-production.yml
name: EAS Build & Submit

on:
  push:
    tags:
      - 'v*'   # trigger em tags de versão: git tag v1.1.0

jobs:
  build-and-submit:
    name: Build e Submit
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Instalar dependências
        run: npm ci

      - name: Setup EAS
        uses: expo/expo-github-action@v8
        with:
          expo-version: latest
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}

      - name: Build produção
        run: eas build --profile production --platform all --non-interactive

      - name: Submit para stores
        run: eas submit --platform all --latest --non-interactive
        env:
          EXPO_APPLE_ID: ${{ secrets.APPLE_ID }}
          EXPO_APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
```

**Secrets necessários no GitHub:**
- `EXPO_TOKEN` — token de acesso do EAS (gerado em expo.dev/settings/access-tokens)
- `APPLE_ID` — Apple ID da conta de desenvolvedor
- `APPLE_APP_SPECIFIC_PASSWORD` — senha específica para apps (não a senha da conta)

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou fazer upload manual do .ipa no Xcode, é mais rápido" | Upload manual não é reproduzível e exige Xcode local — EAS garante builds consistentes e rastreáveis |
| "Posso pular o build de preview e ir direto para produção" | O build de preview em dispositivo real detecta problemas que o simulador não pega (permissões, performance, crashes nativos) |
| "OTA update serve para tudo, vou usar sempre" | OTA não pode atualizar código nativo — usar depois de verificar que a mudança é puramente JavaScript |
| "Vou commitar o `google-play-key.json` no repositório" | O arquivo de Service Account tem permissão de publicar na Play Store — tratar como secret, nunca commitar (`seguranca.md §1`) |

---

## Checklist de conclusão

- [ ] `eas.json` com perfis `development`, `preview` e `production` configurados
- [ ] Credenciais iOS e Android gerenciadas pelo EAS (não localmente)
- [ ] Build de preview testado em dispositivo real (iOS e Android)
- [ ] Versão (`version`) e números de build (`buildNumber`/`versionCode`) incrementados
- [ ] Build de produção executado sem erros
- [ ] Assets de store atualizados (screenshots, ícones, descrição)
- [ ] `eas submit` executado para iOS e Android
- [ ] `google-play-key.json` e outros secrets fora do repositório
- [ ] OTA update configurado com `channel` correto por ambiente
