---
name: kotlin-skill
description: all about kotlin overpower audit.
disable-model-invocation: true
argument-hint: "every kotlin argument and prompt use this skill for audit and anymore"
---

Kalau membuat aplikasi **Android menggunakan Kotlin**, yang perlu dimaksimalkan bukan cuma “aplikasinya bisa jalan”. Ada beberapa lapisan yang sebaiknya dipastikan sejak awal: **arsitektur, performa, keamanan, UI/UX, database, koneksi jaringan, dan maintainability**.

Kalau kamu sedang membangun aplikasi Kotlin yang nantinya ingin benar-benar dipakai orang, saya akan membaginya seperti ini:

## 1. Arsitektur aplikasi — paling penting

Pastikan dari awal kode tidak bercampur antara UI, database, jaringan, dan logika bisnis.

Struktur yang umum dan bagus:

```text
UI
 ↓
ViewModel
 ↓
Use Case / Business Logic
 ↓
Repository
 ↓
Data Source
 ├── Remote API / Firebase
 └── Local Database
```

Contohnya:

```text
LoginScreen
    ↓
LoginViewModel
    ↓
LoginUseCase
    ↓
AuthRepository
    ↓
Firebase / API
```

**Hindari:**

```kotlin
Button {
    // langsung request Firebase
    // langsung manipulasi database
    // langsung menyimpan SharedPreferences
}
```

Karena ketika aplikasi membesar, kode seperti itu cepat menjadi sulit dirawat.

---

# 2. Kotlin-nya sendiri harus dimanfaatkan dengan baik

Jangan menggunakan Kotlin seperti Java yang diganti sintaksnya.

Maksimalkan:

* `data class`
* `sealed class`
* `enum class`
* `object`
* extension function
* nullable safety
* `Result`
* coroutine
* `Flow`
* `StateFlow`
* collection API
* scope function secara wajar

Contoh state UI:

```kotlin
sealed class UiState {
    data object Loading : UiState()

    data class Success(
        val data: List<User>
    ) : UiState()

    data class Error(
        val message: String
    ) : UiState()
}
```

Ini jauh lebih jelas daripada membuat banyak variabel boolean:

```kotlin
var isLoading = false
var isError = false
var isSuccess = false
```

---

# 3. Coroutine dan asynchronous harus benar

Ini salah satu hal yang **wajib dipastikan**.

Jangan melakukan operasi berat di main thread.

Misalnya:

```kotlin
viewModelScope.launch {
    val data = repository.getUsers()
}
```

Kemudian repository menangani pekerjaan yang membutuhkan thread sesuai kebutuhan.

Pahami:

* `Coroutine`
* `Dispatchers`
* `viewModelScope`
* `lifecycleScope`
* `Flow`
* `StateFlow`
* cancellation
* exception handling

Terutama jangan sampai aplikasi mengalami:

```text
Application Not Responding
```

karena operasi database/network dilakukan di UI thread.

---

# 4. State management

Aplikasi modern harus punya pengelolaan keadaan yang jelas.

Misalnya halaman login:

```text
Idle
 ↓
Loading
 ↓
Success
```

atau:

```text
Idle
 ↓
Loading
 ↓
Error
```

Gunakan pola seperti:

```kotlin
StateFlow<UiState>
```

Contohnya:

```kotlin
private val _uiState =
    MutableStateFlow<UiState>(UiState.Loading)

val uiState: StateFlow<UiState> =
    _uiState.asStateFlow()
```

Kemudian UI hanya mengamati state.

Ini sangat membantu ketika aplikasi mulai kompleks.

---

# 5. Jetpack Compose / XML harus konsisten

Kalau menggunakan **Jetpack Compose**, maksimalkan:

* `Composable`
* state hoisting
* `remember`
* `rememberSaveable`
* `LaunchedEffect`
* `DisposableEffect`
* Navigation
* Material 3
* Preview

Jangan membuat satu `Composable` berisi 500–1000 baris.

Pecah:

```text
LoginScreen
 ├── LoginHeader
 ├── EmailField
 ├── PasswordField
 ├── LoginButton
 └── ForgotPasswordButton
```

Kalau menggunakan XML, prinsipnya sama: pisahkan komponen dan jangan membuat Activity menjadi tempat seluruh logika aplikasi.

---

# 6. Navigation

Navigation harus dirancang sejak awal.

Misalnya:

```text
Splash
   ↓
Login
   ↓
Home
 ├── Profile
 ├── Settings
 └── Detail
```

Pastikan:

* back navigation benar
* deep link kalau diperlukan
* state tidak hilang sembarangan
* user tidak bisa kembali ke halaman login setelah logout
* authentication flow jelas

Kesalahan navigation biasanya baru terasa ketika aplikasi sudah besar.

---

# 7. Database lokal

Kalau aplikasi membutuhkan penyimpanan lokal, jangan semuanya dimasukkan ke:

```text
SharedPreferences
```

Untuk data terstruktur gunakan **Room**.

Contoh:

```text
Room
 ├── Entity
 ├── DAO
 └── Database
```

Sedangkan data sederhana seperti:

```text
dark_mode = true
language = id
onboarding_completed = true
```

bisa menggunakan **DataStore**.

Jadi secara sederhana:

| Kebutuhan        | Pilihan                    |
| ---------------- | -------------------------- |
| Data sederhana   | DataStore                  |
| Data terstruktur | Room                       |
| Cache            | Room                       |
| Token/session    | mekanisme penyimpanan aman |
| File/gambar      | Storage/file system        |

---

# 8. Network/API

Kalau aplikasi menggunakan API, pastikan:

```text
UI
 ↓
ViewModel
 ↓
Repository
 ↓
API Service
```

Jangan:

```text
Activity → HTTP request
```

Biasanya stack yang nyaman:

```text
Retrofit
OkHttp
Kotlin Coroutines
Serialization/Moshi
```

Dan wajib menangani:

```text
200 → berhasil
400 → request salah
401 → belum login/token expired
403 → tidak punya akses
404 → data tidak ditemukan
500 → server bermasalah
timeout → koneksi bermasalah
no internet → offline
```

Jangan menganggap network selalu tersedia.

---

# 9. Error handling

Ini sering dilupakan.

Aplikasi jangan hanya memikirkan:

```text
SUCCESS
```

Tapi juga:

```text
Loading
Success
Empty
Error
Offline
Unauthorized
Timeout
```

Misalnya ketika Firebase/API gagal:

**Jangan:**

```text
Something went wrong
```

Kalau bisa tampilkan pesan yang membantu:

```text
Tidak dapat terhubung ke server.
Periksa koneksi internet Anda dan coba lagi.
```

Dan error detail tetap dicatat ke log/crash monitoring, bukan ditampilkan mentah kepada user.

---

# 10. Security

Ini **sangat penting**, terutama kalau aplikasinya berhubungan dengan akun, pembayaran, Firebase, atau data pengguna.

Pastikan:

### Jangan menyimpan secret di APK

Jangan:

```kotlin
const val SECRET_KEY = "xxxxxxxx"
```

karena APK bisa dianalisis.

### Jangan menyimpan password user

Password seharusnya ditangani oleh sistem autentikasi yang memang dirancang untuk itu.

### Lindungi token

Pertimbangkan penyimpanan yang aman untuk credential/session yang sensitif.

### Jangan percaya data dari client

Misalnya:

```text
Harga = 10.000
```

Jangan membuat server percaya:

```text
"harga": 10000
```

yang dikirim aplikasi.

Validasi penting harus dilakukan di server.

---

# 11. Firebase Rules / backend security

Kalau menggunakan Firebase, jangan hanya fokus pada kode Kotlin.

Misalnya Firestore:

```text
allow read, write: if true;
```

untuk aplikasi produksi adalah **red flag besar**.

Rules harus benar-benar membatasi:

```text
siapa yang boleh membaca
siapa yang boleh menulis
data apa yang boleh diubah
```

Ini sama pentingnya dengan kode Kotlin.

---

# 12. Performance

Pastikan aplikasi:

* tidak sering freeze
* tidak boros RAM
* tidak boros baterai
* tidak melakukan request berlebihan
* tidak melakukan recomposition berlebihan
* tidak memuat gambar berukuran sangat besar
* tidak menyimpan object besar tanpa alasan
* tidak membuat memory leak

Perhatikan juga:

```text
Startup time
Frame rendering
Memory
CPU
Battery
Network usage
```

---

# 13. Image handling

Kalau aplikasi menggunakan banyak gambar, jangan:

```kotlin
BitmapFactory.decodeResource(...)
```

untuk semuanya secara sembarangan.

Gunakan image loading library seperti:

```text
Coil
```

dan manfaatkan:

* caching
* resizing
* lazy loading
* thumbnail
* placeholder

Karena gambar sering menjadi salah satu penyebab aplikasi boros RAM.

---

# 14. Offline-first / koneksi buruk

Kalau aplikasimu membutuhkan internet, pikirkan:

```text
Internet tersedia
Internet lambat
Internet putus
Server down
```

Misalnya:

```text
User membuka aplikasi
       ↓
Data lokal
       ↓
Tampilkan data
       ↓
Sinkronisasi server
```

Untuk aplikasi tertentu, pendekatan seperti ini jauh lebih bagus daripada:

```text
Internet harus tersedia
        ↓
baru aplikasi bisa digunakan
```

---

# 15. Logging

Saat development:

```kotlin
Log.d("Auth", "User logged in")
```

boleh.

Tapi jangan sampai production menghasilkan log sensitif:

```text
password=123456
token=eyJ...
```

Gunakan logging secara terkontrol dan hindari data sensitif.

---

# 16. Crash monitoring

Aplikasi produksi sebaiknya bisa menjawab:

> “Kenapa aplikasi user A crash?”

Jangan hanya mengandalkan laporan:

> "Bang aplikasinya keluar sendiri."

Gunakan crash monitoring seperti Firebase Crashlytics atau alternatif lain.

Dengan begitu kamu bisa melihat:

```text
Crash
 ↓
Stack trace
 ↓
Device
 ↓
Android version
 ↓
App version
 ↓
Jumlah pengguna terdampak
```

---

# 17. Testing

Minimal pikirkan tiga level:

```text
Unit Test
    ↓
Repository / Use Case

Integration Test
    ↓
Database / API

UI Test
    ↓
Screen / User interaction
```

Contoh alur yang sangat layak dites:

```text
Login
Register
Logout
Forgot Password
CRUD data
Payment
Network failure
Token expired
```

Jangan hanya mengetes kondisi normal.

---

# 18. Dependency management

Jangan memasukkan library hanya karena:

> "Kayaknya ini bagus."

Setiap dependency menambah:

* ukuran aplikasi
* kemungkinan bug
* vulnerability
* maintenance

Jadi sebelum menambahkan library, tanyakan:

> Apakah saya benar-benar membutuhkannya?

Dan gunakan versi dependency yang masih didukung.

---

# 19. Build dan release

Pastikan kamu memahami perbedaan:

```text
Debug
↓
Testing
↓
Release
↓
Signed APK/AAB
↓
Production
```

Untuk production pastikan:

* signing benar
* `minSdk` sesuai
* `targetSdk` sesuai
* ProGuard/R8 bila diperlukan
* resource shrinking bila sesuai
* build reproducible
* versionCode naik
* versionName jelas

---

# 20. CI/CD

Kalau aplikasi sudah serius, jangan setiap kali:

```text
ubah kode
 ↓
build manual
 ↓
copy APK
 ↓
install
```

Pertimbangkan:

```text
Git
 ↓
Push
 ↓
CI
 ↓
Test
 ↓
Build
 ↓
Release
```

Misalnya menggunakan GitHub Actions.

---

# 21. Struktur project

Untuk project yang akan berkembang, saya sangat menyarankan struktur yang jelas.

Contohnya:

```text
app/
└── src/main/java/com/example/app/

    ├── core/
    │   ├── network/
    │   ├── database/
    │   ├── security/
    │   └── util/

    ├── data/
    │   ├── local/
    │   ├── remote/
    │   └── repository/

    ├── domain/
    │   ├── model/
    │   └── usecase/

    └── presentation/
        ├── login/
        ├── home/
        ├── profile/
        └── settings/
```

Tidak harus persis seperti ini, tetapi prinsip pemisahannya bagus.

---

# 22. UI/UX

Jangan hanya memastikan:

> "Fungsinya bekerja."

Pastikan juga:

```text
User tahu harus melakukan apa
User tahu aplikasi sedang melakukan apa
User tahu ketika terjadi error
User tidak bingung setelah menekan tombol
```

Perhatikan:

* loading
* empty state
* error state
* disabled state
* feedback setelah aksi
* ukuran tombol
* typography
* spacing
* accessibility
* dark mode
* font scaling

---

# 23. Accessibility

Ini sering dilewatkan.

Pastikan:

* teks tidak terlalu kecil
* kontras cukup
* tombol memiliki area sentuh yang layak
* ikon tidak menjadi satu-satunya penanda
* `contentDescription` untuk elemen yang relevan
* aplikasi tetap usable ketika ukuran font diperbesar

---

# 24. Battery & background process

Jangan membuat aplikasi terus menerus melakukan:

```text
while(true)
```

atau polling:

```text
request API
↓
tunggu 1 detik
↓
request API
↓
tunggu 1 detik
```

untuk sesuatu yang sebenarnya bisa menggunakan:

```text
WorkManager
FCM
AlarmManager
Foreground Service
```

sesuai kebutuhan.

---

# 25. Yang paling sering saya prioritaskan

Kalau kamu ingin membuat **aplikasi Kotlin yang benar-benar production-ready**, saya akan memberikan prioritas seperti ini:

| Prioritas | Bagian                | Kepentingan     |
| --------- | --------------------- | --------------- |
| 🔴 1      | Arsitektur            | Sangat tinggi   |
| 🔴 2      | Security              | Sangat tinggi   |
| 🔴 3      | State management      | Sangat tinggi   |
| 🔴 4      | Error handling        | Sangat tinggi   |
| 🔴 5      | Database & data flow  | Sangat tinggi   |
| 🔴 6      | Network handling      | Sangat tinggi   |
| 🟠 7      | Lifecycle & coroutine | Tinggi          |
| 🟠 8      | Performance           | Tinggi          |
| 🟠 9      | Testing               | Tinggi          |
| 🟠 10     | UI/UX                 | Tinggi          |
| 🟡 11     | Logging & monitoring  | Menengah–tinggi |
| 🟡 12     | CI/CD                 | Menengah–tinggi |
| 🟡 13     | Accessibility         | Menengah        |
| 🟡 14     | Optimasi build        | Menengah        |

### Kalau disederhanakan:

```text
                    APLIKASI KOTLIN
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
     UI/UX            BUSINESS LOGIC       DATA
        │                 │                 │
   Compose/XML         ViewModel         Repository
        │              UseCase              │
        │                 │           ┌─────┴─────┐
        │                 │           ↓           ↓
        │                 │        Local       Remote
        │                 │        Room       API/Firebase
        │                 │
        └─────────────────┼─────────────────┘
                          ↓
                  SECURITY + ERROR
                          ↓
                  TEST + MONITORING
                          ↓
                    RELEASE/CI-CD
```

**Kalau kamu baru mulai serius dengan Kotlin Android, jangan langsung mengejar semua hal di atas sekaligus.** Urutan belajarnya lebih efektif:

**Kotlin → Coroutine → Jetpack Compose → ViewModel/State → Navigation → Repository → Room/API/Firebase → Security → Testing → Performance → CI/CD → Release.**

Dengan urutan itu, kamu bukan cuma belajar "cara membuat aplikasi Kotlin", tetapi belajar **cara membuat aplikasi Kotlin yang bisa dipelihara dan dikembangkan ketika project sudah besar**.
