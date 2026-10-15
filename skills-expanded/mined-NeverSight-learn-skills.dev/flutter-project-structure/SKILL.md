---
name: flutter-project-structure
description: |
  Flutter 단일 패키지 프로젝트의 레이어 구조, 디렉터리 규칙, 의존성 방향을 정리한 스킬. 새 기능을 어디에 둘지, 새 화면·리포지토리·유즈케이스를 어느 디렉터리에 만들지, "폴더 구조를 어떻게 잡을까", "feature를 어디에 둘까", "core에 넣을까 말까" 같은 질문이 나올 때 반드시 사용하세요. "프로젝트 구조", "디렉터리 구조", "레이어 분리", "clean architecture", "where does X live", "새 기능 추가" 같은 표현에 트리거합니다.
---

# Flutter 프로젝트 구조 (단일 패키지 / Clean Architecture)

## 핵심 원칙

- **단일 패키지, 레이어 분리**: Android/KMP처럼 Gradle 멀티모듈을 쓰지 않고 `lib/` 하위에서 레이어로 분리한다.
- **Clean Architecture 의존성 방향**: `presentation` → `domain` ← `data`. `domain`은 아무것도 의존하지 않는 순수 Dart 레이어.
- **Feature는 `presentation` 하위에 폴더로 표현한다.** 여러 화면에서 공유되는 코드는 `core/`로 올리고, 단일 기능에만 쓰이는 코드는 해당 feature 폴더 안에 둔다.
- **Feature 간 직접 참조 금지**. 교차 기능 공유 로직은 `core`(공유 위젯·유틸) 또는 `domain`(모델·유즈케이스)으로 올린다.

---

## 디렉터리 레이아웃

이 프로젝트는 아래 구조를 따른다 (`lib/` 기준):

```
lib/
├─ main.dart                          ← 앱 진입점, diSetup() 호출, MaterialApp.router
├─ core/                              ← 전역 공유 인프라
│  ├─ di/di_setup.dart                ← get_it 모듈 등록
│  ├─ routing/router.dart             ← GoRouter 정의
│  ├─ routing/route_paths.dart        ← 경로 상수
│  ├─ domain/error/                   ← Error, Result, NetworkError
│  └─ presentation/
│     ├─ components/                  ← 공용 위젯 (BigButton, SearchInputField 등)
│     └─ dialogs/                     ← 공용 다이얼로그
├─ data/
│  ├─ data_source/                    ← DataSource 인터페이스 + 구현 (local/, remote/)
│  ├─ repository/                     ← Repository 구현체 (*Impl)
│  └─ clipboard/                      ← 기타 플랫폼 서비스 구현
├─ domain/
│  ├─ model/                          ← freezed 도메인 모델
│  ├─ repository/                     ← Repository 인터페이스 (abstract interface class)
│  ├─ use_case/                       ← UseCase 클래스 (execute() 단일 진입점)
│  ├─ clipboard/                      ← 플랫폼 서비스 인터페이스
│  ├─ error/                          ← 기능별 Error enum
│  └─ filter/                         ← 도메인 값 객체
├─ presentation/
│  └─ <feature>/
│     ├─ <feature>_view_model.dart    ← 파일 상단: freezed State·Action, 하단: ChangeNotifier VM
│     └─ <feature>_screen.dart        ← 파일 상단: Root(VM 주입), 하단: Screen(순수 UI)
└─ ui/                                ← 색상/타이포 등 디자인 토큰
```

실제 예: `lib/presentation/ingredient/`, `lib/presentation/saved_recipes/`, `lib/presentation/home/`.

각 feature는 파일 2개로 구성된다:

**`<feature>_view_model.dart` 내부 구성**
```dart
// ① State (freezed)
@freezed
class IngredientState with _$IngredientState {
  const factory IngredientState({ ... }) = _IngredientState;
}

// ② Action (freezed sealed)
@freezed
sealed class IngredientAction with _$IngredientAction {
  const factory IngredientAction.load() = Load;
  const factory IngredientAction.delete(String id) = Delete;
}

// ③ ViewModel
class IngredientViewModel extends ChangeNotifier {
  IngredientState _state = const IngredientState();
  IngredientState get state => _state;

  void onAction(IngredientAction action) { ... }
}
```

**`<feature>_screen.dart` 내부 구성**
```dart
// ① Root — getIt으로 VM 주입, ListenableBuilder로 상태 감지
class IngredientRoot extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final vm = getIt<IngredientViewModel>();
    return ListenableBuilder(
      listenable: vm,
      builder: (_, __) => IngredientScreen(
        state: vm.state,
        onAction: vm.onAction,
      ),
    );
  }
}

// ② Screen — 순수 UI, state·onAction만 인자로 받음
class IngredientScreen extends StatelessWidget {
  const IngredientScreen({required this.state, required this.onAction});
  final IngredientState state;
  final void Function(IngredientAction) onAction;

  @override
  Widget build(BuildContext context) { ... }
}
```

---

## 어디에 무엇을 두는가

| 코드 성격 | 위치 | 실제 예 |
|---|---|---|
| 도메인 모델 (freezed) | `lib/domain/model/` | `recipe.dart`, `ingredient.dart` |
| Repository 인터페이스 | `lib/domain/repository/` | `recipe_repository.dart` |
| UseCase | `lib/domain/use_case/` | `get_saved_recipes_use_case.dart` |
| DataSource 인터페이스 | `lib/data/data_source/` | `recipe_data_source.dart` |
| DataSource 구현 | `lib/data/data_source/{local,remote}/` | `remote_recipe_data_source_impl.dart` |
| Repository 구현 | `lib/data/repository/` | `mock_recipe_repository_impl.dart` |
| State + Action + ViewModel | `lib/presentation/<feature>/<feature>_view_model.dart` | `ingredient_view_model.dart` |
| Root + Screen 위젯 | `lib/presentation/<feature>/<feature>_screen.dart` | `ingredient_screen.dart` |
| 공용 위젯 | `lib/core/presentation/components/` | `big_button.dart` |
| 라우트 정의 | `lib/core/routing/router.dart` | — |
| DI 등록 | `lib/core/di/di_setup.dart` | — |
| 공유 에러 타입 | `lib/core/domain/error/` | `result.dart`, `network_error.dart` |
| 기능별 에러 | `lib/domain/error/` | `bookmark_error.dart`, `new_recipe_error.dart` |

---

## 의존성 규칙

| 레이어 | 의존 가능 |
|---|---|
| `presentation` | `domain`, `core` |
| `data` | `domain`, `core` |
| `domain` | 다른 `domain` 파일, `core/domain` (순수 Dart만). **절대 `data`, `presentation`, `flutter/material` 금지** |
| `core/presentation` | `flutter/material`, `core/domain` |
| `core/domain` | 순수 Dart만 |

`domain/` 파일에서는 `package:flutter/...` import가 나타나면 안 된다. 순수 Dart로 유지해 테스트와 재사용성을 확보한다.

---

## 기능을 추가할 때 (체크리스트)

새 feature(예: `reviews`)를 추가할 때:

- [ ] `lib/domain/model/review.dart` — freezed 모델 정의
- [ ] `lib/domain/repository/review_repository.dart` — `abstract interface class`로 인터페이스 정의
- [ ] `lib/domain/error/review_error.dart` — 필요한 경우 feature별 에러 enum (`implements Error`)
- [ ] `lib/domain/use_case/get_reviews_use_case.dart` — 단일 `execute()` 를 가진 UseCase
- [ ] `lib/data/data_source/remote/remote_review_data_source_impl.dart` — 구현
- [ ] `lib/data/repository/mock_review_repository_impl.dart` 또는 실제 구현
- [ ] `lib/presentation/reviews/reviews_view_model.dart` — 파일 상단에 `ReviewsState`, `ReviewsAction`, 하단에 `ReviewsViewModel`
- [ ] `lib/presentation/reviews/reviews_screen.dart` — 파일 상단에 `ReviewsRoot`, 하단에 `ReviewsScreen`
- [ ] `lib/core/di/di_setup.dart` 에 DataSource, Repository, UseCase, ViewModel 등록
- [ ] `lib/core/routing/route_paths.dart` 에 경로 상수, `router.dart` 에 `GoRoute` 추가

이 순서를 지키면 각 레이어가 하위 레이어만 알게 되어 의존성이 뒤집히지 않는다.

---

## `core`에 올릴지 feature에 둘지 판단

**feature 폴더 안에 두는 경우**
- 그 feature에서만 쓰는 State, Action, ViewModel, UI 모델, 화면 전용 위젯.
- 예: `ingredient_state.dart` 는 `lib/presentation/ingredient/` 아래에 있고 다른 feature에서 쓰지 않는다.

**`core`로 올리는 경우**
- 2개 이상 feature가 실제로 쓰는 위젯/유틸/에러.
- 예: `BigButton`, `SearchInputField`, `Result`, `NetworkError`.
- 단, "언젠가 공유될 것 같다"는 이유만으로는 올리지 않는다. 실제 두 번째 사용처가 생길 때 이동한다.

---

## 핵심 라이브러리

| 관심사 | 라이브러리 | 용도 |
|---|---|---|
| DI | `get_it` | `GetIt.instance` 기반 싱글톤/팩토리 등록 |
| 라우팅 | `go_router` | 선언적 라우팅, `StatefulShellRoute` |
| 모델/상태/액션 | `freezed` + `freezed_annotation` | sealed/immutable 데이터 클래스 |
| JSON | `json_serializable` + `json_annotation` | `fromJson`/`toJson` 생성 |
| 스트림 | `rxdart` | `BehaviorSubject`로 반응형 저장소 |
| 테스트 | `flutter_test` | 위젯/단위 테스트 |

모든 코드 생성이 필요한 파일(`*.freezed.dart`, `*.g.dart`)은 `dart run build_runner build --delete-conflicting-outputs` 로 만든다.
