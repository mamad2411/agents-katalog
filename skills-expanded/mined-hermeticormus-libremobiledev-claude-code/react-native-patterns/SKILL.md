---
name: react-native-patterns
description: "React Native code: typed React Navigation, a Zustand store, a Reanimated 3 swipe-to-dismiss card, TanStack Query pagination, a TurboModule spec, and a FlatList performance checklist. Use when building React Native screens, state, or native modules."
---

# React Native Patterns

## Typed Navigation with React Navigation

```typescript
// navigation/types.ts
import { NativeStackScreenProps } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Home: undefined;
  ProductDetail: { productId: string; source?: string };
  Checkout: { cartId: string };
  OrderConfirmation: { orderId: string };
};

export type ProductDetailScreenProps = NativeStackScreenProps<
  RootStackParamList,
  'ProductDetail'
>;
```

```typescript
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator<RootStackParamList>();

const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      ProductDetail: 'products/:productId',
      Checkout: 'checkout/:cartId',
    },
  },
};

export function App() {
  return (
    <NavigationContainer linking={linking}>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="ProductDetail" component={ProductDetailScreen} />
        <Stack.Screen name="Checkout" component={CheckoutScreen} />
        <Stack.Screen name="OrderConfirmation" component={OrderConfirmationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

```typescript
// screens/ProductDetailScreen.tsx
export function ProductDetailScreen({ route, navigation }: ProductDetailScreenProps) {
  const { productId } = route.params;

  return (
    <View>
      <Button
        title="Checkout"
        onPress={() => navigation.navigate('Checkout', { cartId: 'cart-123' })}
      />
    </View>
  );
}
```

---

## Zustand Store

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

const mmkvStorage = {
  getItem: (key: string) => storage.getString(key) ?? null,
  setItem: (key: string, value: string) => storage.set(key, value),
  removeItem: (key: string) => storage.delete(key),
};

interface CartState {
  items: CartItem[];
  addItem: (product: Product) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product) =>
        set((state) => {
          const existing = state.items.find((i) => i.productId === product.id);
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.productId === product.id ? { ...i, quantity: i.quantity + 1 } : i
              ),
            };
          }
          return {
            items: [...state.items, { productId: product.id, name: product.name, price: product.price, quantity: 1 }],
          };
        }),

      removeItem: (productId) =>
        set((state) => ({ items: state.items.filter((i) => i.productId !== productId) })),

      clearCart: () => set({ items: [] }),

      totalPrice: () => get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    }),
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => mmkvStorage),
    }
  )
);
```

---

## Reanimated 3: Swipe-to-Dismiss Card

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  runOnJS,
} from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

interface SwipeCardProps {
  onDismiss: () => void;
  children: React.ReactNode;
}

export function SwipeCard({ onDismiss, children }: SwipeCardProps) {
  const translateX = useSharedValue(0);
  const opacity = useSharedValue(1);
  const DISMISS_THRESHOLD = 120;

  const panGesture = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
      opacity.value = 1 - Math.abs(e.translationX) / 300;
    })
    .onEnd((e) => {
      if (Math.abs(e.translationX) > DISMISS_THRESHOLD) {
        const direction = e.translationX > 0 ? 500 : -500;
        translateX.value = withTiming(direction, { duration: 200 });
        opacity.value = withTiming(0, { duration: 200 }, () => {
          runOnJS(onDismiss)();
        });
      } else {
        // Snap back
        translateX.value = withSpring(0);
        opacity.value = withSpring(1);
      }
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
    opacity: opacity.value,
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}
```

---

## TanStack Query: Paginated Product List

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';
import { FlatList, ActivityIndicator } from 'react-native';

function useProducts(categoryId: string) {
  return useInfiniteQuery({
    queryKey: ['products', categoryId],
    queryFn: ({ pageParam = 1 }) => api.getProducts({ categoryId, page: pageParam }),
    getNextPageParam: (lastPage) =>
      lastPage.hasNextPage ? lastPage.nextPage : undefined,
    staleTime: 5 * 60 * 1000,  // 5 minutes
  });
}

export function ProductListScreen({ categoryId }: { categoryId: string }) {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } =
    useProducts(categoryId);

  const products = data?.pages.flatMap((page) => page.products) ?? [];

  if (isLoading) return <ActivityIndicator />;

  return (
    <FlatList
      data={products}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ProductCard product={item} />}
      onEndReached={() => {
        if (hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      }}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
    />
  );
}
```

---

## TurboModule Spec (New Architecture)

```typescript
// NativeBiometrics.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  authenticate(reason: string): Promise<boolean>;
  isAvailable(): boolean; // Synchronous — possible via JSI
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeBiometrics');
```

```typescript
// Usage
import NativeBiometrics from './NativeBiometrics';

// Synchronous availability check
if (NativeBiometrics.isAvailable()) {
  const authenticated = await NativeBiometrics.authenticate('Confirm payment');
}
```

---

## FlatList Performance Checklist

```typescript
<FlatList
  data={products}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ProductCard product={item} />}  // Must be memoized
  // Performance props
  removeClippedSubviews={true}    // Unmount off-screen items (Android)
  maxToRenderPerBatch={10}        // Batch size per render cycle
  windowSize={10}                 // Render window in screen heights
  initialNumToRender={8}          // First render count
  getItemLayout={(_data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}                             // Skip layout measurement when heights are fixed
/>
```
