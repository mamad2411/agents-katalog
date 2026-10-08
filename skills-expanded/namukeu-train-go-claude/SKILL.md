# train-go

> SRT + Korail 기차 자동 예매 서버. 개인용.

## Architecture

- **Runtime:** Python 3.12
- **Framework:** FastAPI + uvicorn
- **DB:** SQLite (로컬, `data/train-go.db`)
- **암호화:** cryptography (Fernet)
- **예매:** SRTrain (SRT), korail2 (Korail/KTX)
- **스케줄러:** asyncio tasks (반복 검색)
- **알림:** Telegram Bot API (httpx)

## Directory Structure

```
train-go/
├── src/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   ├── auth.py          # Bearer token 인증
│   │   └── routes.py        # API 엔드포인트
│   ├── core/
│   │   ├── config.py        # 환경변수 설정
│   │   ├── crypto.py        # Fernet 암호화/복호화
│   │   └── database.py      # SQLite 스키마 + CRUD
│   ├── services/
│   │   ├── srt.py           # SRT 검색/예약
│   │   ├── korail.py        # Korail 검색/예약
│   │   ├── scheduler.py     # 매크로 (반복 검색 + 자동 예약)
│   │   └── notifier.py      # 텔레그램 알림 발송
│   └── models/
│       ├── credential.py    # 자격증명 Pydantic 모델
│       └── reservation.py   # 예약 Pydantic 모델
├── pyproject.toml
├── .env.example
└── .gitignore
```

## Commands

| Command | Description |
|---------|-------------|
| `python -m src.main` | 서버 시작 |
| `pip install -e .` | 개발 설치 |

## API Endpoints

### 인증
모든 API 요청에 `Authorization: Bearer {API_TOKEN}` 헤더 필요.

### 자격증명

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/credentials` | 로그인 정보 등록 (암호화 저장) |
| DELETE | `/credentials/{provider}` | 로그인 정보 삭제 |

**POST /credentials**
```json
{ "provider": "srt", "login_id": "010-xxxx-xxxx", "password": "xxx" }
```

### 예약

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reservations` | 예약 요청 → 매크로 시작 |
| GET | `/reservations` | 전체 예약 목록 (?status=searching) |
| GET | `/reservations/{id}` | 예약 상태 조회 |
| DELETE | `/reservations/{id}` | 예약 취소 (매크로 중단) |

**POST /reservations**
```json
{
  "provider": "srt",
  "dep_station": "수서",
  "arr_station": "부산",
  "date": "20260215",
  "time_range_start": "1400",
  "time_range_end": "1700",
  "passengers": { "adult": 1, "child": 0, "senior": 0 },
  "seat_type": "general"
}
```

### 시스템

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | 서버 상태 (인증 불필요) |
| GET | `/status` | 활성 매크로 수, 예약 현황 |

## 매크로 흐름

1. POST /reservations → DB 저장 (status: pending)
2. 스케줄러가 5초 간격으로 열차 검색 (status: searching)
3. 시간 범위 내 좌석 있는 열차 발견 → 예약 시도
4. 예약 성공 → status: reserved, 텔레그램 알림
5. 시간 초과 (기본 24시간) → status: failed, 텔레그램 알림

## 보안

- 로그인 정보: Fernet 암호화 → SQLite 저장
- `.env`에 API_TOKEN, ENCRYPTION_KEY 보관
- `.env`, `*.db`, `data/` 모두 `.gitignore` 포함
- 레포에는 코드만 존재

## Reservation Status Flow

```
pending → searching → reserved (성공)
                    → failed (시간 초과/에러)
                    → cancelled (수동 취소)
```
