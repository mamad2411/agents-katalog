# AGENTS.md

## 프로젝트 설명

- 해당 디렉토리는 Redis를 학습하기 위한 Python 프로젝트이다.
- 프로젝트 기준 디렉터리는 `레디스` 디렉토리이다.
- `pyproject.toml`과 `uv.lock`은 `레디스` 디렉터리 기준으로 관리한다.

## 학습 방향

- 이 프로젝트는 단순 구현보다 Redis를 백엔드 시스템 관점에서 이해하는 것을 목표로 한다.
- 기능을 추가할 때는 항상 아래 질문에 답할 수 있어야 한다.
    - 왜 Redis를 사용하는가?
    - Redis의 어떤 자료구조를 선택했는가?
    - 해당 선택의 장점과 한계는 무엇인가?
    - 장애, 동시성, TTL, 메모리 정책에서 어떤 문제가 생길 수 있는가?
    - 테스트로 무엇을 보장했는가?

## AI 사용 규칙

- AI는 구현, 설계 검토, 테스트 보조, 리뷰를 도울 수 있다.
- AI가 구현을 도울 수 있지만 최종 설계 판단과 설명 책임은 사람에게 있다.
- AI가 제안한 코드는 반드시 사람이 의도를 이해한 뒤 반영한다.
- Redis 자료구조 선택, API 설계, 테스트 전략은 AI에게 위임하지 않고 직접 판단한다.
- AI에게 작업을 요청할 때는 `왜`, `대안`, `트레이드오프`, `검증 방법`을 함께 묻는다.
- AI가 만든 변경은 PR 전에 직접 읽고 설명할 수 있어야 한다.

## PR 및 커밋 추가 규칙

- PR 제목, PR 설명, 커밋 메시지는 루트 `../AGENTS.md`의 규칙을 따른다.
- Redis 관련 변경은 자료구조 선택 이유와 운영 관점의 고려사항을 함께 기록한다.

## Python 코드 규칙

- 공통 Python 규칙은 `../docs/python-guidelines.md`를 따른다.
- 코드에서는 `from app...` 형태의 absolute import를 유지한다.
- Redis 비동기 코드는 `async`/`await` 흐름과 connection close를 명확히 관리한다.
- Redis가 필요한 테스트는 실제 Redis 의존성을 숨기지 말고, fixture 또는 testcontainers 사용 여부를 명확히 한다.

## 실행 및 개발 환경 규칙

- 명령어는 특별한 이유가 없으면 항상 `레디스` 디렉터리에서 실행한다.
- 루트 `.venv`를 사용하지 않고 `레디스/.venv`를 사용한다.
- PyCharm Interpreter는 `레디스/.venv/bin/python`으로 맞춘다.
- 서버 실행은 아래 중 하나를 사용한다.
    ```
    uv run fastapi dev app/main.py
  
    uv run uvicorn app.main:app --reload
    ```
    - app/main.py를 직접 실행하는 방식에 의존하지 않는다.
    - 레디스/app 디렉터리 안에서 실행하지 않는다. from app... import가 깨질 수 있다.

## Redis 규칙

- 로컬 개발/학습용 Redis는 Docker Compose로 실행한다.
- 애플리케이션 Redis 연결은 REDIS_URL 환경변수를 우선 사용하고, 기본값은 redis://localhost:6379/0이다.

## 테스트 규칙

- 테스트는 아래 명령으로 실행한다.
    ```
    uv run pytest -q
    ```
- 테스트 실행 전 별도로 docker compose up을 할 필요는 없다.
- Docker가 실행 중이어야 한다. 실행되어있지않다면 사용자가 인식할 수 있도록 알려준다.

## 코드 구조 규칙

- FastAPI 앱 객체는 app/main.py의 app이다.
- 라우터는 app/routes/에 둔다.
- Redis 접근 코드는 app/storages/redis.py를 기준으로 관리한다.
- API 응답 모델은 app/representations/에 둔다.
