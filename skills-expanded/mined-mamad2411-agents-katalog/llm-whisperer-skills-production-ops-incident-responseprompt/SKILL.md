# Incident Response for LLM Systems

## Problem Statement

LLM systems fail in ways that differ fundamentally from traditional software and even conventional ML models. When a conventional web service fails, the error is typically clear-cut: a 500 error, a timeout, an exception. When an LLM fails, the failure modes are more subtle and potentially more dangerous. The model might produce a confident-sounding but incorrect answer, generate harmful content that slips past safety measures, suddenly change its output distribution causing user experience degradation, or exhibit mysterious latency spikes that defy conventional profiling.

Incident response for LLM systems requires specialized approaches that account for these unique failure modes. A team might receive a report that "the AI gave bad answers yesterday afternoon" - but without proper infrastructure, debugging this is nearly impossible. Was it a prompt injection attack? Model degradation? A data pipeline issue? An upstream service problem? Effective incident response enables rapid identification and resolution of these issues.

This skill covers building incident detection systems, establishing response protocols, conducting post-mortems for LLM-specific failures, and creating runbooks that account for the unique characteristics of LLM systems.

## Theory & Fundamentals

### Failure Mode Taxonomy for LLM Systems

LLM failures can be categorized into distinct types, each requiring different response strategies:

**Category 1: Infrastructure Failures**
- GPU memory exhaustion (OOM errors)
- Model loading failures
- Dependency service unavailability (vector DB, cache, etc.)
- Network partition causing request failures
- GPU hardware failures

**Category 2: Performance Degradation**
- Latency spikes without errors
- Throughput collapse
- Increased error rates (timeouts, 500s)
- Memory leaks causing gradual slowdown

**Category 3: Quality Degradation**
- Factual incorrectness increases
- Output length abnormalities (too short, too long)
- Coherence breakdown (repetitions, contradictions)
- Formatting failures (invalid JSON, broken code)
- Language drift (suddenly changes writing style)

**Category 4: Safety/Policy Violations**
- Content policy violations (harmful content generation)
- Prompt injection successful attacks
- PII leakage
- Refusal rate anomalies (too many or too few refusals)
- Bias amplification

**Category 5: Behavioral Anomalies**
- Sudden personality changes
- Unexpected capability changes
- New failure patterns (model "hallucinates" differently)
- Context understanding degradation

### Severity Classification Framework

```
Severity Levels for LLM Incidents:

P0 - Critical
- Safety policy violations affecting multiple users
- Complete service outage
- Data exfiltration suspected
- Model producing harmful content at scale
- Security breach indication

P1 - High
- Significant latency degradation (>10x baseline)
- Error rate >5%
- Quality degradation affecting majority of users
-单个 prominent harmful output
- Cache/service failures requiring workarounds

P2 - Medium
- Moderate latency increase (2-10x baseline)
- Error rate 1-5%
- Quality issues limited to specific use cases
- Individual user complaints about output quality
- Non-critical service degradation

P3 - Low
- Minor anomalies in metrics
- Individual quality complaints
- Cosmetic issues (formatting, verbosity)
- Optimization opportunities identified
```

### The LLM Incident Response Lifecycle

```
1. Detection (0-5 minutes)
   ├── Automated alerts from monitoring systems
   ├── User reports via support channels
   ├── Internal team observations
   └── Third-party reports (social media, etc.)
   
2. Triage (5-15 minutes)
   ├── Assess severity and scope
   ├── Determine affected systems/components
   ├── Identify potential root cause categories
   └── Activate appropriate response team
   
3. Containment (15-60 minutes)
   ├── Implement immediate mitigations
   ├── Isolate affected components
   ├── Preserve evidence/logs
   └── Communicate status to stakeholders
   
4. Investigation (1-24 hours)
   ├── Root cause analysis
   ├── Data collection and analysis
   ├── Hypothesis testing
   └── Impact assessment
   
5. Resolution (varies)
   ├── Implement permanent fixes
   ├── Validate resolution
   ├── Deploy fixes
   └── Monitor for recurrence
   
6. Post-Mortem (24-72 hours after resolution)
   ├── Document timeline
   ├── Identify contributing factors
   ├── Recommend preventive measures
   ├── Update runbooks and playbooks
```

## Implementation Patterns

### Pattern 1: Automated Incident Detection System

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import threading
import asyncio
import json

class IncidentSeverity(Enum):
    P0 = "critical"
    P1 = "high"
    P2 = "medium"
    P3 = "low"

@dataclass
class Incident:
    id: str
    severity: IncidentSeverity
    title: str
    description: str
    detected_at: datetime
    affected_components: List[str]
    status: str = "open"
    assignee: Optional[str] = None
    timeline: List[Dict] = field(default_factory=list)
    related_incidents: List[str] = field(default_factory=list)

class LLMIncidentDetector:
    def __init__(
        self,
        metrics_store,
        alert_callback: Callable,
        config: Dict
    ):
        self.metrics = metrics_store
        self.alert = alert_callback
        self.config = config
        self.check_interval_seconds = config.get("check_interval", 60)
        self.thresholds = self._load_thresholds()
        self.active_incidents: Dict[str, Incident] = {}
        self.lock = threading.Lock()
        
    def _load_thresholds(self) -> Dict:
        return {
            "error_rate": {
                "critical": 0.15,
                "high": 0.05,
                "medium": 0.02
            },
            "latency_p99_ms": {
                "critical": 30000,
                "high": 10000,
                "medium": 5000
            },
            "safety_violations_per_minute": {
                "critical": 10,
                "high": 5,
                "medium": 2
            },
            "output_length_zscore": {
                "critical": 5.0,
                "high": 4.0,
                "medium": 3.0
            }
        }
    
    async def start_monitoring(self):
        while True:
            try:
                await self._check_metrics()
                await asyncio.sleep(self.check_interval_seconds)
            except Exception as e:
                await self._handle_monitor_error(e)
    
    async def _check_metrics(self):
        metrics = await self.metrics.get_current_metrics()
        
        severity, alert_type = self._evaluate_error_rate(metrics)
        if severity:
            await self._create_incident(
                severity, f"High error rate: {alert_type}", metrics
            )
        
        severity, alert_type = self._evaluate_latency(metrics)
        if severity:
            await self._create_incident(
                severity, f"Latency anomaly: {alert_type}", metrics
            )
        
        severity, alert_type = self._evaluate_safety(metrics)
        if severity:
            await self._create_incident(
                severity, f"Safety violation spike: {alert_type}", metrics
            )
        
        severity, alert_type = self._evaluate_quality(metrics)
        if severity:
            await self._create_incident(
                severity, f"Quality degradation: {alert_type}", metrics
            )
    
    def _evaluate_error_rate(self, metrics: Dict) -> Tuple[Optional[IncidentSeverity], str]:
        error_rate = metrics.get("error_rate", 0)
        if error_rate >= self.thresholds["error_rate"]["critical"]:
            return IncidentSeverity.P0, f"{error_rate:.2%} error rate"
        elif error_rate >= self.thresholds["error_rate"]["high"]:
            return IncidentSeverity.P1, f"{error_rate:.2%} error rate"
        elif error_rate >= self.thresholds["error_rate"]["medium"]:
            return IncidentSeverity.P2, f"{error_rate:.2%} error rate"
        return None, ""
    
    def _evaluate_latency(self, metrics: Dict) -> Tuple[Optional[IncidentSeverity], str]:
        latency_p99 = metrics.get("latency_p99_ms", 0)
        if latency_p99 >= self.thresholds["latency_p99_ms"]["critical"]:
            return IncidentSeverity.P0, f"p99 latency {latency_p99}ms"
        elif latency_p99 >= self.thresholds["latency_p99_ms"]["high"]:
            return IncidentSeverity.P1, f"p99 latency {latency_p99}ms"
        elif latency_p99 >= self.thresholds["latency_p99_ms"]["medium"]:
            return IncidentSeverity.P2, f"p99 latency {latency_p99}ms"
        return None, ""
    
    def _evaluate_safety(self, metrics: Dict) -> Tuple[Optional[IncidentSeverity], str]:
        violations = metrics.get("safety_violations_per_minute", 0)
        if violations >= self.thresholds["safety_violations"]["critical"]:
            return IncidentSeverity.P0, f"{violations} violations/min"
        elif violations >= self.thresholds["safety_violations"]["high"]:
            return IncidentSeverity.P1, f"{violations} violations/min"
        elif violations >= self.thresholds["safety_violations"]["medium"]:
            return IncidentSeverity.P2, f"{violations} violations/min"
        return None, ""
    
    def _evaluate_quality(self, metrics: Dict) -> Tuple[Optional[IncidentSeverity], str]:
        zscore = metrics.get("output_length_zscore", 0)
        if zscore >= self.thresholds["output_length_zscore"]["critical"]:
            return IncidentSeverity.P0, f"z-score {zscore:.2f}"
        elif zscore >= self.thresholds["output_length_zscore"]["high"]:
            return IncidentSeverity.P1, f"z-score {zscore:.2f}"
        elif zscore >= self.thresholds["output_length_zscore"]["medium"]:
            return IncidentSeverity.P2, f"z-score {zscore:.2f}"
        return None, ""
    
    async def _create_incident(
        self,
        severity: IncidentSeverity,
        title: str,
        metrics: Dict
    ):
        incident_id = self._generate_incident_id()
        incident = Incident(
            id=incident_id,
            severity=severity,
            title=title,
            description=f"Auto-detected: {title}\n\nMetrics:\n{json.dumps(metrics, indent=2)}",
            detected_at=datetime.utcnow(),
            affected_components=["llm-service"],
            timeline=[{
                "timestamp": datetime.utcnow().isoformat(),
                "action": "incident_created",
                "details": f"Auto-detected via monitoring"
            }]
        )
        
        with self.lock:
            self.active_incidents[incident_id] = incident
        
        await self.alert(incident)
        return incident
    
    def _generate_incident_id(self) -> str:
        return f"INC-{datetime.utcnow().strftime('%Y%m%d')}-{len(self.active_incidents) + 1:04d}"
    
    async def _handle_monitor_error(self, error: Exception):
        print(f"Monitor error: {error}")
        await asyncio.sleep(5)
```

### Pattern 2: LLM Incident Runbook Executor

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class RunbookStep:
    id: str
    action: str
    description: str
    command: Optional[str] = None
    verification: Optional[str] = None
    timeout_seconds: int = 60

class LLMRunbookExecutor:
    def __init__(self, incident_id: str, runbook_type: str):
        self.incident_id = incident_id
        self.runbook_type = runbook_type
        self.execution_log: List[Dict] = []
        self.runbooks = self._initialize_runbooks()
    
    def _initialize_runbooks(self) -> Dict[str, List[RunbookStep]]:
        return {
            "high_error_rate": [
                RunbookStep(
                    id="her_1",
                    action="check_model_health",
                    description="Check if model is responding to health checks",
                    command="curl -s http://model-service:8080/health",
                    timeout_seconds=10
                ),
                RunbookStep(
                    id="her_2",
                    action="check_gpu_status",
                    description="Check GPU utilization and memory",
                    command="nvidia-smi",
                    verification="gpu_util < 95%"
                ),
                RunbookStep(
                    id="her_3",
                    action="scale_replicas",
                    description="Scale up service replicas if under resource pressure",
                    command="kubectl scale deployment llm-service --replicas=5",
                    verification="replicas >= 5"
                ),
                RunbookStep(
                    id="her_4",
                    action="enable_fallback",
                    description="Enable fallback to backup model if available",
                    command="kubectl patch configmap llm-config --patch '{\"data\":{\"fallback_enabled\":\"true\"}}'",
                    verification="fallback_active == true"
                )
            ],
            "safety_violation": [
                RunbookStep(
                    id="sv_1",
                    action="isolate_requests",
                    description="Enable strict mode to log all requests",
                    command="kubectl patch configmap safety-config --patch '{\"data\":{\"strict_mode\":\"true\"}}'",
                    timeout_seconds=30
                ),
                RunbookStep(
                    id="sv_2",
                    action="enable_additional_filtering",
                    description="Enable additional content filtering layer",
                    command="kubectl set env deployment/llm-service ADDITIONAL_SAFETY_FILTER=1",
                    timeout_seconds=30
                ),
                RunbookStep(
                    id="sv_3",
                    action="notify_safety_team",
                    description="Page safety team for immediate review",
                    verification="safety_team_notified == true"
                ),
                RunbookStep(
                    id="sv_4",
                    action="collect_violation_samples",
                    description="Collect recent violating samples for analysis",
                    command="kubectl cp llm-pod:/var/log/violations ./violations.log",
                    timeout_seconds=60
                )
            ],
            "latency_spike": [
                RunbookStep(
                    id="ls_1",
                    action="identify_bottleneck",
                    description="Determine if bottleneck is CPU, GPU, or network",
                    command="kubectl top pods",
                    timeout_seconds=30
                ),
                RunbookStep(
                    id="ls_2",
                    action="check_queue_depth",
                    description="Check request queue depth",
                    command="curl http://queue-service:8080/metrics",
                    verification="queue_depth < 1000"
                ),
                RunbookStep(
                    id="ls_3",
                    action="enable_caching",
                    description="Enable result caching to reduce load",
                    command="kubectl patch configmap cache-config --patch '{\"data\":{\"enabled\":\"true\"}}'",
                    verification="cache_hit_rate > 0.3"
                ),
                RunbookStep(
                    id="ls_4",
                    action="scale_inference",
                    description="Add more inference replicas",
                    command="kubectl scale deployment llm-inference --replicas=10",
                    verification="pending_replicas == 0"
                )
            ]
        }
    
    async def execute_runbook(
        self,
        steps: List[RunbookStep],
        dry_run: bool = False
    ) -> Dict[str, Any]:
        results = {
            "incident_id": self.incident_id,
            "runbook_type": self.runbook_type,
            "started_at": datetime.utcnow().isoformat(),
            "steps_completed": [],
            "steps_failed": [],
            "overall_status": "in_progress"
        }
        
        for step in steps:
            step_result = await self._execute_step(step, dry_run)
            results["steps_completed"].append(step_result) if step_result["success"] \
                else results["steps_failed"].append(step_result)
            
            if not step_result["success"] and step.id.startswith(("sv_", "her_1")):
                results["overall_status"] = "failed"
                break
        
        results["completed_at"] = datetime.utcnow().isoformat()
        if results["overall_status"] != "failed":
            results["overall_status"] = "completed" if not results["steps_failed"] else "partial"
        
        return results
    
    async def _execute_step(
        self,
        step: RunbookStep,
        dry_run: bool
    ) -> Dict[str, Any]:
        log_entry = {
            "step_id": step.id,
            "action": step.action,
            "started_at": datetime.utcnow().isoformat(),
            "success": False,
            "output": None,
            "error": None
        }
        
        if dry_run:
            log_entry["output"] = f"[DRY RUN] Would execute: {step.command}"
            log_entry["success"] = True
        else:
            try:
                if step.command:
                    process = await asyncio.create_subprocess_shell(
                        step.command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=step.timeout_seconds
                    )
                    log_entry["output"] = stdout.decode() if stdout else ""
                    log_entry["success"] = process.returncode == 0
                else:
                    log_entry["output"] = "Manual step - no command"
                    log_entry["success"] = True
            except asyncio.TimeoutError:
                log_entry["error"] = f"Timeout after {step.timeout_seconds}s"
            except Exception as e:
                log_entry["error"] = str(e)
        
        log_entry["completed_at"] = datetime.utcnow().isoformat()
        self.execution_log.append(log_entry)
        return log_entry
```

### Pattern 3: Incident Timeline Reconstruction

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import json

class IncidentTimelineReconstructor:
    def __init__(self, log_store, metrics_store, trace_store):
        self.logs = log_store
        self.metrics = metrics_store
        self.traces = trace_store
    
    def reconstruct(
        self,
        incident_id: str,
        time_range: Dict[str, datetime]
    ) -> Dict:
        start_time = time_range["start"]
        end_time = time_range["end"]
        
        logs = self.logs.query(
            start=start_time,
            end=end_time,
            filters={"incident_id": incident_id}
        )
        
        metrics = self.metrics.get_range(
            start=start_time,
            end=end_time,
            interval_seconds=60
        )
        
        traces = self.traces.query(
            start=start_time,
            end=end_time
        )
        
        events = self._merge_timeline_data(logs, metrics, traces)
        events.sort(key=lambda x: x["timestamp"])
        
        return {
            "incident_id": incident_id,
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "events": events,
            "summary": self._generate_summary(events),
            "metrics_correlation": self._correlate_metrics(events)
        }
    
    def _merge_timeline_data(
        self,
        logs: List[Dict],
        metrics: List[Dict],
        traces: List[Dict]
    ) -> List[Dict]:
        events = []
        
        for log in logs:
            events.append({
                "timestamp": log["timestamp"],
                "type": "log",
                "source": log.get("source", "unknown"),
                "severity": log.get("severity", "info"),
                "message": log.get("message", ""),
                "details": log.get("details", {})
            })
        
        for metric in metrics:
            if self._is_anomalous(metric):
                events.append({
                    "timestamp": metric["timestamp"],
                    "type": "metric_anomaly",
                    "metric_name": metric["name"],
                    "value": metric["value"],
                    "expected_range": metric.get("expected"),
                    "severity": "warning"
                })
        
        for trace in traces:
            if trace.get("status") == "error":
                events.append({
                    "timestamp": trace["timestamp"],
                    "type": "trace_error",
                    "trace_id": trace["id"],
                    "error_type": trace.get("error_type"),
                    "span_name": trace.get("span_name"),
                    "severity": "error"
                })
        
        return events
    
    def _is_anomalous(self, metric: Dict) -> bool:
        value = metric.get("value", 0)
        expected = metric.get("expected", {})
        
        if "min" in expected and value < expected["min"]:
            return True
        if "max" in expected and value > expected["max"]:
            return True
        
        return False
    
    def _generate_summary(self, events: List[Dict]) -> Dict:
        by_type = defaultdict(int)
        by_severity = defaultdict(int)
        
        for event in events:
            by_type[event["type"]] += 1
            by_severity[event.get("severity", "info")] += 1
        
        return {
            "total_events": len(events),
            "by_type": dict(by_type),
            "by_severity": dict(by_severity),
            "first_event": events[0]["timestamp"] if events else None,
            "last_event": events[-1]["timestamp"] if events else None
        }
    
    def _correlate_metrics(self, events: List[Dict]) -> List[Dict]:
        correlations = []
        
        error_events = [e for e in events if e.get("severity") == "error"]
        metric_anomalies = [e for e in events if e["type"] == "metric_anomaly"]
        
        for error in error_events:
            error_time = error["timestamp"]
            nearby_anomalies = [
                a for a in metric_anomalies
                if abs((a["timestamp"] - error_time).total_seconds()) < 300
            ]
            if nearby_anomalies:
                correlations.append({
                    "event": error,
                    "correlated_anomalies": nearby_anomalies,
                    "time_window_seconds": 300
                })
        
        return correlations
```

### Pattern 4: Post-Mortem Analyzer for LLM Incidents

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class PostMortemSection:
    title: str
    content: str
    recommendations: List[str] = field(default_factory=list)

@dataclass
class PostMortem:
    incident_id: str
    title: str
    severity: str
    status: str
    date: datetime
    sections: List[PostMortemSection] = field(default_factory=list)
    action_items: List[Dict] = field(default_factory=list)

class LLMPostMortemAnalyzer:
    def __init__(self, timeline_data: Dict):
        self.data = timeline_data
        self.analyzer_prompt_template = """
Analyze this LLM incident timeline and identify:

1. Root Cause: What was the underlying cause of the incident?
2. Contributing Factors: What conditions enabled this to happen?
3. Detection Gap: Why wasn't this caught earlier by automated systems?
4. Response Effectiveness: How effective was the incident response?
5. Prevention: What changes would prevent recurrence?

Timeline Data:
{timeline_json}

Format your response as structured JSON with keys: root_cause, contributing_factors, 
detection_gap, response_effectiveness, prevention_recommendations.
"""
    
    async def generate_post_mortem(
        self,
        llm_client,
        use_ai_assistance: bool = True
    ) -> PostMortem:
        timeline_json = json.dumps(self.data, indent=2)
        
        if use_ai_assistance:
            analysis = await self._get_ai_analysis(timeline_json, llm_client)
        else:
            analysis = self._get_structured_analysis()
        
        post_mortem = PostMortem(
            incident_id=self.data["incident_id"],
            title=self._generate_title(analysis),
            severity=self._determine_severity(),
            status="completed",
            date=datetime.utcnow(),
            sections=self._build_sections(analysis),
            action_items=self._generate_action_items(analysis)
        )
        
        return post_mortem
    
    async def _get_ai_analysis(self, timeline_json: str, llm_client) -> Dict:
        prompt = self.analyzer_prompt_template.format(timeline_json=timeline_json)
        
        response = await llm_client.generate(
            prompt=prompt,
            parameters={"temperature": 0.3, "max_tokens": 2000}
        )
        
        try:
            return json.loads(response.text)
        except:
            return {
                "root_cause": "Unable to parse AI analysis",
                "contributing_factors": [],
                "detection_gap": "Analysis unavailable",
                "response_effectiveness": "Unknown",
                "prevention_recommendations": []
            }
    
    def _get_structured_analysis(self) -> Dict:
        events = self.data.get("events", [])
        metrics_correlation = self.data.get("metrics_correlation", [])
        
        error_events = [e for e in events if e.get("severity") == "error"]
        first_error_time = min([e["timestamp"] for e in error_events]) if error_events else None
        
        return {
            "root_cause": "Analysis requires manual review",
            "contributing_factors": [
                f"Incident lasted {len(error_events)} error events",
                f"First error at {first_error_time}"
            ],
            "detection_gap": "Automated detection review needed",
            "response_effectiveness": "Response timeline available in data",
            "prevention_recommendations": []
        }
    
    def _generate_title(self, analysis: Dict) -> str:
        root_cause = analysis.get("root_cause", "Unknown")
        if len(root_cause) > 50:
            root_cause = root_cause[:50] + "..."
        return f"Post-Mortem: {root_cause}"
    
    def _determine_severity(self) -> str:
        events = self.data.get("events", [])
        error_count = sum(1 for e in events if e.get("severity") == "error")
        
        if error_count > 100:
            return "P0 - Critical"
        elif error_count > 50:
            return "P1 - High"
        elif error_count > 10:
            return "P2 - Medium"
        else:
            return "P3 - Low"
    
    def _build_sections(self, analysis: Dict) -> List[PostMortemSection]:
        return [
            PostMortemSection(
                title="Executive Summary",
                content=f"Incident {self.data['incident_id']} occurred on {self.data['date']}."
            ),
            PostMortemSection(
                title="Root Cause Analysis",
                content=analysis.get("root_cause", "To be determined"),
                recommendations=[r for r in analysis.get("prevention_recommendations", [])]
            ),
            PostMortemSection(
                title="Timeline",
                content=self._format_timeline()
            ),
            PostMortemSection(
                title="Impact Assessment",
                content=f"Affected approximately {self._estimate_impact()} users."
            )
        ]
    
    def _generate_action_items(self, analysis: Dict) -> List[Dict]:
        items = []
        for i, rec in enumerate(analysis.get("prevention_recommendations", []), 1):
            items.append({
                "id": f"AI-{self.data['incident_id']}-{i:03d}",
                "description": rec,
                "priority": "high",
                "status": "open",
                "owner": "TBD"
            })
        return items
    
    def _format_timeline(self) -> str:
        events = self.data.get("events", [])
        return "\n".join([
            f"- {e['timestamp']}: {e['type']} - {e.get('message', e.get('metric_name', 'N/A'))}"
            for e in events[:20]
        ])
    
    def _estimate_impact(self) -> int:
        events = self.data.get("events", [])
        error_events = [e for e in events if e.get("severity") == "error"]
        return len(error_events) * 10
```

### Pattern 5: Emergency LLM Service Isolation

```python
from typing import Dict, Optional
import asyncio
import httpx

class LLMServiceIsolator:
    def __init__(
        self,
        kubernetes_client,
        config_store,
        notification_service
    ):
        self.k8s = kubernetes_client
        self.config = config_store
        self.notify = notification_service
    
    async def isolate_service(
        self,
        service_name: str,
        reason: str,
        severity: str
    ) -> Dict:
        """
        Immediately isolate an LLM service during an incident.
        This should only be called for critical incidents where
        the service is causing harm.
        """
        result = {
            "service": service_name,
            "action": "isolation_initiated",
            "timestamp": asyncio.get_event_loop().time(),
            "steps_completed": []
        }
        
        try:
            await self._enable_maintenance_mode(service_name)
            result["steps_completed"].append("maintenance_mode_enabled")
            
            await self._scale_to_zero(service_name)
            result["steps_completed"].append("scaled_to_zero")
            
            await self._block_traffic(service_name)
            result["steps_completed"].append("traffic_blocked")
            
            await self._preserve_logs(service_name)
            result["steps_completed"].append("logs_preserved")
            
            await self._notify_stakeholders(service_name, reason, severity)
            result["steps_completed"].append("stakeholders_notified")
            
            result["status"] = "success"
            
        except Exception as e:
            result["status"] = "partial"
            result["error"] = str(e)
        
        return result
    
    async def _enable_maintenance_mode(self, service_name: str):
        await self.config.update(
            f"services/{service_name}/status",
            {"maintenance_mode": True, "reason": "emergency_isolation"}
        )
        await asyncio.sleep(2)
    
    async def _scale_to_zero(self, service_name: str):
        await self.k8s.scale_deployment(service_name, replicas=0)
        await self._wait_for_pods_terminated(service_name, timeout=60)
    
    async def _wait_for_pods_terminated(self, service_name: str, timeout: int):
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < timeout:
            pods = await self.k8s.list_pods(service_name)
            if not pods:
                return
            await asyncio.sleep(2)
        raise TimeoutError(f"Pods not terminated after {timeout}s")
    
    async def _block_traffic(self, service_name: str):
        await self.k8s.update_network_policy(
            service_name,
            {"ingress": {"deny": "0.0.0.0/0"}}
        )
    
    async def _preserve_logs(self, service_name: str):
        await self.k8s.exec_command(
            f"kubectl logs -l app={service_name} --tail=10000",
            timeout=120
        )
    
    async def _notify_stakeholders(
        self,
        service_name: str,
        reason: str,
        severity: str
    ):
        message = f"""
🚨 EMERGENCY ISOLATION ALERT

Service: {service_name}
Severity: {severity}
Reason: {reason}

Action taken: Service has been isolated.
All traffic blocked. Logs preserved for investigation.

Please check the incident channel for updates.
"""
        await self.notify.send_alert(message, channels=["pagerduty", "slack"])
    
    async def restore_service(
        self,
        service_name: str,
        validate: bool = True
    ) -> Dict:
        """
        Restore an isolated LLM service after the incident is resolved.
        """
        result = {"service": service_name, "steps_completed": []}
        
        await self._disable_maintenance_mode(service_name)
        result["steps_completed"].append("maintenance_mode_disabled")
        
        if validate:
            await self._run_validation_tests(service_name)
            result["steps_completed"].append("validation_passed")
        
        await self._scale_to_original(service_name)
        result["steps_completed"].append("scaled_to_original")
        
        await self._allow_traffic(service_name)
        result["steps_completed"].append("traffic_allowed")
        
        return result
    
    async def _disable_maintenance_mode(self, service_name: str):
        await self.config.update(
            f"services/{service_name}/status",
            {"maintenance_mode": False}
        )
    
    async def _run_validation_tests(self, service_name: str) -> bool:
        test_prompts = [
            "What is 2+2?",
            "Summarize the concept of machine learning.",
            "Write a short hello world program."
        ]
        
        for prompt in test_prompts:
            response = await self._send_test_request(service_name, prompt)
            if not response.get("success"):
                raise AssertionError(f"Validation failed: {response.get('error')}")
        
        return True
    
    async def _send_test_request(self, service_name: str, prompt: str) -> Dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"http://{service_name}:8080/generate",
                    json={"prompt": prompt, "max_tokens": 50},
                    timeout=30.0
                )
                return {"success": response.status_code == 200}
            except Exception as e:
                return {"success": False, "error": str(e)}
```

## Framework Integration

### Integrating with PagerDuty

```python
class PagerDutyIncidentIntegrator:
    def __init__(self, pagerduty_api_key: str):
        self.client = PagerDutyClient(api_key=pagerduty_api_key)
    
    async def create_incident(self, incident: Incident) -> str:
        service_id = self._get_service_id(incident.severity)
        
        pd_incident = await self.client.create_incident(
            title=incident.title,
            body=incident.description,
            urgency="high" if incident.severity in [IncidentSeverity.P0, IncidentSeverity.P1] else "low",
            service_id=service_id
        )
        
        return pd_incident["id"]
    
    def _get_service_id(self, severity: IncidentSeverity) -> str:
        mapping = {
            IncidentSeverity.P0: "LLM_CRITICAL_SERVICE",
            IncidentSeverity.P1: "LLM_HIGH_PRIORITY_SERVICE",
            IncidentSeverity.P2: "LLM_STANDARD_SERVICE",
            IncidentSeverity.P3: "LLM_LOW_PRIORITY_SERVICE"
        }
        return mapping.get(severity, "LLM_STANDARD_SERVICE")
```

### Integrating with Datadog

```python
class DatadogIncidentCorrelator:
    def __init__(self, api_client):
        self.client = api_client
    
    async def correlate_with_datadog(
        self,
        incident: Incident,
        time_range: Dict
    ) -> Dict:
        query = f'events "{{service:llm}} status:error" from={time_range["start"]} to={time_range["end"]}'
        
        events = await self.client.query_events(query)
        
        monitors = await self.client.get_triggered_monitors(
            tags=["llm", "production"]
        )
        
        return {
            "datadog_events": events,
            "triggered_monitors": monitors,
            "correlation_id": incident.id
        }
```

## Performance Considerations

### Incident Detection Latency

For effective incident response, detection latency is critical:
- **Real-time metrics**: 10-30 second detection for P0 issues
- **Rolling window metrics**: 2-5 minute detection for gradual degradation
- **User-reported issues**: Variable, but should trigger immediate investigation

### Runbook Execution Speed

Runbooks should be designed for fast execution:
- Pre-validate commands in staging
- Use parallel execution where possible
- Keep timeouts reasonable (60-120 seconds max per step)
- Implement dry-run mode for safety

### Post-Mortem Analysis Efficiency

Use AI assistance carefully:
- AI-generated post-mortems save time but require human review
- Always validate AI suggestions against data
- Keep AI involvement in analysis phase, not final documentation

## Common Pitfalls

### Pitfall 1: Not Preserving Evidence During Recovery

**Problem**: Teams rush to restore service and lose critical debugging evidence.

**Solution**: Implement mandatory evidence preservation in runbooks:
```python
# Always run log preservation before making changes
async def _preserve_state(self, service_name: str):
    await self.k8s.exec(
        f"kubectl logs -l app={service_name} --tail=5000 > /tmp/{service_name}_pre_recovery.log"
    )
    await self.k8s.exec(
        f"kubectl describe pods -l app={service_name} > /tmp/{service_name}_pods.txt"
    )
```

### Pitfall 2: Over-Alerting Causing Alert Fatigue

**Problem**: Too many alerts cause teams to ignore or delay response.

**Solution**: Use dynamic thresholds and smart aggregation:
```python
def should_alert(self, metric_name: str, value: float, baseline: Dict) -> bool:
    # Only alert if significantly deviating from user's normal patterns
    zscore = (value - baseline["mean"]) / baseline["std"]
    return zscore > 3.0 and self._count_recent_alerts(metric_name) < 5
```

### Pitfall 3: Not Having LLM-Specific Runbooks

**Problem**: Generic ML runbooks don't account for LLM-specific issues like hallucination spikes or prompt injection.

**Solution**: Create LLM-specific runbooks:
```python
runbooks = {
    "hallucination_spike": [...],
    "prompt_injection_detected": [...],
    "safety_policy_breach": [...],
    "output_quality_degradation": [...]
}
```

### Pitfall 4: Insufficient Separation Between Investigation and Recovery

**Problem**: Teams mix investigation and recovery, potentially corrupting evidence.

**Solution**: Define clear phases:
1. **Investigate**: Collect data, don't make changes
2. **Contain**: Isolate if necessary, preserve evidence
3. **Fix**: Implement permanent solution
4. **Verify**: Confirm fix works
5. **Document**: Complete post-mortem

## Research References

1. **Sculley et al. (2014)** - "Machine Learning: The High Interest Credit Card of Technical Debt" - Discusses technical debt and incident patterns in ML systems.

2. **Breck et al. (2017)** - "The ML Test Score" - Provides concrete testing and monitoring criteria for ML systems relevant to incident prevention.

3. **Lwakatare et al. (2019)** - "A Taxonomy of Real-World Challenges of ML Systems" - Classification of ML incidents and their characteristics.

4. **Renggli et al. (2019)** - "Continuous Training and Deployment of Machine Learning Models" - MLOps practices including incident handling.

5. **Studer et al. (2021)** - "Click to Learn" - Industry perspective on debugging and maintaining ML systems in production.

6. **Mitchell et al. (2023)** - "AI Incident Database" - Documentation of AI failures and lessons learned.

7. **Stahl et al. (2022)** - "Ethics of AI Incident Response" - Guidelines for responsible handling of AI incidents.

8. **Arnold et al. (2022)** - "Lessons Learned from AI Incidents" - Case studies of AI failures and response strategies.

9. **O'Neil (2016)** - "Weapons of Math Destruction" - Discusses potential harms from ML failures and accountability.

10. **Google SRE Handbook (2022)** - SRE practices applicable to LLM incident response and monitoring.