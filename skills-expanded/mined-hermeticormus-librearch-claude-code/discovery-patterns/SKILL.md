---
name: "discovery-patterns"
description: "Service discovery patterns with configuration: health-gated Kubernetes Services, headless Services for StatefulSets, Consul registration with health checks, LoadBalancer Services, and Spring Boot readiness checks. Use when services need to find each other reliably."
---

# Discovery Patterns

> Named patterns with code for Kubernetes service routing, Consul registration with health checks, headless service for StatefulSets, and client-side load balancing.

## Patterns

### Pattern: Kubernetes Service with Health-Gated Readiness

```yaml
# Service — stable DNS name, routes to ready pods only
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: production
  labels:
    app: order-service
spec:
  selector:
    app: order-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# Deployment with readiness and liveness probes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: order-service:v1.4.2
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness  # Checks DB, downstream deps
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3       # 3 failures → remove from Service endpoints
            successThreshold: 1       # 1 success → add back to endpoints
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness   # Only checks process alive
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3       # 3 failures → restart pod
          startupProbe:               # For slow-starting JVMs
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            failureThreshold: 30      # 30 × 10s = 5 min before liveness kicks in
            periodSeconds: 10
```

### Pattern: Headless Service for StatefulSet Discovery (Kafka, Cassandra)

```yaml
# Headless service — DNS returns individual pod IPs (not a single ClusterIP)
# Used when clients need to connect to specific StatefulSet pods
apiVersion: v1
kind: Service
metadata:
  name: kafka-headless
  namespace: production
spec:
  clusterIP: None    # Headless — no single virtual IP
  selector:
    app: kafka
  ports:
    - port: 9092
      name: broker

# DNS for headless service returns all pod A records:
# kafka-0.kafka-headless.production.svc.cluster.local → pod 0 IP
# kafka-1.kafka-headless.production.svc.cluster.local → pod 1 IP
# kafka-2.kafka-headless.production.svc.cluster.local → pod 2 IP
```

Kafka client bootstrap configuration using headless DNS:
```yaml
# application.yml for Kafka producers/consumers
spring.kafka.bootstrap-servers: >-
  kafka-0.kafka-headless.production.svc.cluster.local:9092,
  kafka-1.kafka-headless.production.svc.cluster.local:9092,
  kafka-2.kafka-headless.production.svc.cluster.local:9092
```

### Pattern: Consul Service Registration with Health Check (Go)

```go
package main

import (
    "fmt"
    consul "github.com/hashicorp/consul/api"
)

func registerService(client *consul.Client, instanceID, address string, port int) error {
    registration := &consul.AgentServiceRegistration{
        ID:      instanceID,                // Unique per instance
        Name:    "order-service",           // Service name (DNS: order-service.service.consul)
        Address: address,
        Port:    port,
        Tags:    []string{"v2", "production"},
        Check: &consul.AgentServiceCheck{
            HTTP:                           fmt.Sprintf("http://%s:%d/health/ready", address, port),
            Interval:                       "10s",
            Timeout:                        "2s",
            DeregisterCriticalServiceAfter: "30s",  // Remove if down 30s
        },
    }
    return client.Agent().ServiceRegister(registration)
}

// Deregister on graceful shutdown
func deregisterService(client *consul.Client, instanceID string) {
    client.Agent().ServiceDeregister(instanceID)
}

// Discover healthy instances via Consul API
func discoverInstances(client *consul.Client, serviceName string) ([]*consul.ServiceEntry, error) {
    services, _, err := client.Health().Service(serviceName, "", true, nil)
    // true = only healthy instances (passing health check)
    return services, err
}
```

### Pattern: External Service (LoadBalancer) for Public Traffic

```yaml
# Exposes service externally via cloud load balancer (AWS ALB, GCP LB)
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
spec:
  selector:
    app: api-gateway
  ports:
    - port: 443
      targetPort: 8443
      protocol: TCP
  type: LoadBalancer

---
# ExternalName service — routes to external hostname (outside cluster)
# Useful for migrating to external managed services
apiVersion: v1
kind: Service
metadata:
  name: legacy-payment-service
  namespace: production
spec:
  type: ExternalName
  externalName: payment.internal.company.com  # DNS CNAME
  # Access: legacy-payment-service.production.svc.cluster.local → company.com host
```

### Pattern: Readiness Health Check (Spring Boot)

```java
// Composite readiness check — all must pass for pod to receive traffic
@Component("orderServiceReadinessIndicator")
public class OrderServiceReadinessIndicator implements HealthIndicator {

    private final DataSource dataSource;
    private final InventoryServiceClient inventoryClient;

    @Override
    public Health health() {
        Map<String, Object> details = new LinkedHashMap<>();
        boolean healthy = true;

        // Check 1: Database connection
        try (Connection conn = dataSource.getConnection()) {
            conn.createStatement().execute("SELECT 1");
            details.put("database", "UP");
        } catch (SQLException e) {
            details.put("database", "DOWN: " + e.getMessage());
            healthy = false;
        }

        // Check 2: Critical downstream service
        try {
            inventoryClient.ping();  // Lightweight ping endpoint
            details.put("inventory-service", "UP");
        } catch (Exception e) {
            details.put("inventory-service", "DOWN: " + e.getMessage());
            healthy = false;
        }

        return healthy
            ? Health.up().withDetails(details).build()
            : Health.down().withDetails(details).build();
    }
}
```

## Anti-Patterns

### Anti-Pattern: Hardcoded IP Addresses in Configuration

```yaml
# WRONG: hardcoded IP — breaks when pod restarts and gets a new IP
spring:
  datasource:
    url: jdbc:postgresql://10.0.1.45:5432/orders  # Pod IP, not Service name
```

Fix: use the Kubernetes Service DNS name: `jdbc:postgresql://postgres-service.production:5432/orders`. The Service DNS is stable; the pod IP is not.

### Anti-Pattern: Checking Remote Services in Liveness Probe

A liveness probe that calls downstream services (payment service, inventory service). If payment service is down, liveness fails, Kubernetes restarts the pod. After restart, liveness still fails (payment service still down). All pods restart in a loop — cascading failure from a temporary downstream outage.

Fix: liveness probes check only local process health (`/ping`, thread pool alive). Readiness probes check dependencies — readiness failure removes pod from rotation without restarting it.

### Anti-Pattern: Missing Startup Probe for Slow JVMs

JVM services often take 20-30 seconds to warm up. Without a startup probe, the liveness probe begins checking immediately. The service is killed before it finishes starting. With a startup probe, Kubernetes gives extended time before liveness kicks in.

### Anti-Pattern: Stale Registry Entries (Eureka Without TTL)

Service crashes without deregistering. Stale entry remains in Eureka. Other services get the stale IP and fail to connect. With Eureka, each instance sends heartbeats; after 3 missed heartbeats (90s default), it is removed. Configure `eureka.instance.leaseExpirationDurationInSeconds` to control TTL.

## References

- Kubernetes Services and DNS: kubernetes.io/docs/concepts/services-networking
- Consul health checks: developer.hashicorp.com/consul/docs/services/usage/checks
- Spring Boot Actuator health: docs.spring.io/spring-boot/docs/current/reference/html/actuator.html
- Netflix Eureka: github.com/Netflix/eureka/wiki
