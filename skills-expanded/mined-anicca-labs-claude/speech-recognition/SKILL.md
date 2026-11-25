---
name: speech-recognition
description: On-device voice-to-text dictation via expo-speech-recognition — permissions, continuous recognition, partial vs final results, and cross-platform transcript handling. Use when adding voice input to a text field, transcribing speech, or debugging dictation start/stop and permission flows.
---

Apply the following speech-recognition standards to all voice-to-text code in this project.

## Stack

- `expo-speech-recognition` — native iOS/Android speech recognition with a config plugin, event hooks, and a permissions API
- Optionally a Zustand preferences store for the user's chosen recognition language (Auto = device locale)

## Install

```bash
yarn expo install expo-speech-recognition
```

Pin to the version that matches your Expo SDK major — reflect on SDK 56 uses `"expo-speech-recognition": "~56.0.1"`. This package versions in lockstep with the Expo SDK (each SDK major has its own line, e.g. SDK 55 → 3.x, SDK 56 → 56.x). Installing a mismatched major pulls native code built against a different React Native and breaks the build, so let `expo install` resolve the right version rather than pinning by hand.

## app.config.ts

Add the config plugin with both iOS usage strings as plugin options (the plugin writes them into `Info.plist` and adds Android `RECORD_AUDIO` for you):

```ts
plugins: [
  [
    'expo-speech-recognition',
    {
      microphonePermission:
        'This app uses your microphone to let you dictate text by voice.',
      speechRecognitionPermission:
        'This app uses speech recognition to transcribe your voice into text.',
    },
  ],
],
```

- `microphonePermission` → `NSMicrophoneUsageDescription`
- `speechRecognitionPermission` → `NSSpeechRecognitionUsageDescription`
- Android `RECORD_AUDIO` is injected by the plugin — no manual `AndroidManifest.xml` edit needed.

Both iOS strings are mandatory. iOS rejects the build (or crashes at request time) if either is missing. This is a native change — after adding the plugin you must run a fresh dev/prod build; it cannot ship as an OTA update.

## Canonical hook (`src/hooks/useVoiceToText.ts`)

The module exposes `ExpoSpeechRecognitionModule` (imperative start/stop/permissions) plus a `useSpeechRecognitionEvent(name, handler)` hook for events. The hard part is not the API — it's reconciling iOS and Android transcript semantics into a single append-to-a-draft behavior.

```ts
import { useState, useRef, useCallback } from 'react';
import { getLocales } from 'expo-localization';
import { ExpoSpeechRecognitionModule, useSpeechRecognitionEvent } from 'expo-speech-recognition';

type UseVoiceToTextOptions = {
  // `replaces` is the running transcript for this segment — swap it out instead of appending,
  // so interim updates don't pile up duplicate text in the draft.
  onResult: (transcript: string, replaces: string) => void;
  onError?: (message: string) => void;
  // Fired when permission was previously denied and the OS won't show the dialog again.
  onPermissionDenied?: () => void;
};

const getLocale = (): string => {
  // Use expo-localization — it reads the device's preferred language list cross-platform
  // and returns BCP-47 tags. Do NOT use NativeModules.SettingsManager: it's iOS-only
  // (undefined on Android → always 'en-US') and its AppleLocale is the *region*, not the
  // language, so a Spanish phone set to a US region would dictate in English.
  const [primary] = getLocales();
  return primary?.languageTag ?? primary?.languageCode ?? 'en-US'; // BCP-47, e.g. es-ES
};

// The recognizer only accepts locales it has a MODEL for — and that's a per-region list.
// A real device tag like "es-AR" usually has no exact model, and iOS throws
// "language-not-supported". Resolve the device tag to a supported variant of the SAME
// language (es-AR → es-ES/es-US) before starting. Works for any language, not just Spanish.
const resolveSupportedLocale = async (desired: string): Promise<string> => {
  let locales: string[] = [];
  try {
    ({ locales } = await ExpoSpeechRecognitionModule.getSupportedLocales({}));
  } catch {
    // Android ≤12 returns empty (or throws without a service package) — can't validate.
  }
  if (!locales.length) return desired; // no list to check against; let the recognizer decide
  if (locales.some((l) => l.toLowerCase() === desired.toLowerCase())) return desired; // exact (keep region)
  const lang = desired.toLowerCase().split('-')[0];
  const sameLang = locales.find((l) => l.toLowerCase().split('-')[0] === lang); // any region of the language
  if (sameLang) return sameLang;
  return locales.find((l) => l.toLowerCase().startsWith('en')) ?? locales[0]; // last resort
};

export const useVoiceToText = ({ onResult, onError, onPermissionDenied }: UseVoiceToTextOptions) => {
  const [isListening, setIsListening] = useState(false);

  // "Latest ref" pattern: the async speech-event listeners are registered once but must call
  // the freshest callbacks. Keep them in refs and update every render.
  const onResultRef = useRef(onResult);
  const onErrorRef = useRef(onError);
  const onPermissionDeniedRef = useRef(onPermissionDenied);
  onResultRef.current = onResult;
  onErrorRef.current = onError;
  onPermissionDeniedRef.current = onPermissionDenied;

  const sessionTranscriptRef = useRef('');   // running transcript for the current segment
  const sessionEndedRef = useRef(false);
  const userStoppedRef = useRef(false);
  const pendingErrorRef = useRef<string | null>(null);
  // iOS dedup: on stop(), iOS re-fires the same isFinal transcript. Track the last committed
  // final so a duplicate arriving before `end` can be skipped.
  const lastFinalRef = useRef('');

  useSpeechRecognitionEvent('start', () => {
    sessionEndedRef.current = false;
    userStoppedRef.current = false;
    pendingErrorRef.current = null;
    sessionTranscriptRef.current = '';
    lastFinalRef.current = '';
    setIsListening(true);
  });

  useSpeechRecognitionEvent('end', () => {
    sessionEndedRef.current = true;
    sessionTranscriptRef.current = '';
    lastFinalRef.current = '';
    setIsListening(false);
    // Surface a real engine error only if the user didn't stop on purpose.
    if (pendingErrorRef.current && !userStoppedRef.current) {
      onErrorRef.current?.(pendingErrorRef.current);
    }
    pendingErrorRef.current = null;
  });

  useSpeechRecognitionEvent('result', (event) => {
    if (sessionEndedRef.current || userStoppedRef.current) return;
    const transcript = event.results[0]?.transcript;
    if (!transcript) return;

    if (event.isFinal) {
      if (transcript === lastFinalRef.current) return; // iOS double-fire
      lastFinalRef.current = transcript;
      onResultRef.current(transcript, sessionTranscriptRef.current);
      sessionTranscriptRef.current = '';
    } else {
      lastFinalRef.current = ''; // new utterance forming — reset the dedup window
      // Android cumulative transcripts only grow within a segment. If the new one is SHORTER,
      // the engine restarted internally after a pause (no end/start fired) — treat it as a
      // fresh segment so we append rather than overwrite.
      if (transcript.length < sessionTranscriptRef.current.length) {
        sessionTranscriptRef.current = '';
      }
      onResultRef.current(transcript, sessionTranscriptRef.current);
      sessionTranscriptRef.current = transcript;
    }
  });

  useSpeechRecognitionEvent('error', (event) => {
    // Don't surface immediately — stash it and decide in `end` whether it was user-initiated.
    // Include event.error (the CODE, e.g. "language-not-supported") — on a release build
    // that code is often the only way to diagnose without device logs, so don't discard it.
    const code = event.error ? `[${event.error}] ` : '';
    pendingErrorRef.current = `${code}${event.message ?? 'Speech recognition failed'}`;
  });

  const start = useCallback(async () => {
    const current = await ExpoSpeechRecognitionModule.getPermissionsAsync();
    if (!current.granted && !current.canAskAgain) {
      // Permanently denied — the OS won't re-prompt. Let the caller deep-link to Settings.
      onPermissionDeniedRef.current?.();
      return;
    }
    const { granted } = await ExpoSpeechRecognitionModule.requestPermissionsAsync();
    if (!granted) return; // first denial — stay silent, don't redirect

    try {
      // Resolve to a locale the recognizer actually has a model for (see resolveSupportedLocale).
      const lang = await resolveSupportedLocale(getLocale()); // or a user-chosen language (see Settings)
      ExpoSpeechRecognitionModule.start({
        lang,
        continuous: true,             // keep listening across pauses
        interimResults: true,         // emit partial (non-final) transcripts as the user speaks
        // volumeChangeEventOptions enables the 'volumechange' event for mic-level UI
        volumeChangeEventOptions: { enabled: true, intervalMillis: 80 },
      });
    } catch (e) {
      // A synchronous native throw (e.g. no recognition service) would otherwise be an
      // unhandled rejection. Route it through onError so the user sees a real message.
      onErrorRef.current?.(`start failed: ${e instanceof Error ? e.message : String(e)}`);
    }
  }, []);

  const stop = useCallback(() => {
    userStoppedRef.current = true; // mark intentional stop so we don't show an error
    sessionTranscriptRef.current = '';
    ExpoSpeechRecognitionModule.stop();
  }, []);

  return { isListening, start, stop };
};
```

## Consumer pattern (append into a text draft)

The `onResult(transcript, replaces)` contract lets the screen swap the current segment in place — find the previously-inserted `replaces` text and replace it, otherwise append with a separator:

```ts
const { isListening, start, stop } = useVoiceToText({
  onResult: (transcript, replaces) => {
    setDraft((prev) => {
      if (replaces) {
        const idx = prev.lastIndexOf(replaces);
        if (idx !== -1) return prev.slice(0, idx) + transcript;
      }
      const separator = prev.trim().length > 0 ? ' ' : '';
      return prev + separator + transcript;
    });
  },
  onError: (message) => showToast(`Voice recognition failed: ${message}`), // show the code, don't swallow it
  onPermissionDenied: () =>
    Alert.alert(
      'Microphone access required',
      'To use voice input, enable microphone access in Settings.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Open Settings', onPress: () => Linking.openSettings() },
      ],
    ),
});
```

Mic-level UI (optional): subscribe to `volumechange` in the component to drive an animated ring. `event.value` is roughly in `[-2, 10]` dB; normalize before use:

```ts
useSpeechRecognitionEvent('volumechange', (event) => {
  const vol = Math.max(0, (event.value + 2) / 12); // → ~[0, 1]
  ringScale.value = withSpring(1 + vol * 0.7);
});
```

## Language / locale

- Default to the device locale via `expo-localization` `getLocales()` (`getLocale()` above) — do not hardcode `en-US`, and do not read `NativeModules.SettingsManager` (iOS-only; see Gotchas).
- **Validate the locale against the recognizer before `start`** (`resolveSupportedLocale` above). The device tag is region-specific (`es-AR`, `de-AT`, `fr-CA`) and the recognizer only ships models per region — `es-AR` typically has no model, so iOS throws `language-not-supported`. Query `getSupportedLocales()` and fall back to any variant of the same language (`es-AR` → `es-ES`/`es-US`). This is language-agnostic — only the region is dropped, and only when there's no exact match.
- Pass a BCP-47 tag (`en-US`, `pt-BR`, `es-ES`) to `start({ lang })`. To let users override, persist their choice (reflect stores `voiceLanguage: string | null` in a Zustand preferences store; `null` = Auto/device locale) and read it at `start` time.

## Gotchas (encountered in reflect)

- **"Auto" locale must come from `expo-localization`, not `NativeModules.SettingsManager`.** `SettingsManager` is iOS-only — on Android it's `undefined`, so `getLocale()` silently fell back to `en-US` and every Android device dictated in English. On iOS its `AppleLocale` is the *region*, not the language, so a Spanish phone set to a US region also dictated in English. Resolve the locale with `getLocales()[0].languageTag` (BCP-47, cross-platform), the same way the app detects locale for i18n/dates.
- **The device locale's region may have no recognizer model → `language-not-supported`.** Once `getLocale()` correctly returned the real tag `es-AR`, iOS rejected it: the recognizer ships per-region models and has no `es-AR`. Don't pass the raw device tag — run it through `resolveSupportedLocale` (query `getSupportedLocales()`, fall back to a same-language variant). Note `getSupportedLocales()` returns `[]` on Android ≤12, so treat an empty list as "can't validate, pass the tag through."
- **Don't swallow the `error` event message.** A generic "Voice recognition failed" toast hides the code (`language-not-supported`, `service-not-allowed`, …). On a release/full build with no logs, surfacing `event.error` + `event.message` in the toast is the fastest way to diagnose — and it's OTA-deliverable, so you don't need a rebuild to see what's wrong.
- **iOS double-fires the final result.** On `stop()`, iOS emits the same `isFinal` transcript twice. Dedup by comparing against the last committed final (`lastFinalRef`) — otherwise the last phrase is inserted twice.
- **Android restarts internally without end/start.** With `continuous: true`, after a natural pause the Android engine begins a fresh cumulative transcript. There's no `end`/`start` event — detect it by the new interim transcript being *shorter* than the tracked one, then append instead of overwrite.
- **Distinguish user-stop from real errors.** `stop()` can surface as an `error` event. Stash errors in a ref and only report them in `end` when `userStoppedRef` is false — otherwise every normal stop looks like a failure.
- **Two-stage permission UX.** First denial: stay silent (the user can tap the mic again to re-prompt). Once `canAskAgain` is false, the OS won't show the dialog — deep-link to Settings via `Linking.openSettings()`.
- **Simulators are unreliable.** Speech recognition needs real microphone hardware; test dictation on a physical device.
- **Native change, not OTA.** Adding the config plugin / permissions changes the native fingerprint — it requires a new build and won't reach existing binaries via OTA.
- **Latest-ref pattern is required.** `useSpeechRecognitionEvent` listeners are registered once; reading `onResult`/`onError` directly would capture stale closures. Keep them in refs updated each render.

## Rules

- Always check `getPermissionsAsync()` before `requestPermissionsAsync()` — branch on `canAskAgain` for the Settings deep-link path.
- Never hardcode `en-US`; default to the device locale and allow a persisted override.
- Always resolve the locale against `getSupportedLocales()` before `start` — the device's region (`es-AR`) often has no model; fall back to a same-language variant rather than letting it throw `language-not-supported`.
- Surface the `error` event's code + message to the user (at least on stg); never show a generic-only failure toast — the code is your only diagnostic on a release build.
- Set `continuous: true` + `interimResults: true` for live dictation; commit on `isFinal`, preview on interim.
- Dedup iOS final results (compare to last final) and detect Android internal restarts (shorter interim) — both are required for correct cross-platform appending.
- Stash `error` events and decide in `end` whether to surface them, so intentional stops aren't reported as failures.
- Both iOS usage strings (`microphonePermission`, `speechRecognitionPermission`) are mandatory; ship a new native build after adding the plugin.
- Test on a physical device — simulators don't have working mic input for recognition.
