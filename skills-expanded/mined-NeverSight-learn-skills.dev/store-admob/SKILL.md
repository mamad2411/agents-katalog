---
name: store-admob
description: "Set up AdMob app and create ad units (banner, interstitial, rewarded) via Python+Playwright automation. Saves ad unit IDs to project config."
argument-hint: "[ios|android|both]"
---

This skill sets up AdMob using **Python scripts with Playwright** (NOT Playwright MCP).
Zero LLM token cost for browser automation.

## Step 1: Ensure Credentials

```bash
python3 ${PLUGIN_DIR}/scripts/credentials_manager.py --show
```

If not configured:
```bash
python3 ${PLUGIN_DIR}/scripts/credentials_manager.py --setup
```

## Step 2: Determine Setup Parameters

Read `app.json` to extract:
- App name (expo.name)
- Bundle ID (expo.ios.bundleIdentifier)
- Package name (expo.android.package)

Ask the developer:
- Which ad types? (banner, interstitial, rewarded) — default: all three
- Is the app already published? (affects AdMob app linking)
- Output format? (json or typescript)

## Step 3: Run AdMob Setup Script

**IMPORTANT**: Tell the user:
> "Browser will open. Please log into AdMob (https://apps.admob.com) if prompted."

### Both platforms:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py \
  --app-name "{APP_NAME}" \
  --platform both \
  --bundle-id {BUNDLE_ID} \
  --package-name {PACKAGE_NAME} \
  --project .
```

### iOS only:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py \
  --app-name "{APP_NAME}" \
  --platform ios \
  --bundle-id {BUNDLE_ID} \
  --project .
```

### Android only:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py \
  --app-name "{APP_NAME}" \
  --platform android \
  --package-name {PACKAGE_NAME} \
  --project .
```

### Custom ad types:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py \
  --app-name "{APP_NAME}" \
  --platform both \
  --bundle-id {BUNDLE_ID} \
  --package-name {PACKAGE_NAME} \
  --ad-types banner,interstitial \
  --project .
```

### With TypeScript output:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py \
  --app-name "{APP_NAME}" \
  --platform both \
  --bundle-id {BUNDLE_ID} \
  --package-name {PACKAGE_NAME} \
  --output typescript \
  --project .
```

### Dry run:
```bash
python3 ${PLUGIN_DIR}/scripts/admob_setup.py --app-name "My App" --dry-run
```

## Step 4: Verify Output

The script saves AdMob IDs to `store-deploy.json`:
```json
{
  "admob": {
    "ios": {
      "app_id": "ca-app-pub-XXXXX~XXXXX",
      "ad_units": {
        "banner": "ca-app-pub-XXXXX/XXXXX",
        "interstitial": "ca-app-pub-XXXXX/XXXXX",
        "rewarded": "ca-app-pub-XXXXX/XXXXX"
      }
    },
    "android": {
      "app_id": "ca-app-pub-XXXXX~XXXXX",
      "ad_units": {
        "banner": "ca-app-pub-XXXXX/XXXXX",
        "interstitial": "ca-app-pub-XXXXX/XXXXX",
        "rewarded": "ca-app-pub-XXXXX/XXXXX"
      }
    }
  }
}
```

If `--output typescript` was used, also check `src/shared/config/admob.ts`.

Read the output file and confirm the IDs are populated. If any are empty, the script encountered issues — check `~/.store-deploy/error-screenshots/`.

## Step 5: Integrate into App

If the project uses `react-native-google-mobile-ads`, help configure:

1. Add app IDs to `app.json`:
```json
{
  "expo": {
    "plugins": [
      ["react-native-google-mobile-ads", {
        "androidAppId": "ca-app-pub-XXXXX~XXXXX",
        "iosAppId": "ca-app-pub-XXXXX~XXXXX"
      }]
    ]
  }
}
```

2. Use ad unit IDs from the generated config in the app code.

## Step 6: Report

```
AdMob Setup Complete
====================
iOS App ID:     ca-app-pub-XXXXX~XXXXX
Android App ID: ca-app-pub-XXXXX~XXXXX

Ad Units:
  banner:       ca-app-pub-XXXXX/XXXXX (iOS) / ca-app-pub-XXXXX/XXXXX (Android)
  interstitial: ca-app-pub-XXXXX/XXXXX (iOS) / ca-app-pub-XXXXX/XXXXX (Android)
  rewarded:     ca-app-pub-XXXXX/XXXXX (iOS) / ca-app-pub-XXXXX/XXXXX (Android)

Config saved to: store-deploy.json
```

## Step 7: Policy Compliance Checklist (계정 정지 방어)

After setup, walk the user through this checklist. These are account-level items that code alone cannot fix:

1. **app-ads.txt 게시**: 개발자 웹사이트 루트에 `app-ads.txt`를 게시한다
   (`~/works/seungmanchoi.github.io/app-ads.txt` → `https://seungmanchoi.github.io/app-ads.txt`).
   내용은 AdMob Console → 앱 → 모든 앱 보기 → app-ads.txt 탭에서 확인. 형식:
   ```
   google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
   ```
   스토어 리스팅의 "개발자 웹사이트"가 같은 도메인을 가리켜야 크롤링된다.
   미게시 시 광고 게재 제한(ad serving limit)으로 직행한다.

2. **스토어 리스팅 연결**: 앱 출시 후 AdMob 앱을 스토어 리스팅에 연결한다
   (AdMob Console → 앱 설정 → 앱 스토어 세부정보). 미연결/미검증 상태가
   길어지면 광고 게재가 제한된다.

3. **테스트 기기 등록**: 실제 광고 단위 ID가 들어간 internal/TestFlight 빌드를
   배포하기 전, 개발자/테스터 실기기를 `setRequestConfiguration({ testDeviceIdentifiers })`에
   등록한다 (템플릿의 `TEST_DEVICE_IDS` 상수). 미등록 기기의 클릭은 무효 트래픽으로
   집계되어 계정 정지 사유가 된다.

4. **본인 광고 클릭 절대 금지**: 프로덕션 빌드에서 본인 광고를 클릭하지 않는다.
   스토어 스크린샷 촬영도 테스트 기기/TestIds 상태에서만 진행한다 (실광고 화면 캡처 금지).
