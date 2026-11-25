---
name: grafana-dashboards
description: "Criar e gerenciar dashboards Grafana prontos para produção com observabilidade abrangente do sistema."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Dashboards Grafana

Criar e gerenciar dashboards Grafana prontos para produção com observabilidade abrangente do sistema.

## Não use essa habilidade quando

- A tarefa não estiver relacionada a dashboards Grafana
- Você precisar de um domínio ou ferramenta diferente fora deste escopo

## Instruções

- Esclareça objetivos, restrições e inputs necessários.
- Aplique as melhores práticas relevantes e valide os resultados.
- Forneça etapas acionáveis e verificação.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

## Propósito

Projetar dashboards Grafana eficazes para monitorar aplicações, infraestrutura e métricas de negócios.

## Use essa habilidade quando

- Visualizar métricas do Prometheus
- Criar dashboards personalizados
- Implementar dashboards de SLO
- Monitorar infraestrutura
- Rastrear KPIs de negócios

## Princípios de Design de Dashboard

### 1. Hierarquia de Informações
```
┌─────────────────────────────────────┐
│  Métricas Críticas (Números Grandes)│
├─────────────────────────────────────┤
│  Tendências Principais (Séries)     │
├─────────────────────────────────────┤
│  Métricas Detalhadas (Tabelas)      │
└─────────────────────────────────────┘
```

### 2. Método RED (Serviços)
- **Rate** - Requisições por segundo
- **Errors** - Taxa de erro
- **Duration** - Latência/tempo de resposta

### 3. Método USE (Recursos)
- **Utilization** - % de tempo que o recurso está em uso
- **Saturation** - Comprimento da fila/tempo de espera
- **Errors** - Contagem de erros

## Estrutura de Dashboard

### Dashboard de Monitoramento de API

```json
{
  "dashboard": {
    "title": "API Monitoring",
    "tags": ["api", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Error Rate %",
        "type": "graph",
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))) * 100",
            "legendFormat": "Error Rate"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [5], "type": "gt"},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "type": "query"
            }
          ]
        },
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 24, "h": 8}
      }
    ]
  }
}
```

**Referência:** Veja `assets/api-dashboard.json`

## Tipos de Painel

### 1. Painel Stat (Valor Único)
```json
{
  "type": "stat",
  "title": "Total Requests",
  "targets": [{
    "expr": "sum(http_requests_total)"
  }],
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "orientation": "auto",
    "textMode": "auto",
    "colorMode": "value"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": 0, "color": "green"},
          {"value": 80, "color": "yellow"},
          {"value": 90, "color": "red"}
        ]
      }
    }
  }
}
```

### 2. Gráfico de Série Temporal
```json
{
  "type": "graph",
  "title": "CPU Usage",
  "targets": [{
    "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
  }],
  "yaxes": [
    {"format": "percent", "max": 100, "min": 0},
    {"format": "short"}
  ]
}
```

### 3. Painel de Tabela
```json
{
  "type": "table",
  "title": "Service Status",
  "targets": [{
    "expr": "up",
    "format": "table",
    "instant": true
  }],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "indexByName": {},
        "renameByName": {
          "instance": "Instance",
          "job": "Service",
          "Value": "Status"
        }
      }
    }
  ]
}
```

### 4. Mapa de Calor
```json
{
  "type": "heatmap",
  "title": "Latency Heatmap",
  "targets": [{
    "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
    "format": "heatmap"
  }],
  "dataFormat": "tsbuckets",
  "yAxis": {
    "format": "s"
  }
}
```

## Variáveis

### Variáveis de Query
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 1,
        "multi": false
      },
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
        "refresh": 1,
        "multi": true
      }
    ]
  }
}
```

### Usar Variáveis em Queries
```
sum(rate(http_requests_total{namespace="$namespace", service=~"$service"}[5m]))
```

## Alertas em Dashboards

```json
{
  "alert": {
    "name": "High Error Rate",
    "conditions": [
      {
        "evaluator": {
          "params": [5],
          "type": "gt"
        },
        "operator": {"type": "and"},
        "query": {
          "params": ["A", "5m", "now"]
        },
        "reducer": {"type": "avg"},
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "for": "5m",
    "frequency": "1m",
    "message": "Error rate is above 5%",
    "noDataState": "no_data",
    "notifications": [
      {"uid": "slack-channel"}
    ]
  }
}
```

## Provisionamento de Dashboard

**dashboards.yml:**
```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'General'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/dashboards
```

## Padrões Comuns de Dashboard

### Dashboard de Infraestrutura

**Painéis-chave:**
- Utilização de CPU por nó
- Uso de memória por nó
- I/O de disco
- Tráfego de rede
- Contagem de pods por namespace
- Status do nó

**Referência:** Veja `assets/infrastructure-dashboard.json`

### Dashboard de Banco de Dados

**Painéis-chave:**
- Queries por segundo
- Uso do pool de conexões
- Latência de query (P50, P95, P99)
- Conexões ativas
- Tamanho do banco de dados
- Lag de replicação
- Queries lentas

**Referência:** Veja `assets/database-dashboard.json`

### Dashboard de Aplicação

**Painéis-chave:**
- Taxa de requisições
- Taxa de erro
- Tempo de resposta (percentis)
- Usuários/sessões ativas
- Taxa de acerto de cache
- Comprimento da fila

## Melhores Práticas

1. **Comece com templates** (dashboards da comunidade Grafana)
2. **Use nomenclatura consistente** para painéis e variáveis
3. **Agrupe métricas relacionadas** em linhas
4. **Defina intervalos de tempo apropriados** (padrão: Últimas 6 horas)
5. **Use variáveis** para flexibilidade
6. **Adicione descrições de painel** para contexto
7. **Configure unidades** corretamente
8. **Defina limites significativos** para cores
9. **Use cores consistentes** em dashboards
10. **Teste com diferentes intervalos de tempo**

## Dashboard como Código

### Provisionamento com Terraform

```hcl
resource "grafana_dashboard" "api_monitoring" {
  config_json = file("${path.module}/dashboards/api-monitoring.json")
  folder      = grafana_folder.monitoring.id
}

resource "grafana_folder" "monitoring" {
  title = "Production Monitoring"
}
```

### Provisionamento com Ansible

```yaml
- name: Deploy Grafana dashboards
  copy:
    src: "{{ item }}"
    dest: /etc/grafana/dashboards/
  with_fileglob:
    - "dashboards/*.json"
  notify: restart grafana
```

## Arquivos de Referência

- `assets/api-dashboard.json` - Dashboard de monitoramento de API
- `assets/infrastructure-dashboard.json` - Dashboard de infraestrutura
- `assets/database-dashboard.json` - Dashboard de monitoramento de banco de dados
- `references/dashboard-design.md` - Guia de design de dashboard

## Habilidades Relacionadas

- `prometheus-configuration` - Para coleta de métricas
- `slo-implementation` - Para dashboards de SLO