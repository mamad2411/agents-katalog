---
description: PPTX 생성 스크립트 실행 (PPTX 모드 전용)
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/generate_제안서.py` 를 실행해 PPTX를 생성합니다.

## 전제

`output/$ARGUMENTS/generate_제안서.py` 가 없으면 중단하고 안내:

> 이 커맨드는 **PPTX 모드 전용**입니다.
> HTML→Figma 모드라면 `/convert $ARGUMENTS` 를 사용하세요.
> PPTX 스크립트가 필요하면 `/p $ARGUMENTS --format pptx` 로 생성하세요.

## 실행

```bash
python3 "output/$ARGUMENTS/generate_제안서.py"
```

## 오류 처리

오류가 나면 수정 후 재실행합니다. 자주 나는 원인:

| 증상 | 원인 | 조치 |
|------|------|------|
| `TypeError: 함수명() got unexpected keyword` | slide_kit 시그니처 불일치 | `.claude/rules/pptx-rules.md` 확인 |
| 텍스트 넘침 / 겹침 | VStack 높이 계산 오류 | `python3 tools/visual_check.py` 로 Y좌표 진단 |
| `FileNotFoundError` (폰트) | Pretendard 미설치 | 기본 폰트로 폴백 후 경고 |

3회 이상 같은 오류가 반복되면 임의 수정을 멈추고 사용자에게 보고하세요.

## 완료

생성된 `.pptx` 경로를 안내하고 `/open $ARGUMENTS` 를 제안합니다.
