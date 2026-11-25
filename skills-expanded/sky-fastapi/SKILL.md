---
name: sky-fastapi
description: >-
  FastAPI ile API geliştirme: proje yapısı (router, service, repository), Pydantic v2 şemaları
  (giriş/çıkış ayrımı), dependency injection (DB oturumu, mevcut kullanıcı, yetki), async
  SQLAlchemy 2.0 ve Alembic migration, JWT/OAuth2 auth, hata yönetimi ve tutarlı hata gövdesi,
  arka plan işleri, CORS, sayfalama, OpenAPI dokümantasyonu, httpx ile testler ve uvicorn ile
  dağıtım. FastAPI projesinde veya "Python API yaz" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · FastAPI

Genel API kuralları `sky-backend-api`'de; Python temelleri `sky-python`'da.

## Yapı

```
app/
  main.py              # FastAPI(), router'lar, middleware, lifespan
  core/config.py       # pydantic-settings
  core/security.py     # şifre hash, JWT
  db/session.py        # async engine + sessionmaker
  models/booking.py    # SQLAlchemy modelleri
  schemas/booking.py   # Pydantic: BookingCreate, BookingOut
  services/booking.py  # iş mantığı + yetki
  api/deps.py          # get_db, get_current_user
  api/routes/bookings.py
alembic/
tests/
```

## Şemalar: giriş ≠ çıkış

```python
class BookingCreate(BaseModel):
    service_id: UUID
    starts_at: AwareDatetime
class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    starts_at: datetime
    status: BookingStatus
```
`response_model=BookingOut` → parola hash'i gibi iç alanlar asla sızmaz.

## Dependency injection

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session

DB = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB) -> User:
    payload = decode_jwt(token)                     # geçersizse HTTPException(401)
    user = await db.get(User, payload.sub)
    if not user:
        raise HTTPException(status_code=401)
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/bookings", response_model=BookingOut, status_code=201)
async def create_booking(body: BookingCreate, db: DB, user: CurrentUser):
    return await booking_service.create(db, user, body)
```
Yetki kontrolü serviste (sahiplik/org).

## SQLAlchemy 2.0 (async)

```python
class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    org_id: Mapped[UUID] = mapped_column(ForeignKey("orgs.id"), index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    client: Mapped["Client"] = relationship(lazy="raise")    # yanlışlıkla lazy load → hata (N+1 koruması)

stmt = (select(Booking).where(Booking.org_id == org_id)
        .options(selectinload(Booking.client)).order_by(Booking.starts_at))
rows = (await db.scalars(stmt)).all()
```
- Async'te lazy loading çalışmaz → `selectinload`/`joinedload` açık; `lazy="raise"` hatayı erkenden gösterir.
- Migration: `alembic revision --autogenerate -m "add bookings"` → **üretileni oku** → `alembic upgrade head`.
- Küçük projelerde SQLModel (Pydantic + SQLAlchemy tek model) da olur.

## Hatalar

```python
class AppError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message

@app.exception_handler(AppError)
async def app_error_handler(_: Request, e: AppError):
    return JSONResponse(status_code=e.status, content={"error": {"code": e.code, "message": e.message}})
```

## Diğer

- **Lifespan**: `@asynccontextmanager async def lifespan(app)` — bağlantı havuzu, paylaşılan HTTP istemcisi.
- **CORS**: `CORSMiddleware(allow_origins=[settings.frontend_url], allow_credentials=True)` — `*` değil.
- **Arka plan**: `BackgroundTasks` yalnızca kısa işler; gerçek kuyruk için Celery/ARQ/Dramatiq (bkz. `sky-jobs`).
- **Sayfalama**: cursor parametreleri, `limit: int = Query(20, le=100)`.
- **Rate limit**: `slowapi` veya gateway.
- **OpenAPI**: `/docs` prod'da gerekiyorsa kapat veya auth arkasına al.

## Test

```python
@pytest.fixture
async def client(app_with_test_db):
    async with AsyncClient(transport=ASGITransport(app=app_with_test_db), base_url="http://t") as c:
        yield c

async def test_create_booking_requires_auth(client):
    r = await client.post("/bookings", json={})
    assert r.status_code == 401
```
`app.dependency_overrides[get_current_user] = lambda: fake_user`; gerçek Postgres (Testcontainers) tercih.

## Dağıtım

`uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`; Docker çok aşamalı imaj (`uv sync --frozen --no-dev`),
sağlık uç noktası, `alembic upgrade head` deploy öncesi (bkz. `sky-deploy`, `sky-docker`).
