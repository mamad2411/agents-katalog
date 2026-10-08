# 작업자 진입점 — Chemvas

공장 공통 규칙은 `~/manual/AGENTS.md`가 지정하는 순서를 따른다(`FACTORY_MANUAL.md` →
자기 사이트 장부 → 이 파일). 여기에는 그 규칙을 복제하지 않고, **이 레포에만 해당하는
운영 사실**만 둔다.

## 이 레포가 무엇인가

PyQt6 기반 2D 화학 구조 드로잉 데스크톱 앱이자 오픈소스 연구 소프트웨어(MIT, PyPI
`chemvas`)다. 정비는 WSL `/home/daehyupsohn/Chemvas`가 canonical이다.

## 검증

```bash
make check
```

Ruff·format·mypy를 돌린 뒤 **테스트를 `test_*.py` 파일마다 별도 pytest 프로세스로**
실행한다(offscreen). Qt가 모듈 간에 완전히 리셋되지 않는 전역 상태를 유지하므로, 전체를
한 프로세스에 몰아넣은 실행은 통과해도 CI를 대표하지 않는다 — 이 루프가 게이트다.
`machine.json` 적합성 검증은 게이트가 `~/machine_contracts`의 정본 validator를 직접
연결한다(`FACTORY_MACHINE_CONTRACT_REPO`로 위치 변경 가능). 해당 테스트를 직접 돌릴
때도 validator 경로가 없으면 검증 없이 성공하지 않고 실패한다. 만진 파일만 좁혀 돌리려면:

```bash
bash scripts/check.sh tests/test_<area>.py
```

## 고치기 전에 읽을 것

| 무엇을 만지는가 | 원본 |
| --- | --- |
| 모듈 경계·마이그레이션 규칙·테스트 관례 | [CONTRIBUTING.md](CONTRIBUTING.md) — 구조 변경 전 필독, `tests/test_architecture_boundaries.py`가 강제한다 |
| 릴리스 절차 | [RELEASING.md](RELEASING.md) |
| `machine.json` 공통 봉투 | `~/machine_contracts`의 `COMPATIBILITY.md`(v1 동결) |

`machine.json` 표면을 바꾸려면 `machine-contracts`에 먼저 랜딩·릴리스하고, 이 레포 CI의
pin(`.github/workflows/ci.yml`의 `ref:`)을 의도적으로 전진시킨다.

## `make check`가 흡수하지 못하는 것

- **RDKit·wheel 스모크는 CI 전용이다.** 선택적 RDKit 백엔드와 휠 패키징이 걸린 변경은
  CI의 `rdkit-smoke`·`package-smoke` 잡이 판정한다.
- **GUI 실검증은 별도다.** offscreen 스위트는 실제 창·입력기·Wayland 상호작용을 증명하지
  않는다 — 캔버스가 걸린 변경은 실캔버스 확인을 따로 한다.
- **사용자 문서(`.chemvas`)는 실물이다.** 라이브 확인에 쓴 문서에 테스트 잔여물이 남지
  않았는지 되돌려 확인한다.
