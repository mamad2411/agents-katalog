---
description: Run Mobile Development and React Native Standards Check
globs: ['**/mobile/**/*.tsx', '**/native/**/*.ts', '**/ios/**/*.swift', '**/android/**/*.kt']
---

# Mobile: React Native & Mobile Development Standards

<audit_rules>

- You MUST implement proper platform-specific code separation using platform-specific files and conditional imports.
- You MUST optimize bundle size for mobile by implementing code splitting and lazy loading of heavy components.
- You MUST ensure proper memory management by avoiding memory leaks in components and implementing proper cleanup.
- You MUST implement proper offline support with data synchronization and conflict resolution strategies.
- You MUST configure proper push notification handling with user consent management and preference controls.
- You MUST ensure proper deep linking implementation with route validation and security checks.
- You MUST implement proper biometric authentication and secure storage for sensitive data.
- You MUST optimize performance by implementing flat lists, image optimization, and proper state management.
- You MUST ensure proper accessibility support with screen reader compatibility and touch target sizes.
- You MUST implement proper background processing and task scheduling for mobile-specific operations.
  </audit_rules>

<example_good>

```typescript
import React, { useEffect, useCallback } from 'react';
import { Platform, AppState } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import SecureStorage from 'react-native-secure-storage';
import { BiometricAuth } from '@/lib/biometric';

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Proper cleanup to prevent memory leaks
  useFocusEffect(
    useCallback(() => {
      let isActive = true;

      const loadUserData = async () => {
        try {
          // Biometric authentication for sensitive data
          const isAuth = await BiometricAuth.authenticate();
          if (!isAuth) {
            throw new Error('Authentication failed');
          }

          // Secure storage for sensitive data
          const token = await SecureStorage.getItem('auth_token');
          const userData = await fetchUserSecurely(userId, token);

          if (isActive) {
            setUser(userData);
          }
        } catch (error) {
          console.error('Failed to load user data:', error);
        } finally {
          if (isActive) {
            setIsLoading(false);
          }
        }
      };

      loadUserData();

      return () => {
        isActive = false;
      };
    }, [userId])
  );

  // Platform-specific implementation
  const renderPlatformSpecific = () => {
    if (Platform.OS === 'ios') {
      return <IOSSpecificComponent user={user} />;
    } else if (Platform.OS === 'android') {
      return <AndroidSpecificComponent user={user} />;
    }
    return <DefaultComponent user={user} />;
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <View>
      {renderPlatformSpecific()}
    </View>
  );
}
```

</example_good>

<example_bad>

```typescript
// BAD: No cleanup, no biometric auth, no platform separation
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // BAD: No cleanup function, memory leak risk
    fetchUser(userId).then(setUser);
  }, [userId]);

  // BAD: Storing token in AsyncStorage (not secure)
  const token = AsyncStorage.getItem('token');

  // BAD: No platform-specific handling
  return (
    <View>
      <Text>{user?.name}</Text>
    </View>
  );
}
```

</example_bad>
