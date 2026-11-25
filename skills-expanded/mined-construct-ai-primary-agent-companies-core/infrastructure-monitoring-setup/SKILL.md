---
name: infrastructure-monitoring-setup
description: >
  Use this skill when the task involves setting up monitoring and alerting for cloud deployments,
  configuring health checks, implementing logging systems, or establishing performance monitoring
  for infrastructure components.
  
  Use when: Deployment monitoring needs setup; health checks require configuration; logging systems
  need implementation; performance metrics need collection; alerting for infrastructure issues is needed;
  uptime monitoring and incident response require setup.
  
  Don't use when: The task is about deployment verification (use deployment-verification-testing instead);
  the task requires network tunneling (use network-tunneling-configuration instead).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Infrastructure Monitoring Setup Skill

## Overview

The Infrastructure Monitoring Setup skill enables the Render Deployment Specialist agent to configure comprehensive monitoring, logging, and alerting systems for cloud deployments. This skill covers health checks, performance monitoring, log aggregation, incident alerting, and infrastructure observability.

## Capabilities

### Health Check Configuration
- **Application Health**: Configure application-specific health endpoints
- **Dependency Checks**: Monitor database, cache, and external service health
- **Custom Metrics**: Set up custom health check logic and thresholds
- **Automated Recovery**: Implement self-healing mechanisms

### Logging and Observability
- **Log Aggregation**: Set up centralized log collection and storage
- **Structured Logging**: Implement structured logging with proper levels
- **Log Analysis**: Configure log parsing and anomaly detection
- **Distributed Tracing**: Set up request tracing across services

### Performance Monitoring
- **Metrics Collection**: Configure system and application metrics
- **Performance Thresholds**: Set up performance alerts and warnings
- **Resource Monitoring**: Monitor CPU, memory, disk, and network usage
- **Scalability Metrics**: Track auto-scaling triggers and performance

### Alerting and Incident Response
- **Alert Configuration**: Set up multi-channel alerting (email, Slack, SMS)
- **Escalation Policies**: Configure alert escalation and on-call rotation
- **Incident Response**: Implement automated incident response workflows
- **Post-Mortem Analysis**: Set up incident analysis and reporting

## Common Patterns

### Comprehensive Health Check Setup
```python
# health_check.py - Comprehensive health check endpoint
from flask import Flask, jsonify
import psycopg2
import redis
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

class HealthChecker:
    def __init__(self):
        self.checks = {}
        self.last_check_time = None
        self.check_interval = 30  # seconds

    def add_check(self, name, check_function, critical=True):
        """Add a health check function"""
        self.checks[name] = {
            'function': check_function,
            'critical': critical,
            'last_result': None,
            'last_check': None
        }

    async def run_checks(self):
        """Run all health checks"""
        current_time = datetime.utcnow()
        results = {
            'status': 'healthy',
            'timestamp': current_time.isoformat(),
            'checks': {},
            'version': '1.0.0'
        }

        all_passed = True

        for name, check_info in self.checks.items():
            try:
                # Run the check
                start_time = time.time()
                result = await check_info['function']()
                duration = time.time() - start_time

                check_info['last_result'] = result
                check_info['last_check'] = current_time

                results['checks'][name] = {
                    'status': 'healthy' if result['status'] == 'ok' else 'unhealthy',
                    'response_time': f"{duration:.3f}s",
                    'details': result.get('details', {}),
                    'timestamp': current_time.isoformat()
                }

                if result['status'] != 'ok' and check_info['critical']:
                    all_passed = False
                    results['status'] = 'unhealthy'

            except Exception as e:
                results['checks'][name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': current_time.isoformat()
                }

                if check_info['critical']:
                    all_passed = False
                    results['status'] = 'unhealthy'

        if all_passed:
            results['status'] = 'healthy'

        self.last_check_time = current_time
        return results

# Initialize health checker
health_checker = HealthChecker()

# Database health check
async def check_database():
    """Check database connectivity and performance"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            connect_timeout=5
        )

        # Test query execution time
        start_time = time.time()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        query_time = time.time() - start_time

        # Check connection count
        with conn.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM pg_stat_activity")
            connection_count = cursor.fetchone()[0]

        conn.close()

        return {
            'status': 'ok',
            'details': {
                'query_time': f"{query_time:.3f}s",
                'connection_count': connection_count,
                'max_connections': int(os.getenv('DATABASE_MAX_CONNECTIONS', 100))
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'details': {
                'error': str(e)
            }
        }

# Redis health check
async def check_redis():
    """Check Redis connectivity and performance"""
    try:
        r = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            password=os.getenv('REDIS_PASSWORD'),
            socket_connect_timeout=5
        )

        # Test basic operations
        start_time = time.time()
        r.ping()
        r.set('health_check', 'ok', ex=60)
        r.get('health_check')
        r.delete('health_check')
        operation_time = time.time() - start_time

        # Get Redis info
        info = r.info()

        return {
            'status': 'ok',
            'details': {
                'operation_time': f"{operation_time:.3f}s",
                'connected_clients': info.get('connected_clients', 0),
                'used_memory': info.get('used_memory_human', 'unknown'),
                'uptime_days': info.get('uptime_in_days', 0)
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'details': {
                'error': str(e)
            }
        }

# External service health check
async def check_external_services():
    """Check external API dependencies"""
    services = [
        {'name': 'OpenRouter', 'url': 'https://openrouter.ai/api/v1/models', 'timeout': 10},
        {'name': 'GitHub', 'url': 'https://api.github.com/zen', 'timeout': 5},
    ]

    results = {}

    for service in services:
        try:
            start_time = time.time()
            response = requests.get(service['url'], timeout=service['timeout'])
            response_time = time.time() - start_time

            results[service['name']] = {
                'status': 'ok' if response.status_code < 400 else 'error',
                'response_time': f"{response_time:.3f}s",
                'status_code': response.status_code
            }

        except Exception as e:
            results[service['name']] = {
                'status': 'error',
                'error': str(e)
            }

    # Check if all services are healthy
    all_healthy = all(result['status'] == 'ok' for result in results.values())

    return {
        'status': 'ok' if all_healthy else 'degraded',
        'details': results
    }

# Application health check
async def check_application():
    """Check application-specific health"""
    try:
        # Check memory usage
        import psutil
        memory = psutil.virtual_memory()
        memory_usage_percent = memory.percent

        # Check disk usage
        disk = psutil.disk_usage('/')
        disk_usage_percent = disk.percent

        # Check if critical processes are running
        critical_processes = ['hermes', 'worker']
        running_processes = []

        for proc in psutil.process_iter(['pid', 'name']):
            proc_name = proc.info['name'].lower()
            for critical in critical_processes:
                if critical in proc_name:
                    running_processes.append(proc_name)

        return {
            'status': 'ok',
            'details': {
                'memory_usage': f"{memory_usage_percent:.1f}%",
                'disk_usage': f"{disk_usage_percent:.1f}%",
                'running_processes': running_processes,
                'uptime': f"{time.time() - psutil.boot_time():.0f}s"
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'details': {
                'error': str(e)
            }
        }

# Register health checks
health_checker.add_check('database', check_database, critical=True)
health_checker.add_check('redis', check_redis, critical=False)
health_checker.add_check('external_services', check_external_services, critical=False)
health_checker.add_check('application', check_application, critical=True)

@app.route('/health')
async def health():
    """Health check endpoint"""
    results = await health_checker.run_checks()
    status_code = 200 if results['status'] == 'healthy' else 503

    return jsonify(results), status_code

@app.route('/health/live')
async def liveness():
    """Kubernetes liveness probe"""
    return jsonify({'status': 'alive'}), 200

@app.route('/health/ready')
async def readiness():
    """Kubernetes readiness probe"""
    # Check if application is ready to serve requests
    results = await health_checker.run_checks()
    status_code = 200 if results['status'] in ['healthy', 'degraded'] else 503

    return jsonify({'status': 'ready' if status_code == 200 else 'not ready'}), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
```

### Structured Logging Configuration
```python
# logging_config.py - Structured logging setup
import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class StructuredLogger:
    def __init__(self, service_name, version="1.0.0"):
        self.service_name = service_name
        self.version = version
        self.setup_logging()

    def setup_logging(self):
        """Configure structured JSON logging"""

        # Create logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Create JSON formatter
        formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        )

        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler for production
        if not os.getenv('FLASK_ENV') == 'development':
            file_handler = logging.FileHandler('/var/log/paperclip/app.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Set up specific loggers
        self.setup_module_loggers()

    def setup_module_loggers(self):
        """Configure loggers for different modules"""
        # Database logger
        db_logger = logging.getLogger('database')
        db_logger.setLevel(logging.INFO)

        # API logger
        api_logger = logging.getLogger('api')
        api_logger.setLevel(logging.INFO)

        # Hermes logger
        hermes_logger = logging.getLogger('hermes')
        hermes_logger.setLevel(logging.INFO)

    def get_logger(self, name):
        """Get a configured logger"""
        return logging.getLogger(name)

# Custom log filter for sensitive data
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        # Remove sensitive information from logs
        if hasattr(record, 'message'):
            message = record.getMessage()

            # Remove API keys
            import re
            message = re.sub(r'pcak_[a-zA-Z0-9_]+', '[API_KEY_REDACTED]', message)
            message = re.sub(r'sk-[a-zA-Z0-9-]+', '[OPENROUTER_KEY_REDACTED]', message)

            # Remove passwords
            message = re.sub(r'password["\']?\s*[:=]\s*["\'][^"\']+["\']', 'password=[REDACTED]', message)

            record.message = message

        return True

# Request logging middleware
class RequestLogger:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger

    def __call__(self, environ, start_response):
        # Log incoming request
        method = environ.get('REQUEST_METHOD', 'UNKNOWN')
        path = environ.get('PATH_INFO', '/')
        query = environ.get('QUERY_STRING', '')
        remote_addr = environ.get('REMOTE_ADDR', 'unknown')

        self.logger.info(f"Incoming request: {method} {path}",
                        extra={
                            'method': method,
                            'path': path,
                            'query': query,
                            'remote_addr': remote_addr,
                            'user_agent': environ.get('HTTP_USER_AGENT', ''),
                            'request_id': environ.get('HTTP_X_REQUEST_ID', 'unknown')
                        })

        # Wrap start_response to log response
        def logged_start_response(status, headers, exc_info=None):
            status_code = int(status.split()[0])

            self.logger.info(f"Response: {status_code}",
                           extra={
                               'status_code': status_code,
                               'method': method,
                               'path': path,
                               'response_time': getattr(self, '_start_time', 0)
                           })

            return start_response(status, headers, exc_info)

        # Record start time
        import time
        self._start_time = time.time()

        return self.app(environ, logged_start_response)

# Error logging
def log_error(error, context=None):
    """Log application errors with context"""
    logger = logging.getLogger('error')

    error_data = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'stack_trace': traceback.format_exc(),
        'context': context or {},
        'timestamp': datetime.utcnow().isoformat()
    }

    logger.error("Application error occurred",
                extra=error_data,
                exc_info=True)

# Performance monitoring
class PerformanceMonitor:
    def __init__(self, logger):
        self.logger = logger

    def monitor_function(self, func):
        """Decorator to monitor function performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                self.logger.info(f"Function {func.__name__} executed",
                               extra={
                                   'function': func.__name__,
                                   'execution_time': execution_time,
                                   'status': 'success'
                               })

                return result

            except Exception as e:
                execution_time = time.time() - start_time

                self.logger.error(f"Function {func.__name__} failed",
                                extra={
                                    'function': func.__name__,
                                    'execution_time': execution_time,
                                    'status': 'error',
                                    'error': str(e)
                                })

                raise

        return wrapper

# Usage
structured_logger = StructuredLogger('paperclip-app', '1.0.0')
logger = structured_logger.get_logger('app')

# Add sensitive data filter
sensitive_filter = SensitiveDataFilter()
logging.getLogger().addFilter(sensitive_filter)

# Performance monitoring
perf_monitor = PerformanceMonitor(logger)

@perf_monitor.monitor_function
def process_request(request_data):
    # Simulate request processing
    time.sleep(0.1)
    return {"status": "processed"}

# Error handling
try:
    result = process_request({"data": "test"})
    logger.info("Request processed successfully", extra={'result': result})
except Exception as e:
    log_error(e, {'request_data': {"data": "test"}})
```

### Alerting and Incident Response
```python
# alerting.py - Alerting and incident response system
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import time
from datetime import datetime, timedelta
from enum import Enum

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertChannel(Enum):
    EMAIL = "email"
    SLACK = "slack"
    SMS = "sms"
    WEBHOOK = "webhook"

class AlertManager:
    def __init__(self):
        self.alerts = {}
        self.channels = {}
        self.escalation_policies = {}
        self.setup_channels()

    def setup_channels(self):
        """Configure alert channels"""
        # Email configuration
        self.channels[AlertChannel.EMAIL] = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('ALERT_FROM_EMAIL', 'alerts@paperclip.com')
        }

        # Slack configuration
        self.channels[AlertChannel.SLACK] = {
            'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
            'channel': os.getenv('SLACK_CHANNEL', '#alerts')
        }

        # SMS configuration (using Twilio)
        self.channels[AlertChannel.SMS] = {
            'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
            'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
            'from_number': os.getenv('TWILIO_FROM_NUMBER')
        }

    def send_alert(self, title, message, severity=AlertSeverity.MEDIUM, channels=None):
        """Send an alert through configured channels"""
        if channels is None:
            channels = [AlertChannel.EMAIL, AlertChannel.SLACK]

        alert_id = f"alert_{int(time.time())}_{hash(title) % 1000}"

        alert_data = {
            'id': alert_id,
            'title': title,
            'message': message,
            'severity': severity.value,
            'timestamp': datetime.utcnow().isoformat(),
            'channels': [channel.value for channel in channels]
        }

        # Store alert
        self.alerts[alert_id] = alert_data

        # Send through each channel
        for channel in channels:
            try:
                self._send_to_channel(channel, alert_data)
            except Exception as e:
                print(f"Failed to send alert to {channel.value}: {e}")

        # Apply escalation policy
        self._apply_escalation_policy(alert_data)

        return alert_id

    def _send_to_channel(self, channel, alert_data):
        """Send alert to specific channel"""
        if channel == AlertChannel.EMAIL:
            self._send_email_alert(alert_data)
        elif channel == AlertChannel.SLACK:
            self._send_slack_alert(alert_data)
        elif channel == AlertChannel.SMS:
            self._send_sms_alert(alert_data)
        elif channel == AlertChannel.WEBHOOK:
            self._send_webhook_alert(alert_data)

    def _send_email_alert(self, alert_data):
        """Send email alert"""
        config = self.channels[AlertChannel.EMAIL]

        msg = MIMEMultipart()
        msg['From'] = config['from_email']
        msg['To'] = os.getenv('ALERT_EMAIL_RECIPIENTS', 'admin@paperclip.com')
        msg['Subject'] = f"[{alert_data['severity'].upper()}] {alert_data['title']}"

        body = f"""
Alert Details:
- Title: {alert_data['title']}
- Severity: {alert_data['severity']}
- Time: {alert_data['timestamp']}

Message:
{alert_data['message']}

Alert ID: {alert_data['id']}
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        server.send_message(msg)
        server.quit()

    def _send_slack_alert(self, alert_data):
        """Send Slack alert"""
        config = self.channels[AlertChannel.SLACK]

        color = {
            'low': 'good',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'danger'
        }.get(alert_data['severity'], 'warning')

        payload = {
            'channel': config['channel'],
            'attachments': [{
                'color': color,
                'title': alert_data['title'],
                'text': alert_data['message'],
                'fields': [
                    {
                        'title': 'Severity',
                        'value': alert_data['severity'],
                        'short': True
                    },
                    {
                        'title': 'Time',
                        'value': alert_data['timestamp'],
                        'short': True
                    }
                ],
                'footer': f"Alert ID: {alert_data['id']}"
            }]
        }

        requests.post(config['webhook_url'], json=payload)

    def _send_sms_alert(self, alert_data):
        """Send SMS alert (using Twilio)"""
        config = self.channels[AlertChannel.SMS]

        from twilio.rest import Client
        client = Client(config['account_sid'], config['auth_token'])

        to_numbers = os.getenv('SMS_ALERT_RECIPIENTS', '').split(',')

        message_body = f"ALERT [{alert_data['severity'].upper()}]: {alert_data['title']} - {alert_data['message'][:100]}..."

        for number in to_numbers:
            if number.strip():
                client.messages.create(
                    body=message_body,
                    from_=config['from_number'],
                    to=number.strip()
                )

    def _send_webhook_alert(self, alert_data):
        """Send webhook alert"""
        webhook_urls = os.getenv('ALERT_WEBHOOK_URLS', '').split(',')

        for url in webhook_urls:
            if url.strip():
                requests.post(url.strip(), json=alert_data, timeout=10)

    def _apply_escalation_policy(self, alert_data):
        """Apply escalation policy based on severity"""
        severity = alert_data['severity']

        if severity in ['high', 'critical']:
            # Escalate immediately
            self._escalate_alert(alert_data)
        elif severity == 'medium':
            # Escalate after 15 minutes if not resolved
            time.sleep(900)  # 15 minutes
            if alert_data['id'] in self.alerts:  # Still active
                self._escalate_alert(alert_data)

    def _escalate_alert(self, alert_data):
        """Escalate alert to higher priority channels"""
        escalation_channels = [AlertChannel.SMS, AlertChannel.SLACK]

        for channel in escalation_channels:
            if channel not in [AlertChannel(c) for c in alert_data.get('channels', [])]:
                try:
                    self._send_to_channel(channel, {
                        **alert_data,
                        'title': f"ESCALATED: {alert_data['title']}",
                        'escalated': True
                    })
                except Exception as e:
                    print(f"Failed to escalate alert to {channel.value}: {e}")

    def resolve_alert(self, alert_id, resolution_notes=""):
        """Resolve an active alert"""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            alert['resolved_at'] = datetime.utcnow().isoformat()
            alert['resolution_notes'] = resolution_notes
            alert['status'] = 'resolved'

            # Send resolution notification
            self.send_alert(
                f"RESOLVED: {alert['title']}",
                f"Alert has been resolved.\n\nResolution: {resolution_notes}",
                AlertSeverity.LOW,
                [AlertChannel.SLACK]
            )

# Usage
alert_manager = AlertManager()

# Send alerts based on monitoring
def check_system_health():
    # Simulate health checks
    issues = []

    # Check database connections
    if get_db_connection_count() > 80:  # 80% of max connections
        issues.append(("Database connection pool near capacity",
                      AlertSeverity.HIGH))

    # Check response times
    avg_response_time = get_average_response_time()
    if avg_response_time > 5.0:  # 5 seconds
        issues.append((f"High response time: {avg_response_time:.2f}s",
                      AlertSeverity.MEDIUM))

    # Check error rates
    error_rate = get_error_rate_percentage()
    if error_rate > 5.0:  # 5% error rate
        issues.append((f"High error rate: {error_rate:.1f}%",
                      AlertSeverity.HIGH))

    # Send alerts for issues
    for message, severity in issues:
        alert_manager.send_alert(
            "System Health Alert",
            message,
            severity
        )

# Periodic health checking
def start_monitoring():
    while True:
        check_system_health()
        time.sleep(300)  # Check every 5 minutes

# Example alert triggers
alert_manager.send_alert(
    "Database Connection Issue",
    "Database connection pool is at 95% capacity. Consider scaling.",
    AlertSeverity.HIGH
)

alert_manager.send_alert(
    "Deployment Failed",
    "Latest deployment to production failed with exit code 1.",
    AlertSeverity.CRITICAL
)
```

### Metrics Collection and Visualization
```python
# metrics.py - Metrics collection and visualization
import time
import psutil
import threading
from collections import deque
import json
from datetime import datetime, timedelta

class MetricsCollector:
    def __init__(self, retention_period_minutes=60):
        self.metrics = {}
        self.retention_period = timedelta(minutes=retention_period_minutes)
        self.lock = threading.Lock()

        # Start background collection
        self.collection_thread = threading.Thread(target=self._collect_metrics_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()

    def _collect_metrics_loop(self):
        """Background metrics collection"""
        while True:
            self._collect_system_metrics()
            self._collect_application_metrics()
            time.sleep(60)  # Collect every minute

    def _collect_system_metrics(self):
        """Collect system-level metrics"""
        timestamp = datetime.utcnow()

        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self._add_metric('system.cpu.percent', cpu_percent, timestamp)

        # Memory metrics
        memory = psutil.virtual_memory()
        self._add_metric('system.memory.percent', memory.percent, timestamp)
        self._add_metric('system.memory.used_bytes', memory.used, timestamp)
        self._add_metric('system.memory.available_bytes', memory.available, timestamp)

        # Disk metrics
        disk = psutil.disk_usage('/')
        self._add_metric('system.disk.percent', disk.percent, timestamp)
        self._add_metric('system.disk.used_bytes', disk.used, timestamp)
        self._add_metric('system.disk.free_bytes', disk.free, timestamp)

        # Network metrics
        network = psutil.net_io_counters()
        self._add_metric('system.network.bytes_sent', network.bytes_sent, timestamp)
        self._add_metric('system.network.bytes_recv', network.bytes_recv, timestamp)

    def _collect_application_metrics(self):
        """Collect application-specific metrics"""
        timestamp = datetime.utcnow()

        # Request metrics (would be populated by middleware)
        # These would be updated by request handlers
        self._add_metric('app.requests.total', getattr(self, 'request_count', 0), timestamp)
        self._add_metric('app.requests.errors', getattr(self, 'error_count', 0), timestamp)

        # Database metrics
        db_connection_count = get_db_connection_count()
        self._add_metric('app.database.connections', db_connection_count, timestamp)

        # Queue metrics
        queue_size = get_queue_size()
        self._add_metric('app.queue.size', queue_size, timestamp)

    def _add_metric(self, name, value, timestamp):
        """Add a metric data point"""
        with self.lock:
            if name not in self.metrics:
                self.metrics[name] = deque()

            # Add new data point
            self.metrics[name].append({
                'timestamp': timestamp,
                'value': value
            })

            # Remove old data points
            cutoff_time = datetime.utcnow() - self.retention_period
            while self.metrics[name] and self.metrics[name][0]['timestamp'] < cutoff_time:
                self.metrics[name].popleft()

    def get_metric(self, name, start_time=None, end_time=None):
        """Get metric data points"""
        with self.lock:
            if name not in self.metrics:
                return []

            data = list(self.metrics[name])

            # Filter by time range
            if start_time:
                data = [d for d in data if d['timestamp'] >= start_time]
            if end_time:
                data = [d for d in data if d['timestamp'] <= end_time]

            return data

    def get_metric_stats(self, name, hours=1):
        """Get metric statistics for the last N hours"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        data = self.get_metric(name, start_time, end_time)

        if not data:
            return None

        values = [d['value'] for d in data]

        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'current': values[-1] if values else None,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        }

    def export_metrics(self, format='json'):
        """Export all metrics"""
        with self.lock:
            if format == 'json':
                return json.dumps({
                    name: list(data) for name, data in self.metrics.items()
                }, default=str, indent=2)

            elif format == 'prometheus':
                lines = []
                for name, data in self.metrics.items():
                    if data:
                        # Convert metric name to Prometheus format
                        prom_name = name.replace('.', '_').replace('-', '_')
                        value = data[-1]['value']
                        timestamp = int(data[-1]['timestamp'].timestamp() * 1000)

                        lines.append(f'# HELP {prom_name} Metric {name}')
                        lines.append(f'# TYPE {prom_name} gauge')
                        lines.append(f'{prom_name} {value} {timestamp}')

                return '\n'.join(lines)

# Global metrics collector
metrics_collector = MetricsCollector()

# Middleware to track requests
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Track request
        metrics_collector._add_metric('app.requests.total',
                                    getattr(metrics_collector, 'request_count', 0) + 1,
                                    datetime.utcnow())

        def tracked_start_response(status, headers, exc_info=None):
            status_code = int(status.split()[0])

            # Track errors
            if status_code >= 400:
                metrics_collector._add_metric('app.requests.errors',
                                            getattr(metrics_collector, 'error_count', 0) + 1,
                                            datetime.utcnow())

            return start_response(status, headers, exc_info)

        return self.app(environ, tracked_start_response)

# Health check endpoint with metrics
@app.route('/metrics')
def get_metrics():
    """Prometheus-style metrics endpoint"""
    return metrics_collector.export_metrics('prometheus'), 200, {'Content-Type': 'text/plain'}

@app.route('/metrics/json')
def get_metrics_json():
    """JSON metrics endpoint"""
    return jsonify(json.loads(metrics_collector.export_metrics('json')))

# Example usage
def get_db_connection_count():
    """Get current database connection count"""
    # Implementation would query database
    return 15

def get_queue_size():
    """Get current queue size"""
    # Implementation would check queue
    return 5

def get_average_response_time():
    """Get average response time"""
    stats = metrics_collector.get_metric_stats('app.response_time', hours=1)
    return stats['avg'] if stats else 0

def get_error_rate_percentage():
    """Get error rate percentage"""
    request_stats = metrics_collector.get_metric_stats('app.requests.total', hours=1)
    error_stats = metrics_collector.get_metric_stats('app.requests.errors', hours=1)

    if request_stats and request_stats['count'] > 0:
        return (error_stats['count'] / request_stats['count']) * 100 if error_stats else 0
    return 0

# Example queries
def demonstrate_metrics():
    # Add some sample data
    for i in range(10):
        metrics_collector._add_metric('app.response_time', 0.1 + (i * 0.05), datetime.utcnow())
        time.sleep(0.1)

    # Get statistics
    cpu_stats = metrics_collector.get_metric_stats('system.cpu.percent', hours=1)
    response_stats = metrics_collector.get_metric_stats('app.response_time', hours=1)

    print("CPU Stats:", cpu_stats)
    print("Response Time Stats:", response_stats)

    # Export metrics
    prometheus_metrics = metrics_collector.export_metrics('prometheus')
    print("\nPrometheus Metrics:")
    print(prometheus_metrics[:500] + "..." if len(prometheus_metrics) > 500 else prometheus_metrics)

if __name__ == '__main__':
    demonstrate_metrics()
```

## Troubleshooting Common Issues

### Health Check Failures
1. **Timeout Issues**
   ```bash
   # Increase timeout in health check
   curl --max-time 60 https://your-app.onrender.com/health
   ```

2. **Dependency Failures**
   ```bash
   # Check individual dependencies
   curl https://your-app.onrender.com/health/database
   curl https://your-app.onrender.com/health/redis
   ```

3. **Resource Constraints**
   ```bash
   # Monitor resource usage
   docker stats
   top -p $(pgrep -f "python|node")
   ```

### Logging Issues
1. **Log Volume**
   ```bash
   # Reduce log verbosity
   export LOG_LEVEL=WARNING
   ```

2. **Log Rotation**
   ```bash
   # Set up log rotation
   logrotate -f /etc/logrotate.d/app
   ```

3. **Structured Logging**
   ```bash
   # Validate JSON log format
   tail -f /var/log/app.log | jq .
   ```

### Alerting Problems
1. **False Positives**
   ```bash
   # Adjust alert thresholds
   ALERT_CPU_THRESHOLD=90
   ALERT_MEMORY_THRESHOLD=85
   ```

2. **Alert Fatigue**
   ```bash
   # Implement alert deduplication
   # Group similar alerts
   ```

3. **Delivery Issues**
   ```bash
   # Test alert channels
   curl -X POST $SLACK_WEBHOOK_URL -d '{"text": "Test alert"}'
   ```

## Security Considerations

### Monitoring Security
- **Access Control**: Restrict access to monitoring endpoints
- **Data Encryption**: Encrypt monitoring data in transit and at rest
- **Audit Logging**: Log all monitoring access and configuration changes
- **Compliance**: Ensure monitoring complies with data protection regulations

### Alert Security
- **Alert Validation**: Validate alert sources and prevent alert injection
- **Secure Channels**: Use encrypted channels for alert delivery
- **Authentication**: Require authentication for alert management
- **Rate Limiting**: Implement rate limiting on alert endpoints

## Integration Points

### Internal InfraForge AI
- **Security Agent**: Coordinates monitoring security
- **Database Agent**: Provides database monitoring integration
- **Network Agent**: Integrates network monitoring

### Cross-Company Integration
- **DevForge AI**: Collaborates on application monitoring
- **PaperclipForge AI**: Works with project monitoring requirements
- **QualityForge AI**: Partners on monitoring validation

## Success Metrics

- **Uptime Monitoring**: ≥99.9% monitoring system availability
- **Alert Response**: <5 minutes average alert response time
- **False Positive Rate**: <5% false positive alerts
- **Incident Detection**: ≥95% incidents detected within 1 minute

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
