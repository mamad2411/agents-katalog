-----
name: latency
description: >
  Expert in network latency analysis, optimization, and performance engineering. 
  Use this skill for measuring, diagnosing, and reducing latency in distributed 
  systems, web applications, APIs, and real-time systems. Covers latency fundamentals, 
  measurement techniques, optimization strategies, and architecture patterns.
license: MIT
compatibility: opencode
metadata:
  audience: web-developers
  category: networking
  tags: [latency, performance, networking, optimization, distributed-systems]

# Network Latency Fundamentals

Covers: **Latency Components · Measurement Techniques · Optimization Strategies · CDN · Caching · Connection Management · Real-Time Systems**

-----

## Latency Fundamentals

### Understanding Latency

**Latency** is the time delay between a request and its response. Unlike bandwidth (capacity), latency represents the minimum time needed for data to travel:

```
Latency = Distance / Speed of Signal

Examples:
- Speed of light in fiber: ~200,000 km/s (2/3 c)
- NYC → London fiber: ~70ms minimum
- NYC → Sydney fiber: ~150ms minimum
```

### Components of Total Latency

| Component | Description | Typical Values |
|-----------|-------------|-----------------|
| **Propagation** | Distance / speed of light | 10-200ms |
| **Transmission** | Putting bits on wire | 1-10ms per hop |
| **Processing** | Router/switch processing | <1ms per hop |
| **Queuing** | Waiting in buffers | Variable, 0-100ms+ |
| **Serialization** | Converting to bits | 1-10ms per KB |
| **Application** | Server processing | 10-500ms |

```python
import time
from dataclasses import dataclass
from typing import List, Dict, Optional
import statistics

@dataclass
class LatencyMeasurement:
    """Single latency measurement"""
    timestamp: float
    latency_ms: float
    success: bool
    error: Optional[str] = None

class LatencyProfiler:
    """Profile latency components"""
    
    @staticmethod
    def estimate_min_latency(distance_km: float, 
                            medium: str = 'fiber') -> float:
        """Estimate minimum latency based on distance"""
        speed_map = {
            'fiber': 200000,      # km/s
            'copper': 200000000,  # m/s
            'wireless': 300000000 # speed of light
        }
        
        speed = speed_map.get(medium, 200000)
        return (distance_km / speed) * 1000  # Convert to ms
    
    @staticmethod
    def calculate_rtt(distance_km: float, hops: int = 10,
                     processing_per_hop_ms: float = 0.5) -> float:
        """Calculate approximate RTT"""
        # One-way distance
        one_way = LatencyProfiler.estimate_min_latency(distance_km)
        
        # Add processing per hop (both directions)
        processing = hops * processing_per_hop_ms * 2
        
        return one_way * 2 + processing
    
    @staticmethod
    def decompose_latency(total_latency: float, 
                         distance_km: float,
                         data_size_bytes: int = 1000,
                         bandwidth_mbps: float = 100) -> Dict[str, float]:
        """Decompose total latency into components"""
        # Propagation (both directions)
        propagation = LatencyProfiler.estimate_min_latency(distance_km) * 2
        
        # Serialization (both directions)
        serialization = (data_size_bytes * 8 / (bandwidth_mbps * 1e6)) * 1000 * 2
        
        # Processing (estimated)
        processing = 5  # ms, rough estimate
        
        # Remaining is queuing/variability
        queuing = max(0, total_latency - propagation - serialization - processing)
        
        return {
            'propagation': propagation,
            'serialization': serialization,
            'processing': processing,
            'queuing_variability': queuing,
            'total': total_latency
        }
```

-----

## Latency Measurement

### Measurement Tools and Techniques

```python
import subprocess
import socket
import struct
from datetime import datetime

class LatencyMeasurer:
    """Measure network latency"""
    
    @staticmethod
    def ping(host: str, count: int = 4) -> Dict:
        """Ping host and collect statistics"""
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), host],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse output
            lines = result.stdout.split('\n')
            times = []
            
            for line in lines:
                if 'time=' in line:
                    try:
                        time_ms = float(line.split('time=')[1].split()[0])
                        times.append(time_ms)
                    except:
                        continue
            
            if times:
                return {
                    'host': host,
                    'packets_sent': count,
                    'packets_received': len(times),
                    'packet_loss': (count - len(times)) / count * 100,
                    'min_ms': min(times),
                    'max_ms': max(times),
                    'avg_ms': statistics.mean(times),
                    'std_ms': statistics.stdev(times) if len(times) > 1 else 0,
                    'median_ms': statistics.median(times)
                }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def traceroute(host: str) -> List[Dict]:
        """Trace route to host"""
        try:
            result = subprocess.run(
                ['traceroute', '-m', 30, host],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            hops = []
            for line in result.stdout.split('\n')[1:]:
                parts = line.strip().split()
                if parts and parts[0].isdigit():
                    try:
                        hop_num = int(parts[0])
                        times = [float(t) for t in parts[1:] if t != '*' and t.replace('.','').isdigit()]
                        
                        hops.append({
                            'hop': hop_num,
                            'ip': parts[1] if len(parts) > 1 else '*',
                            'avg_ms': statistics.mean(times) if times else None,
                            'times': times
                        })
                    except:
                        continue
            
            return hops
        except Exception as e:
            return [{'error': str(e)}]
    
    @staticmethod
    def http_latency(url: str, repeats: int = 5) -> Dict:
        """Measure HTTP request latency"""
        import requests
        
        measurements = []
        
        for _ in range(repeats):
            start = time.time()
            try:
                response = requests.get(url, timeout=10)
                end = time.time()
                
                measurements.append({
                    'latency_ms': (end - start) * 1000,
                    'status': response.status_code,
                    'success': response.ok
                })
            except Exception as e:
                measurements.append({
                    'latency_ms': None,
                    'error': str(e),
                    'success': False
                })
        
        valid = [m['latency_ms'] for m in measurements if m['success']]
        
        return {
            'url': url,
            'total_requests': repeats,
            'successful': len(valid),
            'min_ms': min(valid) if valid else None,
            'max_ms': max(valid) if valid else None,
            'avg_ms': statistics.mean(valid) if valid else None,
            'median_ms': statistics.median(valid) if valid else None,
            'p95_ms': sorted(valid)[int(len(valid) * 0.95)] if len(valid) >= 20 else None,
            'p99_ms': sorted(valid)[int(len(valid) * 0.99)] if len(valid) >= 100 else None
        }


class LatencyMonitor:
    """Continuous latency monitoring"""
    
    def __init__(self, interval_seconds: float = 1.0):
        self.interval = interval_seconds
        self.measurements: List[LatencyMeasurement] = []
    
    def measure_latency(self, host: str = 'google.com', port: int = 80) -> LatencyMeasurement:
        """Measure TCP connection latency"""
        start = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            sock.close()
            
            end = time.time()
            return LatencyMeasurement(
                timestamp=end=(end - start) * 100,
                latency_ms0,
                success=True
            )
        except Exception as e:
            return LatencyMeasurement(
                timestamp=time.time(),
                latency_ms=0,
                success=False,
                error=str(e)
            )
    
    def run_monitoring(self, duration_seconds: int, host: str = 'google.com'):
        """Run monitoring for specified duration"""
        import threading
        
        def measure_loop():
            end_time = time.time() + duration_seconds
            
            while time.time() < end_time:
                measurement = self.measure_latency(host)
                self.measurements.append(measurement)
                time.sleep(self.interval)
        
        thread = threading.Thread(target=measure_loop)
        thread.start()
        thread.join()
        
        return self.get_statistics()
    
    def get_statistics(self) -> Dict:
        """Calculate statistics from measurements"""
        valid = [m.latency_ms for m in self.measurements if m.success]
        
        if not valid:
            return {'error': 'No successful measurements'}
        
        sorted_vals = sorted(valid)
        
        return {
            'count': len(valid),
            'min_ms': min(valid),
            'max_ms': max(valid),
            'mean_ms': statistics.mean(valid),
            'median_ms': statistics.median(valid),
            'std_ms': statistics.stdev(valid) if len(valid) > 1 else 0,
            'p95_ms': sorted_vals[int(len(valid) * 0.95)],
            'p99_ms': sorted_vals[int(len(valid) * 0.99)],
            'p999_ms': sorted_vals[int(len(valid) * 0.999)] if len(valid) >= 1000 else None,
            'jitter_ms': statistics.stdev(valid) if len(valid) > 1 else 0
        }
```

-----

## Latency Optimization

### Connection Management

```python
import httpx
import aiohttp
import asyncio

class ConnectionPool:
    """Optimized HTTP connection pool"""
    
    def __init__(self, max_connections: int = 100):
        self.max_connections = max_connections
        self.session = None
    
    def create_session(self):
        """Create optimized HTTP session"""
        # Use connection pooling
        adapter = httpx.HTTPAdapter(
            pool_maxsize=self.max_connections,
            pool_connections=10,
            max_keepalive_connections=20,
            keepalive_expiry=30.0
        )
        
        self.session = httpx.Client(adapters=[adapter])
        return self.session
    
    def enable_http2(self):
        """Enable HTTP/2 for multiplexing"""
        adapter = httpx.HTTPAdapter(
            pool_maxsize=self.max_connections,
            http2=True  # Enable HTTP/2
        )
        self.session = httpx.Client(adapters=[adapter])
        return self.session


class AsyncLatencyOptimizer:
    """Async optimization for reduced latency"""
    
    @staticmethod
    async def parallel_requests(urls: List[str]) -> List[Dict]:
        """Execute requests in parallel"""
        async with aiohttp.ClientSession() as session:
            tasks = [session.get(url) for url in urls]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            results = []
            for url, resp in zip(urls, responses):
                if isinstance(resp, Exception):
                    results.append({'url': url, 'error': str(resp)})
                else:
                    results.append({
                        'url': url,
                        'status': resp.status,
                        'ok': resp.ok
                    })
            
            return results
    
    @staticmethod
    async def request_batching(urls: List[str], batch_size: int = 10) -> List[Dict]:
        """Batch requests with concurrency limit"""
        results = []
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            batch_results = await AsyncLatencyOptimizer.parallel_requests(batch)
            results.extend(batch_results)
        
        return results
```

### Caching Strategies

```python
from functools import lru_cache
import hashlib
import json
from typing import Any, Optional

class LatencyCache:
    """Caching to reduce latency"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.cache = {}
        self.timestamps = {}
    
    def _generate_key(self, key: str) -> str:
        """Generate cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        cache_key = self._generate_key(key)
        
        if cache_key in self.cache:
            # Check TTL
            if time.time() - self.timestamps[cache_key] < self.ttl:
                return self.cache[cache_key]
            else:
                # Expired
                del self.cache[cache_key]
                del self.timestamps[cache_key]
        
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        cache_key = self._generate_key(key)
        self.cache[cache_key] = value
        self.timestamps[cache_key] = time.time()
    
    def invalidate(self, key: str):
        """Invalidate cache entry"""
        cache_key = self._generate_key(key)
        if cache_key in self.cache:
            del self.cache[cache_key]
            del self.timestamps[cache_key]


class RedisCache:
    """Redis-based distributed cache"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get_cached(self, key: str) -> Optional[str]:
        """Get from Redis"""
        try:
            return await self.redis.get(key)
        except:
            return None
    
    async def set_cached(self, key: str, value: str, ttl: int = 300):
        """Set in Redis with TTL"""
        try:
            await self.redis.setex(key, ttl, value)
        except:
            pass
    
    async def cache_result(self, key: str, value: Any, ttl: int = 300):
        """Cache function result"""
        serialized = json.dumps(value)
        await self.set_cached(key, serialized, ttl)
```

### Content Delivery Networks

```python
class CDNOptimizer:
    """CDN configuration for latency optimization"""
    
    @staticmethod
    def configure_cdn_headers(headers: dict) -> dict:
        """Configure optimal CDN headers"""
        # Cache-Control for CDN
        cdn_headers = {
            'Cache-Control': 'public, max-age=3600, s-maxage=86400',
            'CDN-Cache-Control': 'max-age=86400',
            'Surrogate-Control': 'max-age=86400'
        }
        
        # Compression
        cdn_headers['Accept-Encoding'] = 'gzip, deflate, br'
        
        headers.update(cdn_headers)
        return headers
    
    @staticmethod
    def calculate_optimal_ttl(file_type: str, file_size: int) -> int:
        """Calculate optimal TTL based on content type"""
        ttl_map = {
            'static': 31536000,      # 1 year
            'css': 2592000,          # 30 days
            'javascript': 2592000,  # 30 days
            'image': 604800,         # 7 days
            'api': 0,                # Don't cache
            'html': 3600             # 1 hour
        }
        
        # Adjust based on size
        base_ttl = ttl_map.get(file_type, 3600)
        
        if file_size > 1024 * 1024:  # > 1MB
            base_ttl = int(base_ttl * 1.5)
        
        return base_ttl
```

-----

## Real-Time Latency Optimization

### WebSocket Optimization

```python
import websockets
import asyncio
from collections import deque

class LatencyOptimizedWebSocket:
    """Optimized WebSocket for low latency"""
    
    def __init__(self, max_queue_size: int = 100):
        self.send_queue = deque(maxlen=max_queue_size)
        self.receive_queue = deque(maxlen=max_queue_size)
        self.last_latency = 0
    
    async def send_optimized(self, websocket, message: str):
        """Send with latency tracking"""
        send_time = time.time()
        
        try:
            await websocket.send(message)
            return {'success': True, 'send_time': send_time}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def receive_with_latency(self, websocket) -> Dict:
        """Receive with latency measurement"""
        receive_time = time.time()
        
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            return {
                'success': True,
                'message': message,
                'receive_time': receive_time
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def enable_permessage_deflate(websocket):
        """Enable compression for lower bandwidth/latency"""
        # In websockets library, compression is enabled via parameters
        return websocket


class MessageBatching:
    """Batch messages for throughput optimization"""
    
    def __init__(self, batch_size: int = 10, max_wait_ms: float = 50):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.batch = []
        self.last_send = time.time()
    
    def add_message(self, message: Any) -> List[Any]:
        """Add message to batch, return completed batches"""
        self.batch.append(message)
        
        now = time.time()
        time_elapsed = (now - self.last_send) * 1000
        
        # Check if batch is full or wait time exceeded
        if len(self.batch) >= self.batch_size or time_elapsed >= self.max_wait_ms:
            batch_to_send = self.batch.copy()
            self.batch = []
            self.last_send = now
            return batch_to_send
        
        return []
```

-----

## Performance Targets

### Latency Budgets by Application

| Application | Target Latency | P99 Target | Notes |
|-------------|----------------|------------|-------|
| **Web (First Paint)** | < 1.5s | < 3s | Above fold visible |
| **Web (Interactive)** | < 3s | < 5s | Page fully interactive |
| **API (Simple)** | < 50ms | < 200ms | Single DB query |
| **API (Complex)** | < 200ms | < 500ms | Multiple services |
| **Database Query** | < 10ms | < 100ms | Indexed query |
| **Real-time (Gaming)** | < 50ms | < 100ms | Round trip |
| **Real-time (Trading)** | < 1ms | < 5ms | HFT systems |
| **VoIP** | < 150ms | < 300ms | Acceptable quality |
| **Video Streaming** | < 2s (start) | < 5s | Buffer to start |
| **CDN Access** | < 20ms | < 100ms | Cache hit |

```python
class LatencyBudget:
    """Manage latency budgets for applications"""
    
    def __init__(self, budget_ms: float):
        self.budget_ms = budget_ms
        self.components = {}
    
    def add_component(self, name: str, budget_ms: float):
        """Add component budget"""
        self.components[name] = budget_ms
    
    def check_budget(self, actual_ms: float) -> Dict:
        """Check if within budget"""
        return {
            'within_budget': actual_ms <= self.budget_ms,
            'budget_ms': self.budget_ms,
            'actual_ms': actual_ms,
            'headroom_ms': self.budget_ms - actual_ms,
            'utilization_pct': (actual_ms / self.budget_ms) * 100
        }
    
    def allocate_components(self, allocations: Dict[str, float]) -> Dict:
        """Allocate budget across components"""
        total_allocated = sum(allocations.values())
        
        if total_allocated > self.budget_ms:
            return {'error': 'Allocation exceeds budget'}
        
        return {
            'allocations': allocations,
            'total_allocated_ms': total_allocated,
            'remaining_ms': self.budget_ms - total_allocated,
            'utilization_pct': (total_allocated / self.budget_ms) * 100
        }
    
    @staticmethod
    def typical_web_request() -> 'LatencyBudget':
        """Typical web request latency budget"""
        budget = LatencyBudget(budget_ms=1000)
        
        budget.add_component('DNS', 50)
        budget.add_component('TCP Connect', 50)
        budget.add_component('TLS Handshake', 100)
        budget.add_component('Server Processing', 200)
        budget.add_component('Database Query', 150)
        budget.add_component('Response Transfer', 300)
        budget.add_component('Client Processing', 100)
        
        return budget
```

### Monitoring and Alerting

```python
class LatencyAlerting:
    """Latency monitoring and alerting"""
    
    def __init__(self, warning_threshold_ms: float, critical_threshold_ms: float):
        self.warning = warning_threshold_ms
        self.critical = critical_threshold_ms
        self.violations = []
    
    def check_latency(self, latency_ms: float, timestamp: float = None) -> Dict:
        """Check latency against thresholds"""
        if timestamp is None:
            timestamp = time.time()
        
        if latency_ms >= self.critical:
            level = 'critical'
            violation = True
        elif latency_ms >= self.warning:
            level = 'warning'
            violation = True
        else:
            level = 'ok'
            violation = False
        
        if violation:
            self.violations.append({
                'timestamp': timestamp,
                'latency_ms': latency_ms,
                'level': level
            })
        
        return {
            'latency_ms': latency_ms,
            'level': level,
            'warning_threshold': self.warning,
            'critical_threshold': self.critical
        }
    
    def get_violation_summary(self) -> Dict:
        """Get summary of violations"""
        if not self.violations:
            return {'total': 0}
        
        warnings = sum(1 for v in self.violations if v['level'] == 'warning')
        criticals = sum(1 for v in self.violations if v['level'] == 'critical')
        
        return {
            'total': len(self.violations),
            'warnings': warnings,
            'critical': criticals,
            'violation_rate_pct': len(self.violations) / 100  # Per 100 requests
        }
```
