---
name: flutter-widget-ui
description: |
  Flutter 위젯 UI 작성 패턴 — StatelessWidget 선호, `const` 최적화, `ListenableBuilder`로 ViewModel 관찰, `ListView.builder`/`IndexedStack`, 공용 컴포넌트 재사용, 접근성(Semantics), 다이얼로그·스낵바 처리. "위젯 만들기", "UI 만들기", "StatelessWidget", "ListView", "ListenableBuilder", "Scaffold", "스낵바", "다이얼로그", "디자인 토큰", "공용 컴포넌트" 같은 표현에 트리거합니다.
---

# Flutter 위젯 UI 패턴

## 핵심 원칙

UI는 바보다. Screen 위젯은 `state` 와 `onAction` 을 받아 렌더링과 사용자 인터랙션만 담당한다. 비즈니스 로직, 데이터 변환, 네트워크 호출은 전부 ViewModel/UseCase/Data 레이어에서 끝난다. Screen 안에는 로직이 없어야 테스트와 디자인 리뷰가 쉬워진다.

---

## StatelessWidget을 기본으로

이 프로젝트의 거의 모든 화면은 `StatelessWidget` 이다. 상태는 ViewModel(`ChangeNotifier`)이 보관하고 `ListenableBuilder` 가 구독한다. `StatefulWidget` 은 다음 경우에만 쓴다:

- 위젯 생애주기 안에서만 의미 있는 로컬 UI 상태 (`TextEditingController`, `ScrollController`, `TabController`, 애니메이션 컨트롤러).
- `initState` / `dispose` 가 꼭 필요한 구독·리소스 초기화.

앱 전반 상태는 전부 ViewModel 로 옮긴다.

---

## `const` 를 최대한 활용하라

생성자 호출 앞의 `const` 는 리빌드 시 동일 인스턴스가 재사용되게 해 준다. 정적 위젯, 리터럴 스타일, `SizedBox(height: N)` 등 거의 모든 정적 노드에 `const` 를 붙인다.

```dart
const SizedBox(height: 10),
const ChefProfile(),
const Icon(Icons.share, size: 20),
```

하위 위젯이 `const` 생성자를 갖도록 작성해 재사용 경로를 열어준다.

---

## ViewModel 구독 — ListenableBuilder

Root 위젯에서 ViewModel 변화를 구독할 때의 표준 패턴은 `ListenableBuilder`. `builder` 안에서만 `viewModel.state` 를 읽어 불필요한 리빌드 범위를 줄인다.

```dart
return ListenableBuilder(
  listenable: viewModel,
  builder: (context, _) {
    final state = viewModel.state;
    if (state.isLoading) return const Center(child: CircularProgressIndicator());
    return IngredientScreen(state: state, onAction: viewModel.onAction);
  },
);
```

Screen 은 `ListenableBuilder` 를 몰라야 한다. 그 책임은 Root.

---

## 리스트 — ListView.builder

항목 수가 작더라도 고정 리스트는 `Column` 대신 `ListView.builder` 를 써서 확장에 대비한다.

```dart
ListView.builder(
  itemCount: state.ingredients.length,
  itemBuilder: (context, index) {
    return Column(
      children: [
        IngredientItem(ingredient: state.ingredients[index]),
        const SizedBox(height: 10),
      ],
    );
  },
)
```

큰 리스트이거나 키가 필요한 경우 `itemBuilder` 가 반환하는 위젯에 `Key(item.id.toString())` 를 넣어 재배치/삭제 시 상태가 섞이지 않게 한다.

**탭 간 전환**에서 상태를 보존하고 싶다면 `IndexedStack` 이 깔끔하다:
```dart
IndexedStack(
  index: state.selectedTabIndex,
  children: [IngredientList(state: state), ProcedureList(state: state)],
)
```

---

## 공용 컴포넌트 재사용

이 프로젝트는 `lib/core/presentation/components/` 에 디자인 시스템 격 위젯이 모여 있다. 새 화면에서 비슷한 버튼/카드/입력이 필요하면 **먼저 이 디렉터리를 뒤진다**. 예:

- `BigButton`, `MediumButton`, `SmallButton`
- `SearchInputField`, `InputField`
- `FilterButton`, `FilterButtons`, `RatingButton`
- `RecipeCard`, `NewRecipeCard`, `DishCard`, `IngredientRecipeCard`, `RecipeGridItem`
- `TwoTab`, `ChefProfile`, `IngredientItem`, `ProcedureItem`

없으면 같은 디렉터리에 새 컴포넌트를 추가한다. 두 번 이상 쓸 일이 있는 UI만 공용으로 올리고, 한 화면 전용이라면 해당 feature 폴더에 보조 위젯으로 둔다.

디자인 토큰은 `lib/ui/color_styles.dart`, `lib/ui/text_styles.dart` 에 있으므로 raw 색/폰트를 쓰지 않고 토큰을 재사용한다.

```dart
Text('1 serve', style: TextStyles.smallerTextRegular.copyWith(color: ColorStyles.gray3)),
```

---

## 다이얼로그와 스낵바

다이얼로그/스낵바는 `BuildContext` 가 필요하므로 **Root 위젯의 인터랙션 콜백**에서 띄운다. ViewModel 은 "어떤 메뉴가 선택됐다"는 Action 만 알면 된다.

```dart
// ingredient_root.dart
IngredientScreen(
  state: viewModel.state,
  onAction: viewModel.onAction,
  onTapMenu: (menu) {
    switch (menu) {
      case IngredientMenu.share:
        showDialog(
          context: context,
          builder: (_) => ShareDialog(
            link: 'app.Recipe.co/jollof_rice',
            onTapCopyLink: (link) {
              viewModel.onAction(IngredientAction.onTapShareMenu(link));
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Link Copied', textAlign: TextAlign.center)),
              );
            },
          ),
        );
      // ...
    }
  },
),
```

**요령**: 다이얼로그 닫기와 상태 반영을 같이 해야 한다면 콜백 안에서 `viewModel.onAction(...)` → `Navigator.pop(context)` → 후속 UI 표시 순서로.

---

## Scaffold 구성 관례

- `Scaffold` → `AppBar` → `SafeArea` → `Padding(horizontal: 30)` → `Column` 이 이 프로젝트의 기본 골격 (`ingredient_screen.dart` 참고). 수평 패딩을 `SafeArea` 안쪽에 두어 노치 회피와 일관 여백을 동시에 얻는다.
- `AppBar` 의 `actions` 는 `PopupMenuButton` 으로 메뉴를 꽂고, 각 `PopupMenuItem` 은 `onTap` 에서 Screen이 받은 콜백(`onTapMenu`)을 호출한다.

---

## 텍스트 필드

`TextField` / `TextFormField` 값은 **로컬 컨트롤러 + ViewModel Action** 로 이중화한다. 사용자 입력마다 Action 을 디스패치해 상태에 기록한다. 지속이 필요 없는 순수 로컬이라면 `StatefulWidget` + `TextEditingController` 만으로도 충분하다.

```dart
TextField(
  onChanged: (value) => onAction(SearchAction.onQueryChange(value)),
)
```

---

## 접근성

- 의미 있는 이미지/아이콘에는 `Semantics(label: '...')` 또는 `IconButton(tooltip: '...')` 을 달아 스크린리더 사용자를 배려한다.
- 텍스트 크기 변경에 대비해 고정 `height` 대신 `Padding` + `mainAxisSize` / `Expanded` 로 레이아웃을 구성한다.
- 터치 타깃은 최소 48×48 논리 픽셀. 작은 아이콘 버튼은 `IconButton` 이나 `InkWell` + 충분한 padding 으로 감싼다.

---

## 성능 요령

- `const` 생성자 적극 사용.
- 리스트 아이템에 무거운 계산이 있으면 `itemBuilder` 밖에서 미리 수행 (예: 포매팅은 UI 모델에 이미 반영).
- 애니메이션은 `AnimatedBuilder` / `TweenAnimationBuilder` / `ImplicitlyAnimatedWidget` 으로 리빌드 범위를 좁힌다. 프레임마다 부모 Scaffold 를 재빌드하지 않도록 애니메이션 영역을 작은 위젯으로 분리.
- 큰 이미지는 `cacheWidth`/`cacheHeight` 로 디코딩 크기를 제한한다.

---

## 체크리스트 — 새 Screen 위젯

- [ ] `StatelessWidget` 으로 선언하고 `state`, `onAction` 만 파라미터로 받는다
- [ ] Root 에서 전달된 네비게이션/다이얼로그 콜백이 있다면 추가 파라미터로 받는다
- [ ] 정적 자식은 전부 `const`
- [ ] 리스트는 `ListView.builder`, 탭 전환은 `IndexedStack` 검토
- [ ] 공용 컴포넌트(`core/presentation/components`)를 먼저 사용, 없으면 추가
- [ ] 색/폰트는 `ColorStyles`, `TextStyles` 사용
- [ ] `BuildContext` 가 필요한 효과(다이얼로그·스낵바·내비게이션)는 Root 에서 처리

---

## 안티 패턴

- ❌ Screen 안에서 `getIt<...>()` 호출 → Root 가 주입해야 한다.
- ❌ Screen 안에서 `context.push(...)` 직접 호출 → 콜백으로 위임.
- ❌ `setState` 로 앱 상태를 관리 → ViewModel 로 올려라.
- ❌ 매직 넘버 색상/폰트 직접 사용 → `ColorStyles` / `TextStyles` 를 쓴다.
- ❌ `Column` + 수동 스크롤 — 항목이 많아질 수 있으면 `ListView.builder`.
- ❌ `const` 생략으로 동일 위젯이 매 프레임 재생성.
