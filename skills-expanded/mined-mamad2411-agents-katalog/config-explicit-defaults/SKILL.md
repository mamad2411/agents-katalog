---
name: config-explicit-defaults
category: architecture
description: "설정 안 한 값 = 자동 처리되니 괜찮다"는 가장 흔한 mental model 오류 방지. 명시값/기본값/환경별 override 3단 검증 체크리스트로 config sprawl과 silent default drift를 차단한다.
---

# Config Explicit Defaults (M3: 묵시적 기본값)

가장 빈도 높은 안티패턴(15건+). 라이브러리·프레임워크·플랫폼이 제공하는 **묵시적 기본값**을 신뢰하면, 버전업이나 환경 차이로 동작이 silent 하게 바뀐다.

> Claude mental model 오류: "내가 설정 안 한 것은 reasonable default 가 있을 것" → 실제로는 default 가 minor 버전 사이에 바뀌고, override 가 환경마다 다르며, application code 는 항상 default 가 적용되었다고 가정한다.

---

## 3단 검증 (MANDATORY)

설정 값 하나마다 반드시 3개 layer 의 값을 확인한다.

```
┌───────────────────────────────────────────────────┐
│ Layer 1: 명시값 (앱 코드 / Helm values / env)     │ ← grep 으로 직접 확인
│ Layer 2: 라이브러리/프레임워크 기본값             │ ← docs / source 확인
│ Layer 3: 환경별 override (dev / staging / prod)   │ ← 환경 diff 확인
└───────────────────────────────────────────────────┘
```

### Layer 1 — 명시값 grep

```bash
# 예: JWT issuer 가 어디서 설정되는지 전수 스캔
rg -i 'issuer|iss' src/ values/ k8s/ --type yaml --type java
```

명시값이 **여러 곳**에 분산되면 위험 신호. 단일 SoT(Source of Truth) 로 통합.

### Layer 2 — 라이브러리 기본값 확인 의무

| 라이브러리 | 기본값 확인 방법 |
|---|---|
| Spring Boot | `application-default.properties` + `@ConfigurationProperties` source |
| OTel SDK | [OpenTelemetry SDK Spec](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/) |
| Viper (Go) | `SetDefault` 등록값 — **AutomaticEnv 는 SetDefault 된 key 만 바인딩** |
| Helm chart | `values.yaml` 의 `default:` 또는 `_helpers.tpl` |
| K8s API | `kubectl explain <resource>.<field>` |

함정 사례:
- **OTel exporter protocol** — `grpc` → `http/protobuf` 로 default 변경 (특정 minor 버전)
- **JWT issuer** — Spring Security 5.x → 6.x 로 검증 strictness 변경
- **HikariCP `maximumPoolSize`** — 10 (default) 인데 prod 에서 100 이라 가정한 design
- **Spring Boot `server.tomcat.threads.max`** — 200 default, 멀티 인스턴스 합산 미고려

### Layer 3 — 환경별 override

```bash
# 환경별 diff — 가장 자주 빠지는 검증
diff <(helm template -f values-dev.yaml chart/) <(helm template -f values-prod.yaml chart/)
```

체크:
- prod 에만 있고 dev 에 없는 값?
- prod 에서 정의했지만 dev 에서 default 로 폴백하는 값?
- ConfigMap / Secret 의 env 가 application.yml 의 값을 덮는가? (Spring `spring.config.import` 순서)

---

## ❌ 안티패턴 5종

### 1. `${VAR}` 리터럴 expand 안 됨

```yaml
# ❌ Spring Boot 외부에서 ${VAR} 가 그대로 들어감
jwt:
  issuer: ${JWT_ISSUER}   # env 미설정 시 리터럴 "${JWT_ISSUER}"
```

```yaml
# ✅ default 명시
jwt:
  issuer: ${JWT_ISSUER:goti-user-service}
```

### 2. Viper SetDefault 없이 AutomaticEnv

```go
// ❌ env 가 안 묻음
viper.AutomaticEnv()
viper.SetEnvPrefix("APP")
cfg.JWT.PrivateKey = viper.GetString("jwt.private_key")  // env APP_JWT_PRIVATE_KEY 미바인딩

// ✅ SetDefault 필수
viper.SetDefault("jwt.private_key", "")
viper.AutomaticEnv()
```

### 3. Spring `dependency-management` 가 OTel BOM 덮음

```xml
<!-- ❌ Spring Boot parent 가 OTel agent 버전을 다운그레이드 -->
<parent>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.5.10</version>  <!-- otel-bom 2.10 사용 -->
</parent>
<dependencies>
  <dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
    <!-- 2.25 의도했지만 Spring 의 2.10 으로 덮임 -->
  </dependency>
</dependencies>
```

```xml
<!-- ✅ OTel BOM 을 dependencyManagement 상위에 명시 -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.opentelemetry.instrumentation</groupId>
      <artifactId>opentelemetry-instrumentation-bom</artifactId>
      <version>2.25.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 4. K8s Pod 의 `resources.requests` 미설정

requests 없으면 scheduler 가 0 으로 가정 → 노드 과배치 → OOMKilled 시 다른 Pod 까지 압박.

### 5. ConfigMap 변경에도 Pod restart 없음

ConfigMap 갱신만으로 Pod 의 env / mounted file 이 **자동 반영되지 않는다** (envFrom). Deployment annotation 에 hash 를 넣어 강제 rollout.

```yaml
spec:
  template:
    metadata:
      annotations:
        checksum/config: "{{ include (print $.Template.BasePath \"/configmap.yaml\") . | sha256sum }}"
```

---

## 자가 검증 체크리스트

새 설정값 추가/변경 시:

- [ ] **Layer 1** 명시값이 단일 SoT 인가? (앱 / Helm / env 중복 없음)
- [ ] **Layer 2** 라이브러리 기본값을 docs/source 로 확인했는가?
- [ ] **Layer 3** 환경별 override diff 를 확인했는가?
- [ ] env 변수가 미설정일 때 **fallback default 가 명시**되었는가? (`${VAR:default}`)
- [ ] 라이브러리/프레임워크 **버전업 시 default 변경**을 CHANGELOG 에서 확인했는가?
- [ ] ConfigMap 변경 시 Pod **자동 rollout** 메커니즘이 있는가? (checksum annotation 또는 reloader)
- [ ] 보안 민감값(Secret) 의 default 가 **empty string** 인가? (예: dummy key 절대 금지)

---

## 진단 명령

```bash
# Spring Boot 실제 적용된 설정 확인
curl http://localhost:8080/actuator/configprops
curl http://localhost:8080/actuator/env

# Viper 현재 settings 확인
viper.Debug()   # 모든 key/value 출력

# Helm values 병합 결과 확인
helm template -f values.yaml -f values-prod.yaml chart/ | grep -A2 'configMap'

# K8s effective config (defaults 포함)
kubectl get deployment X -o jsonpath='{.spec.template.spec.containers[0].env}'
```

---

## 외부 근거

- [12factor.net III: Config](https://12factor.net/config) — config 는 env 에 저장, code 와 분리
- [Twelve-Factor Config: Misunderstandings and Advice — Kristian Glass](https://blog.doismellburning.co.uk/twelve-factor-config-misunderstandings-and-advice/) — 12-factor config 함정 정리
- [OpenTelemetry SDK Configuration Spec](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/)
- [Viper docs — Working with environment variables](https://github.com/spf13/viper#working-with-environment-variables) — AutomaticEnv + SetDefault 의존 관계

---

## 연계 skill

- [`platform/dev-prod-parity-checklist.md`](../dev-prod-parity-checklist/SKILL.md) — M3 가 환경별로 drift 하면 M7 (snowflake) 으로 진화
- [`architecture/service-ownership-matrix.md`](../service-ownership-matrix/SKILL.md) — 각 config 의 owner 가 없으면 drift 감지 불가
- [`go/viper-config-binding.md`](../viper-config-binding/SKILL.md) — Go 특화 binding 함정
