---
name: docker-up
effort: low
description: >
  프로젝트의 Docker 환경을 자동으로 감지하고 실행/업데이트하는 스킬.
  Docker Desktop 실행 여부를 체크하여 미실행 시 자동 시작하고,
  docker-compose.yml을 찾아 컨테이너를 띄우거나 업데이트한다.
  "도커 띄워줘", "도커 실행", "도커 시작", "컨테이너 시작", "컨테이너 올려줘",
  "docker up", "도커 업데이트", "컨테이너 업데이트", "도커 재시작", "도커 리빌드",
  "docker restart", "서버 띄워줘" (프로젝트에 docker-compose가 있을 때),
  "개발 환경 시작", "로컬 환경 띄워줘" 같은 요청에 사용한다.
  docker-compose 파일이 없으면 프로젝트를 분석하여 적절한 docker-compose.yml + Dockerfile을 자동 생성할 수도 있다.
  프로젝트에 docker-compose.yml이나 compose.yml이 존재하거나, Docker로 띄우고 싶은 프로젝트가 있으면 이 스킬 사용을 적극 고려한다.
---

# Docker Up

프로젝트의 Docker 환경을 자동으로 감지하고 실행/업데이트하는 스킬.
Docker Desktop이 꺼져 있으면 알아서 켜고, docker-compose 파일을 찾아 컨테이너를 관리한다.

## 실행 흐름

### 1단계: docker-compose 파일 탐색

프로젝트 루트부터 아래 파일명을 순서대로 탐색한다:

1. `docker-compose.yml`
2. `docker-compose.yaml`
3. `compose.yml`
4. `compose.yaml`

프로젝트 루트에 없으면 하위 디렉토리 1단계까지 탐색한다 (예: `doc/docker-compose.yml`, `infra/docker-compose.yml`).

**파일을 찾지 못한 경우**: 1-A단계(Docker 환경 자동 생성)로 진행한다.

**여러 개 발견된 경우**: 목록을 보여주고 어떤 것을 실행할지 사용자에게 선택을 요청한다.

### 1-A단계: Docker 환경 자동 생성 (compose 파일 없는 경우)

compose 파일을 찾지 못하면 프로젝트를 분석하여 적절한 Docker 환경을 생성한다.

#### 프로젝트 분석

아래 파일/디렉토리로 프로젝트 유형을 판별한다:

| 감지 파일 | 프로젝트 유형 | 기본 이미지 |
|----------|-------------|-----------|
| `pom.xml` | Java/Maven | `eclipse-temurin:17-jre-alpine` |
| `build.gradle`, `build.gradle.kts` | Java/Gradle | `eclipse-temurin:17-jre-alpine` |
| `package.json` | Node.js | `node:20-alpine` |
| `requirements.txt`, `pyproject.toml` | Python | `python:3.12-slim` |
| `go.mod` | Go | `golang:1.22-alpine` |
| `index.html` (루트 또는 하위) | 정적 사이트 | `nginx:alpine` |
| `*.md` 파일만 존재 | 문서 서버 | `nginx:alpine` |

#### 생성 흐름

1. **프로젝트 유형 판별** 후 사용자에게 확인:
   ```
   프로젝트 유형: [Java/Maven] (pom.xml 감지)
   docker-compose.yml과 Dockerfile을 생성할까요?
   - 생성 위치: [프로젝트 루트 / 특정 디렉토리]
   - 서비스 포트: [8080 (기본) / 사용자 지정]
   ```

2. **사용자 승인 후** Dockerfile + docker-compose.yml 생성

3. 프로젝트 유형별 **Dockerfile 템플릿** 적용:
   - Java: 멀티스테이지 빌드 (빌드 → 런타임 분리)
   - Node.js: `npm ci` → `npm start`
   - Python: `pip install` → entrypoint
   - 정적 사이트/문서: nginx 복사 + 커스텀 nginx.conf

4. **docker-compose.yml 생성** 시 포함 항목:
   - 서비스명 (프로젝트 디렉토리명 기반)
   - 포트 매핑
   - 볼륨 (개발용 핫 리로드가 유리한 경우)
   - `restart: unless-stopped`
   - `.env` 파일 참조 (있는 경우)

5. 생성 완료 후 **2단계로 진행** (Docker Desktop 확인 → 실행)

#### 주의사항

- 파일 생성 전 반드시 사용자 확인을 받는다 (어떤 파일을 어디에 생성할지)
- 기존 Dockerfile이 있으면 덮어쓰지 않고 경고한다
- `.dockerignore`도 함께 생성한다 (node_modules, .git, build 산출물 등 제외)
- 프로젝트 유형을 판별할 수 없으면 사용자에게 직접 물어본다

### 2단계: Docker Desktop 실행 확인

```bash
docker info > /dev/null 2>&1
```

- **성공 (exit 0)**: Docker가 이미 실행 중. 3단계로 진행.
- **실패**: Docker Desktop을 시작해야 한다. 아래 플랫폼별 명령을 실행한다.

#### Windows (현재 환경)
```bash
# Docker Desktop 시작
cmd.exe /c "start "" \"C:\Program Files\Docker\Docker\Docker Desktop.exe\""
```

#### macOS (참고)
```bash
open -a "Docker Desktop"
```

#### Linux (참고)
```bash
sudo systemctl start docker
```

Docker Desktop은 시작 후 데몬이 준비되기까지 시간이 걸린다.
아래 루프로 준비 상태를 확인한다:

```bash
# 최대 60초 대기, 5초 간격으로 체크
for i in $(seq 1 12); do
  docker info > /dev/null 2>&1 && break
  echo "Docker 데몬 시작 대기 중... (${i}/12)"
  sleep 5
done
```

60초 후에도 실패하면 사용자에게 "Docker Desktop이 시작되지 않습니다. 수동으로 실행해주세요."라고 안내한다.

### 3단계: 현재 컨테이너 상태 확인

docker-compose 파일이 위치한 디렉토리에서 실행한다:

```bash
docker compose -f <compose-file> ps
```

이 결과로 현재 상태를 판단한다:
- **컨테이너 없음**: 신규 실행 (4a단계)
- **컨테이너 있음 + 실행 중**: 업데이트 필요 여부 판단 (4b단계)
- **컨테이너 있음 + 중지됨**: 재시작 (4c단계)

### 4단계: 실행/업데이트

#### 4a. 신규 실행 (컨테이너 없음)

```bash
docker compose -f <compose-file> up -d --build
```

#### 4b. 업데이트 (컨테이너 실행 중)

사용자가 "업데이트", "리빌드", "갱신" 등을 요청한 경우:

```bash
docker compose -f <compose-file> up -d --build --force-recreate
```

단순 "띄워줘" 요청이고 이미 실행 중이면:
- 사용자에게 "이미 실행 중입니다. 업데이트(리빌드)하시겠습니까?"라고 확인한다.

#### 4c. 재시작 (컨테이너 중지됨)

```bash
docker compose -f <compose-file> up -d
```

### 5단계: 결과 확인 및 보고

```bash
docker compose -f <compose-file> ps
```

실행 결과를 아래 형식으로 보고한다:

```
Docker 환경 실행 완료:
- Compose 파일: <경로>
- 서비스: <서비스 목록>
- 상태: <running/error>
- 포트: <매핑된 포트 목록>
- 접속: http://localhost:<포트>
```

에러가 있으면 로그를 확인한다:

```bash
docker compose -f <compose-file> logs --tail=30
```

## 추가 명령

사용자가 특정 동작을 요청할 수 있다:

| 요청 | 동작 |
|------|------|
| "도커 내려줘", "컨테이너 중지" | `docker compose down` |
| "도커 로그", "로그 보여줘" | `docker compose logs --tail=50` |
| "도커 상태", "컨테이너 상태" | `docker compose ps` |
| "도커 리빌드" | `docker compose up -d --build --force-recreate` |
| "도커 초기화", "볼륨까지 삭제" | `docker compose down -v` (확인 후 실행) |

## 주의사항

- `docker compose down -v` (볼륨 삭제)는 데이터 손실 가능성이 있으므로 반드시 사용자 확인 후 실행한다.
- `.env` 파일이 compose 파일과 같은 디렉토리에 있으면 자동으로 로드된다. 별도 처리 불필요.
- 빌드 에러 발생 시 로그 전문을 보여주고 원인을 분석한다.
- 포트 충돌 시 어떤 프로세스가 해당 포트를 사용 중인지 확인하여 안내한다.
