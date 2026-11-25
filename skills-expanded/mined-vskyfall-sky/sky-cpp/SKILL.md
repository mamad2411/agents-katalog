---
name: sky-cpp
description: >-
  Modern C++ (17/20/23) ve C: CMake ile proje yapısı ve bağımlılıklar (vcpkg, Conan,
  FetchContent), RAII ve akıllı işaretçiler, değer semantiği ve move, std::span/string_view/
  optional/expected/variant, hata yönetimi, bellek güvenliği (sanitizer'lar), eşzamanlılık
  (std::thread, jthread, atomic, mutex), şablonlar ve concepts, derleyici uyarıları, clang-tidy
  ve clang-format, testler (GoogleTest, Catch2), gömülü sistemlerde C/C++ notları. C veya C++
  kodu yazarken/incelerken kullan.
disable-model-invocation: true
---

# Sky · C++ / C

## Proje (CMake)

```cmake
cmake_minimum_required(VERSION 3.25)
project(skycore LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)            # clangd / clang-tidy için

add_library(skycore src/slots.cpp)
target_include_directories(skycore PUBLIC include)
target_compile_options(skycore PRIVATE $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic -Wconversion -Werror>)

include(FetchContent)
FetchContent_Declare(googletest URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip)
FetchContent_MakeAvailable(googletest)
add_executable(skycore_tests tests/slots_test.cpp)
target_link_libraries(skycore_tests PRIVATE skycore GTest::gtest_main)
```
Hedef bazlı (target_*) CMake; global `include_directories` yok. Bağımlılıklar: vcpkg (manifest modu) veya Conan; küçükler FetchContent.
`CMakePresets.json` ile debug/release/asan yapılandırmaları.

## Modern C++ kuralları

- **RAII**: kaynak = nesne ömrü. Ham `new/delete` yok → `std::unique_ptr` (varsayılan), paylaşım gerçekten gerekiyorsa `std::shared_ptr`.
- Parametre: okuma `const T&` / `std::string_view` / `std::span<const T>`; sahiplik devri `T` (by value) + `std::move`.
- `std::optional` (olmayabilir), `std::expected<T, E>` (C++23 — hata dönüşü), `std::variant` + `std::visit` (durum modelleme).
- `auto` okunurluğu artırıyorsa; aralık tabanlı `for`, `<algorithm>` / `<ranges>`.
- `enum class`, `constexpr`, `[[nodiscard]]`, `= delete` / `= default`.
- Beşler kuralı veya sıfırlar kuralı (tercihen sıfır: üyeler kendi kaynaklarını yönetsin).
- Concepts ile şablon kısıtları (`template <std::integral T>`), hata mesajları okunur.

## Bellek güvenliği

Geliştirme/CI'da sanitizer'lar: `-fsanitize=address,undefined` (ASan/UBSan), eşzamanlılıkta `-fsanitize=thread`; Valgrind alternatif.
Sık hatalar: sarkan referans/`string_view` (geçici nesneye), yineleyici geçersizleşmesi (döngüde `push_back`), işaretsiz/işaretli karşılaştırma, ilklendirilmemiş değişken, tamsayı taşması.

## Eşzamanlılık

`std::jthread` (+ `stop_token`), `std::mutex` + `std::scoped_lock`, `std::atomic`, `std::async` dikkatli; veri yarışlarını TSan ile ara. Mümkünse paylaşılan durumu azalt, mesaj kuyruğu kullan.

## Araçlar

clang-format (`.clang-format`), clang-tidy (`modernize-*`, `bugprone-*`, `cppcoreguidelines-*`), cppcheck; testler GoogleTest veya Catch2; benchmark Google Benchmark; profil `perf` / Instruments.

## C ve gömülü notları

C'de: sınır kontrolü (`snprintf`, uzunluklu kopyalama), `-Wall -Wextra`, statik analiz, `const` doğruluğu. Gömülü (bkz. `sky-iot`): dinamik bellekten kaçın (ön ayrılmış tamponlar), `volatile` donanım yazmaçları için, kesme (ISR) içinde kısa iş, `static_assert` ile boyut kontrolleri.
