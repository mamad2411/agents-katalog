---
name: aws-messaging
category: infrastructure
description: "AWS 메시징 서비스 가이드 — SQS, SNS, EventBridge 비교 및 구현 패턴, K8s 통합 Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# AWS 메시징 서비스 가이드

SQS, SNS, EventBridge 비교 및 구현 패턴, K8s 통합

## Quick Reference (결정 트리)

```
메시징 서비스 선택?
    │
    ├─ 1:1 비동기 작업 큐 ─────────> SQS
    │     ├─ 순서 보장 필요 ────────> SQS FIFO
    │     └─ 순서 불필요 + 처리량 ──> SQS Standard
    │
    ├─ 1:N 메시지 브로드캐스트 ────> SNS
    │     ├─ 필터링 필요 ──────────> SNS + Filter Policy
    │     └─ Fan-out ──────────────> SNS → SQS (각 서비스별)
    │
    └─ 이벤트 기반 라우팅 ─────────> EventBridge
          ├─ 다중 소스 통합 ────────> Event Bus + Rules
          ├─ SaaS 이벤트 ──────────> Partner Event Source
          └─ 데이터 변환 + 연결 ───> EventBridge Pipes

DLQ 전략?
    │
    ├─ SQS 소비 실패 ──────────────> SQS DLQ (maxReceiveCount)
    ├─ Lambda 비동기 실패 ─────────> SQS/SNS DLQ
    └─ EventBridge 전송 실패 ──────> DLQ on Rule Target
```

---

## CRITICAL: 서비스 비교

| 기준 | SQS | SNS | EventBridge |
|------|-----|-----|-------------|
| **패턴** | Point-to-Point | Pub/Sub | Event Bus |
| **전달** | Pull (폴링) | Push (구독자 전송) | Push (Rule 매칭) |
| **순서** | FIFO 큐만 | FIFO 토픽만 | 보장 안 됨 |
| **처리량** | 무제한 (Standard) | 30만/초 | 수천~수만/초 |
| **크기** | 256KB (S3 연동 2GB) | 256KB | 256KB |
| **보존** | 1분~14일 | 재시도 후 삭제 | 24시간 (아카이브 가능) |
| **필터** | 없음 | Filter Policy | Content-based Rules |
| **비용/백만** | $0.40 (요청) | $0.50 (발행) | $1.00 (이벤트) |

---

## SQS (Simple Queue Service)

### Standard vs FIFO

| 속성 | Standard | FIFO |
|------|----------|------|
| **처리량** | 무제한 | 3,000/초 (배치 30,000) |
| **순서** | Best-effort | 엄격한 FIFO |
| **중복** | At-least-once | Exactly-once (5분 중복 제거) |
| **큐 이름** | 자유 | `.fifo` 접미사 필수 |

### CRITICAL: Visibility Timeout & Long Polling

```
Visibility Timeout = 평균 처리 시간 × 6 (Lambda 시 = Lambda Timeout × 6)
Long Polling: WaitTimeSeconds = 20 (최대) → 빈 응답 감소, 비용 절감

DLQ 흐름:
┌──────────┐  실패 반복   ┌──────────┐  알림   ┌───────────┐
│ Source Q  │ ──────────> │   DLQ    │ ─────> │ CloudWatch│
└──────────┘ maxReceive=3 └──────────┘        └───────────┘
```

### Go SDK v2 — SQS 송수신

```go
package messaging

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
	"github.com/aws/aws-sdk-go-v2/service/sqs/types"
)

type SQSClient struct {
	client   *sqs.Client
	queueURL string
}

func NewSQSClient(ctx context.Context, queueURL string) (*SQSClient, error) {
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return nil, fmt.Errorf("AWS 설정 로드 실패: %w", err)
	}
	return &SQSClient{client: sqs.NewFromConfig(cfg), queueURL: queueURL}, nil
}

// SendMessage — Standard 큐 전송
func (s *SQSClient) SendMessage(ctx context.Context, body any) error {
	payload, _ := json.Marshal(body)
	_, err := s.client.SendMessage(ctx, &sqs.SendMessageInput{
		QueueUrl:    &s.queueURL,
		MessageBody: aws.String(string(payload)),
		MessageAttributes: map[string]types.MessageAttributeValue{
			"Source": {DataType: aws.String("String"), StringValue: aws.String("order-service")},
		},
	})
	return err
}

// SendFIFO — FIFO 큐 전송 (MessageGroupId 필수)
func (s *SQSClient) SendFIFO(ctx context.Context, body any, groupID, dedupID string) error {
	payload, _ := json.Marshal(body)
	_, err := s.client.SendMessage(ctx, &sqs.SendMessageInput{
		QueueUrl: &s.queueURL, MessageBody: aws.String(string(payload)),
		MessageGroupId: &groupID, MessageDeduplicationId: &dedupID,
	})
	return err
}

// ReceiveAndProcess — Long Polling 기반 수신 루프
func (s *SQSClient) ReceiveAndProcess(ctx context.Context, handler func(string) error) error {
	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}
		out, err := s.client.ReceiveMessage(ctx, &sqs.ReceiveMessageInput{
			QueueUrl:            &s.queueURL,
			MaxNumberOfMessages: 10,
			WaitTimeSeconds:     20, // Long Polling 필수
			VisibilityTimeout:   60,
		})
		if err != nil {
			slog.Error("SQS 수신 실패", "error", err)
			time.Sleep(5 * time.Second)
			continue
		}
		for _, msg := range out.Messages {
			if err := handler(*msg.Body); err != nil {
				slog.Error("처리 실패", "id", *msg.MessageId, "error", err)
				continue // Visibility Timeout 후 재처리
			}
			s.client.DeleteMessage(ctx, &sqs.DeleteMessageInput{
				QueueUrl: &s.queueURL, ReceiptHandle: msg.ReceiptHandle,
			})
		}
	}
}
```

### Spring Cloud AWS — SQS

```java
// implementation 'io.awspring.cloud:spring-cloud-aws-starter-sqs:3.1.0'

@Service @RequiredArgsConstructor
public class OrderEventPublisher {
    private final SqsTemplate sqsTemplate;

    public void publishOrderCreated(OrderCreatedEvent event) {
        sqsTemplate.send(to -> to.queue("order-events")
            .payload(event).header("eventType", "OrderCreated"));
    }
    // FIFO 큐 전송
    public void publishOrderUpdated(OrderUpdatedEvent event) {
        sqsTemplate.send(to -> to.queue("order-events.fifo").payload(event)
            .header(SqsHeaders.SQS_GROUP_ID_HEADER, event.getOrderId())
            .header(SqsHeaders.SQS_DEDUPLICATION_ID_HEADER, event.getEventId()));
    }
}

@Component @Slf4j
public class OrderEventListener {
    @SqsListener(value = "order-events", maxConcurrentMessages = "10")
    public void handle(@Payload OrderCreatedEvent event, @Header("eventType") String type) {
        log.info("주문 이벤트 수신: type={}, orderId={}", type, event.getOrderId());
    }
}
```

---

## SNS (Simple Notification Service)

### Fan-out 패턴

```
                     ┌─────────────────┐
                     │   SNS Topic     │
                     └────────┬────────┘
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │ SQS(재고)│  │ SQS(알림)│  │Lambda(분석)│
         └──────────┘  └──────────┘  └──────────┘
SNS → SQS 구독 시 Raw Message Delivery 활성화 권장
```

### Filter Policy (속성 기반 / 페이로드 기반)

```json
// 속성 기반: MessageAttributes 기준 필터링
{"eventType": ["OrderCreated"], "amount": [{"numeric": [">=", 10000]}]}

// 페이로드 기반 (FilterPolicyScope: MessageBody): 본문 JSON 기준
{"detail": {"status": ["COMPLETED"], "amount": [{"numeric": [">", 50000]}]}}
```

### Go SDK v2 — SNS Publish

```go
// 초기화: config.LoadDefaultConfig → sns.NewFromConfig (SQSClient 패턴 동일)
func (p *SNSPublisher) Publish(ctx context.Context, event any, eventType string) error {
	payload, _ := json.Marshal(event)
	_, err := p.client.Publish(ctx, &sns.PublishInput{
		TopicArn: &p.topicARN, Message: aws.String(string(payload)),
		MessageAttributes: map[string]types.MessageAttributeValue{
			"eventType": {DataType: aws.String("String"), StringValue: aws.String(eventType)},
		},
	})
	return err
}

// FIFO 토픽: MessageGroupId + MessageDeduplicationId 필수
func (p *SNSPublisher) PublishFIFO(ctx context.Context, event any, groupID, dedupID string) error {
	payload, _ := json.Marshal(event)
	_, err := p.client.Publish(ctx, &sns.PublishInput{
		TopicArn: &p.topicARN, Message: aws.String(string(payload)),
		MessageGroupId: &groupID, MessageDeduplicationId: &dedupID,
	})
	return err
}
```

### Spring Cloud AWS — SNS

```java
// implementation 'io.awspring.cloud:spring-cloud-aws-starter-sns:3.1.0'

@Service @RequiredArgsConstructor
public class NotificationPublisher {
    private final SnsTemplate snsTemplate;

    public void publishEvent(String topicArn, DomainEvent event) {
        snsTemplate.sendNotification(topicArn, SnsNotification.builder(event)
            .header("eventType", event.getType())
            .groupId(event.getAggregateId())        // FIFO 토픽용
            .deduplicationId(event.getEventId())     // FIFO 토픽용
            .build());
    }
}
```

---

## EventBridge

### 핵심 구성 요소

```
Event Source ──> Event Bus (라우터) ──> Rules (패턴 매칭) ──> Targets
                                                              ├─ Lambda
                                                              ├─ SQS / SNS
                                                              ├─ Step Functions
                                                              └─ API Gateway
추가: Schema Registry(스키마 검색), Pipes(파이프라인), Archive & Replay
```

### Event Rule 패턴 / Pipes

```json
{
  "source": ["com.myapp.orders"],
  "detail-type": ["OrderCreated"],
  "detail": {
    "amount": [{"numeric": [">", 10000]}],
    "status": ["CONFIRMED"],
    "region": [{"prefix": "ap-"}]
  }
}
```

```
Pipes: Source(SQS/DynamoDB/Kinesis) → Filter → Enrich(Lambda) → Target(EventBridge)
```

### Go SDK v2 — EventBridge PutEvents

```go
// 초기화: config.LoadDefaultConfig → eventbridge.NewFromConfig
func (p *EventBridgePublisher) PutEvent(ctx context.Context, detailType string, detail any) error {
	payload, _ := json.Marshal(detail)
	out, err := p.client.PutEvents(ctx, &eventbridge.PutEventsInput{
		Entries: []ebtypes.PutEventsRequestEntry{{
			EventBusName: &p.busName, Source: &p.source,
			DetailType: &detailType, Detail: aws.String(string(payload)),
		}},
	})
	if err != nil {
		return err
	}
	if out.FailedEntryCount > 0 {
		return fmt.Errorf("이벤트 전송 실패: %d건", out.FailedEntryCount)
	}
	return nil
}
```

### Spring — EventBridge 연동

```java
// implementation 'software.amazon.awssdk:eventbridge:2.25.0'

@Service @RequiredArgsConstructor
public class EventBridgePublisher {
    private final EventBridgeClient ebClient;
    private final ObjectMapper objectMapper;

    public void publish(String busName, DomainEvent event) throws Exception {
        PutEventsResponse resp = ebClient.putEvents(PutEventsRequest.builder()
            .entries(PutEventsRequestEntry.builder()
                .eventBusName(busName).source("com.myapp." + event.getSource())
                .detailType(event.getType()).detail(objectMapper.writeValueAsString(event))
                .build()).build());
        if (resp.failedEntryCount() > 0) log.error("전송 실패: {}", resp.entries());
    }
}
```

---

## K8s 통합

### IRSA (IAM Roles for Service Accounts)

```bash
# OIDC Provider 연결 + IAM 역할 생성
eksctl utils associate-iam-oidc-provider --cluster my-cluster --approve
eksctl create iamserviceaccount \
  --cluster my-cluster --namespace production --name order-service-sa \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess \
  --override-existing-serviceaccounts --approve
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/order-service-role
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: order-service-sa
      containers:
        - name: order-service
          image: 123456789012.dkr.ecr.ap-northeast-2.amazonaws.com/order-service:latest
          env:
            - name: SQS_QUEUE_URL
              value: https://sqs.ap-northeast-2.amazonaws.com/123456789012/order-queue
```

### KEDA SQS Scaler — 큐 기반 오토스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: order-processor
  minReplicaCount: 1
  maxReplicaCount: 50
  pollingInterval: 15
  cooldownPeriod: 60
  triggers:
    - type: aws-sqs-queue
      authenticationRef:
        name: keda-aws-credentials
      metadata:
        queueURL: https://sqs.ap-northeast-2.amazonaws.com/123456789012/order-queue
        queueLength: "5"              # 메시지 5개당 Pod 1개
        awsRegion: ap-northeast-2
        identityOwner: operator       # IRSA 사용
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: keda-aws-credentials
  namespace: production
spec:
  podIdentity:
    provider: aws-eks                  # IRSA 자동 인증
```

### ACK — SQS 큐를 K8s 리소스로 관리

```yaml
apiVersion: sqs.services.k8s.aws/v1alpha1
kind: Queue
metadata:
  name: order-queue
  namespace: production
spec:
  queueName: order-queue
  visibilityTimeout: "60"
  messageRetentionPeriod: "345600"
  receiveMessageWaitTimeSeconds: "20"
  redrivePolicy: |
    {"deadLetterTargetArn": "arn:aws:sqs:ap-northeast-2:123456789012:order-queue-dlq", "maxReceiveCount": 3}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| SQS Short Polling | 빈 응답 과다 + 비용 낭비 | `WaitTimeSeconds=20` |
| Visibility Timeout 짧음 | 중복 처리 발생 | 처리 시간 × 6 |
| DLQ 미설정 | 실패 메시지 무한 루프 | `maxReceiveCount=3` + DLQ |
| SNS → Lambda 직접 연결 | 스로틀링 시 유실 | SNS → SQS → Lambda |
| EventBridge 단일 Bus | 서비스 간 결합 | 도메인별 Custom Bus |
| 큰 페이로드 직접 전송 | 256KB 초과 | Claim Check (S3 + URL) |
| 멱등성 미구현 | 중복 시 데이터 오염 | 멱등키 기반 중복 확인 |
| FIFO 과도한 그룹 수 | 처리량 병목 | 그룹 최소화 |

---

## 체크리스트

### SQS
- [ ] Long Polling (`WaitTimeSeconds=20`)
- [ ] DLQ + `maxReceiveCount` 설정
- [ ] Visibility Timeout = 처리시간 × 6
- [ ] Consumer 멱등성 보장
- [ ] FIFO 시 MessageGroupId 전략

### SNS
- [ ] SNS → SQS 구독 시 Raw Message Delivery 활성화
- [ ] Filter Policy 설정
- [ ] Fan-out 각 구독자별 DLQ
- [ ] 메시지 암호화 (SSE-KMS)

### EventBridge
- [ ] Custom Event Bus 사용 (default bus 남용 금지)
- [ ] Rule 패턴 검증 (EventBridge Sandbox)
- [ ] Rule Target DLQ 설정
- [ ] Schema Registry 활용
- [ ] Archive 설정 (이벤트 재처리)

### K8s 운영
- [ ] IRSA 설정 (최소 권한 IAM)
- [ ] KEDA ScaledObject 큐 기반 스케일링
- [ ] ACK/Terraform으로 IaC 관리
- [ ] CloudWatch 알람 (DLQ 수, 큐 지연)

---

## 관련 Skills

- `/aws-lambda` — Lambda 이벤트 소스 통합 (SQS, SNS, EventBridge 트리거)
- `/aws-eks` — EKS 클러스터 구성, IRSA, Karpenter
- `/msa-event-driven` — 이벤트 기반 아키텍처 패턴, Outbox, Saga
