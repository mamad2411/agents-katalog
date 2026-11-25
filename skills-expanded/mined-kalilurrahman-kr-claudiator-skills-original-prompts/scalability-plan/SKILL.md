---
name: scalability-plan
description: Design scalability strategies for horizontal and vertical scaling. Outputs capacity planning, bottleneck analysis, and scaling triggers.
argument-hint: [current load, growth projections, budget constraints]
allowed-tools: Read, Write, Bash
---

# Scalability Planning

Design systems to handle 10x, 100x, 1000x growth. Not reactive scaling — proactive architecture with horizontal scaling, caching, async processing, and database sharding.

## Process

1. **Measure current capacity.** Requests/sec, concurrent users, database load.
2. **Project growth.** Expected traffic, peak loads, seasonal spikes.
3. **Identify bottlenecks.** Database, network, CPU, memory, disk I/O.
4. **Design scaling strategy.** Horizontal (add servers), vertical (bigger servers).
5. **Implement autoscaling.** Metrics-based triggers, scale up/down rules.
6. **Add caching layers.** Redis, CDN, application cache.
7. **Shard data.** Partition databases, distributed storage.
8. **Test at scale.** Load testing, chaos engineering, capacity verification.

## Output Format

### Scalability Plan: [System]

**Current Capacity:** 10k RPS  
**Target Capacity:** 100k RPS (10x)  
**Strategy:** Horizontal scaling + Redis + Read replicas  
**Bottleneck:** Database (resolved with sharding)  
**Autoscaling:** CPU > 70% triggers scale-up

---

## Scaling Strategies

### Horizontal Scaling (Scale Out)
```
Add more servers (commodity hardware)

Pros:
- Linear scaling (2x servers = 2x capacity)
- High availability (redundancy)
- Cost-effective at scale

Cons:
- Requires stateless application
- Load balancer needed
- Complexity in distributed systems
```

### Vertical Scaling (Scale Up)
```
Bigger servers (more CPU/RAM)

Pros:
- Simple (no architecture changes)
- No distributed systems complexity
- Good for databases (vertical first)

Cons:
- Limited ceiling (max instance size)
- Single point of failure
- Expensive at high end
```

**Recommendation:** Horizontal for app servers, vertical for databases (initially)

---

## Capacity Planning

### Current State Analysis
```python
import pandas as pd

# Collect metrics for 30 days
metrics = load_metrics(days=30)

current_capacity = {
    'avg_rps': metrics['requests_per_second'].mean(),
    'peak_rps': metrics['requests_per_second'].quantile(0.99),
    'avg_cpu': metrics['cpu_percent'].mean(),
    'peak_cpu': metrics['cpu_percent'].quantile(0.99),
    'avg_memory': metrics['memory_percent'].mean(),
    'db_connections': metrics['db_connections'].quantile(0.95)
}

print(f"""
Current Capacity:
- Average RPS: {current_capacity['avg_rps']:.0f}
- Peak RPS (p99): {current_capacity['peak_rps']:.0f}
- Average CPU: {current_capacity['avg_cpu']:.1f}%
- Peak CPU (p99): {current_capacity['peak_cpu']:.1f}%
- DB Connections (p95): {current_capacity['db_connections']:.0f}
""")
```

### Growth Projection
```python
# Project 6-month growth
growth_scenarios = {
    'conservative': 1.5,  # 50% growth
    'expected': 2.0,      # 100% growth
    'optimistic': 5.0     # 400% growth
}

for scenario, multiplier in growth_scenarios.items():
    projected_rps = current_capacity['peak_rps'] * multiplier
    
    # Calculate required servers
    # Assume 70% CPU target, current 50% at peak
    current_servers = 10
    cpu_per_server = current_capacity['peak_cpu']
    target_cpu = 70
    
    required_servers = (projected_rps / current_capacity['peak_rps']) * \
                      (cpu_per_server / target_cpu) * current_servers
    
    print(f"""
{scenario.upper()} Scenario ({multiplier}x growth):
- Projected Peak RPS: {projected_rps:.0f}
- Required Servers: {required_servers:.0f} (currently {current_servers})
- Monthly Cost: ${required_servers * 100:.0f}
""")
```

---

## Autoscaling

### Kubernetes HPA (Horizontal Pod Autoscaler)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  # Scale on CPU
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  
  # Scale on memory
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  # Scale on custom metric (requests per second)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
    
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### AWS Auto Scaling
```python
import boto3

autoscaling = boto3.client('autoscaling')

# Create Auto Scaling Group
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='api-asg',
    LaunchTemplate={
        'LaunchTemplateId': 'lt-123456',
        'Version': '$Latest'
    },
    MinSize=3,
    MaxSize=20,
    DesiredCapacity=5,
    VPCZoneIdentifier='subnet-a,subnet-b,subnet-c',
    TargetGroupARNs=['arn:aws:elasticloadbalancing:...'],
    HealthCheckType='ELB',
    HealthCheckGracePeriod=300
)

# CPU-based scaling policy
autoscaling.put_scaling_policy(
    AutoScalingGroupName='api-asg',
    PolicyName='cpu-scale-up',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        },
        'TargetValue': 70.0
    }
)

# Request count scaling
autoscaling.put_scaling_policy(
    AutoScalingGroupName='api-asg',
    PolicyName='request-scale',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'CustomizedMetricSpecification': {
            'MetricName': 'RequestCountPerTarget',
            'Namespace': 'AWS/ApplicationELB',
            'Statistic': 'Sum'
        },
        'TargetValue': 1000.0  # Target 1000 requests per instance
    }
)
```

---

## Caching Layers

### Application Cache (Redis)
```python
import redis
from functools import wraps
import pickle

r = redis.Redis(host='redis', port=6379)

def cache(ttl=300):
    """Cache decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{pickle.dumps((args, kwargs))}"
            
            # Check cache
            cached = r.get(key)
            if cached:
                return pickle.loads(cached)
            
            # Call function
            result = func(*args, **kwargs)
            
            # Cache result
            r.setex(key, ttl, pickle.dumps(result))
            
            return result
        return wrapper
    return decorator

@cache(ttl=600)  # Cache for 10 minutes
def get_product(product_id):
    # Expensive database query
    return db.query("SELECT * FROM products WHERE id = ?", (product_id,))

# First call: Database query
product = get_product(123)  # 100ms

# Subsequent calls: Cache hit
product = get_product(123)  # 1ms
```

### CDN (CloudFront)
```python
import boto3

cloudfront = boto3.client('cloudfront')

# Create distribution
response = cloudfront.create_distribution(
    DistributionConfig={
        'CallerReference': str(time.time()),
        'Origins': {
            'Quantity': 1,
            'Items': [{
                'Id': 'api-origin',
                'DomainName': 'api.example.com',
                'CustomOriginConfig': {
                    'HTTPPort': 80,
                    'HTTPSPort': 443,
                    'OriginProtocolPolicy': 'https-only'
                }
            }]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'api-origin',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'AllowedMethods': {
                'Quantity': 7,
                'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE']
            },
            'CachedMethods': {
                'Quantity': 2,
                'Items': ['GET', 'HEAD']
            },
            'ForwardedValues': {
                'QueryString': True,
                'Cookies': {'Forward': 'all'}
            },
            'MinTTL': 0,
            'DefaultTTL': 300,  # 5 minutes
            'MaxTTL': 3600      # 1 hour
        },
        'Enabled': True
    }
)

# Cache behavior for static assets
# GET /static/* → Cache for 1 year
# GET /api/* → Cache for 5 minutes
# POST /api/* → No cache
```

---

## Database Scaling

### Read Replicas
```sql
-- PostgreSQL streaming replication
-- Primary database (writes)
CREATE DATABASE myapp;

-- Read replica 1 (reads)
-- Async replication from primary

-- Read replica 2 (reads)
-- Async replication from primary

-- Application code
def get_user(user_id):
    # Read from replica
    return read_db.query("SELECT * FROM users WHERE id = ?", (user_id,))

def create_user(user_data):
    # Write to primary
    return write_db.execute("INSERT INTO users (...) VALUES (...)")
```

### Connection Pooling
```python
from psycopg2 import pool

# Create connection pool
db_pool = pool.SimpleConnectionPool(
    minconn=5,
    maxconn=20,
    host='db.example.com',
    database='myapp',
    user='appuser',
    password='...'
)

def query(sql, params):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result
    finally:
        db_pool.putconn(conn)
```

### Database Sharding
```python
def get_shard(user_id):
    """Determine which database shard to use"""
    shard_count = 4
    shard_id = hash(user_id) % shard_count
    return shard_id

def get_user(user_id):
    shard_id = get_shard(user_id)
    db = shards[shard_id]
    return db.query("SELECT * FROM users WHERE id = ?", (user_id,))

# Shard mapping
shards = {
    0: connect('shard-0.db.example.com'),
    1: connect('shard-1.db.example.com'),
    2: connect('shard-2.db.example.com'),
    3: connect('shard-3.db.example.com')
}

# Shard 0: users with IDs 0, 4, 8, 12, ...
# Shard 1: users with IDs 1, 5, 9, 13, ...
# Shard 2: users with IDs 2, 6, 10, 14, ...
# Shard 3: users with IDs 3, 7, 11, 15, ...
```

---

## Async Processing

### Message Queue (Celery + Redis)
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def send_email(to, subject, body):
    """Async email sending"""
    # Send email (takes 1-2 seconds)
    smtp.send(to, subject, body)

# API endpoint
@app.route('/signup', methods=['POST'])
def signup():
    user = create_user(request.json)
    
    # Queue email (returns immediately)
    send_email.delay(
        to=user.email,
        subject='Welcome!',
        body='Thanks for signing up'
    )
    
    return {'user_id': user.id}, 201  # Fast response
```

### Background Jobs
```python
# Convert video upload (expensive)
@app.task
def convert_video(video_id):
    video = get_video(video_id)
    
    # CPU-intensive processing (10 minutes)
    converted = ffmpeg.convert(video.file_path, format='mp4')
    
    # Upload to S3
    s3.upload(converted, bucket='videos')
    
    # Update database
    db.update(video_id, status='completed')

# API returns immediately, job runs in background
@app.route('/videos', methods=['POST'])
def upload_video():
    video = save_video(request.files['video'])
    
    convert_video.delay(video.id)
    
    return {'video_id': video.id, 'status': 'processing'}, 202
```

---

## Load Testing

### Simulate 10x Traffic
```python
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)  # 3x more likely
    def browse_products(self):
        self.client.get('/products')
    
    @task(1)
    def view_product(self):
        self.client.get(f'/products/{random.randint(1, 1000)}')
    
    @task(1)
    def add_to_cart(self):
        self.client.post('/cart', json={'product_id': random.randint(1, 1000)})

# Run test
# locust -f loadtest.py --users 10000 --spawn-rate 100
```

### Verify Autoscaling
```bash
# Start load test
locust --users 5000 --spawn-rate 100 &

# Watch autoscaling
watch -n 5 'kubectl get hpa && kubectl get pods | grep api'

# Expected behavior:
# CPU increases → HPA scales up → New pods start → CPU normalizes
```

---

## Bottleneck Analysis

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()

# Run expensive operation
result = process_request()

profiler.disable()

# Analyze results
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest functions

# Output:
# 1. database_query: 2.5s (50%)
# 2. external_api_call: 1.2s (24%)
# 3. json_serialization: 0.8s (16%)
```

**Fix:**
1. Add Redis cache for database queries
2. Call external API async
3. Use faster JSON library (orjson)

---

## Cost Optimization

### Reserved Instances vs On-Demand
```python
# Cost comparison
instances_needed = 20
hours_per_month = 730

# On-demand pricing
on_demand_cost = instances_needed * 0.10 * hours_per_month
# $1,460/month

# Reserved instances (1-year commitment)
reserved_cost = instances_needed * 0.06 * hours_per_month
# $876/month (40% savings)

# Spot instances (interruptible)
spot_cost = instances_needed * 0.03 * hours_per_month
# $438/month (70% savings, but can be terminated)
```

### Hybrid Strategy
```
Baseline (always running): Reserved instances (10 servers)
Peak traffic (business hours): On-demand (5 servers)
Batch jobs (interruptible): Spot instances (5 servers)

Total cost: $876 + $365 + $110 = $1,351/month
vs All on-demand: $2,920/month
Savings: 54%
```

## Rules

- Horizontal scaling preferred over vertical — easier to scale infinitely, higher availability.
- Autoscale on CPU/memory, not requests — requests can spike without resource usage.
- Cache aggressively at every layer — CDN, application, database query cache.
- Database vertical first, horizontal later — sharding is complex, delay until necessary.
- Use read replicas before sharding — handles 10x read growth, simpler than sharding.
- Async processing for non-critical paths — emails, reports, video processing off main thread.
- Load test at 2x expected peak — verify autoscaling works before traffic spike.
- Monitor saturation, not just utilization — disk I/O, network bandwidth have hard limits.
- Reserved instances for baseline capacity — 40-60% cost savings for predictable load.
- Stateless applications required for horizontal scaling — no local session storage.
