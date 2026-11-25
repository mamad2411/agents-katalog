---
name: sky-django
description: >-
  Django ve Django REST Framework: proje/app yapısı, ayarların ortamlara bölünmesi, modeller ve
  migration'lar, ORM performansı (select_related, prefetch_related, annotate, N+1 avı), özel
  User modeli, admin özelleştirme, DRF serializer/viewset/izinler, Celery ile arka plan işleri,
  güvenlik kontrol listesi (check --deploy), pytest-django ile testler ve dağıtım. Django
  projesinde çalışırken kullan.
disable-model-invocation: true
---

# Sky · Django

## Başlangıç kararları (sonradan değiştirmek zor)

- **Özel User modeli** ilk migration'dan önce: `class User(AbstractUser): email = models.EmailField(unique=True)` + `AUTH_USER_MODEL`.
- Ayarlar: `settings/base.py`, `dev.py`, `prod.py` veya tek dosya + `django-environ`. Sırlar env'den.
- Postgres. `TIME_ZONE = "Europe/Istanbul"`, `USE_TZ = True`, `LANGUAGE_CODE = "tr"`.
- App'ler alan bazlı (`bookings`, `clients`, `billing`): `models.py`, `services.py` (yazma), `selectors.py` (okuma), `api/`.

## Modeller

```python
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Beklemede"
        CONFIRMED = "confirmed", "Onaylandı"
    org = models.ForeignKey("orgs.Org", on_delete=models.CASCADE, related_name="bookings")
    client = models.ForeignKey("clients.Client", on_delete=models.PROTECT)
    starts_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=16, choices=Status, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["org", "starts_at"])]
        constraints = [models.UniqueConstraint(fields=["org", "client", "starts_at"], name="uniq_booking_slot")]
```
İş kuralı kısıtları DB'de. Para: `DecimalField` veya kuruş `IntegerField`.

## ORM performansı

```python
Booking.objects.filter(org=org).select_related("client", "service").order_by("starts_at")   # FK/1-1: JOIN
Client.objects.prefetch_related("bookings")                                                  # ters/M2M: 2 sorgu
Client.objects.annotate(n=Count("bookings")).filter(n__gt=3)
```
- N+1 tespiti: `django-debug-toolbar`, testte `assertNumQueries`.
- Toplu: `bulk_create`, `update()`, `iterator(chunk_size=2000)`; atomik `F()` (`stock=F("stock") - 1`).
- Yarış: `select_for_update()` + `transaction.atomic()`.

## İş mantığı nerede?

View/serializer ince; kurallar `services.py` fonksiyonlarında (`create_booking(*, user, data) -> Booking`).
Sinyalleri iş mantığı için kullanma — akış görünmez olur.

## DRF

```python
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "client", "starts_at", "status"]
        read_only_fields = ["status"]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOrgMember]

    def get_queryset(self):                                  # kiracı izolasyonu BURADA
        return Booking.objects.filter(org=self.request.user.active_org).select_related("client")

    def perform_create(self, serializer):
        serializer.instance = create_booking(user=self.request.user, data=serializer.validated_data)
```
- `get_queryset` filtresi → başka org'un kaydı 404 (IDOR koruması).
- `CursorPagination`, `django-filter`, OpenAPI için `drf-spectacular`.
- Auth: oturum (aynı domain SPA) veya `simplejwt`; throttle sınıfları.

## Admin

`list_display`, `list_filter`, `search_fields`, `autocomplete_fields`, `list_select_related` (admin N+1'i);
admin yolunu tahmin edilmesi zor yap, 2FA (`django-otp`). Admin müşteri paneli değildir.

## Arka plan

Celery + Redis (veya Huey / django-q2); görevler idempotent, argüman ID;
`transaction.on_commit(lambda: send_reminder.delay(booking.id))` — commit'ten sonra kuyruğa at. Bkz. `sky-jobs`.

## Güvenlik

`python manage.py check --deploy` sıfır uyarı: `DEBUG=False`, `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`,
`CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECRET_KEY` env'den. Ham SQL'de `params`; şablonlarda `|safe` dikkat.

## Test ve dağıtım

pytest-django + `factory_boy`, `@pytest.mark.django_db`, API için `APIClient`, yetki matrisi testleri.
gunicorn/uvicorn, `collectstatic` + WhiteNoise veya CDN, `migrate` deploy adımında, ayrı Celery worker/beat (bkz. `sky-deploy`).
