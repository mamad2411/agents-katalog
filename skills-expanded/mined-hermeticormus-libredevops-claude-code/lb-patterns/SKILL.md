---
name: lb-patterns
description: "Load balancing patterns: a full production NGINX config, AWS ALB in Terraform, HAProxy with active health checks, Traefik IngressRoute on Kubernetes, and NGINX upstream health checks. Use when configuring or reviewing reverse proxies and load balancers."
---

# Load Balancing Patterns

Traffic distribution, SSL termination, upstream health checks, rate limiting, and canary deployments.

## NGINX Full Production Config

```nginx
# /etc/nginx/nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    use epoll;
    multi_accept on;
}

http {
    # Rate limit zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # Upstream: main app servers with health checks
    upstream app_backend {
        least_conn;
        server 10.0.1.10:8080 max_fails=3 fail_timeout=30s;
        server 10.0.1.11:8080 max_fails=3 fail_timeout=30s;
        server 10.0.1.12:8080 max_fails=3 fail_timeout=30s;
        server 10.0.1.13:8080 backup;  # Only used if all primaries fail
        keepalive 64;
        keepalive_requests 10000;
        keepalive_timeout 75s;
    }

    # Upstream: canary (10% of traffic)
    upstream app_canary {
        server 10.0.2.10:8080;
        keepalive 16;
    }

    # Split traffic: 90% stable, 10% canary
    split_clients "${remote_addr}${request_uri}" $app_upstream {
        90%    app_backend;
        *      app_canary;
    }

    server {
        listen 80;
        server_name api.example.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name api.example.com;

        # TLS
        ssl_certificate     /etc/ssl/api.example.com.crt;
        ssl_certificate_key /etc/ssl/api.example.com.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 1d;
        ssl_session_tickets off;
        ssl_stapling on;
        ssl_stapling_verify on;
        resolver 8.8.8.8 valid=300s;

        # Security headers
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # Proxy settings
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;

        # API: rate limited
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
            limit_conn addr 20;
            proxy_pass http://$app_upstream;
        }

        # Auth: strict rate limit
        location /auth/login {
            limit_req zone=login burst=5;
            limit_req_status 429;
            proxy_pass http://$app_upstream;
        }

        # Health check endpoint: no rate limit, no logging
        location /health {
            access_log off;
            proxy_pass http://app_backend;
        }

        # Static assets: serve directly with caching
        location /static/ {
            root /var/www;
            expires 1y;
            add_header Cache-Control "public, immutable";
            gzip_static on;
        }
    }
}
```

## AWS ALB with Terraform

```hcl
# ALB with HTTPS listener, target group, and weighted forwarding
resource "aws_lb" "app" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true
  enable_http2               = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.id
    prefix  = "alb"
    enabled = true
  }
}

resource "aws_lb_target_group" "app_stable" {
  name        = "app-stable"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"  # Use "ip" for ECS Fargate

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  deregistration_delay = 30  # Seconds to wait before removing from rotation
}

resource "aws_lb_target_group" "app_canary" {
  name     = "app-canary"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  target_type = "ip"

  health_check {
    path    = "/health"
    matcher = "200"
  }
}

# HTTPS listener with weighted forwarding (canary deployment)
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.app_stable.arn
        weight = 90
      }
      target_group {
        arn    = aws_lb_target_group.app_canary.arn
        weight = 10
      }
      stickiness {
        enabled  = false
        duration = 1
      }
    }
  }
}

# HTTP -> HTTPS redirect
resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# Path-based routing rule
resource "aws_lb_listener_rule" "api_v2" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_stable.arn
  }

  condition {
    path_pattern {
      values = ["/api/v2/*"]
    }
  }
}
```

## HAProxy with Active Health Checks

```
# haproxy.cfg - Production HTTP load balancer
global
    maxconn 100000
    log /dev/log local0
    log /dev/log local1 notice
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    tune.ssl.default-dh-param 2048

defaults
    log global
    mode http
    option httplog
    option dontlognull
    option forwardfor
    option http-server-close
    option redispatch
    retries 3
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    timeout tunnel  1h     # WebSocket / long-poll connections
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 503 /etc/haproxy/errors/503.http

# HTTP -> HTTPS redirect frontend
frontend http_in
    bind *:80
    redirect scheme https code 301

# HTTPS frontend
frontend https_in
    bind *:443 ssl crt /etc/ssl/private/myapp.pem alpn h2,http/1.1
    http-response set-header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    # Rate limit: 20 req/s per IP, table of 1M entries
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 200 }

    # Route by path
    acl is_api path_beg /api/
    acl is_ws  hdr(Upgrade) -i websocket

    use_backend ws_backend  if is_ws
    use_backend api_backend if is_api
    default_backend http_backend

backend http_backend
    balance leastconn
    option httpchk GET /health HTTP/1.1\r\nHost:\ myapp.internal
    http-check expect status 200
    server app1 10.0.1.10:8080 check inter 5s rise 2 fall 3 weight 1
    server app2 10.0.1.11:8080 check inter 5s rise 2 fall 3 weight 1
    server app3 10.0.1.12:8080 check inter 5s rise 2 fall 3 weight 1

backend api_backend
    balance roundrobin
    timeout server 120s
    option httpchk GET /health HTTP/1.1\r\nHost:\ myapp.internal
    http-check expect status 200
    server api1 10.0.2.10:8080 check inter 5s rise 2 fall 3
    server api2 10.0.2.11:8080 check inter 5s rise 2 fall 3

backend ws_backend
    balance source   # Sticky by client IP for WebSocket
    timeout server 3600s
    timeout tunnel 3600s
    server ws1 10.0.3.10:8080 check inter 10s

# Stats
listen stats
    bind *:8404
    stats enable
    stats uri /haproxy-stats
    stats refresh 10s
    stats auth admin:${HAPROXY_STATS_PASSWORD}
    stats hide-version
```

## Traefik on Kubernetes (IngressRoute)

```yaml
# Traefik v3 with middleware chain
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: myapp
  namespace: production
spec:
  entryPoints: [websecure]
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/api`)
      kind: Rule
      services:
        - name: myapp
          port: 80
          weight: 90
        - name: myapp-canary
          port: 80
          weight: 10
      middlewares:
        - name: rate-limit
        - name: security-headers
  tls:
    secretName: myapp-tls

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
  namespace: production
spec:
  rateLimit:
    average: 100
    burst: 50
    period: 1m
    sourceCriterion:
      ipStrategy:
        depth: 1

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: security-headers
  namespace: production
spec:
  headers:
    stsSeconds: 63072000
    stsIncludeSubdomains: true
    stsPreload: true
    forceSTSHeader: true
    contentTypeNosniff: true
    frameDeny: true
    referrerPolicy: "strict-origin-when-cross-origin"
```

## NGINX Upstream Health Check (nginx_upstream_check_module)

```nginx
# Requires nginx_upstream_check_module (OpenResty or custom build)
upstream backend {
    server app1.internal:8080;
    server app2.internal:8080;
    server app3.internal:8080;

    check interval=5000 rise=2 fall=3 timeout=1000 type=http;
    check_http_send "GET /health HTTP/1.0\r\nHost: app.internal\r\n\r\n";
    check_http_expect_alive http_2xx;
}

# Health check status page
location /upstream_status {
    check_status;
    access_log off;
    allow 10.0.0.0/8;
    deny all;
}
```
