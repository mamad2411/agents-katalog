# Agent Notes

## Auto-build rules (per user request)
After editing code, automatically build without being asked:
- Mobile (Dart) changes: run `flutter analyze` then `flutter build apk --release`
  - Working dir: `mobile/`
  - Output APK: `mobile/build/app/outputs/flutter-apk/app-release.apk`
- Backend (Java) changes: run `mvn compile -DskipTests` to verify.
  - Requires `JAVA_HOME="C:\Program Files\Java\jdk-17"` (default env JDK 8 breaks `--release`).
  - Commit + push deploys backend via CI (image `ghcr.io/tranhoangtrunghieu/pokemon-be:latest`).
  - Ask before committing/pushing backend (push triggers production deploy).

## Environment
- Repo: `D:\PRM-pokemon`, GitHub `https://github.com/TranHoangTrungHieu/PRM-project.git`, branch `main`.
- VPS `129.80.105.58` (ubuntu, SSH key `C:\Users\ASUS\Downloads\ssh-key-2026-07-12 (3).key`), container `pokemon_backend`.
- Mobile `baseUrl` = `http://129.80.105.58`.
- MongoDB backend: new fields need no migration.
