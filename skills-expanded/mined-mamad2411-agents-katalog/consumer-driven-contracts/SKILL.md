---
name: consumer-driven-contracts
category: msa
description: 마이크로서비스 간 API contract drift를 막는 Consumer-Driven Contracts(CDC) + Pact 운영 가이드. consumer test로 contract 정의 → provider verification 자동화 → GitOps 통합. Martin Fowler canon + Microsoft playbook 기반.
---

# Consumer-Driven Contracts (M10: 외부 시스템 contract drift)

마이크로서비스에서 가장 silent 한 사고: provider 가 API 를 **이전 호환** 변경했다고 가정했는데, 일부 consumer 가 제거된 field 를 사용 중. End-to-end test 로는 잡기 어렵고, OpenAPI 명세는 lockstep 으로 유지되지 않는다.

> Claude mental model 오류: "OpenAPI 명세 있고 backward compatible 하면 안전" → 실제로는 *어떤 field 가 어떤 consumer 에게 critical 한지* provider 가 모름. CDC = consumer 가 "내가 이 field 를 이렇게 쓴다" 를 contract 로 선언 → provider 가 검증.

---

## CDC 흐름

```
1. Consumer 테스트 작성
   "나는 GET /users/{id} 가 {id, name, email} 을 반환한다고 가정한다"
   ↓
2. Pact broker 에 contract 등록
   ↓
3. Provider CI 가 contract 다운로드
   ↓
4. Provider 가 contract 에 맞는 응답 반환하는지 verify
   ↓
5. 모든 consumer 의 contract 가 통과 → can-i-deploy 허용
```

**핵심**: provider 가 release 전 모든 consumer 의 기대를 검증. **OpenAPI 명세 + E2E test 만으로는 안 됨.**

---

## ❌ 안티패턴 5종

### 1. OpenAPI spec 만 의존

```yaml
# provider 의 openapi.yaml
/users/{id}:
  responses:
    200:
      schema:
        properties:
          id: integer
          name: string
          email: string
          # phone 필드 추가됨 — backward compatible
```

문제: provider 는 phone 만 추가하면 안전이라 생각. 하지만 일부 consumer 가 `email` 의 **format** ("user@domain") 에 의존 → 갑자기 `"+phone:1234"` 같은 비표준 format 반환 시 깨짐. 명세는 string 이라 lint 통과.

### 2. E2E test 만 의존

```
[Consumer A] → [Provider] → 200 OK
```

→ E2E 통과 = 안전?
실제로는 **Consumer B/C/D 까지 모든 조합 테스트해야** 검증 완전. CDC 는 이를 contract 파일로 명시화.

### 3. Provider 가 알 수 없는 consumer 의 존재

```
주의: 새 consumer 가 등장했지만 provider 는 모름
→ provider 가 "별로 안 쓰이는 field" 라 판단해 제거
→ 새 consumer 가 그 field 의존 → 운영 사고
```

→ Pact broker / contract 등록이 의무화되어야 발견.

### 4. Contract 가 production 과 lockstep 아님

```
Pact contract: v1.0 (consumer test 기준)
Provider 실제: v1.2 (3개월 후)
```

→ contract 가 stale → consumer 가 새 field 사용 가능하나 명시 안 됨 → provider 가 그 field 제거 시 사고.

### 5. provider verification 이 manual

```
"이번 분기에 한 번 돌렸어요" — 안 됨
```

→ 매 PR 마다 자동 verification 의무.

---

## ✅ Pact 운영 패턴

### Pact (consumer 측 — Java 예시)

```java
@PactTestFor(providerName = "user-service", port = "8080")
class UserClientPactTest {

    @Pact(consumer = "order-service")
    public RequestResponsePact getUserPact(PactDslWithProvider builder) {
        return builder
            .given("user 12345 exists")
            .uponReceiving("get user by id")
            .path("/users/12345")
            .method("GET")
            .willRespondWith()
            .status(200)
            .body(new PactDslJsonBody()
                .integerType("id", 12345)
                .stringType("name")
                .stringMatcher("email", ".+@.+\\..+")
                .booleanType("active", true))
            .toPact();
    }

    @Test
    void testGetUser(MockServer mockServer) {
        UserClient client = new UserClient(mockServer.getUrl());
        User user = client.getUser(12345);
        assertEquals(12345, user.getId());
        assertNotNull(user.getEmail());
    }
}
```

→ 테스트 통과 시 `pacts/order-service-user-service.json` 생성 → Pact broker 업로드.

### Pact (provider 측 — Java)

```java
@Provider("user-service")
@PactBroker(host = "pact-broker.internal")
class UserServiceProviderTest {

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void pactVerificationTestTemplate(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("user 12345 exists")
    void userExists() {
        userRepository.save(new User(12345, "alice", "alice@example.com", true));
    }
}
```

→ provider CI 가 broker 에서 contract 다운로드 → 자신의 endpoint 가 expectation 만족하는지 검증.

### can-i-deploy 게이트

```bash
# CI 에서 provider 배포 전
pact-broker can-i-deploy --pacticipant user-service --version $GIT_SHA --to-environment prod
```

→ 모든 consumer 의 prod contract 가 통과한 경우만 배포 허용.

---

## GitOps 통합 패턴

```yaml
# ArgoCD pre-sync hook 으로 contract verification
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  source:
    helm:
      hooks:
        preSync:
        - name: pact-verify
          job: pact-verify-job
```

```yaml
# Job 정의
apiVersion: batch/v1
kind: Job
metadata:
  name: pact-verify
  annotations:
    argocd.argoproj.io/hook: PreSync
spec:
  template:
    spec:
      containers:
      - name: pact-cli
        image: pactfoundation/pact-cli
        command:
          - pact-broker
          - can-i-deploy
          - --pacticipant
          - user-service
          - --version
          - $GIT_SHA
          - --to-environment
          - prod
```

→ contract 미통과 시 ArgoCD sync 실패 → 배포 차단.

---

## API 진화 패턴 (CDC 와 함께)

| 변경 | 호환성 | 처리 |
|---|---|---|
| 새 field 추가 (optional) | ✅ backward | OpenAPI 갱신 + 새 consumer test 추가 |
| 기존 field 제거 | ❌ breaking | **Expand-Contract**: deprecate → 모든 consumer 마이그 → drop |
| field type 변경 | ❌ breaking | 새 field 추가 + dual write + old drop |
| URL path 변경 | ❌ breaking | versioning (`/v2/users`) + 양쪽 운영 |
| Required → Optional | ✅ backward | OpenAPI 갱신 |
| Optional → Required | ❌ breaking | 새 endpoint 또는 deprecate |

---

## 자가 검증 체크리스트

새 endpoint / API 변경 시:

- [ ] **Consumer test** (Pact) 가 작성되었는가? 어떤 consumer 가 어떤 field 를 사용?
- [ ] **Provider verification** 이 매 PR CI 에서 실행되는가?
- [ ] **Pact broker** 가 운영 중이고 contract 가 등록되었는가?
- [ ] **can-i-deploy** 가 배포 게이트로 동작하는가?
- [ ] Breaking change 시 **Expand-Contract** 또는 versioning 패턴 적용?
- [ ] Consumer 가 production 으로 배포된 contract 만 verify?
- [ ] 새 consumer 등장 시 provider 팀이 **자동 알림** 받는가? (Pact webhook)

---

## 외부 근거

- [Consumer-Driven Contracts: A Service Evolution Pattern — Martin Fowler](https://martinfowler.com/articles/consumerDrivenContracts.html) — canon
- [Contract Test — Martin Fowler bliki](https://martinfowler.com/bliki/ContractTest.html)
- [Writing Consumer tests — Pact Docs](https://docs.pact.io/consumer)
- [Provider verification — Pact Docs](https://docs.pact.io/provider)
- [CDC Testing — Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/cdc-testing/)
- [can-i-deploy — Pact Docs](https://docs.pact.io/pact_broker/can_i_deploy)

---

## 의외의 발견

- **CDC 는 monolith → microservice 전환의 핵심 안전망** — 서비스 분리 시 어떤 service 가 어떤 contract 의존하는지 명시화
- **OpenAPI 와 상호 보완** — OpenAPI 는 구조, Pact 는 의미적 기대 (특정 consumer 의 사용 패턴)
- **K8s GitOps 와 통합**이 검증 자동화의 핵심 — ArgoCD pre-sync hook 으로 contract 미통과 시 배포 차단

---

## 연계 skill

- [`migration/expand-contract-pattern.md`](../expand-contract-pattern/SKILL.md) — API breaking change 의 무중단 변경
- [`testing/negative-path-coverage.md`](../negative-path-coverage/SKILL.md) — 외부 의존 실패 시나리오
- [`msa/api-design.md`](../api-design/SKILL.md) — REST/gRPC API design
- [`msa/contract-first.md`](../contract-first/SKILL.md) — Contract-first 개발
