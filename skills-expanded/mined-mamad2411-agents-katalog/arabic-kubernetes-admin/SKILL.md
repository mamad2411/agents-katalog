---
name: arabic-kubernetes-admin
name_ar: إدارة كوبرنتيس
description: Master Kubernetes administration in Arabic
description_ar: إتقان إدارة كوبرنتيس بالعربية
category: cloud-devops
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان أساسيات إدارة Kubernetes.

## مفاهيم أساسية

### ١. المكونات

| المكون | الوصف |
|--------|-------|
| **Pod** | أصغر وحدة |
| **Service** | وصول للشبكة |
| **Deployment** | إدارة Pods |
| **ConfigMap** | إعدادات |
| **Secret** | بيانات حساسة |

### ٢. أوامر kubectl

```bash
# عرض موارد
kubectl get pods
kubectl get deployments
kubectl get services

# إنشاء مورد
kubectl apply -f deployment.yaml

# حذف مورد
kubectl delete pod my-pod

# الدخول لـ Pod
kubectl exec -it my-pod -- bash

# عرض سجلات
kubectl logs my-pod
```

### ٣. YAML مثال

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

## أفضل الممارسات

✅ استخدم Namespaces للعزل
✅ حدد Resource Limits
✅ فعل Health Checks
✅ استخدم Helm للحزم

❌ لا تشغل كـ root
❌ لا تهمل Updates
❌ لا تهمل Backup

---

## الكلمات المفتاحية

عربي: "كوبرنتيس", "Kubernetes", "K8s", "حاويات"
English: "Kubernetes arabic", "K8s", "container orchestration", "DevOps"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
