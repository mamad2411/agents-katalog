---
name: intel-platforms-threat-hunt
description: "Intel Platforms Threat Hunt."
domain: cybersecurity
---

cortex:
    image: thehiveproject/cortex:3.1.8
    ports:
      - "9001:9001"
    depends_on:
      - elasticsearch

volumes:
  es-data:
  misp-data:
```

### Step 2: Configure Feed Ingestion Pipeline

```python
from pymisp import PyMISP
from pycti import OpenCTIApiClient
import json

class TIPFeedManager:
    """Manage threat intelligence feed ingestion across platform components."""

    def __init__(self, misp_url, misp_key, opencti_url, opencti_token):
        self.misp = PyMISP(misp_url, misp_key, ssl=False)
        self.opencti = OpenCTIApiClient(opencti_url, opencti_token)

    def configure_osint_feeds(self):
        """Enable default OSINT feeds in MISP."""
        osint_feeds = [
            {"name": "CIRCL OSINT", "id": 1},
            {"name": "Botvrij.eu", "id": 2},
            {"name": "abuse.ch URLhaus", "id": 5},
            {"name": "abuse.ch Feodo Tracker", "id": 6},
        ]
        for feed in osint_feeds:
            try:
                self.misp.enable_feed(feed["id"])
                self.misp.fetch_feed(feed["id"])
                print(f"[+] Enabled feed: {feed['name']}")
            except Exception as e:
                print(f"[-] Failed: {feed['name']}: {e}")

    def configure_opencti_connectors(self):
        """List and verify OpenCTI connector status."""
        connectors = self.opencti.connector.list()
        for conn in connectors:
            print(
                f"  Connector: {conn['name']} - "
                f"Active: {conn['active']} - "
                f"Type: {conn['connector_type']}"
            )

    def sync_misp_to_opencti(self):
        """Verify MISP-OpenCTI sync is operational."""
        # OpenCTI MISP connector handles this automatically
        # Check connector status
        connectors = self.opencti.connector.list()
        misp_connector = [
            c for c in connectors if "misp" in c["name"].lower()
        ]
        if misp_connector:
            print(f"[+] MISP connector active: {misp_connector[0]['active']}")
        else:
            print("[-] MISP connector not found - configure in Docker Compose")
```

### Step 3: Build Enrichment Pipeline with Cortex

```python
import requests

class CortexEnrichment:
    """Integrate Cortex analyzers for automated enrichment."""

    def __init__(self, cortex_url, cortex_key):
        self.url = cortex_url
        self.headers = {"Authorization": f"Bearer {cortex_key}"}

    def list_analyzers(self):
        """List available Cortex analyzers."""
        resp = requests.get(
            f"{self.url}/api/analyzer",
            headers=self.headers,
            timeout=30,
        )
        if resp.status_code == 200:
            analyzers = resp.json()
            for a in analyzers:
                print(f"  {a['name']}: {a.get('description', '')[:60]}")
            return analyzers
        return []

    def analyze_observable(self, observable_type, observable_value, analyzer_id):
        """Submit an observable for analysis."""
        job = {
            "data": observable_value,
            "dataType": observable_type,
            "tlp": 2,
            "message": "TIP automated enrichment",
        }
        resp = requests.post(
            f"{self.url}/api/analyzer/{analyzer_id}/run",
            json=job,
            headers=self.headers,
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        return None

    def get_job_report(self, job_id):
        """Get the report for a completed analysis job."""
        resp = requests.get(
            f"{self.url}/api/job/{job_id}/report",
            headers=self.headers,
            timeout=60,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
```

### Step 4: Implement Analyst Dashboard Metrics

```python
class TIPMetrics:
    """Collect platform metrics for analyst dashboards."""

    def __init__(self, misp, opencti):
        self.misp = misp
        self.opencti = opencti

    def get_platform_stats(self):
        """Collect statistics across all platform components."""
        stats = {}

        # MISP stats
        misp_stats = self.misp.get_server_statistics()
        stats["misp"] = {
            "total_events": misp_stats.get("event_count", 0),
            "total_attributes": misp_stats.get("attribute_count", 0),
            "active_feeds": len([
                f for f in self.misp.feeds()
                if f.get("Feed", {}).get("enabled")
            ]),
        }

        # OpenCTI stats via GraphQL
        stats["opencti"] = {
            "total_indicators": self.opencti.indicator.list(
                first=0, withPagination=True
            ).get("pagination", {}).get("globalCount", 0),
            "total_reports": self.opencti.report.list(
                first=0, withPagination=True
            ).get("pagination", {}).get("globalCount", 0),
        }

        return stats
```

## Validation Criteria

- All platform components (MISP, OpenCTI, TheHive, Cortex) deployed and accessible
- MISP-OpenCTI bidirectional sync operational
- At least 3 OSINT feeds ingesting data
- Cortex analyzers configured and returning enrichment results
- Platform metrics dashboard showing real-time statistics
- STIX/TAXII export functional for intelligence sharing

## References

- [OpenCTI Documentation](https://docs.opencti.io/)
- [MISP Project](https://www.misp-project.org/)
- [TheHive Project](https://thehive-project.org/)
- [Cortex Documentation](https://github.com/TheHive-Project/Cortex)
- [MISP-OpenCTI Integration](https://docs.opencti.io/latest/deployment/connectors/)
