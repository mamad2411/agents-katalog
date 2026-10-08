---
name: mvvm-architecture
description: 이 저장소의 MVVM 계층 배치 규칙. 파일을 추가·이동·리팩토링하거나 새 화면·새 파이프라인 단계를 만들 때 어느 폴더에 두고 무엇을 import·참조해도 되는지 판단하는 데 사용한다.
---

# MVVM 배치 규칙

폴더 경계가 곧 실행 문맥 경계다. 채택 근거는 `DESIGN.md` 1.1절, 현재 스냅샷은 `docs/architecture/folder-structure.md`. 이 skill은 안정적인 배치·의존 규칙만 소유한다.

## 계층과 의존 방향

```
App  →  View  →  ViewModel  →  Model
```

- `View`는 `ViewModel`과 Model의 불변 값 타입(`MinimapSnapshot`, `ScanEvent`, `ScanOutput`, `ColoredMesh`, `GridPointCloud`)만 참조한다. Model 객체(`ARSessionManager`, `ScanPipeline`, `OccupancyGrid`, `MinimapRenderer`, `DepthFrameProcessor`)를 직접 호출하지 않는다. 화면 상태(전체화면 열림, 측정점, 세계 창)는 View의 `@State`가 아니라 ViewModel이 소유한다 — View의 `@State`는 제스처 진행 중 기준값·마운트 지연 같은 순수 표시 임시값만.
- Model → ViewModel 출력은 `ARSessionManager.outputs`(`AsyncStream<ScanOutput>`) 하나로만 흐른다. 새 출력이 필요하면 콜백을 추가하지 말고 `ScanOutput` case를 추가한다.
- `ViewModel`은 `Model`을 소유·호출하고 `View`를 모른다. `SwiftUI`·`UIKit`을 import하지 않는다 (`ARKit`은 세션 타입 때문에 허용).
- `Model`은 `ViewModel`·`View`를 모른다. `SwiftUI`·`UIKit`·`Observation`을 import하지 않는다. 최상위 타입은 `nonisolated`를 명시한다.
- 위 규칙은 `scripts/check-structure.sh`가 grep으로 검사한다. 스크립트가 잡지 못하는 위반(간접 참조 등)은 리뷰에서 본다.

## 무엇을 어디에 두는가

| 만드는 것 | 위치 | 이름 |
| --- | --- | --- |
| 새 화면 | `View/<Screen>View.swift` + `ViewModel/<Screen>ViewModel.swift` | 화면 이름 접두 |
| 화면 일부 컴포넌트 (독립 재사용) | `View/<Name>View.swift` | |
| UIKit/RealityKit 래퍼 | `View/` (`UIViewRepresentable`) — Model 객체 대신 콜백을 받는다 | `<Name>View.swift` |
| UI 상태 enum, 이벤트 → 상태 변환 | 해당 `ViewModel` 파일 안 | |
| 파이프라인 단계 (순수 함수) | `Model/<Name>.swift`, `nonisolated enum` | 동사형 (`Processor`, `Renderer`) |
| 큐 전용 가변 상태 | `Model/<Name>.swift`, `nonisolated final class` | |
| 계층을 넘는 값 (스냅샷, 이벤트) | 생산하는 Model 파일 안, `Sendable` 불변 struct/enum. Model → ViewModel은 `ScanOutput` case로 |
| 파이프라인 단계 추가 (누적·렌더 계열) | `ScanPipeline.process` 안 또는 그것이 호출하는 순수 함수. 게이트 판정은 `ARSessionManager` | |
| 튜닝 파라미터 | 사용하는 Model 타입의 `static let` 상수 + `DESIGN.md` 표 | |

- 폴더는 네 개로 유지한다. 하위 폴더는 같은 계층 파일이 8개를 넘어 탐색이 불편해질 때만 만든다.
- 구현이 하나인 protocol, 단순 위임만 하는 UseCase·Repository 계층은 만들지 않는다 (`TECH_RULES.md` 금지).
- 파일을 옮기면 `docs/architecture/folder-structure.md`를 같은 커밋에서 갱신한다. `project.pbxproj`는 손대지 않는다.

## 확장 조건

- 화면이 셋 이상이고 화면 간 공유 상태가 생기면 `Features/<Feature>/{Model,ViewModel,View}` 상위 폴더를 검토한다. 그때 이 skill의 규칙도 함께 개정한다.
- Model 객체를 View에서 직접 써야 할 것 같으면, 먼저 ViewModel에 중계 메서드를 두는 쪽이 더 짧은지 본다 (`ScanViewModel.attach(session:)`이 선례).
