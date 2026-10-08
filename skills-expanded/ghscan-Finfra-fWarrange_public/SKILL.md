---
name: LogMonitor Skill
description: 실시간 키 입력 및 앱 로그 모니터링 환경을 구성합니다.
title: LogMonitor Skill
date: 2026-03-26
---

이 스킬은 fWarrange의 디버깅을 위해 로컬 키 입력(KeyLogger)과 앱 로그(`flog.log`)를 모니터링할 수 있는 환경을 자동으로 구성합니다.

# 필수 조건 (Prerequisites)
* KeyLogger 바이너리가 `resources/key_code/`에 존재해야 함.
* `/tmp` 디렉토리 쓰기 권한.

# 사용법 (Usage)

`scripts` 디렉토리의 `setup-log-monitor.sh`를 실행하여 모니터링 환경을 셋업합니다.

```bash
/bin/bash .agent/skills/log-monitor/scripts/setup-log-monitor.sh
```

# 기능 (Features)
1. `~/.tmp` 디렉토리 생성 및 환경 구성.
2. `KeyLogger` 바이너리를 `~/.tmp`로 복사.
3. 앱 로그(`flog.log`)를 `~/.tmp/flog.log`로 심볼릭 링크 생성.
4. KeyLogger 프로세스 실행 여부 확인 및 안내.

# 고급 모니터링 (Advanced Monitoring)
새로 추가된 `monitor.sh` 스크립트를 사용하여 로그를 분석할 수 있습니다.

```bash
sh .agent/skills/log-monitor/scripts/monitor.sh
```

**기능**:
* **Startup Log**: 앱 초기화 로그 추출
* **Layout Verification**: 창 레이아웃 동작 여부 확인
* **Spam Analysis**: 상위 반복 로그 분석

# 모니터링 시작 방법 (Manual)
설정이 완료된 후, 별도의 터미널 탭에서 다음 명령어를 실행하여 모니터링을 시작하세요:

```bash
# 앱 로그 모니터링
tail -f ~/Documents/finfra/fWarrangeData/logs/flog.log

# 키 입력 로그 모니터링
tail -f /tmp/fkey.log
```
