---
name: kubernetes-deployment-pro
description: Production Kubernetes patterns — deployments, services, ingress, scaling, health checks
triggers: [Kubernetes, K8s, container orchestration, deployment, pods, services, ingress, scaling]
---

# SKILL: Kubernetes Deployment Pro

## Core Resources

### Pattern 1: Deployment (Stateless Apps)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app: api
spec:
  replicas: 3  # 3 pod instances
  
  selector:
    matchLabels:
      app: api
  
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
        
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Pattern 2: Service (Load Balancing)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api  # Routes to pods with this label
  
  type: LoadBalancer  # Options: ClusterIP, NodePort, LoadBalancer
  
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Pattern 3: Ingress (HTTP Routing)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls
  
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### Pattern 4: ConfigMap & Secrets
```yaml
# ConfigMap (non-sensitive config)
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"

---
# Secret (sensitive data)
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  url: <base64-encoded-connection-string>
```

### Pattern 5: Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  
  minReplicas: 3
  maxReplicas: 10
  
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Pattern 6: StatefulSet (Stateful Apps)
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  
  selector:
    matchLabels:
      app: postgres
  
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:14
        ports:
        - containerPort: 5432
        
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

### Pattern 7: Job (One-time Tasks)
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:v1.0.0
        command: ["npm", "run", "migrate"]
      
      restartPolicy: Never
  
  backoffLimit: 3  # Retry 3 times on failure
```

### Pattern 8: CronJob (Scheduled Tasks)
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"  # Every day at 2 AM
  
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["backup.sh"]
          
          restartPolicy: OnFailure
```

## Quality Checks
- [ ] Resource limits set (memory, CPU)
- [ ] Health checks configured (liveness, readiness)
- [ ] Horizontal Pod Autoscaler enabled
- [ ] Secrets used for sensitive data
- [ ] Ingress with TLS certificates
- [ ] Rolling update strategy configured
- [ ] Pod disruption budget set
- [ ] Monitoring & logging configured
