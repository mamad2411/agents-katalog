---
name: wasm-edge-iot
category: platform
description: "WASM Edge/IoT 활용 가이드 — Edge Computing, IoT 배포, 성능 최적화 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# WASM Edge/IoT 활용 가이드

Edge Computing, IoT 배포, 성능 최적화

## Edge/IoT 활용 사례

### CDN Edge 함수

```rust
// Cloudflare Workers 스타일
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[http_component]
fn handle_edge_request(req: Request) -> anyhow::Result<impl IntoResponse> {
    // 지리적 위치 기반 응답
    let country = req.header("cf-ipcountry")
        .map(|v| v.as_str())
        .unwrap_or("unknown");

    let response = match country {
        "KR" => "안녕하세요!",
        "JP" => "こんにちは!",
        "US" => "Hello!",
        _ => "Hello!",
    };

    Ok(Response::builder()
        .status(200)
        .body(response)
        .build())
}
```

### IoT 디바이스

```rust
// 경량 센서 데이터 처리
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct SensorReading {
    temperature: f32,
    humidity: f32,
    timestamp: u64,
}

#[derive(Serialize)]
struct ProcessedData {
    avg_temp: f32,
    status: String,
}

fn process_sensor_data(readings: &[SensorReading]) -> ProcessedData {
    let avg_temp = readings.iter()
        .map(|r| r.temperature)
        .sum::<f32>() / readings.len() as f32;

    let status = if avg_temp > 30.0 {
        "warning"
    } else {
        "normal"
    }.to_string();

    ProcessedData { avg_temp, status }
}
```

---

## 성능 최적화

### AOT 컴파일

```bash
# WasmEdge AOT 컴파일 (시작 시간 최적화)
wasmedgec myapp.wasm myapp_aot.wasm

# 실행 시간 비교
time wasmedge myapp.wasm       # JIT
time wasmedge myapp_aot.wasm   # AOT (더 빠름)
```

### 메모리 최적화

```rust
// wasm32-wasip1에서 메모리 사용 최소화

// 작은 할당자 사용
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

// 릴리즈 최적화 (Cargo.toml)
[profile.release]
opt-level = "z"     // 크기 최적화
lto = true          // 링크 타임 최적화
codegen-units = 1   // 단일 코드 생성
panic = "abort"     // panic 핸들러 제거
strip = true        // 심볼 제거
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 모든 워크로드에 WASM | 복잡한 앱에 부적합 | 적합한 사례 선별 |
| WASI 제한 무시 | 런타임 에러 | 지원 기능 확인 |
| 큰 의존성 사용 | WASM 크기 증가 | 경량 라이브러리 선택 |
| AOT 컴파일 누락 | Cold start 느림 | 프로덕션 AOT 빌드 |
| 컨테이너 리소스 그대로 | 낭비 | WASM용 최적화 |
| Edge에서 무거운 로직 | 지연 증가 | 경량 처리만 Edge에 |
| IoT 보안 미적용 | 취약점 노출 | WASI 샌드박스 활용 |

---

## 체크리스트

### 최적화
- [ ] AOT 컴파일 설정
- [ ] 릴리즈 프로필 최적화 (opt-level z, lto, strip)
- [ ] 경량 할당자 적용 (wee_alloc)
- [ ] 리소스 제한 조정

### Edge 배포
- [ ] CDN/Edge 플랫폼 선택
- [ ] 지역별 배포 전략
- [ ] 모니터링 설정
- [ ] 지리적 라우팅 구성

### IoT
- [ ] 센서 데이터 처리 파이프라인
- [ ] 경량 바이너리 크기 확인 (KB 단위)
- [ ] 디바이스 리소스 프로파일링
- [ ] OTA 업데이트 전략

---

## Sources

- [WasmEdge](https://wasmedge.org/)
- [Spin (Fermyon)](https://developer.fermyon.com/spin/)
- [WASI](https://wasi.dev/)
- [SpinKube](https://www.spinkube.dev/)
- [runwasi](https://github.com/containerd/runwasi)
- [WebAssembly in 2026](https://dev.to/mysterious_xuanwu_5a00815/webassembly-in-2026-beyond-the-browser-and-into-the-cloud-2599)
- [Kubernetes WASM](https://kubernetes.io/blog/2023/08/25/webassembly-workloads/)

---

## 참조 스킬

- `wasm-edge.md` - WASM/WASI 기초, WasmEdge, Spin, Kubernetes 통합
- `/docker` - 컨테이너 비교
- `/k8s-scheduling` - 워크로드 스케줄링
- `/finops` - 비용 최적화
