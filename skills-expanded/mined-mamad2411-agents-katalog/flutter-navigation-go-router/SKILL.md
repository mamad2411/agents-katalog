---
name: flutter-navigation-go-router
description: |
  Flutter 프로젝트의 라우팅 패턴 — `go_router` 기반 경로 선언, `RoutePaths` 상수 관리, `StatefulShellRoute`로 바텀 내비게이션 구현, 경로 파라미터(`:recipeId`) 처리, `context.go`/`context.push` 사용. "라우트 추가", "go_router", "화면 이동", "네비게이션", "GoRoute", "StatefulShellRoute", "pathParameters", "딥링크" 같은 표현에 트리거합니다.
---

# Flutter Navigation — go_router

## 원칙

- **경로 상수는 한 곳에 모은다.** `lib/core/routing/route_paths.dart` 의 `RoutePaths` 에 문자열 상수로 선언한다. 코드 어디에서도 raw 문자열을 직접 쓰지 않는다.
- **라우터 정의는 `lib/core/routing/router.dart` 하나.** `GoRouter` 인스턴스는 전역 `router` 변수로 노출되고 `main.dart` 의 `MaterialApp.router` 가 소비한다.
- **라우트 빌더는 Root 위젯만 만든다.** DI/이벤트/상태 구독은 Root 가 담당하므로 라우터는 Screen 에 대한 지식이 없다.
- **크로스 feature 네비게이션은 `context.go` / `context.push` 콜백으로** 처리한다. Screen/Root 가 다른 feature 의 라우트 문자열을 알아도 된다는 것이 이 프로젝트의 관례다 — `RoutePaths` 상수를 통해서 참조하기 때문에 안전하다.

---

## 경로 상수

```dart
// lib/core/routing/route_paths.dart
abstract class RoutePaths {
  static const String splash = '/Splash';
  static const String signIn = '/SingIn';
  static const String signUp = '/SingUp';

  static const String home = '/Home';
  static const String savedRecipes = '/SavedRecipes';
  static const String notifications = '/Notifications';
  static const String profile = '/Profile';

  static const String search = '/Home/Search';
  static const String ingredient = '/Home/Ingredient/:recipeId';
}
```

**규칙**:
- 최상위 화면은 `/<Name>` 형태.
- 중첩(서브) 경로는 상위 경로를 접두어로 포함 (`/Home/Ingredient/:recipeId`).
- 경로 파라미터는 `:name` 토큰으로.

---

## GoRouter 정의

```dart
// lib/core/routing/router.dart
final router = GoRouter(
  initialLocation: RoutePaths.splash,
  routes: [
    GoRoute(
      path: RoutePaths.ingredient,
      builder: (context, state) {
        final recipeId = int.parse(state.pathParameters['recipeId']!);
        return IngredientRoot(recipeId: recipeId);
      },
    ),
    GoRoute(
      path: RoutePaths.splash,
      builder: (context, state) => SplashScreen(
        onTapStartCooking: () => context.go(RoutePaths.signIn),
      ),
    ),
    // ... 기타 라우트
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) => MainScreen(
        body: navigationShell,
        currentPageIndex: navigationShell.currentIndex,
        onChangeIndex: (index) => navigationShell.goBranch(
          index,
          initialLocation: index == navigationShell.currentIndex,
        ),
      ),
      branches: [
        StatefulShellBranch(routes: [
          GoRoute(path: RoutePaths.home, builder: (c, s) => const HomeRoot()),
        ]),
        StatefulShellBranch(routes: [
          GoRoute(path: RoutePaths.savedRecipes, builder: (c, s) => const SavedRecipesRoot()),
        ]),
        // notifications, profile ...
      ],
    ),
  ],
);
```

```dart
// lib/main.dart
return MaterialApp.router(
  routerConfig: router,
  // ...
);
```

---

## 경로 파라미터 읽기

파라미터는 `state.pathParameters` 에서 문자열로 나온다. 타입 변환은 builder 안에서 수행해 Root 위젯에는 타입이 맞춰진 값만 전달한다.

```dart
GoRoute(
  path: RoutePaths.ingredient, // '/Home/Ingredient/:recipeId'
  builder: (context, state) {
    final recipeId = int.parse(state.pathParameters['recipeId']!);
    return IngredientRoot(recipeId: recipeId);
  },
),
```

**Root 위젯 시그니처**:
```dart
class IngredientRoot extends StatelessWidget {
  final int recipeId;
  const IngredientRoot({super.key, required this.recipeId});
}
```

`IngredientRoot` 는 내부에서 `getIt<IngredientViewModel>()` 로 ViewModel 을 꺼내고 `loadRecipe(recipeId)` 를 디스패치한다.

---

## 화면 이동

### `context.go` vs `context.push`

- `context.go(path)` — 스택을 **교체**한다. 로그인 → 홈처럼 돌아갈 필요가 없을 때.
- `context.push(path)` — 스택에 **쌓는다**. 디테일 화면처럼 돌아갈 수 있어야 할 때.

```dart
// 교체: splash → sign in
context.go(RoutePaths.signIn);

// 푸시: 레시피 상세로 진입
context.push('/Home/Ingredient/${recipe.id}');
```

경로에 파라미터가 있으면 보간으로 만든다. 상수 외의 부분을 문자열로 조립해도 상위 경로 상수는 유지하는 것이 좋다.

### Root 위젯에서 쓰는 전형적 패턴

Root 위젯이 Action 을 받아 적절히 분기한다 (`saved_recipes_root.dart` 참고):

```dart
onAction: (action) {
  if (action is OnTapRecipe) {
    context.push('/Home/Ingredient/${action.recipe.id}');
    return;
  }
  viewModel.onAction(action);
},
```

즉 **상태를 바꾸는 Action** 은 ViewModel 로, **이동이라는 효과**는 `context.push` 로 분리한다.

---

## 바텀 내비게이션 — StatefulShellRoute

각 탭이 자기 스택을 유지해야 할 때 `StatefulShellRoute.indexedStack` 을 쓴다. `navigationShell.goBranch(index, initialLocation: ...)` 로 탭을 전환한다. `initialLocation: index == currentIndex` 로 두면 같은 탭을 다시 눌렀을 때 루트로 돌아가는 동작이 구현된다.

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) => MainScreen(
    body: navigationShell,
    currentPageIndex: navigationShell.currentIndex,
    onChangeIndex: (index) => navigationShell.goBranch(
      index,
      initialLocation: index == navigationShell.currentIndex,
    ),
  ),
  branches: [ /* 탭마다 StatefulShellBranch */ ],
)
```

---

## 콜백을 통해 느슨하게 결합하기

`SplashScreen`, `SignInScreen`, `SignUpScreen` 같은 단순 화면은 ViewModel 없이 콜백만 받는 형태로 구성된다. 라우터가 colback 을 주입해 Screen 이 경로 상수를 몰라도 되게 한다.

```dart
GoRoute(
  path: RoutePaths.signUp,
  builder: (context, state) => SignUpScreen(
    onTapSignIn: () => context.go(RoutePaths.signIn),
  ),
),
```

이 방식은 **테스트 가능한 Screen** 을 만드는 핵심이다. Screen 이 `go_router` 를 직접 import 하지 않는다.

---

## 체크리스트 — 새 화면 라우트 추가

- [ ] `RoutePaths` 에 경로 상수 추가
- [ ] `router.dart` 의 적절한 위치(탭 내부라면 `StatefulShellBranch` 안)에 `GoRoute` 추가
- [ ] builder 가 파라미터를 파싱해 Root 위젯에 전달
- [ ] Root 위젯 생성자는 파라미터를 타입 안전하게 받음
- [ ] 이동이 필요한 호출자는 `context.go` / `context.push` + `RoutePaths` 상수 사용
- [ ] 단순 화면은 Screen 파라미터로 콜백(`onTap...`)을 받아 느슨하게 결합

---

## 안티 패턴

- ❌ 경로 문자열을 화면 곳곳에 하드코딩 → `RoutePaths` 로 모아라.
- ❌ ViewModel 안에서 `context.go(...)` 호출 → ViewModel 은 `BuildContext` 를 모른다.
- ❌ Screen 에서 `go_router` 를 직접 import → 콜백 파라미터로 받게 바꿔라.
- ❌ 서로 다른 feature 간 이동을 위해 `Navigator.of(context).push(MaterialPageRoute(...))` 를 섞어 쓰기 → 일관된 `go_router` API 하나만 쓴다.
- ❌ 경로 파라미터 `state.pathParameters['id']` 에서 `!` 없이 기본값을 걸어 에러를 가림 → 파라미터가 필수라면 `int.parse(state.pathParameters['recipeId']!)` 처럼 강제 언래핑해 라우트 정의 오류가 즉시 드러나게 하라.
