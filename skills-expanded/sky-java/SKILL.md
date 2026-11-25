---
name: sky-java
description: >-
  Modern Java (17/21+) dil ve araçları (framework'ten bağımsız): Maven/Gradle proje yapısı,
  record'lar, sealed tipler ve pattern matching, switch ifadeleri, Optional, Stream API, değişmez
  koleksiyonlar, virtual thread'ler ve structured concurrency, CompletableFuture, istisna
  yönetimi, java.time, null güvenliği, testler (JUnit 5, AssertJ, Mockito), statik analiz
  (Error Prone, SpotBugs), performans ve JVM ayarları. Java kodu yazarken; Spring için ayrıca sky-spring.
disable-model-invocation: true
---

# Sky · Modern Java

## Dil özellikleri (kullan)

```java
public record Money(long minor, Currency currency) {
    public Money { if (minor < 0) throw new IllegalArgumentException("negatif tutar"); }
    public Money plus(Money o) { requireSame(o); return new Money(minor + o.minor, currency); }
}
public sealed interface PaymentResult permits Paid, Failed, Pending {}
public record Paid(String providerId, Instant at) implements PaymentResult {}
public record Failed(String reason) implements PaymentResult {}
public record Pending() implements PaymentResult {}

String message = switch (result) {                 // derleyici tüm durumları kontrol eder
    case Paid p -> "Ödendi: " + p.providerId();
    case Failed f -> "Başarısız: " + f.reason();
    case Pending ignored -> "Bekliyor";
};
```
- **Record** veri taşıyıcıları (DTO, değer nesnesi), **sealed + pattern matching** durum modelleme, `var` yerel çıkarım (okunurluğu artırıyorsa).
- `Optional` dönüş tipi olarak (alan/parametre olarak değil); `List.of`, `Map.of`, `Stream.toList()` değişmez koleksiyonlar.
- Metin blokları (`"""`), `String.formatted`.

## Eşzamanlılık

- **Virtual thread'ler** (21+): bloklayan I/O ağırlıklı işte basit thread-per-request — `Executors.newVirtualThreadPerTaskExecutor()`.
  `synchronized` içinde uzun bloklama "pinning" yapabilir (yeni sürümlerde azaldı) → `ReentrantLock`.
- `CompletableFuture` zincirleri; structured concurrency (önizleme/sürüme göre) ile alt görevlerin birlikte iptali.
- Paylaşılan durum: `java.util.concurrent` (ConcurrentHashMap, atomics), değişmez nesneler.

## Hata ve null

Beklenen hatalar için anlamlı checked/unchecked ayrımı (çoğu modern kod unchecked + sealed sonuç tipleri), istisnayı yutma, `try-with-resources`;
null: `Objects.requireNonNull`, JSpecify/`@Nullable` açıklamaları + NullAway (derleme zamanı null kontrolü).

## Zaman

`java.time`: `Instant` (an), `LocalDate` (yalnızca tarih), `ZonedDateTime` + `ZoneId.of("Europe/Istanbul")`; `Date`/`Calendar` yok (bkz. `sky-date-time`).

## Yapı ve araçlar

- Maven (`./mvnw`) veya Gradle (Kotlin DSL, version catalog `libs.versions.toml`); wrapper commit'li.
- Biçim: Spotless + google-java-format / palantir; analiz: Error Prone, SpotBugs, Checkstyle; bağımlılık açıkları: OWASP dependency-check.
- Test: JUnit 5 (`@ParameterizedTest`), AssertJ, Mockito (sınırlarda), Testcontainers (bkz. `sky-spring`).

## Performans

Önce ölç: JFR (Java Flight Recorder) + JDK Mission Control, async-profiler; GC: varsayılan G1 çoğu iş yükünde iyi, düşük gecikme için ZGC (`-XX:+UseZGC`);
konteynerde `-XX:MaxRAMPercentage=75`; başlangıç süresi için CDS/AOT veya GraalVM native image.
