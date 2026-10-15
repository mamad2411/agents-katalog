---
name: flutter-presentation-mvi
description: |
  Flutter 프로젝트의 Presentation 레이어 패턴 — `ChangeNotifier` 기반 ViewModel, freezed `State`와 sealed `Action`, Root/Screen 위젯 분리, `ListenableBuilder`로 관찰, 1회성 이벤트는 `StreamController`로 전달. "ViewModel 만들기", "State/Action", "MVI", "ChangeNotifier", "Root와 Screen 분리", "onAction", "notifyListeners", "ListenableBuilder" 같은 표현에 트리거합니다.
---

# Flutter Presentation 레이어 (MVI 스타일)

## 구성 요소

모든 화면은 다음 4가지로 구성되며, **파일은 2개**만 만든다:

1. **State** — freezed immutable 클래스. UI 에 필요한 모든 필드.
2. **Action** — freezed sealed class. 사용자가 유발할 수 있는 모든 동작.
3. **ViewModel** — `ChangeNotifier` 를 믹스인. State 를 보관하고 Action 을 처리.
4. **Root / Screen 위젯 분리** — Root 가 DI/이벤트/리빌드 구독을, Screen 이 순수 UI를 담당.

| 파일 | 포함 내용 |
|---|---|
| `<feature>_view_model.dart` | 파일 상단: State → Action, 파일 하단: ViewModel |
| `<feature>_screen.dart` | 파일 상단: Root, 파일 하단: Screen |

선택 요소: **Event (1회성 부작용)** — 스낵바/내비게이션 등 상태에 넣으면 안 되는 일회성 신호. `StreamController` 로 내보낸다.

---

## State

freezed 클래스. 기본값은 `@Default` 로 지정한다.

```dart
// lib/presentation/ingredient/ingredient_view_model.dart (파일 상단)
import 'package:flutter_recipe_app_course/domain/model/ingredient.dart';
import 'package:flutter_recipe_app_course/domain/model/procedure.dart';
import 'package:flutter_recipe_app_course/domain/model/recipe.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part 'ingredient_view_model.freezed.dart';
part 'ingredient_view_model.g.dart';

@freezed
class IngredientState with _$IngredientState {
  const factory IngredientState({
    Recipe? recipe,
    @Default([]) List<Ingredient> ingredients,
    @Default([]) List<Procedure> procedures,
    @Default(0) int selectedTabIndex,
  }) = _IngredientState;

  factory IngredientState.fromJson(Map<String, Object?> json) =>
      _$IngredientStateFromJson(json);
}
```

**규칙**:
- 모든 UI 상태는 State 에만 있다. ViewModel 인스턴스 필드로 UI 관련 변수를 흩뿌리지 않는다.
- State 업데이트는 항상 `copyWith(...)` 로 새 인스턴스를 만들고 `_state` 에 재할당한 뒤 `notifyListeners()`.

---

## Action

`freezed` + `sealed` 로 선언해 `switch` 가 모든 케이스를 강제하도록 만든다.

```dart
// lib/presentation/ingredient/ingredient_view_model.dart (State 바로 아래)
import 'package:flutter_recipe_app_course/domain/model/recipe.dart';

@freezed
sealed class IngredientAction with _$IngredientAction {
  const factory IngredientAction.onTapFavorite(Recipe recipe) = OnTapFavorite;
  const factory IngredientAction.onTapIngredient() = OnTapIngredient;
  const factory IngredientAction.onTapProcedure() = OnTapProcedure;
  const factory IngredientAction.loadRecipe(int recipeId) = LoadRecipe;
  const factory IngredientAction.onTapShareMenu(String link) = OnTapShareMenu;
}
```

**명명**: `on<Trigger>` 또는 동사형(`load...`). 각 factory는 클래스 타입(`OnTapFavorite`)도 같이 정의해 `switch` 패턴 매칭에서 쓴다.

---

## ViewModel

```dart
// lib/presentation/ingredient/ingredient_view_model.dart (Action 바로 아래)
class IngredientViewModel with ChangeNotifier {
  final IngredientRepository _ingredientRepository;
  final ProcedureRepository _procedureRepository;
  final GetDishesByCategoryUseCase _getDishesByCategoryUseCase;
  final ClipboardService _clipboardService;

  IngredientState _state = const IngredientState();
  IngredientState get state => _state;

  IngredientViewModel({
    required IngredientRepository ingredientRepository,
    required ProcedureRepository procedureRepository,
    required GetDishesByCategoryUseCase getDishesByCategoryUseCase,
    required ClipboardService clipboardService,
  })  : _ingredientRepository = ingredientRepository,
        _procedureRepository = procedureRepository,
        _getDishesByCategoryUseCase = getDishesByCategoryUseCase,
        _clipboardService = clipboardService;

  void onAction(IngredientAction action) async {
    switch (action) {
      case LoadRecipe():
        _loadRecipe(action.recipeId);
      case OnTapIngredient():
        _state = state.copyWith(selectedTabIndex: 0);
        notifyListeners();
      case OnTapProcedure():
        _state = state.copyWith(selectedTabIndex: 1);
        notifyListeners();
      case OnTapShareMenu():
        _clipboardService.copyText(action.link);
      // ... 나머지 케이스
    }
  }
}
```

**규칙**:
- `with ChangeNotifier` 믹스인을 쓴다. Flutter의 표준이며 `ListenableBuilder` 와 자연스럽게 결합된다.
- 단일 공개 메서드 `onAction(Action action)` 에서 `switch` 로 디스패치한다. 개별 public 메서드를 늘리지 않는다 — Screen 이 ViewModel을 타입적으로 덜 알게 된다.
- `_state = state.copyWith(...); notifyListeners();` 의 순서를 지킨다. 동일 프레임 내 여러 변경은 한 번의 `copyWith` 로 합친다.
- 생성자 주입으로만 의존성을 받는다. `getIt` 을 ViewModel 내부에서 호출하지 않는다.
- `StreamSubscription` 이 있으면 `@override void dispose()` 에서 반드시 `cancel()` 한다.

---

## 스트림 구독 패턴

UseCase가 `Stream` 을 반환하면 ViewModel 생성자 또는 action 핸들러에서 구독하고, `dispose` 에서 취소한다.

```dart
class SavedRecipesViewModel with ChangeNotifier {
  StreamSubscription? _streamSubscription;

  SavedRecipesViewModel({required GetSavedRecipesUseCase getSavedRecipesUseCase})
      : _getSavedRecipesUseCase = getSavedRecipesUseCase {
    _streamSubscription = _getSavedRecipesUseCase.execute().listen((recipes) {
      _state = state.copyWith(recipes: recipes);
      notifyListeners();
    });
  }

  @override
  void dispose() {
    _streamSubscription?.cancel();
    super.dispose();
  }
}
```

---

## 일회성 이벤트 (스낵바, 내비게이션)

상태로 표현하면 리빌드마다 다시 실행될 수 있다. `StreamController` 를 통해 한 번만 흘려보낸다.

```dart
class HomeViewModel with ChangeNotifier {
  final _eventController = StreamController<NetworkError>();
  Stream<NetworkError> get eventStream => _eventController.stream;

  // 실패 시
  _eventController.add(result.error);
}
```

Root 위젯에서는 `StreamBuilder` 대신 `initState` 의 `listen` 으로 구독해 Snackbar 를 띄운다 (Widget 트리 밖의 부작용이므로).

---

## Root / Screen 분리

`<feature>_screen.dart` 한 파일 안에 두 클래스가 공존한다:
- 파일 **상단**: `Root` — DI + 이벤트 구독 + `ListenableBuilder`
- 파일 **하단**: `Screen` — 순수 UI. `state` 와 `onAction` 만 props 로 받음

### Root 위젯

```dart
// lib/presentation/ingredient/ingredient_screen.dart (파일 상단)
class IngredientRoot extends StatelessWidget {
  final int recipeId;
  const IngredientRoot({super.key, required this.recipeId});

  @override
  Widget build(BuildContext context) {
    final viewModel = getIt<IngredientViewModel>();
    viewModel.onAction(IngredientAction.loadRecipe(recipeId));

    return ListenableBuilder(
      listenable: viewModel,
      builder: (context, _) {
        if (viewModel.state.recipe == null) {
          return const Center(child: CircularProgressIndicator());
        }
        return IngredientScreen(
          state: viewModel.state,
          onAction: viewModel.onAction,
          onTapMenu: (menu) { /* 다이얼로그·네비게이션 */ },
        );
      },
    );
  }
}
```

- `getIt<>()` 호출은 여기서만 일어난다.
- `ListenableBuilder(listenable: viewModel, ...)` 로 `notifyListeners()` 변경을 구독한다.
- 초기 데이터 로딩을 위해 `build` 안에서 `onAction(... load)` 을 호출하는 것은 이 프로젝트의 기존 관례다. 단, 재빌드마다 재로딩되지 않도록 ViewModel 내부에서 중복 요청을 방지하거나(이미 로드됐다면 무시), Root 를 `StatefulWidget` 으로 올려 `initState` 에서 호출해도 된다. **복잡한 초기화가 있다면 `StatefulWidget` 으로 승격하는 쪽이 안전하다.**

### Screen 위젯

```dart
// lib/presentation/ingredient/ingredient_screen.dart (파일 하단)
class IngredientScreen extends StatelessWidget {
  final IngredientState state;
  final void Function(IngredientAction action) onAction;
  final void Function(IngredientMenu menu) onTapMenu;

  const IngredientScreen({
    super.key,
    required this.state,
    required this.onAction,
    required this.onTapMenu,
  });

  @override
  Widget build(BuildContext context) { /* 순수 UI */ }
}
```

- `ViewModel` 에 대한 참조가 없다. 테스트와 위젯 프리뷰가 독립적으로 가능하다.
- 네비게이션이나 다이얼로그가 필요한 인터랙션은 `onTapMenu` 같은 추가 콜백으로 분리해 Root 가 처리하게 한다 — Screen 이 `context.go` 같은 go_router 호출을 직접 하지 않는다.

---

## Action이 아닌 콜백을 쓸 때

Screen 에서 네비게이션/다이얼로그처럼 **context 가 필요한** 인터랙션은 별도 `onTap*` 콜백을 두고 Root 에서 처리한다. 이유는 두 가지:

1. ViewModel 은 `BuildContext` 를 모른다 (테스트 용이성).
2. 네비게이션은 "상태 변경"이 아니라 "효과"라서 Action에 섞으면 모델이 지저분해진다.

예: `saved_recipes_root.dart` 는 `onAction` 콜백 안에서 `OnTapRecipe` 를 가로채 `context.push(...)` 로 이동시키고, 나머지 Action은 ViewModel로 넘긴다.

```dart
onAction: (action) {
  if (action is OnTapRecipe) {
    context.push('/Home/Ingredient/${action.recipe.id}');
    return;
  }
  viewModel.onAction(action);
},
```

---

## UI 모델 (필요할 때)

도메인 모델에 표시 포맷(`"3일 전"`, `"20 min"`)이 얽혀 있으면 Presentation 전용 UI 모델을 만든다. 기본적으로는 도메인 모델을 그대로 쓰고, **포매팅이 복잡해질 때만** UI 모델로 분리한다.

---

## 체크리스트 — 새 화면 추가

- [ ] `lib/presentation/<feature>/<feature>_view_model.dart` — 상단: freezed State → sealed Action, 하단: `with ChangeNotifier` ViewModel, `onAction` 단일 진입
- [ ] `lib/presentation/<feature>/<feature>_screen.dart` — 상단: Root(`getIt`, `ListenableBuilder`, 이벤트 구독), 하단: Screen(state + onAction 만 받는 순수 UI)
- [ ] `diSetup()` 에 ViewModel을 `registerFactory` 로 등록
- [ ] 필요하면 `StreamController` 로 1회성 이벤트 노출
- [ ] `build_runner build` 로 freezed 파일 생성

---

## 안티 패턴

- ❌ Screen 위젯이 `getIt<>()` 를 호출 → Root 위젯으로 끌어올려라.
- ❌ ViewModel 이 `BuildContext` 나 `GoRouter` 를 참조 → 네비게이션은 Root 콜백으로.
- ❌ 여러 공개 메서드(`loadRecipe()`, `onTapBack()`, `onSelectTab()`)를 두고 Screen에서 호출 → `onAction(Action)` 하나로 좁혀라.
- ❌ State 변경 후 `notifyListeners()` 누락 → 리빌드가 일어나지 않는다.
- ❌ `StreamSubscription` 을 `dispose` 에서 취소하지 않음 → 메모리 누수와 ghost callback.
- ❌ 상태에 스낵바 메시지를 담아 매 리빌드마다 다시 표시 → `StreamController` 이벤트로 내보내라.
