# core/router/ — Navigation

## Stack: go_router ≥ 13

## Files to create

### app_router.dart
Creates the singleton GoRouter instance with full route tree.

```
class AppRouter {
  static GoRouter createRouter({required AuthBloc authBloc}) {
    return GoRouter(
      initialLocation: RouteConstants.splash,
      refreshListenable: GoRouterRefreshStream(authBloc.stream),
      redirect: RouteGuards.redirectLogic,
      routes: [
        GoRoute(path: RouteConstants.splash,       builder: (_, __) => const SplashPage()),
        GoRoute(path: RouteConstants.onboarding,   builder: (_, __) => const OnboardingPage()),
        GoRoute(path: RouteConstants.login,        builder: (_, __) => const LoginPage()),
        GoRoute(path: RouteConstants.otp,          builder: (_, state) =>
            OtpVerificationPage(phone: state.pathParameters['phone']!)),

        // Main Shell (bottom nav)
        ShellRoute(
          builder: (_, __, child) => MainShellPage(child: child),
          routes: [
            GoRoute(path: RouteConstants.homeRide,    builder: (_, __) => const RideHomePage()),
            GoRoute(path: RouteConstants.homeFood,    builder: (_, __) => const FoodHomePage()),
            GoRoute(path: RouteConstants.homeVoucher, builder: (_, __) => const VoucherListPage()),
            GoRoute(path: RouteConstants.homeProfile, builder: (_, __) => const ProfilePage()),
          ],
        ),

        // Ride flow
        GoRoute(path: RouteConstants.rideBooking,  builder: (_, __) => const RideBookingPage()),
        GoRoute(path: RouteConstants.rideConfirm,  builder: (_, __) => const RideConfirmPage()),
        GoRoute(path: RouteConstants.rideTracking, builder: (_, state) =>
            RideTrackingPage(orderId: state.pathParameters['orderId']!)),

        // Food flow
        GoRoute(path: RouteConstants.restaurantDetail, builder: (_, state) =>
            RestaurantDetailPage(restaurantId: state.pathParameters['restaurantId']!)),
        GoRoute(path: RouteConstants.cart,             builder: (_, __) => const CartPage()),
        GoRoute(path: RouteConstants.foodCheckout,     builder: (_, __) => const FoodCheckoutPage()),
        GoRoute(path: RouteConstants.foodTracking,     builder: (_, state) =>
            FoodTrackingPage(orderId: state.pathParameters['orderId']!)),

        // Others
        GoRoute(path: RouteConstants.rating,       builder: (_, state) => RatingPage(
            orderType: state.pathParameters['orderType']!,
            orderId:   state.pathParameters['orderId']!)),
        GoRoute(path: RouteConstants.mapPicker,    builder: (_, state) => MapPickerPage(
            extra: state.extra as MapPickerArgs)),
        GoRoute(path: RouteConstants.wallet,       builder: (_, __) => const WalletPage()),
        GoRoute(path: RouteConstants.notifications,builder: (_, __) => const NotificationsPage()),
        GoRoute(path: RouteConstants.orderHistory, builder: (_, __) => const OrderHistoryPage()),
        GoRoute(path: RouteConstants.settings,     builder: (_, __) => const SettingsPage()),
        GoRoute(path: RouteConstants.editProfile,  builder: (_, __) => const EditProfilePage()),
        GoRoute(path: RouteConstants.savedAddresses,builder: (_, __) => const SavedAddressesPage()),
      ],
    );
  }
}
```

### route_guards.dart
Redirect logic called on every navigation event.

```
class RouteGuards {
  static String? redirectLogic(BuildContext context, GoRouterState state) {
    final authState = context.read<AuthBloc>().state;
    final hasSeenOnboarding = sl<StorageService>().getBool(HiveConstants.keyHasSeenOnboarding);

    final isOnSplash      = state.matchedLocation == RouteConstants.splash;
    final isOnOnboarding  = state.matchedLocation == RouteConstants.onboarding;
    final isOnAuth        = state.matchedLocation.startsWith('/login') ||
                             state.matchedLocation.startsWith('/otp');

    if (authState is AuthLoading || isOnSplash) return null;

    if (!hasSeenOnboarding && !isOnOnboarding) return RouteConstants.onboarding;

    if (authState is Unauthenticated && !isOnAuth)  return RouteConstants.login;
    if (authState is Authenticated  &&  isOnAuth)   return RouteConstants.homeRide;

    return null;
  }
}
```

### router_transitions.dart
Custom page transitions (slide from right for normal push, fade for tab switch).

```
class RouterTransitions {
  static CustomTransitionPage<T> slideFromRight<T>({
    required BuildContext context,
    required GoRouterState state,
    required Widget child,
  }) => CustomTransitionPage<T>(
    key: state.pageKey,
    child: child,
    transitionsBuilder: (_, animation, __, child) =>
      SlideTransition(
        position: Tween(begin: const Offset(1, 0), end: Offset.zero)
            .animate(CurvedAnimation(parent: animation, curve: Curves.easeInOut)),
        child: child,
      ),
  );
}
```

## Rules
- NEVER use Navigator.push / Navigator.of(context).push anywhere — always use context.go or context.push
- Deep links: register URI scheme 'gomove://' in Android Manifest + iOS Info.plist
- GoRouterRefreshStream listens to AuthBloc.stream to trigger redirects on auth state change
- Pass complex objects via state.extra (not path params) — define a typed Args class for each
