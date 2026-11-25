---
name: sky-python
description: >-
  Modern Python geliştirme: uv ile proje ve bağımlılık yönetimi, pyproject.toml, src düzeni,
  ruff (lint + format), tip ipuçları ve mypy/pyright, Pydantic ile doğrulama, dataclass ve
  enum, pathlib, logging, async/await (asyncio, TaskGroup), pytest (fixture, parametrize,
  mock), paketleme ve CLI (Typer), performans ipuçları ve sık hatalar. Python kodu yazarken,
  gözden geçirirken veya "Python projesi kur" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Python

## Proje kurulumu (uv)

```bash
uv init --package myapp          # src/myapp + pyproject.toml
uv add httpx pydantic            # bağımlılık
uv add --dev ruff pytest mypy    # geliştirme bağımlılıkları
uv run pytest                    # sanal ortamı otomatik yönetir
uv python pin 3.13               # .python-version
```
`uv` pip + venv + pip-tools + pyenv işini tek ve çok hızlı araçta yapar. `uv.lock` commit'lenir.
Mevcut `requirements.txt` projesinde: `uv add -r requirements.txt` ile geç.

```
myapp/
  pyproject.toml
  src/myapp/__init__.py
  src/myapp/core/…
  tests/test_core.py
```
src düzeni, testlerin kurulu paketi test etmesini sağlar (yanlışlıkla yerel dosyayı import etmezsin).

## pyproject.toml çekirdeği

```toml
[project]
name = "myapp"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27", "pydantic>=2.8"]

[tool.ruff]
line-length = 100
target-version = "py312"
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF", "ASYNC", "S"]   # pyflakes, isort, bugbear, pyupgrade, güvenlik…

[tool.mypy]
strict = true

[tool.pytest.ini_options]
addopts = "-q --strict-markers"
```
`ruff check --fix` + `ruff format` → Black + isort + flake8'in yerini alır.

## Tipler

```python
from typing import Literal, Protocol
type UserId = str                                  # 3.12 tip takma adı
Status = Literal["pending", "confirmed", "cancelled"]

def find(users: list[User], uid: UserId) -> User | None: ...
class Notifier(Protocol):
    def send(self, to: str, body: str) -> None: ...
```
- Yerleşik generic'ler (`list[int]`, `dict[str, X]`), `X | None`. `Any` yerine `object` + daraltma.
- Dış veri (JSON, env, istek) → **Pydantic** ile doğrula; iç veri → `@dataclass(frozen=True, slots=True)`.
- Enum: `class Role(StrEnum): ADMIN = "admin"`.

## Pydantic v2

```python
class BookingIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=2)
    phone: str = Field(pattern=r"^\+905\d{9}$")
    starts_at: AwareDatetime

booking = BookingIn.model_validate(payload)        # hata: ValidationError (alan bazlı)
```
Ayarlar: `pydantic-settings` → `class Settings(BaseSettings): database_url: PostgresDsn` (env'den, doğrulanmış).

## Hata yönetimi

- Geniş `except Exception:` ile yutma yok; beklenen istisnayı yakala, bağlamı koru: `raise AppError("…") from e`.
- Çıplak `except:` asla (KeyboardInterrupt'ı da yutar).
- Kaynaklar `with` ile (dosya, kilit, bağlantı); kendi kaynakların için `contextlib.contextmanager`.

## async

```python
async def fetch_all(urls: list[str]) -> list[httpx.Response]:
    async with httpx.AsyncClient(timeout=10) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(client.get(u)) for u in urls]
    return [t.result() for t in tasks]
```
- `TaskGroup` (3.11+): bir görev patlarsa diğerleri iptal edilir — `gather`'dan güvenli.
- Async kod içinde bloklayan çağrı (requests, time.sleep, ağır CPU) yok → `asyncio.to_thread` veya async kütüphane.
- Eşzamanlılık sınırı: `asyncio.Semaphore(10)`.

## Test (pytest)

```python
@pytest.mark.parametrize("phone,ok", [("+905321234567", True), ("123", False)])
def test_phone(phone, ok):
    assert is_valid(phone) is ok
```
- `monkeypatch` env/fonksiyon için, `pytest-mock`, `time-machine` zaman için, `respx` httpx için.
- Async: `pytest-asyncio` veya `anyio`. Kapsam: `pytest --cov=src`.

## Günlük araçlar

- `pathlib.Path` (`os.path` değil), f-string, `logging` (print değil — `logging.getLogger(__name__)`; yapılandırılmış log için `structlog`).
- CLI: **Typer** (tip ipuçlarından CLI). Zengin çıktı: **rich**.
- HTTP: **httpx** (sync + async). Tarih: `datetime` + `zoneinfo.ZoneInfo("Europe/Istanbul")`, her zaman timezone-aware.

## Sık hatalar

| Hata | Doğrusu |
|---|---|
| Değiştirilebilir varsayılan `def f(x=[])` | `x: list | None = None` |
| `datetime.now()` (naive) | `datetime.now(UTC)` |
| `== None` | `is None` |
| Döngüde string `+=` büyük veride | `"".join(parts)` |
| Global ortama `pip install` | `uv add` / proje venv'i |
| `from x import *` | açık import |
