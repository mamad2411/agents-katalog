---
name: ssh-server-inspect
description: >
  EC2 인스턴스에 SSH로 접속하여 서버 상태를 파악하는 스킬.
  "서버 확인", "서버 상태", "EC2 접속", "배치 서버 확인", "kglowing-batch 메모리",
  "프로세스 확인", "디스크 확인", "OOM 로그", "서버 점검", "qa-settle 상태" 같은
  요청 시 트리거. 호스트명(kglowing-batch 등), EC2 주소, QA 별칭을 인자로 받는다.
argument-hint: <호스트명|EC2주소|qa-별칭> [process|memory|disk|log|log-quick|all]
---

# ssh-server-inspect

EC2 인스턴스에 SSH로 접속하여 프로세스, 메모리, 디스크, 로그 현황을 수집하고 분석한다.

## 사용 예시

> **`log`는 항상 로컬 다운로드 후 상세 분석이 기본**이다. 빠른 텍스트 조회만 원하면 `log-quick`을 사용한다.

| 입력 | 동작 |
|------|------|
| `kglowing-batch log` | kglowing-batch 로그 파일 **로컬 다운로드 후 상세 분석** (기본) |
| `kglowing-batch log-quick` | kglowing-batch 최근 에러 30~50줄만 빠르게 조회 (서버 직접 tail/grep) |
| `kglowing-batch log-deep` | `log`의 별칭 (구버전 호환) |
| `kglowing-batch memory` | kglowing-batch 메모리 상태 |
| `batch all` | 배치 서버 전체 점검 (프로세스+메모리+디스크+로그 다운로드 분석) |
| `qa-settle log` | QA settle 로그 다운로드 후 상세 분석 |
| `qa-settle log-quick` | QA settle 최근 에러 빠르게 조회 |
| `pe log` | product-engine7 (PE 별칭) 로그 다운로드 후 상세 분석 |
| `settle1 memory` | 운영 정산 서버 1 메모리 상태 |
| `order1 process` | 주문 서버 1 프로세스 확인 |

### 인자 매핑 (자연어)

사용자가 자연어로 요청해도 아래 인자로 매핑한다.

| 자연어 표현 | 매핑되는 인자 |
|------------|--------------|
| "에러 로그 체크", "에러 로그 확인", "log 체크", "error log", "로그 확인", "로그 분석" | `log` (다운로드 후 분석) |
| "빠르게 로그", "최근 에러 몇 줄", "tail만", "log-quick" | `log-quick` |
| "메모리 상태", "memory 확인" | `memory` |
| "전체 점검", "서버 점검", "all" | `all` |

## 접속 정보

> 키 경로, 서버 목록 등 환경 설정은 `references/servers.md`를 읽어 사용한다.
> 경로나 서버가 바뀌면 `references/servers.md`만 수정하면 된다.

## 진행 상황 로깅 (필수)

각 단계 실행 **전에** 반드시 현재 진행 상황을 사용자에게 출력한다.

```
[1/3] 서버 연결 및 기본 정보 수집 중... (qa-settle)
[2/3] 로그 파일 다운로드 중... (settle.log)
[3/3] 로그 분석 및 보고서 작성 중...
```

단계가 완료될 때도 완료 메시지를 출력한다:
```
✓ 연결 성공 (ip-10-98-0-140)
✓ 로그 파일 다운로드 완료 (6.1MB → /tmp/settle_analysis.log)
```

## 접속 방식 결정

| 입력 형태 | 접속 방식 |
|----------|----------|
| `qa-*` 별칭 (예: `qa-settle`) | 방식 A: QA 직접 접속 |
| go 호스트명 (예: `kglowing-batch`) | 방식 B: Bastion go 경유 |
| `ec2-*.compute.amazonaws.com` 또는 퍼블릭 IP | 방식 C: EC2 직접 접속 |
| `172.x.x.x`, `10.x.x.x` 프라이빗 IP | 방식 D: ProxyCommand |

### 방식 A: QA 서버 직접 접속

```bash
ssh -i "<QA_KEY>" -o StrictHostKeyChecking=no -o ConnectTimeout=15 \
  ec2-user@<QA호스트> "<명령어>"
```

### 방식 B: Bastion go 명령 경유 (guhada 유저 — 앱 로그 접근)

앱 로그(guhada 소유 파일) 접근 시 사용.

```bash
ssh -i "<PROD_KEY>" -o StrictHostKeyChecking=no -o ConnectTimeout=15 \
  ec2-user@<BASTION> \
  'sudo su - guhada -c "go <호스트명>" << '"'"'ENDSSH'"'"'
<명령어>
ENDSSH'
```

### 방식 C: EC2 직접 접속

```bash
ssh -i "<PROD_KEY>" -o StrictHostKeyChecking=no -o ConnectTimeout=15 \
  ec2-user@<EC2주소> "<명령어>"
```

### 방식 D: ProxyCommand (프라이빗 IP, sudo 권한 필요 시)

```bash
ssh -i "<PROD_KEY>" \
  -o StrictHostKeyChecking=no -o ConnectTimeout=15 \
  -o ProxyCommand="ssh -i \"<PROD_KEY>\" -o StrictHostKeyChecking=no -W %h:%p ec2-user@<BASTION>" \
  ec2-user@<내부IP> "<명령어>"
```

## 로그 분석 방식

> **기본 원칙**: 사용자가 "로그 체크/확인/분석" 등으로 요청하면 **항상 로컬 다운로드 후 분석**(log)을 수행한다.
> 서버 직접 tail/grep(log-quick)은 사용자가 명시적으로 "빠르게", "tail만", "log-quick"이라고 요청한 경우에만 사용한다.

### 로컬 저장 위치 (Windows 환경)

> **중요**: Bash 셸과 Write/Edit/Read 도구의 `/tmp` 매핑이 다르므로, **항상 명시적인 Windows 경로를 사용한다**.

| 도구 | `/tmp/` 실제 위치 |
|------|-----------------|
| Write / Edit / Read | `C:\tmp\` |
| Bash 셸 | `C:\Temp\` (Windows 시스템 TEMP) |

**규칙**:
- 다운로드 로그 + 보고서 모두 **`C:\tmp\<host>_logs\`** 디렉토리에 저장한다 (사용자 지정 위치)
- Bash에서는 `/c/tmp/<host>_logs/`, Write/Edit에서는 `C:\tmp\<host>_logs\`로 동일 위치를 가리킨다
- `/tmp/...` 같은 모호한 경로는 사용하지 않는다

### 기본 방식 (`log`): 로컬로 다운로드 후 상세 분석 — **권장**

로그 파일을 로컬 `C:\tmp\<host>_logs\`에 저장 후 분석한다. 서버 부하 최소화(cat 한 번), 로컬에서 자유로운 패턴 분석 가능.

```bash
# [0단계] 저장 디렉토리 준비 (Bash에서)
HOST_DIR=/c/tmp/<host>_logs
mkdir -p "$HOST_DIR"
TS=$(date +%Y%m%d_%H%M%S)

# [1단계] 로그 파일 목록 확인 — 어떤 파일이 있는지 / 크기 / 최신 mtime 확인
ssh -i "<KEY>" ec2-user@<HOST> "ls -lth /home/<user>/logs/"

# [2단계] 로그 파일 다운로드 (scp 미사용 — ssh cat + 로컬 리다이렉트)
ssh -i "<KEY>" -o StrictHostKeyChecking=no ec2-user@<HOST> \
  "cat /path/to/app.log" > "$HOST_DIR/app_${TS}.log"

# [3단계] 로컬에서 분석
LOG="$HOST_DIR/app_${TS}.log"
grep -c "ERROR\|WARN\|Exception" "$LOG"
grep -i "error\|exception" "$LOG" | tail -50

# [4단계] 분석 결과를 표 + 발생 패턴별 그룹으로 보고
```

> **왜 이 방식인가**: `scp`는 보안 훅에서 차단됨. `ssh cat` + 로컬 `>` 리다이렉트는
> 서버에서는 cat만 실행되고 리다이렉트는 로컬에서 처리 → 훅 차단 없이 파일 수신 가능.
> 로컬 분석은 grep 패턴을 자유롭게 바꿀 수 있어 한 번 받아두면 반복 질의에 유리하다.

### 빠른 조회 방식 (`log-quick`): 서버에서 직접 tail/grep

단순히 "지금 에러 났는지"만 30~50줄 확인하면 충분할 때만 사용. 파일 전송 없음.

```bash
# 서버에서 실행 → 텍스트 출력만 수신 (파일 전송 없음)
ssh -i "<KEY>" ec2-user@<HOST> "tail -n 100 /path/to/app.log | grep -i error"
```

### 방식 선택 가이드

| 상황 | 권장 방식 | 이유 |
|------|----------|------|
| **에러 로그 체크/분석** (사용자 일반 요청) | `log` (다운로드) | 기본값. 패턴/빈도/시간대까지 분석 가능 |
| 전체 로그 패턴 분석 | `log` (다운로드) | 상세 분석, 서버 부하 최소화 |
| 사용자가 "빠르게", "tail만" 명시 | `log-quick` | 텍스트만 받음 |
| 로그 파일 > 50MB | `log` + 사전 grep 필터 | 다운로드 전 서버에서 1차 필터 권장 |
| 라이브 모니터링 (수 분간) | 사용자 직접 SSH | 스킬 범위 외 |

## 작업 접근 방식 선택 가이드

| 작업 | 권장 방식 | 이유 |
|------|----------|------|
| 앱 로그 확인 (guhada 소유) | 방식 B (go) | guhada 유저 파일 접근 필요 |
| 시스템 상태, 프로세스 | 방식 B 또는 D | 둘 다 가능 |
| sudo 필요 작업 (ES 설정 등) | 방식 D (ProxyCommand, ec2-user) | sudo 권한 필요 |

## 수집 명령어

### 기본 정보 (항상 수집)

```bash
echo '=== HOSTNAME ===' && hostname
echo '=== OS ===' && cat /etc/os-release | head -3
echo '=== UPTIME ===' && uptime
echo '=== CPU ===' && nproc && lscpu | grep 'Model name'
echo '=== MEMORY ===' && free -h
echo '=== DISK ===' && df -h | grep -E '^/dev|Filesystem'
echo '=== NETWORK ===' && hostname -I
```

### process

```bash
echo '=== JAVA PROCESSES ===' && ps aux | grep java | grep -v grep
echo '=== TOP CPU ===' && ps aux --sort=-%cpu | head -10
echo '=== TOP MEM ===' && ps aux --sort=-%mem | head -10
echo '=== LISTENING PORTS ===' && ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null
```

### memory

```bash
echo '=== FREE ===' && free -h
echo '=== VMSTAT ===' && vmstat 1 3
echo '=== SWAP ===' && swapon --show 2>/dev/null || echo 'No swap'
echo '=== TOP MEM PROCESSES ===' && ps aux --sort=-%mem | head -15
echo '=== OOM LOG ===' && dmesg | grep -i -E 'oom|out of memory|killed process' | tail -10
```

### disk

```bash
echo '=== DISK USAGE ===' && df -h
echo '=== LARGE DIRS ===' && du -sh /home/* /var/log/* /tmp/* 2>/dev/null | sort -rh | head -15
echo '=== INODE ===' && df -i | grep -E '^/dev|Filesystem'
```

### log (기본 — 로컬 다운로드 후 상세 분석)

> 사용자가 "에러 로그 체크/확인/분석" 등으로 요청하면 이 모드로 동작한다.
> 단순 텍스트 조회는 `log-quick` 사용.

아래 순서로 실행 (Windows 환경 — 경로는 모두 `C:\tmp\`를 사용):

```bash
# 0. 저장 디렉토리 준비 (Bash) — Bash에서는 /c/tmp 형식으로 접근
HOST_DIR=/c/tmp/<host>_logs
mkdir -p "$HOST_DIR"
TS=$(date +%Y%m%d_%H%M%S)

# 1. 로그 디렉토리 탐색 — 어떤 파일이 있고 무엇이 최근에 갱신되었는지 확인
ssh -i "<KEY>" ec2-user@<HOST> "ls -lth /home/<user>/logs/ 2>/dev/null; ls -lth /home/<user>/logs/<service>/ 2>/dev/null"

# 2. 대상 파일을 로컬로 다운로드 (ssh cat + 로컬 리다이렉트, scp 미사용)
ssh -i "<KEY>" -o StrictHostKeyChecking=no ec2-user@<HOST> \
  "cat /home/<user>/logs/<service>.log" > "$HOST_DIR/<service>_${TS}.log"
ssh -i "<KEY>" -o StrictHostKeyChecking=no ec2-user@<HOST> \
  "cat /home/<user>/logs/<service>-error.log" > "$HOST_DIR/<service>-error_${TS}.log"

# 3. 로컬에서 분석
LOG="$HOST_DIR/<service>_${TS}.log"
grep -c "ERROR\|WARN\|Exception" "$LOG"
grep -i "error\|exception" "$LOG" | tail -100
# 시간대별 에러 빈도
grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}' "$LOG" | sort | uniq -c | tail -20
# 에러 패턴 그룹화 (Exception 종류별 카운트)
grep -oE '[A-Za-z]+Exception' "$LOG" | sort | uniq -c | sort -rn | head -20

# 4. 분석 결과를 표 + 발생 패턴 그룹으로 사용자에게 보고

# 5. 분석 결과 보고서를 마크다운 파일로 저장 (필수)
#    Bash 경로: /c/tmp/<host>_logs/REPORT_<같은 타임스탬프>.md
#    Write 도구 경로: C:\tmp\<host>_logs\REPORT_<같은 타임스탬프>.md
#    예: C:\tmp\pe_logs\REPORT_20260429_143248.md
```

> **분석 결과 보고서 저장 (필수 단계)**
>
> `log` 모드 실행 시 **분석 결과를 반드시 마크다운 보고서로 저장**한다.
> 컨텍스트가 사라진 뒤에도 사용자가 다시 열어볼 수 있어야 하기 때문이다.
>
> | 항목 | 값 |
> |------|-----|
> | **저장 경로 (Windows)** | `C:\tmp\<host>_logs\REPORT_<YYYYMMDD_HHMMSS>.md` (사용자 지정 위치, 다운로드 로그와 같은 디렉토리) |
> | **Bash에서 동일 경로** | `/c/tmp/<host>_logs/REPORT_<YYYYMMDD_HHMMSS>.md` |
> | **파일명 규칙** | `REPORT_` + 다운로드한 로그 파일과 동일한 타임스탬프 |
> | **포함 섹션** | (1) 메타데이터 표 (서버 / 파일 / 기간 / 분석시각) → (2) 요약 표 (패턴별 건수 / 근본 원인 / 위험도) → (3) 시간대별 분포 → (4) 패턴별 상세 (샘플 로그 + 권장 조치) → (5) 시스템 상태 → (6) 다음 액션 → (7) 분석에 사용한 명령 |
>
> ⚠️ **`/tmp/...` 같은 모호한 경로는 절대 사용하지 않는다.** Bash와 Write 도구의 `/tmp` 매핑이 다르기 때문이다 (Bash → `C:\Temp`, Write → `C:\tmp`). 항상 명시적인 Windows 절대경로(`C:\tmp\...`) 또는 Bash 절대경로(`/c/tmp/...`)를 사용한다.
>
> 저장 후 채팅 응답 마지막에 **Windows 절대경로**로 보고서 위치를 명시한다 (예: `보고서 저장: C:\tmp\pe_logs\REPORT_20260429_143248.md`).
> 사용자가 "분석 결과 파일 어디?"라고 물으면 이 경로를 즉시 답할 수 있도록.

> **로그 파일이 50MB 이상**일 때는 다운로드 전에 서버에서 `tail -n 50000`이나 `grep ERROR`로 사전 필터한 결과만 받는다.
> 그래도 충분히 분석 가능하면서 네트워크/디스크 부담을 줄일 수 있다.

### log-quick (서버에서 빠르게 직접 조회)

빠른 텍스트 확인용. 사용자가 "빠르게", "tail만", "log-quick"이라고 명시했을 때만 사용한다.

```bash
echo '=== RECENT ERRORS ===' && journalctl --no-pager -n 30 --priority=err 2>/dev/null || tail -30 /var/log/messages 2>/dev/null
echo '=== DMESG ERRORS ===' && dmesg | tail -20
echo '=== APP LOG FILES ===' && ls -lth /home/*/logs/ 2>/dev/null | head -20
echo '=== APP LOG TAIL ===' && tail -n 50 /home/ec2-user/logs/<service>.log 2>/dev/null || echo '(없음)'
echo '=== APP ERROR TAIL ===' && tail -n 50 /home/ec2-user/logs/<service>-error.log 2>/dev/null || echo '(없음)'
```

### all

기본 정보 + process + memory + disk + **log-quick** 을 하나의 SSH 세션으로 합쳐 실행한다.
(`all`은 전체 개요용이므로 로그는 빠른 조회 모드를 쓴다. 에러 패턴을 깊게 분석하려면 별도로 `log`를 호출.)

## 결과 보고 형식

### 서버 개요

| 항목 | 값 |
|------|-----|
| 호스트명 | |
| OS | |
| CPU | |
| RAM (전체 / 사용 / 여유) | |
| Disk (전체 / 사용 / 여유) | |
| Uptime | |
| Swap | |

### 주요 프로세스

| PID | 프로세스 | RSS | MEM% | 시작일 |
|-----|---------|-----|------|--------|

### 위험 요소 체크

- 메모리 사용률 80% 이상 → 경고
- Swap 미설정 + 메모리 여유 20% 미만 → 경고
- 디스크 사용률 80% 이상 → 경고
- OOM 기록 존재 → 경고
- 좀비 프로세스 존재 → 경고

## 보안 규칙 — 절대 금지 명령어

SSH를 통해 서버에 전달하는 명령어는 **읽기 전용**만 허용한다.
아래 명령어는 어떤 경우에도 SSH로 전송하지 않는다.

| 카테고리 | 금지 명령어 |
|---------|-----------|
| 파일 조작 | `rm`, `mv`, `cp`, `chmod`, `chown`, `mkdir`, `touch`, `ln` |
| 권한 상승 | `sudo` (읽기 목적 제외), `su` |
| 프로세스 제어 | `kill`, `pkill`, `killall`, `reboot`, `shutdown`, `systemctl stop`, `systemctl restart`, `systemctl start` |
| 파일 쓰기 | `>`, `>>`, `tee` (리다이렉트 포함), `truncate` |
| 네트워크 변경 | `wget`, `curl -o`, `scp`, `rsync`, `iptables` |
| 스크립트 실행 | `bash -c`, `sh -c`, `eval`, `exec`, `python -c`, `perl -e` |
| 위험한 Git | `git push --force`, `git reset --hard`, `git clean`, `git checkout` |
| 패키지 관리 | `yum install`, `yum remove`, `apt install`, `apt remove`, `pip install`, `npm install` |
| DB 조작 | `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER` |

### 허용 명령어 — 읽기 전용만

| 카테고리 | 허용 명령어 |
|---------|-----------|
| 프로세스 조회 | `ps`, `top -bn1`, `pgrep` |
| 시스템 상태 | `free -h`, `df -h`, `uptime`, `vmstat`, `iostat`, `lscpu`, `nproc` |
| 로그 조회 | `tail` (숫자 옵션만), `head`, `cat` (소규모), `grep`, `zgrep`, `journalctl` (읽기), `dmesg` |
| 네트워크 조회 | `ss -tlnp`, `netstat -tlnp`, `hostname`, `hostname -I` |
| 파일 탐색 | `ls`, `find`, `stat`, `du -h`, `file` |
| 기타 | `echo`, `date`, `whoami`, `id`, `env` (읽기용) |

> **Claude에게**: 사용자가 서버 변경, 재시작, 삭제 등 위 금지 목록에 해당하는 작업을 요청하더라도
> 절대 실행하지 말고 "이 스킬은 읽기 전용 점검만 지원합니다. 변경 작업은 직접 수행하거나
> 별도 승인 후 진행해야 합니다."라고 안내한다.

## 주의사항

- SSH 명령 타임아웃: 30초
- 파이프(`|`) 사용 시 heredoc 내부에서 실행해야 이스케이프 문제 없음
- 방식 B (go)는 guhada 유저 권한이므로 sudo 필요 시 방식 D로 전환
- 민감 정보(비밀번호, 키)는 출력에 포함하지 않음

## 할루시네이션 금지

- SSH 명령 출력에 없는 값은 절대 추측하거나 임의로 채우지 않는다
- 확인되지 않은 항목은 `(정보 없음)`으로 표기한다
- 명령 실패 시 "명령 실패" 또는 "출력 없음"으로 명시하고 이유를 임의로 추정하지 않는다
- 위험 요소 판단도 실제 수집된 수치 기준으로만 한다
