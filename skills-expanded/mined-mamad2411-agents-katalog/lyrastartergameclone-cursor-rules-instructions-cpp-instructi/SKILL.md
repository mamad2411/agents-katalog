---
description: 일반 C++ 코드 스타일 가이드
globs: *.c,*.cpp,*.hpp,*.h
alwaysApply: false
---

# 일반 C++ 코드 스타일 가이드

이 문서는 언리얼 엔진 외부의 일반 C++ 코드 작성을 위한 스타일 가이드입니다. 구글 C++ 스타일 가이드를 기반으로 작성되었습니다.

- https://google.github.io/styleguide/cppguide.html

## 목차

1. [파일 구성](mdc:#1-파일-구성)
2. [명명 규칙](mdc:#2-명명-규칙)
3. [형식 지정](mdc:#3-형식-지정)
4. [주석](mdc:#4-주석)
5. [클래스](mdc:#5-클래스)
6. [함수](mdc:#6-함수)
7. [기타 C++ 기능](mdc:#7-기타-c-기능)
8. [일반 원칙](mdc:#8-일반-원칙)

## 1. 파일 구성

### 1.1 파일 확장자

- C++ 소스 파일: `.cpp`
- C++ 헤더 파일: `.h`
- 인라인 함수 정의: `.inl` (선택 사항)

### 1.2 파일 이름

- 모든 파일 이름은 소문자를 사용합니다.
- 단어 사이에는 밑줄(`_`)을 사용합니다. (예: `my_useful_class.cpp`)
- 클래스가 정의된 헤더 파일은 클래스 이름을 사용합니다. (예: 클래스 `MyClass`는 `my_class.h`에 정의)

### 1.3 헤더 파일

- 모든 `.cpp` 파일은 해당 `.h` 파일이 있어야 합니다 (특수 상황 제외).
- 헤더 파일은 자체 완비적(self-contained)이어야 합니다 - 즉, 어떤 다른 파일의 포함 없이도 독립적으로 컴파일 가능해야 합니다.
- 모든 헤더 파일은 `#include` 가드를 포함해야 합니다:

```cpp
#ifndef PROJECT_PATH_FILE_H_
#define PROJECT_PATH_FILE_H_

// 코드 내용...

#endif  // PROJECT_PATH_FILE_H_
```

또는 `#pragma once`를 사용할 수 있습니다:

```cpp
#pragma once

// 코드 내용...
```

### 1.4 Include 순서

1. 관련 헤더 파일: 소스 파일은 해당 헤더를 첫 번째로 포함 (예: `foo.cpp`는 `foo.h`를 첫 번째로 포함)
2. C 시스템 헤더 (`<stdio.h>` 등)
3. C++ 표준 라이브러리 헤더 (`<vector>` 등)
4. 다른 라이브러리 헤더
5. 프로젝트 헤더

각 그룹은 알파벳 순서로 정렬하고, 그룹 사이에는 빈 줄을 넣습니다.

```cpp
// foo.cpp
#include "foo.h"

#include <sys/types.h>
#include <unistd.h>

#include <algorithm>
#include <string>
#include <vector>

#include "base/logging.h"
#include "base/macros.h"
#include "foo/public/other_header.h"
```

## 2. 명명 규칙

### 2.1 일반 규칙

- 이름은 의미 있고 설명적이어야 합니다.
- 축약어와 단축 형태는 일반적으로 통용되는 경우에만 사용합니다.
- 약어는 모두 대문자로 작성하거나 첫 글자만 대문자로 작성합니다. (예: `HTTP` 또는 `Http`, `URL` 또는 `Url`)

### 2.2 파일 명명

- 소문자와 밑줄(`_`) 사용: `my_useful_class.cpp`

### 2.3 타입 명명

- 클래스, 구조체, 타입 별칭, 열거형, 타입 템플릿 매개변수는 파스칼 케이스를 사용합니다:
  - 단어의 첫 글자를 대문자로 작성, 밑줄 사용하지 않음
  - 예: `MyExcitingClass`, `MyImportantEnum`

```cpp
class UrlTable { ... };
struct UrlTableProperties { ... };
using PropertiesMap = map<string, string>;
enum UrlTableError { ... };
```

### 2.4 변수 명명

- 변수명은 소문자와 밑줄로 작성합니다.
- 클래스 멤버 변수는 끝에 밑줄을 추가합니다.

```cpp
string table_name;       // 일반 변수
string table_name_;      // 클래스 멤버 변수
```

### 2.5 상수 명명

- 상수는 `k`로 시작하는 파스칼 케이스를 사용합니다.

```cpp
const int kDaysInAWeek = 7;
const int kAndroidVersions[] = { 10, 11, 12 };
```

### 2.6 함수 명명

- 일반 함수는 파스칼 케이스를 사용합니다. (예: `AddTableEntry()`)
- 접근자와 변경자는 변수 이름처럼 명명하고, Get/Set을 접두어로 사용합니다. (예: `GetCount()`, `SetCount()`)
- 단순 속성 접근의 경우 속성 이름만 사용합니다. (예: `count()`)

```cpp
class MyClass {
public:
    int count() const { return count_; }
    void set_count(int count) { count_ = count; }
    // 더 복잡한 작업을 할 때:
    void AddCount(int count);
    int GetCalculatedCount() const;

private:
    int count_;
};
```

### 2.7 네임스페이스 명명

- 네임스페이스는 소문자로 작성합니다.
- 최상위 네임스페이스는 프로젝트 이름이나 팀 이름을 기반으로 합니다.

```cpp
namespace project_name {
namespace sub_component {
// ...
}  // namespace sub_component
}  // namespace project_name
```

### 2.8 열거형 명명

- 열거형 값은 상수와 동일한 명명 규칙을 따릅니다 (접두어 `k` 사용).

```cpp
enum class UrlTableError {
    kOk = 0,
    kOutOfMemory,
    kMalformedInput,
};
```

### 2.9 매크로 명명

- 매크로는 되도록 사용하지 않습니다.
- 필요할 경우 모두 대문자와 밑줄을 사용합니다.

```cpp
#define ROUND(x) ...
#define PI_ROUNDED 3.0
```

## 3. 형식 지정

### 3.1 줄 길이

- 한 줄은 80자 이내로 제한합니다.

### 3.2 들여쓰기

- 들여쓰기는 공백 2칸을 사용합니다.
- 탭은 사용하지 않습니다.
- 네임스페이스 내용은 들여쓰기하지 않습니다.

```cpp
namespace outer {
namespace inner {
// 네임스페이스 내용은 들여쓰기하지 않습니다.
class MyClass {  // 클래스 내용은 2칸 들여쓰기
 public:
  void Function() {  // 함수 내용은 2칸 들여쓰기
    if (condition) {  // 조건문 내용은 2칸 들여쓰기
      DoSomething();  // 코드 내용은 2칸 들여쓰기
    }
  }
};
}  // namespace inner
}  // namespace outer
```

### 3.3 괄호 스타일

- 여는 중괄호(`{`)는 함수, 클래스, 네임스페이스 선언에서 새 줄에 배치하지 않고, 문장 끝에 함께 둡니다.
- 조건문과 루프의 경우에도 여는 중괄호는 같은 줄에 배치합니다.

```cpp
if (condition) {  // 여는 중괄호는 같은 줄에
  // 코드
} else {  // else도 같은 줄에
  // 코드
}

for (int i = 0; i < kSomeNumber; ++i) {
  // 코드
}

class MyClass {
 public:
  MyClass() : some_var_(0) {}  // 간단한 생성자는 한 줄로

  void Method() {
    // 메서드 코드
  }

 private:
  int some_var_;
};
```

### 3.4 함수 선언 및 정의

- 함수 매개변수가 한 줄에 맞지 않으면, 들여쓰기를 4칸 하고 각 매개변수를 새 줄에 배치합니다.
- 반환 타입은 함수 이름과 같은 줄에 배치합니다.

```cpp
ReturnType ClassName::FunctionName(Type par1, Type par2) {
  // 함수 내용
}

ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par1,  // 매개변수 4칸 들여쓰기
    Type par2,
    Type par3) {
  // 함수 내용
}
```

### 3.5 조건문

- 조건문은 항상 중괄호를 사용합니다 (한 줄 조건문도 마찬가지).

```cpp
if (condition) {
  DoOneThing();
}

// 한 줄이라도 중괄호 사용
if (condition) {
  DoOneThing();
}

// if-else 체인
if (condition) {
  // 코드
} else if (condition2) {
  // 코드
} else {
  // 코드
}
```

### 3.6 스위치문

- 각 case 문은 switch와 같은 들여쓰기 레벨입니다.
- case 내부 코드는 2칸 들여쓰기합니다.

```cpp
switch (var) {
  case 0:
    DoZero();
    break;
  case 1: {
    // 블록 사용 시 중괄호 필요
    DoOne();
    break;
  }
  default:
    DoDefault();
}
```

### 3.7 포인터와 참조

- 포인터와 참조 기호는 변수 이름이 아닌 타입에 붙입니다.

```cpp
// 올바른 방식
char* c;
const string& str;

// 잘못된 방식
char *c;
const string &str;
```

### 3.8 수평 공백

- 연산자 전후에 공백을 하나씩 추가합니다.
- 콤마 뒤에는 공백을 하나 추가합니다.
- 다음과 같은 경우에는 공백을 추가하지 않습니다:
  - 함수 이름과 여는 괄호 사이
  - 배열 이름과 여는 대괄호 사이
  - 괄호/대괄호의 안쪽

```cpp
// 올바른 사용
sum = a + b;
array[index] = 0;
for (int i = 0; i < 10; ++i) {}
Function(arg1, arg2);
```

### 3.9 수직 공백

- 함수 사이, 클래스 정의 사이에는 빈 줄을 하나 넣습니다.
- 논리적으로 구분되는 코드 블록 사이에는 빈 줄을 넣어 가독성을 높입니다.

## 4. 주석

### 4.1 파일 주석

- 각 소스 파일 상단에 라이센스 표시 후 파일 내용에 대한 간략한 설명을 추가합니다.

```cpp
// Copyright [Year] [의도된 저작권 소유자]. All rights reserved.
// 라이센스 정보...

// 이 파일은 사용자 인증을 처리하는 클래스를 포함합니다.
// 주요 기능:
// - 비밀번호 검증
// - 토큰 생성
// - 세션 관리
```

### 4.2 클래스 주석

- 클래스 정의 전에 해당 클래스의 목적과 사용법을 설명합니다.

```cpp
// MutexLock은 뮤텍스 잠금/해제를 자동으로 처리하는 RAII 타입의 클래스입니다.
// 이 클래스의 인스턴스가 소멸될 때 자동으로 뮤텍스가 해제됩니다.
//
// 사용 예:
//   Mutex mu;
//   {
//     MutexLock lock(&mu);  // 뮤텍스 잠금
//     DoSomething();
//   }  // 범위를 벗어나면 자동으로 뮤텍스 해제
class MutexLock {
  // ...
};
```

### 4.3 함수 주석

- 함수 선언 전에 함수의 동작, 매개변수, 반환값, 예외 등을 설명합니다.

```cpp
// 주어진 문자열에서 모든 공백을 제거합니다.
//
// 매개변수:
//   str - 공백을 제거할 문자열(복사되지 않고 직접 수정됨)
//
// 반환값:
//   제거된 공백 문자의 수
//
// 예외:
//   std::bad_alloc - 메모리 할당에 실패한 경우
int RemoveSpaces(string* str);
```

### 4.4 구현 주석

- 코드의 복잡한 부분이나 비직관적인 부분에 주석을 추가합니다.
- "무엇을"이 아닌 "왜"에 초점을 맞춥니다.

```cpp
// 이 알고리즘은 O(n^2)이지만 n이 항상 작기 때문에 문제가 없습니다.
// 또한 더 효율적인 O(n log n) 알고리즘은 추가 메모리를 필요로 합니다.
for (int i = 0; i < n; ++i) {
  for (int j = 0; j < n; ++j) {
    // ...
  }
}
```

### 4.5 TODO 주석

- 아직 완료되지 않은 작업에 TODO 주석을 사용합니다.
- 일관된 형식을 사용하고 가능하면 담당자나 이슈 번호를 포함합니다.

```cpp
// TODO(username): 이 함수를 더 효율적으로 구현하기 (이슈 #123)
void IneffientFunction() {
  // ...
}
```

## 5. 클래스

### 5.1 클래스 구조

- 접근 제어 지정자(public, protected, private)를 명시적으로 사용하고, 다음 순서로 배치합니다:

  1. public:
  2. protected:
  3. private:

- 각 섹션 내에서는 다음 순서로 멤버를 배치합니다:
  1. 타입 (typedef, using, 중첩 구조체와 클래스 등)
  2. 상수
  3. 생성자
  4. 소멸자
  5. 메서드
  6. 데이터 멤버

```cpp
class MyClass {
 public:  // 접근 지정자는 들여쓰기 없이 왼쪽 정렬
  // 타입
  using Iterator = std::vector<int>::iterator;

  // 상수
  static constexpr int kMaxSize = 100;

  // 생성자 및 소멸자
  MyClass();
  ~MyClass();

  // 메서드
  void DoSomething();

 protected:
  // protected 멤버들...

 private:
  // private 메서드
  void HelperFunction();

  // 데이터 멤버
  int counter_;
};
```

### 5.2 생성자 초기화 리스트

- 한 줄에 맞으면 한 줄로 작성합니다.
- 그렇지 않으면 콜론(:)을 첫 줄에 두고, 각 멤버 초기화를 새 줄에 4칸 들여쓰기하여 배치합니다.

```cpp
// 한 줄로 가능한 경우
MyClass::MyClass(int var) : some_var_(var), other_var_(0) {
  DoSomething();
}

// 여러 줄이 필요한 경우
MyClass::MyClass(int var)
    : some_var_(var),
      some_other_var_(var + 1),
      yet_another_var_(var + 2) {
  DoSomething();
}
```

### 5.3 상속

- 클래스 이름과 콜론 사이에 공백을 두고, 기본 클래스 목록은 들여쓰기합니다.

```cpp
class DerivedClass : public BaseClass1,
                      public BaseClass2,
                      private BaseClass3 {
 public:
  DerivedClass(int var);
  ~DerivedClass() override;

  void Method() override;
};
```

## 6. 함수

### 6.1 매개변수 순서

- 함수 매개변수 순서: 입력 전용 매개변수, 그 다음 입출력 매개변수, 마지막으로 출력 전용 매개변수.

```cpp
// input_param: 입력 전용
// inout_param: 입출력 매개변수
// output_param: 출력 전용
void Function(const string& input_param, int* inout_param, string* output_param);
```

### 6.2 기본 인수

- 기본 인수는 가상 함수와 재정의되는 함수에는 사용하지 않습니다.
- 복잡한 표현식은 기본 인수로 사용하지 않습니다.

```cpp
// 간단한 기본 인수는 허용됩니다
void Connect(const std::string& server, int port = 443);
```

### 6.3 함수 오버로딩

- 오버로딩은 매개변수 타입이 명확하게 다를 때만 사용합니다.
- 매개변수 순서만 다른 오버로딩은 피합니다.

```cpp
// 좋은 예: 타입이 명확하게 다름
void Print(int value);
void Print(const std::string& value);

// 나쁜 예: 순서만 다름
void Process(int priority, const std::string& name);
void Process(const std::string& name, int priority);
```

### 6.4 함수 크기

- 함수는 되도록 짧고 집중적인 기능을 수행해야 합니다.
- 40줄 이상의 함수는 더 작은 함수로 분리하는 것을 고려하세요.

## 7. 기타 C++ 기능

### 7.1 예외 처리

- 예외는 정말 예외적인 상황에만 사용합니다.
- 예외를 사용할 때는 명확한 예외 계층 구조를 만들고, 문서화합니다.
- 생성자에서 발생할 수 있는 예외는 특히 주의합니다.

```cpp
try {
  DoSomethingThatMightThrow();
} catch (const DatabaseException& e) {
  // 데이터베이스 예외 처리
} catch (const NetworkException& e) {
  // 네트워크 예외 처리
} catch (const std::exception& e) {
  // 표준 라이브러리 예외 처리
} catch (...) {
  // 기타 모든 예외 처리
}
```

### 7.2 RTTI (실행 시간 타입 정보)

- RTTI(dynamic_cast, typeid)는 가능한 한 사용을 제한합니다.
- 다형성 계층에서 타입을 구분해야 할 경우, 가상 함수를 사용하는 것이 더 좋습니다.

### 7.3 캐스팅

- C++ 스타일 캐스트를 사용합니다.
  - `static_cast<>`
  - `const_cast<>`
  - `reinterpret_cast<>`
- C 스타일 캐스트는 사용하지 않습니다.

```cpp
// 좋은 예: C++ 스타일 캐스트
float f = 3.14f;
int i = static_cast<int>(f);

// 나쁜 예: C 스타일 캐스트
int j = (int)f;  // 사용하지 마세요
```

### 7.4 스트림

- 간단한 텍스트 입출력은 스트림을 사용합니다.
- 성능이 중요한 코드에서는 스트림 대신 더 효율적인 방법을 고려합니다.

```cpp
// 간단한 파일 읽기 예제
std::ifstream file("filename.txt");
std::string line;
while (std::getline(file, line)) {
  // 라인 처리
}
```

### 7.5 전역 변수

- 전역 변수와 정적 변수 사용을 최소화합니다.
- 필요한 경우 네임스페이스 내에 선언하고, const 또는 constexpr로 만듭니다.

```cpp
namespace myproject {
namespace {
// 이 파일 내에서만 접근 가능한 상수
constexpr int kLocalConstant = 42;
}  // namespace

// 이 네임스페이스 내에서만 접근 가능한 상수
const int kGlobalConstant = 123;
}  // namespace myproject
```

### 7.6 C++11 이상의 기능

- auto: 타입이 명확할 때만 사용하고, 과도한 사용은 피합니다.
- 람다 함수: 간단한 경우에 사용하고, 복잡한 람다는 명명된 함수로 분리합니다.
- 스마트 포인터: 리소스 관리를 위해 `unique_ptr`와 `shared_ptr`을 적절히 활용합니다.
- Move 의미론: 성능이 중요한 곳에서 활용합니다.

```cpp
// auto의 적절한 사용
auto iter = container.begin();  // 타입이 명확함

// 람다 함수
std::sort(v.begin(), v.end(), [](int a, int b) { return a < b; });

// 스마트 포인터
std::unique_ptr<Resource> resource = std::make_unique<Resource>();
```

## 8. 일반 원칙

### 8.1 소유권과 수명

- 리소스 소유권은 명확해야 합니다.
- 가능한 스마트 포인터나 컨테이너를 사용하여 리소스 관리를 자동화합니다.
- RAII 원칙을 따릅니다 (자원의 획득은 초기화, 자원의 해제는 소멸).

```cpp
// RAII 예제
{
  std::unique_ptr<Resource> resource = std::make_unique<Resource>();
  resource->DoSomething();
}  // 범위를 벗어나면 자동으로 Resource가 해제됨
```

### 8.2 단일 책임 원칙

- 각 클래스와 함수는 하나의 책임만 가져야 합니다.
- 여러 책임을 가진 클래스는 더 작은 클래스들로 분리하세요.

### 8.3 코드 재사용

- 중복 코드는 피하고 함수나 클래스로 추출하여 재사용합니다.
- 공통 기능은 헬퍼 클래스나 유틸리티 함수로 제공합니다.

### 8.4 안전성과 성능 균형

- 안전성과 성능의 균형을 맞추세요.
- 명확성을 위해 약간의 성능을 희생하는 것은 종종 가치가 있습니다.
- 성능 최적화는 프로파일링을 통해 병목점이 확인된 후에 적용하세요.

---

이 가이드는 일반적인 C++ 코드 작성을 위한 기본 지침입니다. 특정 프로젝트나 팀의 필요에 따라 규칙을 조정할 수 있습니다. 항상 주변 코드의 스타일과 일관성을 유지하는 것이 가장 중요합니다.
