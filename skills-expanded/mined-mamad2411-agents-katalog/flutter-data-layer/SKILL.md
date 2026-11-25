---
name: flutter-data-layer
description: |
  Flutter 프로젝트의 Data 레이어 패턴 — DataSource 인터페이스·구현, Repository, DTO와 도메인 모델 매핑, freezed 모델의 `fromJson`, 그리고 `rxdart`의 `BehaviorSubject`로 만드는 반응형 저장소. "DataSource 만들기", "Repository 구현", "리포지토리", "로컬/원격 데이터 소스", "BehaviorSubject", "스트림 저장소", "DTO 매핑", "fromJson" 같은 표현에 트리거합니다.
---

# Flutter Data 레이어

## 에러 처리 연계

Data 레이어가 반환하는 타입은 **flutter-error-handling** 스킬에서 정의한 `Result<D, E extends Error>` 를 기반으로 한다. 플랫폼 예외는 Data 레이어에서 catch 해 typed error 로 변환한다. 자세한 규칙은 해당 스킬을 참고.

---

## DataSource vs Repository

- **DataSource**: 단일 소스에 접근. 원격 API, 로컬 DB, 파일시스템, 클립보드 같은 단일 채널 하나만 다룬다. Data 레이어 대부분의 클래스가 여기 해당한다.
- **Repository**: 여러 DataSource를 **조합**해 도메인 관점으로 묶는다. 단일 소스만 쓰는데 굳이 "Repository" 이름을 붙이지 않는다.

이 프로젝트 기준:

```dart
// 단일 소스 → DataSource
abstract interface class RecipeDataSource {
  Future<List<Map<String, dynamic>>> getRecipes();
}

// 도메인 관점의 접근 API → Repository
abstract interface class RecipeRepository {
  Future<List<Recipe>> getRecipes();
  Future<Recipe?> getRecipe(int id);
}
```

Repository 인터페이스는 **도메인 타입(`Recipe`)** 을 주고받지만, DataSource 인터페이스는 **원시 타입/DTO(`Map`)** 를 주고받는다는 점이 핵심이다. 매핑은 Repository 구현체가 담당한다.

---

## 도메인 계약 (lib/domain)

- `lib/domain/` 은 순수 Dart 레이어다. `package:flutter/...` import 금지.
- 포함: 도메인 모델(`freezed`), Repository **인터페이스**, 에러 타입, UseCase.
- ViewModel이 쓰는 모든 Repository는 이 레이어에 인터페이스가 있어야 한다 — Presentation 이 Data를 직접 참조하지 못하도록 보장하기 위함.

```dart
// lib/domain/repository/recipe_repository.dart
abstract interface class RecipeRepository {
  Future<List<Recipe>> getRecipes();
  Future<Recipe?> getRecipe(int id);
}
```

---

## 도메인 모델 (freezed)

모델은 항상 `freezed` + `json_serializable` 조합으로 만든다.

```dart
// lib/domain/model/recipe.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'recipe_ingredient.dart';

part 'recipe.freezed.dart';
part 'recipe.g.dart';

@freezed
class Recipe with _$Recipe {
  const factory Recipe({
    required String category,
    required int id,
    required String name,
    required String image,
    required String chef,
    required String time,
    required double rating,
    required List<RecipeIngredient> ingredients,
    @Default(false) bool isFavorite,
  }) = _Recipe;

  factory Recipe.fromJson(Map<String, Object?> json) => _$RecipeFromJson(json);
}
```

파일 수정 후 반드시:
```
dart run build_runner build --delete-conflicting-outputs
```

---

## DataSource 구현

### 원격

```dart
// lib/data/data_source/remote/remote_recipe_data_source_impl.dart
class RemoteRecipeDataSourceImpl implements RecipeDataSource {
  @override
  Future<List<Map<String, dynamic>>> getRecipes() async {
    // http 호출 또는 mock
    await Future.delayed(const Duration(microseconds: 500));
    return _mockData['recipes']!;
  }
}
```

### 로컬

```dart
// lib/data/data_source/local/default_local_storage.dart
class DefaultLocalStorage implements LocalStorage {
  // SharedPreferences, sqflite 등으로 구현
}
```

**명명 규칙** (이 프로젝트 기준):
- 인터페이스: `RecipeDataSource`, `LocalStorage` — "무엇"을 나타내는 이름
- 구현: `RemoteRecipeDataSourceImpl`, `DefaultLocalStorage` — "어디/어떻게"를 나타내는 이름 + `Impl` 또는 기술명 접두어

Android 가이드라인과 다르게 이 프로젝트는 구현체에 `Impl` 접미어를 일관되게 사용하므로, 기존 컨벤션을 따른다.

---

## Repository 구현

Repository 구현체는 DataSource 결과를 도메인 모델로 **매핑**한다. `Map<String, dynamic>` 같은 raw 타입은 여기서 끝나야 한다.

```dart
// lib/data/repository/mock_recipe_repository_impl.dart
class MockRecipeRepositoryImpl implements RecipeRepository {
  final RecipeDataSource _recipeDataSource;

  const MockRecipeRepositoryImpl({
    required RecipeDataSource recipeDataSource,
  }) : _recipeDataSource = recipeDataSource;

  @override
  Future<List<Recipe>> getRecipes() async {
    final recipes = await _recipeDataSource.getRecipes();
    return recipes.map(Recipe.fromJson).toList();
  }

  @override
  Future<Recipe?> getRecipe(int id) async {
    final recipes = await getRecipes();
    return recipes.where((e) => e.id == id).firstOrNull;
  }
}
```

**핵심**:
- 생성자에서 DataSource 를 주입받는다. `get_it` 이 이걸 해결한다.
- `Repository` 인터페이스는 `domain` 에 있고, 구현은 `data` 에 있어 의존성 방향이 유지된다.
- 매핑은 `Recipe.fromJson` 같은 freezed 생성 팩토리를 이용한다. 별도 mapper 파일이 필요 없을 때가 많다.

---

## 반응형 저장소 — BehaviorSubject 패턴

이 프로젝트는 북마크처럼 **여러 화면이 같은 상태를 관찰**해야 할 때 `rxdart` 의 `BehaviorSubject` 를 쓴다. 최근 값이 있는 브로드캐스트 스트림이므로 새 구독자가 즉시 현재 상태를 받을 수 있다.

```dart
// lib/data/repository/mock_bookmark_repository_impl.dart
class MockBookmarkRepositoryImpl implements BookmarkRepository {
  final _ids = <int>{2, 3};
  final _controller = BehaviorSubject<Set<int>>();

  MockBookmarkRepositoryImpl() {
    _controller.add(_ids);
  }

  @override
  Stream<Set<int>> bookmarkIdsStream() => _controller.stream;

  @override
  Future<void> toggle(int id) async {
    if (_ids.contains(id)) {
      _ids.remove(id);
    } else {
      _ids.add(id);
    }
    _controller.add(_ids);
  }
}
```

**언제 쓰나**
- 저장/해제 같은 변이가 생긴 직후 다른 화면이 즉시 최신 상태를 봐야 할 때.
- 여러 feature가 동일한 데이터(북마크, 장바구니, 로그인 상태 등)를 공유해야 할 때.

**언제 쓰지 말아야 하나**
- 한 화면에서만 쓰고 재진입 시 다시 불러오면 충분한 데이터 → 그냥 `Future` 반환.

UseCase 에서 `BehaviorSubject` 스트림과 일회성 Future 를 합성할 때:

```dart
// lib/domain/use_case/get_saved_recipes_use_case.dart
Stream<List<Recipe>> execute() async* {
  final recipes = await _recipeRepository.getRecipes();

  await for (final ids in _bookmarkRepository.bookmarkIdsStream()) {
    yield recipes.where((e) => ids.contains(e.id)).toList();
  }
}
```

이 패턴이 깔끔하다: Repository는 원자적 데이터(전체 목록, id 집합)만 책임지고, 유즈케이스가 그걸 화면 목적에 맞게 합성한다.

---

## UseCase — Data와 Presentation 사이

UseCase는 "비즈니스 동작 하나"를 나타낸다. 이 프로젝트의 관례는:

- 위치: `lib/domain/use_case/<verb>_<noun>_use_case.dart`
- 단일 진입점 `execute(...)` 하나만 공개
- 상태 없음 (field 는 주입받은 의존성뿐)
- 여러 Repository 를 조합하거나, 도메인 규칙(필터링/정렬)을 적용
- 반환 타입: `Future<T>`, `Future<Result<D, E>>`, 또는 `Stream<T>`

```dart
class GetSavedRecipesUseCase {
  final RecipeRepository _recipeRepository;
  final BookmarkRepository _bookmarkRepository;

  const GetSavedRecipesUseCase({
    required RecipeRepository recipeRepository,
    required BookmarkRepository bookmarkRepository,
  })  : _recipeRepository = recipeRepository,
        _bookmarkRepository = bookmarkRepository;

  Stream<List<Recipe>> execute() async* { ... }
}
```

ViewModel 은 Repository 를 직접 호출해도 되지만, **여러 소스를 섞거나 도메인 규칙이 끼어드는 순간** UseCase 로 분리한다.

---

## 체크리스트 — 새 DataSource / Repository 추가

- [ ] `lib/domain/model/<name>.dart` — freezed 모델
- [ ] `lib/domain/repository/<name>_repository.dart` — `abstract interface class`
- [ ] `lib/data/data_source/{remote|local}/<name>_data_source_impl.dart` — 실제 소스 접근
- [ ] `lib/data/repository/<name>_repository_impl.dart` — DataSource 주입, 매핑, Repository 계약 구현
- [ ] 필요하면 `BehaviorSubject` 로 스트림 노출
- [ ] `diSetup()` 에 인터페이스 타입으로 등록
- [ ] `dart run build_runner build --delete-conflicting-outputs`

---

## 안티 패턴

- ❌ Repository 구현체가 `Map<String, dynamic>` 을 호출자에게 노출 → 매핑은 Data 레이어 안에서 끝나야 한다.
- ❌ `domain/` 파일에 `package:flutter/material.dart` import → 순수성이 깨진다.
- ❌ 구현 클래스 타입을 ViewModel/UseCase 에서 참조 → 인터페이스로 참조하라.
- ❌ UseCase 안에서 `Repository` 가 해야 할 캐싱/저장을 대신 처리 → 책임이 흐려진다.
