---
name: arabic-kubernetes
name_ar: كوبرنتيس
description: Master Kubernetes orchestration in Arabic
description_ar: إتقان أوركسترا كوبرنتيس باللغة العربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان Kubernetes وإدارة الحاويات على نطاق واسع باللغة العربية.

## المفاهيم الأساسية

| المصطلح | العربية | الوصف |
|---------|---------|-------|
| Pod | البود | أصغر وحدة في K8s |
| Service | الخدمة | وصول للشبكة |
| Deployment | النشر | إدارة البودز |
| ConfigMap | الإعدادات | تكوين غير سري |
| Secret | الأسرار | بيانات حساسة |
| Ingress | الدخول | توجيه HTTP |
| Namespace | مساحة الاسم | عزل الموارد |

## أمثلة أساسية

### Pod بسيط

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

## أوامر kubectl

```bash
# عرض الموارد
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get all

# وصف مورد
kubectl describe pod my-pod

# إنشاء/حذف
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml

# الدخول للبود
kubectl exec -it my-pod -- bash

# عرض السجلات
kubectl logs my-pod
kubectl logs -f deployment/my-app

# قياس الموارد
kubectl top pods
kubectl top nodes
```

## أفضل الممارسات

✅ استخدام Namespaces للعزل
✅ تحديد Resources Limits
✅ استخدام Health Checks
✅ ConfigMaps للأسرار غير الحساسة
✅ Secrets للبيانات الحساسة
✅ Labels منظمة

---

## الكلمات المفتاحية

عربي: "كوبرنتيس", "k8s", "أوركسترا", "حاويات"
English: "kubernetes arabic", "k8s tutorial", "container orchestration"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
