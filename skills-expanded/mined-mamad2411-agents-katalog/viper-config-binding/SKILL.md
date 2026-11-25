---
name: viper-config-binding
category: go
description: Go Viper의 설정 바인딩 함정과 정답 패턴. SetDefault + AutomaticEnv + Unmarshal 조합의 silent skip 동작과 mapstructure tag 매핑. 신규 config 추가 시 3곳 동시 갱신.
---

# Viper Config Binding — 함정과 정답 패턴

Go에서 [spf13/viper](https://github.com/spf13/viper)로 환경변수 / 파일 / flag 를 구조체에 바인딩할 때, **silent skip**과 정답 패턴.

> ⚠️ dev에서 동작하던 config가 prod에서 zero value로 나오는 사고의 가장 흔한 원인. Viper 문서는 명확하지 않다.

---

## 핵심 함정: AutomaticEnv는 SetDefault에 등록된 key만 인식

`viper.AutomaticEnv()` + `viper.Unmarshal(&cfg)` 조합은 **`SetDefault`로 등록된 key**만 environment에서 읽는다. SetDefault 없이 구조체 필드만 정의하면 env 변수가 silent skip.

```go
// ❌ BAD: SetDefault 없이 Unmarshal — env 미바인딩
type Config struct {
    JWT struct {
        PrivateKey string `mapstructure:"private_key"`
    } `mapstructure:"jwt"`
}

func Load() (*Config, error) {
    v := viper.New()
    v.AutomaticEnv()
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    var cfg Config
    if err := v.Unmarshal(&cfg); err != nil {
        return nil, err
    }
    return &cfg, nil  // JWT_PRIVATE_KEY 환경변수 줘도 cfg.JWT.PrivateKey 는 빈 문자열
}
```

```go
// ✅ GOOD: SetDefault 등록 후 Unmarshal
func Load() (*Config, error) {
    v := viper.New()

    // 모든 key를 SetDefault로 등록 (값은 zero value여도 OK)
    v.SetDefault("jwt.private_key", "")
    v.SetDefault("jwt.public_key", "")
    v.SetDefault("ticketing.event_id", "")
    v.SetDefault("ticketing.max_concurrent", 1000)

    v.AutomaticEnv()
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    var cfg Config
    return &cfg, v.Unmarshal(&cfg)
}
```

이제 `JWT_PRIVATE_KEY=...` 환경변수가 `cfg.JWT.PrivateKey` 로 정상 매핑됨.

---

## 신규 config 추가 시 3곳 동시 갱신 (MANDATORY)

신규 config key를 추가할 때 **반드시 아래 3곳 모두 갱신**한다.

| 위치 | 내용 | 누락 시 |
|------|------|---------|
| 1. 구조체 정의 | `Config` struct에 필드 + `mapstructure` tag 추가 | unmapped, 항상 zero value |
| 2. `SetDefault` 호출 | 새 key 등록 — value는 zero value여도 OK | env / config 파일 무시됨 |
| 3. 환경별 명세 | `.env.example`, `values-{env}.yaml`, K8s ConfigMap 등 | dev 동작, prod에서 빈 값 |

### 권장 정리 패턴

```go
// config/defaults.go - 모든 key를 한 곳에서 관리
package config

func registerDefaults(v *viper.Viper) {
    // JWT
    v.SetDefault("jwt.private_key", "")
    v.SetDefault("jwt.public_key", "")
    v.SetDefault("jwt.access_ttl", "1h")
    v.SetDefault("jwt.refresh_ttl", "30d")

    // Database
    v.SetDefault("db.host", "localhost")
    v.SetDefault("db.port", 5432)
    v.SetDefault("db.pool.max", 25)

    // Ticketing
    v.SetDefault("ticketing.event_id", "")
    v.SetDefault("ticketing.max_concurrent", 1000)
}
```

이렇게 한 함수에 모아두면 누락 검출도 쉽고 PR diff 단위로 일관성 확인 가능.

---

## env 변수 이름 매핑 규칙

```go
v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
v.SetEnvPrefix("APP")  // 선택 사항
```

- key `jwt.private_key` ↔ env `JWT_PRIVATE_KEY`
- prefix 사용 시 ↔ env `APP_JWT_PRIVATE_KEY`
- mapstructure tag와 SetDefault key는 **동일한 이름** 사용

---

## 구조체 nested 매핑 시 주의

```go
type DBConfig struct {
    Host string `mapstructure:"host"`
    Port int    `mapstructure:"port"`
    Pool struct {
        Max int `mapstructure:"max"`
    } `mapstructure:"pool"`
}

type Config struct {
    DB DBConfig `mapstructure:"db"`
}
```

이 경우 SetDefault는:
```go
v.SetDefault("db.host", "localhost")
v.SetDefault("db.port", 5432)
v.SetDefault("db.pool.max", 25)  // nested도 평탄화된 key로 등록
```

3단 이상 nested는 가독성 떨어짐 — flat 구조 권장.

---

## Slice / Map 바인딩

slice는 환경변수에서 `,` 구분으로 전달:

```go
v.SetDefault("kafka.brokers", []string{})
// env: KAFKA_BROKERS=broker1:9092,broker2:9092,broker3:9092

type Config struct {
    Kafka struct {
        Brokers []string `mapstructure:"brokers"`
    } `mapstructure:"kafka"`
}
```

map은 환경변수로 안 풀린다 — YAML/JSON 파일 사용.

---

## 디버깅: 실제 바인딩 상태 확인

```go
// 모든 key + 값 출력
for _, k := range v.AllKeys() {
    fmt.Printf("%s = %v\n", k, v.Get(k))
}

// 특정 key의 출처 추적 (viper v1.18+)
v.GetViper().AllSettings()
```

prod 환경에서 디버깅용 endpoint로 노출 시 시크릿 마스킹 필수.

---

## 검증 패턴

```go
type Config struct {
    JWT struct {
        PrivateKey string `mapstructure:"private_key" validate:"required"`
    } `mapstructure:"jwt"`
}

func Load() (*Config, error) {
    cfg := &Config{}
    // ... viper unmarshal ...

    if err := validator.New().Struct(cfg); err != nil {
        return nil, fmt.Errorf("invalid config: %w", err)
    }
    return cfg, nil
}
```

required field 누락 시 startup에서 즉시 실패. zero value로 prod 진입 차단.

---

## 자주 발생하는 실제 사고

| 사고 | 원인 |
|------|------|
| dev에서 동작, prod에서 JWT verify 실패 | `jwt.private_key` SetDefault 미등록 → env 미바인딩 |
| ticketing.* 환경변수 모두 zero value | 구조체 필드는 있는데 SetDefault 누락 |
| nested config 일부만 적용 | 한 nested level은 SetDefault, 다른 level은 누락 |
| slice config가 빈 배열 | env 구분자 인식 안 됨 (`,` 외 사용) |

---

## 체크리스트

신규 config 추가 PR 작성 후:

- [ ] 구조체 필드 + `mapstructure` tag 추가
- [ ] `SetDefault` 등록 (registerDefaults 같은 곳)
- [ ] `.env.example` / `values-{env}.yaml` / ConfigMap 갱신
- [ ] required 필드는 validator로 검증
- [ ] startup log에 bound config (시크릿 마스킹) 출력
