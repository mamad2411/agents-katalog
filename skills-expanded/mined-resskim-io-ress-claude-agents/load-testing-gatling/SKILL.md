---
name: load-testing-gatling
category: sre
description: "Gatling 부하 테스트 — Scala/Java DSL, injection 프로파일, Assertions, 분산 실행, HTML 리포트 분석. Use when JVM 기반 부하 테스트 도구로 Gatling 을 선택했거나 Scala/Java DSL 시나리오를 작성할 때."
effort: xhigh
deprecated: false
---

# Gatling 부하 테스트

Scala/Java DSL 기반 JVM 부하 테스트. 코드로 시나리오를 관리하고 상세 HTML 리포트로 병목을 분석한다.

## Quick Reference (결정 트리)

```
Gatling 을 쓸 상황인가?
    │
    ├─ 팀이 JVM 스택(Scala/Java) ────────> Gatling
    ├─ 리포트 상세도가 중요 ─────────────> Gatling (HTML 리포트)
    ├─ DevOps/JS 친화 ──────────────────> K6 (/load-testing)
    └─ GUI 기반, 비개발자 참여 ──────────> nGrinder (/load-testing-analysis)
```

| 상황 | 패턴 | 섹션 |
|------|------|------|
| 프로젝트 생성 | Maven archetype / Gradle 의존성 | [설치 및 설정](#설치-및-설정) |
| 시나리오 작성 (Scala) | `Simulation` + `ScenarioBuilder` | [Scala DSL](#scala-dsl) |
| 시나리오 작성 (Java) | `io.gatling.javaapi` | [Java DSL](#java-dsl) |
| SLO 게이트 | `assertions` | [Assertions](#assertions) |
| 대규모 실행 | injector 분산 + 결과 병합 | [분산 실행](#분산-실행) |

## Gatling Overview

| 특성 | 값 |
|------|-----|
| **언어** | Scala/Java |
| **학습 곡선** | 중간 |
| **단일 인스턴스** | ~10K VUs |
| **분산 테스트** | Gatling Enterprise, 자체 클러스터 |
| **라이선스** | Apache 2.0 |

## 설치 및 설정

```bash
# Maven 프로젝트 생성
mvn archetype:generate \
  -DarchetypeGroupId=io.gatling.highcharts \
  -DarchetypeArtifactId=gatling-highcharts-maven-archetype

# Gradle 의존성
dependencies {
    gatling "io.gatling.highcharts:gatling-charts-highcharts:3.10.0"
}
```

## Scala DSL

```scala
package simulations

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class TicketingSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("https://api.ticketing.example.com")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val eventId = "EVENT-2026-001"
  val sections = Array("A", "B", "C", "D", "E", "VIP")

  val userFeeder = Iterator.continually(Map(
    "userId" -> s"user-${java.util.UUID.randomUUID()}",
    "section" -> sections(scala.util.Random.nextInt(sections.length))
  ))

  val ticketPurchaseScenario = scenario("티켓 구매 시나리오")
    .feed(userFeeder)
    // 1. 대기열 진입
    .exec(
      http("대기열 진입")
        .post("/api/waiting/enter")
        .header("X-User-Id", "#{userId}")
        .check(status.is(200))
        .check(jsonPath("$.position").saveAs("queuePosition"))
    )
    // 대기열 폴링
    .asLongAs(session => session("admitted").asOption[Boolean].getOrElse(false) == false) {
      exec(
        http("대기열 상태 확인")
          .get("/api/waiting/status")
          .header("X-User-Id", "#{userId}")
          .check(status.is(200))
          .check(jsonPath("$.status").saveAs("waitingStatus"))
      )
      .doIf(session => session("waitingStatus").as[String] == "admitted") {
        exec(session => session.set("admitted", true))
      }
      .pause(1.second)
    }
    // 2. 좌석 조회 및 선택
    .exec(
      http("좌석 조회")
        .get(s"/api/events/$eventId/seats")
        .queryParam("section", "#{section}")
        .header("X-User-Id", "#{userId}")
        .check(status.is(200))
        .check(jsonPath("$.seats[?(@.status=='AVAILABLE')][0].id").saveAs("seatId"))
        .check(jsonPath("$.seats[?(@.status=='AVAILABLE')][0].price").saveAs("seatPrice"))
    )
    .exec(
      http("좌석 선택")
        .post(s"/api/events/$eventId/seats/#{seatId}/select")
        .header("X-User-Id", "#{userId}")
        .check(status.is(200))
        .check(jsonPath("$.lockToken").saveAs("lockToken"))
    )
    .pause(1.second, 3.seconds)
    // 3. 결제
    .exec(
      http("결제 처리")
        .post("/api/payment/process")
        .header("X-User-Id", "#{userId}")
        .body(StringBody(
          s"""{"eventId": "$eventId", "seatId": "#{seatId}", "lockToken": "#{lockToken}", "paymentMethod": "CARD", "amount": #{seatPrice}}"""
        ))
        .check(status.is(200))
        .check(jsonPath("$.ticketId").exists)
    )

  setUp(
    ticketPurchaseScenario.inject(
      rampUsers(10000).during(10.seconds),
      constantUsersPerSec(1000).during(5.minutes),
      rampUsersPerSec(1000).to(5000).during(2.minutes),
      constantUsersPerSec(5000).during(10.minutes)
    )
  ).protocols(httpProtocol)
    .assertions(
      global.responseTime.percentile(95).lt(500),
      global.responseTime.percentile(99).lt(1000),
      global.successfulRequests.percent.gt(99),
      details("결제 처리").responseTime.percentile(95).lt(2000)
    )
}
```

## Java DSL

```java
package simulations;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;
import java.util.*;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class TicketingSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api.ticketing.example.com")
        .acceptHeader("application/json")
        .contentTypeHeader("application/json");

    String eventId = "EVENT-2026-001";
    String[] sections = {"A", "B", "C", "D", "E", "VIP"};

    Iterator<Map<String, Object>> userFeeder = Stream.generate(() -> {
        Map<String, Object> map = new HashMap<>();
        map.put("userId", "user-" + UUID.randomUUID());
        map.put("section", sections[new Random().nextInt(sections.length)]);
        return map;
    }).iterator();

    ScenarioBuilder ticketPurchaseScenario = scenario("티켓 구매 시나리오")
        .feed(userFeeder)
        .exec(
            http("대기열 진입")
                .post("/api/waiting/enter")
                .header("X-User-Id", "#{userId}")
                .check(status().is(200))
        )
        .asLongAs(session -> !session.getBoolean("admitted"))
        .on(
            exec(
                http("대기열 상태 확인")
                    .get("/api/waiting/status")
                    .header("X-User-Id", "#{userId}")
                    .check(status().is(200))
                    .check(jsonPath("$.status").saveAs("waitingStatus"))
            )
            .doIf(session -> "admitted".equals(session.getString("waitingStatus")))
            .then(exec(session -> session.set("admitted", true)))
            .pause(Duration.ofSeconds(1))
        )
        .exec(
            http("좌석 선택")
                .post("/api/events/" + eventId + "/seats/#{seatId}/select")
                .header("X-User-Id", "#{userId}")
                .check(status().is(200))
        )
        .exec(
            http("결제 처리")
                .post("/api/payment/process")
                .header("X-User-Id", "#{userId}")
                .body(StringBody("{\"eventId\":\"" + eventId + "\",\"seatId\":\"#{seatId}\"}"))
                .check(status().is(200))
        );

    {
        setUp(
            ticketPurchaseScenario.injectOpen(
                rampUsers(10000).during(Duration.ofSeconds(10)),
                constantUsersPerSec(1000).during(Duration.ofMinutes(5))
            )
        ).protocols(httpProtocol)
         .assertions(
             global().responseTime().percentile(95).lt(500)
         );
    }
}
```

## 분산 실행

```bash
# Maven으로 실행
mvn gatling:test -Dgatling.simulationClass=simulations.TicketingSimulation

# 클러스터 실행 (수동)
GATLING_HOME/bin/gatling.sh -s TicketingSimulation -rd "Node-1"

# 결과 병합
GATLING_HOME/bin/gatling.sh -ro results-node-1 results-node-2
```

### 100만 VU 달성 구성

```
Gatling 방식 (Self-hosted)
├─ Gatling Enterprise: 100 injectors × 10K = 1M VUs
└─ 또는: EC2 c5.4xlarge × 100대
```

## Assertions

```scala
assertions(
  global.responseTime.percentile(95).lt(500),   // P95 < 500ms
  global.responseTime.percentile(99).lt(1000),  // P99 < 1000ms
  global.successfulRequests.percent.gt(99),     // 성공률 > 99%
  details("결제 처리").responseTime.percentile(95).lt(2000)
)
```

## 결과 확인

```bash
# HTML 리포트 열기
open target/gatling/*/index.html
```

| 메트릭 | 정상 | 경고 | 위험 |
|--------|------|------|------|
| P95 응답시간 | < 500ms | 500-1000ms | > 1000ms |
| 에러율 | < 0.1% | 0.1-1% | > 1% |

## Anti-Patterns

| 안티패턴 | 문제 | 대안 |
|---------|------|------|
| `.pause()` 없는 시나리오 | 실사용자 think time 미반영 → 비현실적 부하 | `.pause(1.second, 3.seconds)` 로 범위 지정 |
| assertion 없는 실행 | 성능 회귀가 CI 를 통과 | `global.responseTime.percentile(95).lt(...)` 필수 |
| injector 1대로 100만 VU 시도 | 부하 생성기 자체가 병목 → 측정값 왜곡 | injector 분산 후 결과 병합 |
| Scala/Java DSL 혼용 | 빌드 설정 이원화, 유지보수 비용 | 팀 스택에 맞춰 하나로 고정 |
| HTML 리포트만 보고 종료 | p95/p99 만 보면 부하 생성기 포화를 놓침 | injector CPU / 응답시간 추이를 함께 확인 |

## 체크리스트

- [ ] 시나리오에 think time(`pause`)이 들어갔는가
- [ ] `assertions` 로 SLO 를 코드에 박았는가 (p95 / p99 / 성공률)
- [ ] injection 프로파일이 실제 트래픽 패턴(ramp → constant → spike)을 반영하는가
- [ ] 단일 injector 한계(~10K VU)를 넘는 목표면 분산 구성을 잡았는가
- [ ] 부하 생성기 자체의 리소스 포화를 모니터링하는가
- [ ] CI 에서 assertion 실패 시 빌드가 깨지는가

## 참조 스킬

- [`load-testing`](../load-testing/SKILL.md) — 테스트 유형 / K6 / K8s 실행
- [`load-testing-analysis`](../load-testing-analysis/SKILL.md) — nGrinder / 결과 분석 / SLO Threshold
- [`sre-sli-slo`](../sre-sli-slo/SKILL.md) — assertion 에 넣을 SLO 정의
- [`high-traffic-design`](../high-traffic-design/SKILL.md) — 부하 테스트로 검증할 설계 패턴
