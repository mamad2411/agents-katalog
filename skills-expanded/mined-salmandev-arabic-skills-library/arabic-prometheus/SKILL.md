---
name: arabic-prometheus
name_ar: بروميثيوس
description: Master monitoring with Prometheus in Arabic
description_ar: إتقان المراقبة مع بروميثيوس بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان مراقبة الأنظمة والتطبيقات باستخدام Prometheus.

## المكونات الأساسية

| المكون | الوصف |
|--------|-------|
| **Server** | جمع وتخزين بيانات |
| **Exporters** | جمع مقاييس من أنظمة |
| **Pushgateway** | استقبال بيانات push |
| **Alertmanager** | إدارة التنبيهات |
| **Grafana** | تصور البيانات |

## تثبيت Prometheus

```yaml
# docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
```

## إعداد prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
```

## PromQL أمثلة

```promql
# معدل استخدام CPU
rate(node_cpu_seconds_total{mode="user"}[5m])

# استخدام الذاكرة
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes

# طلبات HTTP
rate(http_requests_total[5m])

# زمن الاستجابة
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# عدد الأخطاء
rate(http_requests_total{status=~"5.."}[5m])
```

## Alertmanager إعدادات

```yaml
# alertmanager.yml
route:
  group_by: ['alertname']
  receiver: 'email-notifications'

receivers:
  - name: 'email-notifications'
    email_configs:
      - to: 'team@example.com'
        from: 'alerts@example.com'
        smarthost: 'smtp.example.com:587'
```

## Alert Rules

```yaml
# alerts.yml
groups:
  - name: example
    rules:
      - alert: HighCPU
        expr: rate(node_cpu_seconds_total[5m]) > 0.8
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "استخدام CPU مرتفع"
          description: "CPU {{ $labels.instance }} الاستخدام {{ $value }}%"

      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "السيرفر {{ $labels.instance }} غير متاح"
```

## Grafana Dashboard

1. أضف Prometheus datasource
2. استورد dashboard جاهز
3. أو أنشئ dashboard مخصص

**Dashboard IDs:**
- Node Exporter: 1860
- Prometheus: 2
- Docker: 179

## أفضل الممارسات

✅ استخدم labels بشكل متسق
✅ اضبط retention period مناسب
✅ استخدم recording rules للاستعلامات المعقدة
✅ اضبط تنبيهات ذات معنى
✅ راجع dashboards دورياً

❌ لا تجمع كل المقاييس
❌ لا تضبط thresholds منخفضة جداً
❌ لا تتجاهل التنبيهات

---

## الكلمات المفتاحية

عربي: "بروميثيوس", "مراقبة", "مقاييس", "تنبيهات"
English: "prometheus arabic", "monitoring", "metrics", "alerting"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
