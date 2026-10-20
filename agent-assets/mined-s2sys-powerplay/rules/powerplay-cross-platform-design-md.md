# Cross-Platform Design Standards

**Version**: 2.7.0  
**Applies to**: React Native, Flutter, Xamarin, shared codebases  
**Last Updated**: 2026-04-09

---

## 🎯 Core Principle

Write code once, run everywhere—but respect platform conventions. Cross-platform frameworks promise efficiency, but failing to adapt UI/UX to each platform results in uncanny-valley apps. This standard balances code reuse with platform-native experience.

---

## 📐 Architecture Pattern: Platform Abstraction Layer

Instead of platform checks scattered throughout (Platform.OS, !kIsWeb), use an abstraction layer:

### React Native Example

```typescript
// services/platformService.ts
const PlatformService = {
  isWeb: Platform.OS === 'web',
  isIOS: Platform.OS === 'ios',
  isAndroid: Platform.OS === 'android',
  
  get canUseNativeAPI() {
    return !PlatformService.isWeb;
  },
  
  async openCamera() {
    if (PlatformService.isWeb) {
      // Web: use browser camera
      return await WebCameraService.open();
    } else {
      // Native: use platform-specific camera
      return await NativeCameraModule.open();
    }
  },
};

// Usage: no Platform checks in components
const CameraComponent = () => {
  const openCamera = async () => {
    const photo = await PlatformService.openCamera();
    // Handle photo
  };
};
```

### Flutter Example

```dart
// services/platform_service.dart
class PlatformService {
  static bool get isWeb => kIsWeb;
  static bool get isIOS => defaultTargetPlatform == TargetPlatform.iOS;
  static bool get isAndroid => defaultTargetPlatform == TargetPlatform.android;
  
  static Future<void> openCamera() async {
    if (isWeb) {
      // Web implementation
    } else {
      // Native implementation
    }
  }
}

// Usage in widget tree
class CameraWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => PlatformService.openCamera(),
      child: Icon(Icons.camera),
    );
  }
}
```

---

## 🎨 UI Principles: Adaptive vs. Responsive

### Responsive Layout
- **Single design** adapts to screen size (portrait/landscape)
- Best for: web, tablets with universal design
- Use: percentage-based layouts, media queries, flexible grids

### Adaptive Layout
- **Different designs** per platform (iOS vs. Android)
- iOS: bar at top (navigation), swipe gestures, large touch targets (44x44)
- Android: bottom navigation, back button, material design, slightly smaller targets (48x48)
- Best for: cross-platform apps where platform conventions matter

**Recommendation**: Use **responsive base** (size adaptation) + **adaptive UI** (platform-specific conventions).

---

## 📱 Platform-Specific UI Patterns

### Navigation

**iOS Convention**
```
┌─────────────────────┐
│ ← Back | Title | (x) | ← Top navigation bar
├─────────────────────┤
│                     │
│   Content           │
│                     │
├─────────────────────┤
│  [Tab1] [Tab2] ...  │ ← Bottom tabs (if multiple sections)
└─────────────────────┘
```

**Android Convention**
```
┌─────────────────────┐
│  ☰ Menu | Title     │ ← Top app bar with hamburger/back
├─────────────────────┤
│                     │
│   Content           │
│                     │
├─────────────────────┤
│ [Home] [Shop] [...] │ ← Bottom navigation (Material Design)
└─────────────────────┘
```

**Cross-Platform Solution**
```typescript
// React Native
const Navigation = ({ platform }) => {
  if (platform === 'ios') {
    return (
      <NavigationContainer>
        <NativeStackNavigator>
          {/* Stack-based navigation, back button in header */}
        </NativeStackNavigator>
      </NavigationContainer>
    );
  } else {
    return (
      <NavigationContainer>
        <BottomTabNavigator>
          {/* Tab-based, back button handled by Android system */}
        </BottomTabNavigator>
      </NavigationContainer>
    );
  }
};
```

### Dialogs & Alerts

**iOS**
- UIAlertController: centered, slide up
- Options: cancel, default, destructive
- Favors Cancel button prominent

**Android**
- AlertDialog: Material Design
- Options: positive, negative, neutral
- Favors Positive button on right

**Cross-Platform Code**
```typescript
// Use react-native-community/hooks
const { showAlert } = useAlert();

const deleteUser = () => {
  showAlert({
    title: 'Delete User?',
    message: 'This cannot be undone.',
    buttons: [
      { text: 'Cancel', onPress: () => {} },
      {
        text: 'Delete',
        onPress: deleteUserAsync,
        style: Platform.OS === 'ios' ? 'destructive' : 'default',
      },
    ],
  });
};
```

### Gestures

**iOS Conventions**
- Swipe back to navigate (gesture, not button)
- Long press for context menu
- Pinch to zoom
- Swipe up for control center

**Android Conventions**
- Back button (system) to navigate
- Long press for context menu
- Pinch to zoom
- Swipe right from edge for navigation drawer

**Cross-Platform Approach**
```typescript
// Platform-specific gesture recognizers
const useBackGesture = (onBack: () => void) => {
  if (Platform.OS === 'ios') {
    // Use React Navigation's swipe-back (default)
  } else {
    // Android: back button handled by system
    useFocusEffect(
      React.useCallback(() => {
        const unsubscribe = navigation.addListener('beforeRemove', (e) => {
          e.preventDefault();
          onBack();
        });
        return unsubscribe;
      }, [])
    );
  }
};
```

---

## 🎯 Design Token System (Adaptive)

Use design tokens that adapt per platform:

```typescript
// tokens/colors.ts
const colors = {
  primary: '#007AFF', // iOS blue
  secondary: '#1F2937', // Dark gray
  // More colors...
};

// tokens/spacing.ts
const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

// tokens/typography.ts
const typography = {
  heading1: {
    fontSize: Platform.OS === 'ios' ? 34 : 32,
    fontWeight: '600',
    lineHeight: Platform.OS === 'ios' ? 41 : 39,
  },
  body: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '400',
  },
};

// components/Button.tsx
const Button = ({ label, onPress }) => {
  const padding = Platform.OS === 'ios' ? 12 : 16; // iOS: compact, Android: spacious
  
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        paddingVertical: padding,
        paddingHorizontal: padding * 2,
        backgroundColor: colors.primary,
        borderRadius: Platform.OS === 'ios' ? 8 : 4, // iOS: rounded, Android: subtle
      }}
    >
      <Text style={typography.body}>{label}</Text>
    </TouchableOpacity>
  );
};
```

---

## 🗂️ Code Organization for Cross-Platform

```
project/
├── src/
│   ├── shared/           # 100% shared (no platform checks)
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── models/
│   │   ├── hooks/
│   │   │   └── useAsync.ts
│   │   └── utils/
│   │
│   ├── platform/         # Platform abstraction layer
│   │   ├── index.ts
│   │   ├── ios.ts
│   │   ├── android.ts
│   │   └── web.ts
│   │
│   ├── ui/               # Platform-adaptive components
│   │   ├── Button.tsx    # Adapts based on platform
│   │   ├── Dialog.tsx
│   │   ├── Navigation.tsx
│   │   ├── ios/          # iOS-specific components
│   │   │   └── SwipeBackHandler.tsx
│   │   └── android/      # Android-specific components
│   │       └── BackButtonHandler.tsx
│   │
│   └── screens/          # Mostly shared, small platform-specific sections
│       ├── HomeScreen.tsx
│       └── SettingsScreen.tsx
```

---

## ⚡ Performance Considerations

### Code Splitting by Platform

```typescript
// Only load iOS-specific code on iOS
import { Platform } from 'react-native';

const IOSSpecificModule = Platform.select({
  ios: () => require('./ios/iosModule').default,
  default: () => null,
})();

// In React Native: dynamic imports for large features
const AdvancedFeature = React.lazy(() =>
  Platform.OS === 'ios' ? import('./features/iOS') : import('./features/generic')
);
```

### Optimize for Each Platform's Performance Profile

**iOS Performance Tips**
- Use Metal for graphics (SwiftUI does this automatically)
- Limit background tasks (background app refresh drains battery)
- Cache aggressively (iOS has less RAM than Android devices)

**Android Performance Tips**
- Optimize for lower-end devices (Android market is fragmented)
- Use ProGuard/R8 to reduce app size
- Optimize garbage collection (avoid object allocation in hot loops)

**Web Performance Tips**
- Code split by route
- Lazy load heavy modules
- Optimize bundle size: tree-shake unused code

---

## 🌍 Localization for Cross-Platform

Use unified i18n library:

```typescript
// i18n/config.ts
import i18n from 'i18next';

i18n.init({
  resources: {
    en: { translation: require('./en.json') },
    es: { translation: require('./es.json') },
  },
  lng: 'en',
  fallbackLng: 'en',
});

// Usage: same across all platforms
const { t } = useTranslation();
return <Text>{t('button.save')}</Text>;
```

Support RTL automatically:
```typescript
const isRTL = i18n.language === 'ar' || i18n.language === 'he';
return <View style={{ flexDirection: isRTL ? 'row-reverse' : 'row' }} />;
```

---

## 🔒 Platform-Specific Security

| Feature | iOS | Android | Web |
|---------|-----|---------|-----|
| Secure Storage | Keychain | KeyStore | LocalStorage (encrypted) |
| Biometric | Face/Touch ID | BiometricPrompt | Web Auth (fingerprint) |
| Certificate Pinning | TrustKit | Network Security Config | HPKP headers |
| Secure Enclave | Available | N/A | N/A |

**Abstraction Layer**
```typescript
const SecureStorage = Platform.select({
  ios: () => require('./secure/ios').default,
  android: () => require('./secure/android').default,
  web: () => require('./secure/web').default,
})();

const token = await SecureStorage.getToken('auth_token');
```

---

## 📊 Testing Cross-Platform Code

### Unit Tests (100% shared)
```typescript
// math.ts (platform-agnostic)
export const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// math.test.ts
test('calculateTotal sums prices correctly', () => {
  expect(calculateTotal([{ price: 10 }, { price: 20 }])).toBe(30);
});
```

### Component Tests (platform-specific)
```typescript
// React Native Testing Library
test('Button renders correctly on iOS', () => {
  Platform.OS = 'ios';
  const { getByText } = render(<Button label="Save" />);
  expect(getByText('Save')).toBeTruthy();
});

test('Button renders correctly on Android', () => {
  Platform.OS = 'android';
  const { getByText } = render(<Button label="Save" />);
  expect(getByText('Save')).toBeTruthy();
});
```

### E2E Tests (critical user flows, all platforms)
```typescript
// Detox (React Native)
describe('User Authentication', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should log in on iOS', async () => {
    await element(by.id('email')).typeText('user@example.com');
    await element(by.id('password')).typeText('password');
    await element(by.id('signIn')).tap();
    await waitFor(element(by.text('Welcome'))).toBeVisible();
  });
});
```

---

## ✅ Cross-Platform Checklist

- [ ] Platform abstraction layer: NO Platform.OS in components
- [ ] Navigation: iOS stack-based, Android tab-based
- [ ] UI: Adapts to platform conventions (dialogs, buttons, spacing)
- [ ] Gestures: Swipe back on iOS, system back button on Android
- [ ] Localization: Works in 2+ languages, RTL supported
- [ ] Testing: Unit tests (shared), component tests (per-platform), E2E (critical flows)
- [ ] Performance: Baseline on iOS + Android + web (different perf profiles)
- [ ] Security: Secrets in secure storage per platform
- [ ] Accessibility: VoiceOver/TalkBack/screen reader works
- [ ] App size: < 100MB on all platforms

---

**Version**: 2.7.0  
**Last Updated**: 2026-04-09  
**Author**: SmartWorkz Dev
