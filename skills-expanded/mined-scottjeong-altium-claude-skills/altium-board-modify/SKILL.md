---
name: altium-board-modify
description: "Modify an existing, already-routed Altium board (SchDoc + PcbDoc) — remove a circuit block, add a connector/module header, push the change through ECO, clear the old routing, rip up what collides, move parts and reroute — working inside the live Altium session via altium-mcp scripts and checking every step yourself. Use when an existing Altium board gets a new revision with parts removed or added, a daughter module is added, or ECO fails. Triggers: \"보드 수정\", \"이 보드 복사해서\", \"모듈 연결\", \"헤더 추가\", \"ECO\", \"Update PCB Document\", \"Footprint Not Found\", \"기존 배선 정리\", \"rip-up\", \"폴리곤\", \"Shelve\". 한국어: 이미 배선된 Altium 보드를 고치는 절차 — 복사 → 검토 시트 → 회로도 → ECO → 폴리곤 숨김 → 배치 → 비아·배선 정리 → 재배선 → 폴리곤 다시 붓기."
---

# 이미 배선된 Altium 보드 고치기

W3200 OCP 보드(`W3200_OCP_TEST_BOARD_IP101GRI_V001`)에서 보드 PHY(U3·RJ45)를 들어내고 IP101GRI MII 모듈용 2×12 암헤더 J3 를 넣으며(2026-11-04~11-10) 사용자에게 받은 정정이 이 스킬이다.
도구는 `scripts/` (그 보드 판 — 경로·부품 이름을 고쳐 쓴다), Altium 안 스크립트는 `scripts/altium_snippets.md`.

## 0. 원칙 (사용자 정정)

- **원본은 고치지 않는다 — 복사해서 새 폴더에서.** 설계 파일만(SchDoc·PcbDoc·OutJob·PrjPcb·PrjPcbStructure) 복사, History·출력·bak 제외. PrjPcb·PcbDoc·OutJob 이름을 바꾸고 PrjPcb 안 경로도 바꾼다 — **CRLF 유지**(git-bash sed 는 CR 을 지운다 → 파이썬 바이너리 치환). 「여기서 그대로 할 게 아니라 복사해서 새로운 곳에서」
- **설명에는 핀이 어느 쪽으로 나오는지·모듈 방향·1번 핀 좌표를 항상 넣는다.** 「모듈 아래로 핀헤더를 뽑나? 방향은? 그런 설명이 없잖아」
- **확인은 직접 한다.** 파일만 고쳐 놓고 사용자에게 「다시 해 보라」 하지 않는다 — ECO 도 Altium 에서 직접 돌려 결과를 보고 보고(세 번 떠넘겨서 크게 혼남). 「니가 해」
- **두 보드가 다르다고 말하기 전에 양쪽 파일 넷을 대조**(같은 회로인 모듈에 「PHY 주소가 바뀐다」 고 지어냈다)
- 설계안은 검토 시트로 먼저(연결표·들어낼 부품·배치·확인 필요) → 확인 뒤 회로도 → PCB
- 판단을 물으면 근거로 정해서 답한다(TXER: 「니가 판단해봐 어떤 게 안정적인지」 → 열린 선이 MII 옆을 달리면 내부 풀다운만으론 불안 → GND)

## 1. 배치 결정 (모듈·헤더를 얹을 때)

- **모듈은 보드 밖으로 나와도 된다**(「좀 보드 밖으로 나와도 되는 거 아니야?」). 보드 안에만 넣으려다 기구홀·커넥터와 부딪히지 않는다
- **헤더는 신호 출발점(칩 핀·TP 줄) 바로 옆에, 모듈 몸체는 그 반대쪽으로 내민다** — 선이 짧아지는 쪽으로 돌린다(「왜 길어져? 그럼 위로 빼도 되잖아」). 오른쪽으로 빼서 MII 가 15~20mm 길어지는 안을 냈다가 정정
- 모듈 끝은 기구홀 나사 머리(M3 ≈ 반지름 3mm)에서 떨어뜨린다 — 「오른쪽으로 더」 요청도 이 한계 안에서
- 모듈과 같은 회로·같은 핀 배정인지, 모듈에 이미 있는 풀업·풀다운·디캡을 보드에서 들어낼지(중복) 모듈 파일에서 넷으로 확인
- 헤더 전원 핀 옆에 0.1µF 하나(모듈 입구에 벌크·비드가 있으면 그것으로 충분). 회로도에서도 그 캡을 헤더 3V3 선 옆에 붙여 그린다
- 쓰지 않는 입력(예: TXER)은 칩 바로 옆 NC 면 내부 풀다운으로 되지만, **헤더까지 선이 나와 열려 있으면 GND 로**

## 2. 회로도 (altium_monkey, 파일로)

`scripts/sch_module.py` (원본에서 매번 다시 만든다) — 수정 전 SchDoc 을 `_eval/` 에 두고 거기서 생성
- 지울 구역(그 블록 객체만 있는 사각형)을 좌표로 확인한 뒤, 구역 안 배선 객체(선·라벨·포트·접점·No-ERC)와 지울 부품을 지운다. 남길 부품(예: C39)과 그 포트는 좌표로 빼 둔다. 갈래 하나만 자를 때는 선 점을 고친다
- 새 부품은 `add_component_from_library` + `add_footprint` — **그대로 두면 ECO 가 「Footprint Not Found」**:
  - 부품 레코드를 같은 라이브러리 기존 부품(J1)과 필드 단위로 맞춘다: `DesignItemId`·`LibraryPath '*'`·`TargetFileName '*'`·`PartCount`(부품 수+1)·`PartIDLocked`·`SourceLibraryName`
  - 구현 레코드에 `UseComponentLibrary`·`IntegratedModel`·`DatalinksLocked`·`DatabaseDatalinksLocked`·`DatabaseModel`
  - 새 객체는 `_raw_record` 가 None → 저장 후 다시 열어 넣는다
  - **그래도 IntLib 에서 못 찾았다**(기존 J1 은 PCB 에 이미 있어 찾을 일이 없었을 뿐). 최종 해결은 Altium 안에서 구현을 `UseComponentLibrary=False` + PcbLib 경로 지정(altium_snippets.md)
- 핀 간격이 100mil 인 헤더에 전원 포트를 핀마다 옆으로 달면 이웃 줄과 겹친다 → 전원 핀은 세로선(트렁크)으로 모아 포트 하나, 지정자는 몸체 위·값은 아래
- 남길 부품을 옮길 때는 지우고 다시 넣지 말고 좌표만(고유 ID 유지 → PCB 짝 유지)
- 검증: `scripts/net_diff.py <수정 전> <수정 후>` — 남은 부품 넷 변화 0, 새 부품 핀별 넷이 연결표대로
- Altium 이 그 SchDoc 을 열고 있으면 **저장하지 말고 닫았다 다시 열기**(열린 판을 저장하면 고친 파일을 덮는다)

## 3. ECO (Altium 에서 직접)

- `Design → Update PCB Document` 를 화면 클릭으로 실행하고 캡처로 본다
- 「Failed to match N of M Components using Unique identifiers」 → N 이 지운 부품 수와 같으면 Automatically Create Component Links
- `Only Show Errors` 를 끄면 지울 항목까지 보인다. 새 부품의 「Unknown Pin」 은 부품이 아직 없어서 나는 검증 단계 표시 — 풋프린트 오류가 없으면 Execute 로 풀린다
- 실행 뒤 부품 수(이전 − 지운 수 + 새 수)와 저장 시각을 파일로 확인

## 4. PCB 고치기 — 순서

1. **폴리곤을 숨긴다**: Tools → Polygon Pours → Shelve. 「폴리곤 그대로 두고 작업해? 원래 안 보이게 하고 작업하고 나중에 다시 붓잖아」
2. **새 부품 배치** — 좌표 환산을 기존 부품(TP 등)으로 확인하고 옮긴다. 옮긴 뒤 핀 좌표를 다시 읽어 방향 확인
3. **예전 배선 정리**: 덤프 → `scripts/prune_graph.py` → 목록대로 삭제 → 목록 수 = 지운 수 확인
   - 패드가 하나도 안 남은 넷(ECO 는 핀만 빼고 넷 이름은 선에 남긴다)은 통째로
   - 핀이 빠진 넷은 패드↔패드 최단 경로 위 선만 남긴다(막다른 선 반복 자르기는 비아 위 짧은 토막 고리에서 멈춘다)
   - **지운 부품 둘레 구역 안, 바뀐 넷만** — 범위를 안 걸면 패드 모양 근사 때문에 무관한 넷(VDD·WB_DATA)까지 지우려 한다
   - 「기존 배선 정리 안 하고 이것만 옮기면 될 거라고 생각했냐?」
4. **새 부품 자리·배선 통로의 비아 정리**(GND 스티치 등) — 「비아들은 그냥 두고 할 거야???」. 뒤에서 면 붓고 다시 넣는다
5. **새 부품 패드와 겹치는 다른 넷 배선을 미리 걷는다(rip-up)**: `scripts/ripup_plan.py` — 간격(0.2) 안에 드는 다른 넷 선·비아 + 그 넷의 끊긴 나머지를 패드·분기점까지. 걷은 뒤 다시 덤프해 충돌 0 확인. 「지금 겹치는 다른 배선들도 있잖아 이것도 미리 조치해야지」
6. 재배선(우회·새 연결) — 그림으로 먼저 보이고
7. 폴리곤 Restore → 다시 붓기 → 스티치 보강 → DRC

각 단계 전 PcbDoc 을 `_eval/` 에 백업, 단계 끝에 그 문서만 저장(`DoFileSave`).

## 5. 함정

- `run_altium_script` 는 짧게, 단계마다 로그. 멈추면 직접 Run → Stop(altium_snippets.md)
- 화면 클릭은 메뉴가 열린 걸 캡처로 보고 — 빗나가면 공유 라이브러리를 연다
- PC 잠금 화면이면 캡처가 엉뚱하다 → 덤프 숫자로 확인
- 같은 계열 메모: 메모리 altium-monkey-component-record-check, compare-before-claiming-diff, review-sheet-first
