# Kafka Topic Provisioning

## Purpose
Declares and provisions Kafka topics using Jikkou's declarative YAML format.

## Role
Data Engineer

## Phase
Development (after schema registered in Apicurio)

## Triggered By
New Kafka topic needed for story.

## Inputs
- Registered event schema from `apicurio-registration`

## Tool
Jikkou (runs as CI/CD job — not manually). Topic definitions: `kafka/state.yaml`.

## Process

### Topic Declaration Format
```yaml
apiVersion: "kafka.jikkou.io/v1beta2"
kind: KafkaTopicList
items:
  - metadata:
      name: {service}-{event-name}         # e.g. user-user-created
      labels:
        owner: {service-name}
    spec:
      partitions: 6                         # start here, increase if needed
      replicas: 3                           # always 3 in production
      configs:
        retention.ms: "604800000"           # 7 days default
        cleanup.policy: delete              # or compact for state topics
        compression.type: lz4
        min.insync.replicas: "2"
```

### Partition Count Guidance
- 6 partitions: default for most topics
- 12 partitions: high-throughput topics (100k+ events/day)
- Higher: only with explicit throughput justification

CI/CD: `Jikkou plan` runs on PR, `Jikkou apply` runs after merge to main.

## Outputs
Topic declared in `kafka/state.yaml`, provisioned via CI/CD.

## Quality Gates
- [ ] Topic added to kafka/state.yaml (not created manually)
- [ ] Partition count justified
- [ ] Retention policy appropriate for data type
- [ ] Schema linked to topic in Apicurio

## References
- `.claude/skills/data-engineer/apicurio-registration/SKILL.md`
- `.claude/skills/backend-developer/kafka-driver-implementation/SKILL.md`
