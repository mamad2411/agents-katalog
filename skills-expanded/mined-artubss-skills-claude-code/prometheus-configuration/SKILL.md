---
name: prometheus-configuration
description: "Guia completo para configuração do Prometheus, coleta de métricas, configuração de scrape e recording rules."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Configuração do Prometheus

Guia completo para configuração do Prometheus, coleta de métricas, configuração de scrape e recording rules.

## Não use essa skill quando

- A tarefa não está relacionada à configuração do Prometheus
- Você precisa de um domínio ou ferramenta diferente fora desse escopo

## Instruções

- Esclareça objetivos, restrições e entradas necessárias.
- Aplique as melhores práticas relevantes e valide os resultados.
- Forneça etapas acionáveis e verificação.
- Se forem necessários exemplos detalhados, abra `resources/implementation-playbook.md`.

## Propósito

Configurar o Prometheus para coleta abrangente de métricas, alertas e monitoramento de infraestrutura e aplicações.

## Use essa skill quando

- Configurar monitoramento com Prometheus
- Configurar scrape de métricas
- Criar recording rules
- Projetar alert rules
- Implementar service discovery

## Arquitetura do Prometheus

```
┌──────────────┐
│ Applications │ ← Instrumentadas com bibliotecas de cliente
└──────┬───────┘
       │ /metrics endpoint
       ↓
┌──────────────┐
│  Prometheus  │ ← Faz scrape de métricas periodicamente
│    Server    │
└──────┬───────┘
       │
       ├─→ AlertManager (alertas)
       ├─→ Grafana (visualização)
       └─→ Armazenamento de longo prazo (Thanos/Cortex)
```

## Instalação

### Kubernetes com Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageVolumeSize=50Gi
```

### Docker Compose

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'

volumes:
  prometheus-data:
```

## Arquivo de Configuração

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-west-2'

# Configuração do Alertmanager
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

# Carregar arquivos de regras
rule_files:
  - /etc/prometheus/rules/*.yml

# Configurações de scrape
scrape_configs:
  # Prometheus em si
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporters
  - job_name: 'node-exporter'
    static_configs:
      - targets:
        - 'node1:9100'
        - 'node2:9100'
        - 'node3:9100'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: '([^:]+)(:[0-9]+)?'
        replacement: '${1}'

  # Pods do Kubernetes com anotações
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod

  # Métricas de aplicação
  - job_name: 'my-app'
    static_configs:
      - targets:
        - 'app1.example.com:9090'
        - 'app2.example.com:9090'
    metrics_path: '/metrics'
    scheme: 'https'
    tls_config:
      ca_file: /etc/prometheus/ca.crt
      cert_file: /etc/prometheus/client.crt
      key_file: /etc/prometheus/client.key
```

**Referência:** Veja `assets/prometheus.yml.template`

## Configurações de Scrape

### Alvos Estáticos

```yaml
scrape_configs:
  - job_name: 'static-targets'
    static_configs:
      - targets: ['host1:9100', 'host2:9100']
        labels:
          env: 'production'
          region: 'us-west-2'
```

### Service Discovery Baseado em Arquivo

```yaml
scrape_configs:
  - job_name: 'file-sd'
    file_sd_configs:
      - files:
        - /etc/prometheus/targets/*.json
        - /etc/prometheus/targets/*.yml
        refresh_interval: 5m
```

**targets/production.json:**
```json
[
  {
    "targets": ["app1:9090", "app2:9090"],
    "labels": {
      "env": "production",
      "service": "api"
    }
  }
]
```

### Service Discovery do Kubernetes

```yaml
scrape_configs:
  - job_name: 'kubernetes-services'
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

**Referência:** Veja `references/scrape-configs.md`

## Recording Rules

Crie métricas pré-computadas para expressões frequentemente consultadas:

```yaml
# /etc/prometheus/rules/recording_rules.yml
groups:
  - name: api_metrics
    interval: 15s
    rules:
      # Taxa de requisições HTTP por serviço
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      # Taxa de erros
      - record: job:http_requests_errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      # Percentual de taxa de erro
      - record: job:http_requests_error_rate:percentage
        expr: |
          (job:http_requests_errors:rate5m / job:http_requests:rate5m) * 100

      # Latência P95
      - record: job:http_request_duration:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

  - name: resource_metrics
    interval: 30s
    rules:
      # Percentual de utilização de CPU
      - record: instance:node_cpu:utilization
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      # Percentual de utilização de memória
      - record: instance:node_memory:utilization
        expr: |
          100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)

      # Percentual de uso de disco
      - record: instance:node_disk:utilization
        expr: |
          100 - ((node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)
```

**Referência:** Veja `references/recording-rules.md`

## Alert Rules

```yaml
# /etc/prometheus/rules/alert_rules.yml
groups:
  - name: availability
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} está inativo"
          description: "{{ $labels.job }} está inativo há mais de 1 minuto"

      - alert: HighErrorRate
        expr: job:http_requests_error_rate:percentage > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Taxa de erro alta para {{ $labels.job }}"
          description: "Taxa de erro é {{ $value }}% (limite: 5%)"

      - alert: HighLatency
        expr: job:http_request_duration:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latência alta para {{ $labels.job }}"
          description: "Latência P95 é {{ $value }}s (limite: 1s)"

  - name: resources
    interval: 1m
    rules:
      - alert: HighCPUUsage
        expr: instance:node_cpu:utilization > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Uso de CPU alto em {{ $labels.instance }}"
          description: "Uso de CPU é {{ $value }}%"

      - alert: HighMemoryUsage
        expr: instance:node_memory:utilization > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Uso de memória alto em {{ $labels.instance }}"
          description: "Uso de memória é {{ $value }}%"

      - alert: DiskSpaceLow
        expr: instance:node_disk:utilization > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Espaço em disco baixo em {{ $labels.instance }}"
          description: "Uso de disco é {{ $value }}%"
```

## Validação

```bash
# Validar configuração
promtool check config prometheus.yml

# Validar regras
promtool check rules /etc/prometheus/rules/*.yml

# Testar query
promtool query instant http://localhost:9090 'up'
```

**Referência:** Veja `scripts/validate-prometheus.sh`

## Melhores Práticas

1. **Use nomenclatura consistente** para métricas (prefix_name_unit)
2. **Defina intervalos de scrape apropriados** (15-60s típico)
3. **Use recording rules** para queries caras
4. **Implemente alta disponibilidade** (múltiplas instâncias do Prometheus)
5. **Configure retenção** com base na capacidade de armazenamento
6. **Use relabeling** para limpeza de métricas
7. **Monitore o Prometheus em si**
8. **Implemente federação** para deployments grandes
9. **Use Thanos/Cortex** para armazenamento de longo prazo
10. **Documente métricas customizadas**

## Troubleshooting

**Verificar alvos de scrape:**
```bash
curl http://localhost:9090/api/v1/targets
```

**Verificar configuração:**
```bash
curl http://localhost:9090/api/v1/status/config
```

**Testar query:**
```bash
curl 'http://localhost:9090/api/v1/query?query=up'
```

## Arquivos de Referência

- `assets/prometheus.yml.template` - Template de configuração completo
- `references/scrape-configs.md` - Padrões de configuração de scrape
- `references/recording-rules.md` - Exemplos de recording rules
- `scripts/validate-prometheus.sh` - Script de validação

## Skills Relacionadas

- `grafana-dashboards` - Para visualização
- `slo-implementation` - Para monitoramento de SLO
- `distributed-tracing` - Para rastreamento de requisições