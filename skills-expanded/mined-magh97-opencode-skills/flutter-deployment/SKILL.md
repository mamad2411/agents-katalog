---
name: flutter-deployment
description: "Despliegue de apps Flutter en iOS y Android. Cubre code signing, App Store Connect, Google Play Console, Codemagic CI/CD, versionado semántico, splash screen, íconos, y publicación. Actívala al preparar un release, configurar CI/CD móvil, o publicar en las tiendas."
disable-model-invocation: true
---

# Flutter Deployment

Guía de despliegue móvil. App Store (iOS) + Google Play (Android) + Codemagic CI/CD.

---

## Versionado

```yaml
# pubspec.yaml
version: 1.3.0+7
# 1.3.0 = version name (semántica)
# 7     = version code (entero incremental)
```

| Cambio | version name | version code |
|--------|-------------|--------------|
| feat | 1.4.0 | 8 |
| fix | 1.3.1 | 8 |
| breaking | 2.0.0 | 8 |

---

## App Icons y Splash Screen

```bash
flutter pub add flutter_launcher_icons
flutter pub add flutter_native_splash
```

```yaml
# pubspec.yaml
flutter_launcher_icons:
  android: true
  ios: true
  image_path: "assets/icon/app_icon.png"

flutter_native_splash:
  color: "#1677FF"
  image: "assets/splash.png"
  android: true
  ios: true
```

```bash
flutter pub run flutter_launcher_icons
flutter pub run flutter_native_splash:create
```

---

## Android — Google Play

### Code signing

```bash
# Generar keystore (una sola vez)
keytool -genkey -v -keystore ~/upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Crear key.properties (NO commitear)
```

```properties
# android/key.properties
storePassword=***  
keyPassword=***  
keyAlias=upload
storeFile=/home/user/upload-keystore.jks
```

```gradle
// android/app/build.gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### Build

```bash
# APK (para testing)
flutter build apk --release

# App Bundle (para Google Play)
flutter build appbundle --release
```

---

## iOS — App Store

### Code signing (Xcode)

```
Xcode → Signing & Capabilities → Team → Automatically manage signing
```

Provisioning profiles manejados por Xcode automáticamente.

### Build

```bash
flutter build ipa --release
# Genera build/ios/ipa/miapp.ipa
```

### Subir a App Store Connect

```bash
# altool fue deprecado por Apple en 2023. Usa notarytool (o Xcode Organizer /
# Transporter como alternativa gráfica) para subir a App Store Connect.
xcrun notarytool submit build/ios/ipa/miapp.ipa \
  --apple-id "apple@email.com" \
  --team-id "TEAMID1234" \
  --password "@keychain:app-specific-password" \
  --wait
```

---

## Codemagic CI/CD

```yaml
# codemagic.yaml
workflows:
  android-release:
    name: Android Release
    environment:
      flutter: stable
    scripts:
      - flutter test
      - flutter build appbundle --release
    artifacts:
      - build/app/outputs/bundle/release/app-release.aab
    publishing:
      google_play:
        credentials: $GCLOUD_SERVICE_ACCOUNT_CREDENTIALS
        track: production

  ios-release:
    name: iOS Release
    environment:
      flutter: stable
      xcode: latest
    scripts:
      - flutter test
      - flutter build ipa --release
    artifacts:
      - build/ios/ipa/*.ipa
    publishing:
      app_store_connect:
        api_key: $APP_STORE_CONNECT_PRIVATE_KEY
        key_id: $APP_STORE_CONNECT_KEY_IDENTIFIER
        issuer_id: $APP_STORE_CONNECT_ISSUER_ID
```

Trigger: push a `main`, tag `v*`, o manual desde UI de Codemagic.

---

## Checklist pre-release

```dart
// ✅ Quitar logs de debug
if (kDebugMode) print('...');

// ✅ Cambiar URL de API a producción
const apiUrl = 'https://api.miapp.com';

// ✅ Habilitar ofuscación (Android)
flutter build appbundle --release --obfuscate --split-debug-info=build/debug-info

// ✅ Verificar permisos (AndroidManifest + Info.plist)
// Solo los permisos realmente usados

// ✅ Testear en dispositivo físico (no solo emulador)
```

---

## Checklist deployment

- [ ] Version code incrementado en cada release
- [ ] Keystore seguro (no commitear `key.properties` ni `.jks`)
- [ ] App bundle para Google Play (no APK)
- [ ] Codemagic configurado con credentials seguras
- [ ] iOS code signing automático o manual con CI
- [ ] Ofuscación habilitada en release
- [ ] URLs de API apuntan a producción
- [ ] Permisos mínimos necesarios declarados
- [ ] Testeado en dispositivo físico antes de publicar
