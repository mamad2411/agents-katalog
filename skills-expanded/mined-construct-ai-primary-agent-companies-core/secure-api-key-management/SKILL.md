---
name: secure-api-key-management
description: >
  Use this skill when the task involves generating, managing, rotating, or securing API keys for cloud deployments,
  configuring authentication tokens, or implementing secure credential management practices.
  
  Use when: API keys need generation or rotation; secure key storage is required; authentication tokens
  need configuration; credential management policies need implementation; key access needs auditing.
  
  Don't use when: The task is about general environment variable access (use environment-variable-access instead);
  the task requires network tunneling (use network-tunneling-configuration instead).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Secure API Key Management Skill

## Overview

The Secure API Key Management skill enables the Render Deployment Specialist agent to generate, manage, rotate, and secure API keys and authentication tokens for cloud deployments. This skill covers secure key generation, storage, rotation, access control, and audit logging practices.

## Capabilities

### Key Generation and Storage
- **Cryptographically Secure Keys**: Generate keys using secure random generation
- **Key Storage**: Implement secure storage mechanisms for sensitive keys
- **Key Encryption**: Encrypt keys at rest and in transit
- **Key Format Standards**: Use standardized key formats and naming conventions

### Key Lifecycle Management
- **Key Rotation**: Implement automated and manual key rotation procedures
- **Key Revocation**: Safely revoke compromised or expired keys
- **Key Expiration**: Set appropriate expiration times for different key types
- **Key Backup**: Maintain secure backups of critical keys

### Access Control and Auditing
- **Role-Based Access**: Implement granular access control for key management
- **Audit Logging**: Log all key access, creation, and modification activities
- **Access Monitoring**: Monitor and alert on suspicious key usage patterns
- **Compliance Reporting**: Generate reports for security compliance requirements

### Integration Security
- **Third-Party Integration**: Securely manage keys for external service integrations
- **Environment Separation**: Maintain separate keys for different environments
- **Service-Specific Keys**: Create keys with appropriate permissions for specific services
- **Token Management**: Handle JWT tokens and other authentication tokens

## Common Patterns

### Secure Key Generation
```bash
#!/bin/bash
set -euo pipefail

# Configuration
KEY_TYPE="${1:-api_key}"
ENVIRONMENT="${2:-production}"
SERVICE_NAME="${3:-paperclip}"

# Generate cryptographically secure API key
generate_secure_key() {
  local length="${1:-32}"
  # Use /dev/urandom for cryptographically secure random bytes
  openssl rand -hex "$length"
}

# Generate different types of keys
case "$KEY_TYPE" in
  "api_key")
    # Standard API key (hex format)
    KEY_PREFIX="pcak"
    KEY_VALUE=$(generate_secure_key 32)
    FULL_KEY="${KEY_PREFIX}_${KEY_VALUE}"
    ;;

  "jwt_secret")
    # JWT signing secret (base64 encoded)
    KEY_VALUE=$(openssl rand -base64 64 | tr -d '\n')
    FULL_KEY="$KEY_VALUE"
    ;;

  "service_token")
    # Service-to-service token
    KEY_PREFIX="pcst"
    TIMESTAMP=$(date +%s)
    RANDOM_PART=$(generate_secure_key 16)
    FULL_KEY="${KEY_PREFIX}_${TIMESTAMP}_${RANDOM_PART}"
    ;;

  "webhook_secret")
    # Webhook verification secret
    KEY_PREFIX="whsec"
    KEY_VALUE=$(generate_secure_key 32)
    FULL_KEY="${KEY_PREFIX}_${KEY_VALUE}"
    ;;
esac

# Store key securely
KEY_ID=$(uuidgen)
KEY_NAME="${SERVICE_NAME}_${ENVIRONMENT}_${KEY_TYPE}"

# Create key record
cat > "/tmp/key_record.json" << EOF
{
  "id": "$KEY_ID",
  "name": "$KEY_NAME",
  "type": "$KEY_TYPE",
  "environment": "$ENVIRONMENT",
  "service": "$SERVICE_NAME",
  "created_at": "$(date -Iseconds)",
  "expires_at": "$(date -Iseconds -d '+90 days')",
  "status": "active",
  "key_hash": "$(echo -n "$FULL_KEY" | openssl sha256 -hex | awk '{print $2}')"
}
EOF

# Encrypt and store key (don't show full key in logs)
echo "Generated $KEY_TYPE for $SERVICE_NAME ($ENVIRONMENT)"
echo "Key ID: $KEY_ID"
echo "Key Hash: $(echo -n "$FULL_KEY" | openssl sha256 -hex | awk '{print $2}')"

# In production, store encrypted key in secure vault
# encrypt_and_store_key "$FULL_KEY" "$KEY_ID"

# Output key for immediate use (only do this securely!)
echo "WARNING: Store this key securely - it will only be shown once:"
echo "$FULL_KEY"
```

### Key Rotation Automation
```bash
#!/bin/bash
set -euo pipefail

# Configuration
SERVICE_NAME="${1:-paperclip}"
ENVIRONMENT="${2:-production}"
ROTATION_GRACE_PERIOD="${3:-24}"  # Hours before expiration to rotate

# Log helper
log() {
  echo "[$(date -Iseconds)] [KEY_ROTATION] $1"
}

# Find keys nearing expiration
find_expiring_keys() {
  local cutoff_date
  cutoff_date=$(date -Iseconds -d "+${ROTATION_GRACE_PERIOD} hours")

  # Query key database for expiring keys
  # In production, this would query a secure key management system
  find /etc/paperclip/keys -name "*.json" -exec grep -l "\"expires_at\": \"[^\"]*\"" {} \; | \
  while read -r key_file; do
    local expires_at
    expires_at=$(jq -r '.expires_at' "$key_file")

    if [[ "$expires_at" < "$cutoff_date" ]]; then
      echo "$key_file"
    fi
  done
}

# Rotate a single key
rotate_key() {
  local key_file="$1"
  local key_data
  key_data=$(cat "$key_file")

  local key_id key_name key_type service environment
  key_id=$(echo "$key_data" | jq -r '.id')
  key_name=$(echo "$key_data" | jq -r '.name')
  key_type=$(echo "$key_data" | jq -r '.type')
  service=$(echo "$key_data" | jq -r '.service')
  environment=$(echo "$key_data" | jq -r '.environment')

  log "Rotating key: $key_name (ID: $key_id)"

  # Generate new key
  local new_key
  case "$key_type" in
    "api_key")
      new_key="pcak_$(openssl rand -hex 32)"
      ;;
    "jwt_secret")
      new_key=$(openssl rand -base64 64 | tr -d '\n')
      ;;
    "service_token")
      new_key="pcst_$(date +%s)_$(openssl rand -hex 16)"
      ;;
    "webhook_secret")
      new_key="whsec_$(openssl rand -hex 32)"
      ;;
  esac

  # Update key record
  local updated_data
  updated_data=$(echo "$key_data" | jq \
    --arg new_key_hash "$(echo -n "$new_key" | openssl sha256 -hex | awk '{print $2}')" \
    --arg new_expires "$(date -Iseconds -d '+90 days')" \
    --arg rotated_at "$(date -Iseconds)" \
    '.key_hash = $new_key_hash | .expires_at = $new_expires | .rotated_at = $rotated_at | .previous_key_hash = .key_hash')

  # Save updated record
  echo "$updated_data" > "$key_file"

  # Update service configuration
  update_service_config "$service" "$environment" "$key_type" "$new_key"

  # Log rotation
  log "Successfully rotated key: $key_name"
  log "New expiration: $(date -Iseconds -d '+90 days')"

  # Send notifications
  notify_key_rotation "$key_name" "$service" "$environment"
}

# Update service configuration with new key
update_service_config() {
  local service="$1" environment="$2" key_type="$3" new_key="$4"

  case "$service" in
    "paperclip")
      case "$environment" in
        "production")
          # Update Render environment variables
          update_render_env_var "$service" "$key_type" "$new_key"
          ;;
        "staging")
          # Update staging configuration
          update_staging_config "$key_type" "$new_key"
          ;;
      esac
      ;;
    "hermes")
      # Update Hermes configuration
      update_hermes_config "$key_type" "$new_key"
      ;;
  esac
}

# Send rotation notifications
notify_key_rotation() {
  local key_name="$1" service="$2" environment="$3"

  # Send notification to team
  curl -X POST "https://api.paperclip.com/notifications" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $NOTIFICATION_TOKEN" \
    -d "{
      \"message\": \"API key rotated: $key_name\",
      \"service\": \"$service\",
      \"environment\": \"$environment\",
      \"timestamp\": \"$(date -Iseconds)\"
    }"
}

# Main rotation process
main() {
  log "Starting key rotation check for $SERVICE_NAME ($ENVIRONMENT)"

  local expiring_keys
  expiring_keys=$(find_expiring_keys)

  if [[ -z "$expiring_keys" ]]; then
    log "No keys require rotation"
    exit 0
  fi

  local key_count
  key_count=$(echo "$expiring_keys" | wc -l)
  log "Found $key_count keys requiring rotation"

  echo "$expiring_keys" | while read -r key_file; do
    if [[ -f "$key_file" ]]; then
      rotate_key "$key_file"
    fi
  done

  log "Key rotation process completed"
}

main "$@"
```

### Secure Key Storage and Access
```python
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from datetime import datetime, timedelta

class SecureKeyManager:
    def __init__(self, master_key=None, storage_path="/etc/paperclip/keys"):
        self.storage_path = storage_path
        self.master_key = master_key or os.getenv('KEY_MASTER_KEY')
        if not self.master_key:
            raise ValueError("Master key not provided")

        # Derive encryption key from master key
        self.encryption_key = self._derive_key(self.master_key.encode())

    def _derive_key(self, master_key):
        """Derive encryption key using PBKDF2"""
        salt = b'paperclip_key_salt'  # In production, use unique salt per deployment
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_key))

    def generate_key(self, key_type="api_key", service="paperclip", environment="production"):
        """Generate a new secure API key"""
        import secrets
        import uuid

        # Generate key based on type
        if key_type == "api_key":
            key_value = secrets.token_hex(32)
            full_key = f"pcak_{key_value}"
        elif key_type == "jwt_secret":
            key_value = base64.b64encode(secrets.token_bytes(64)).decode()
            full_key = key_value
        elif key_type == "webhook_secret":
            key_value = secrets.token_hex(32)
            full_key = f"whsec_{key_value}"
        else:
            raise ValueError(f"Unknown key type: {key_type}")

        # Create key record
        key_record = {
            "id": str(uuid.uuid4()),
            "name": f"{service}_{environment}_{key_type}",
            "type": key_type,
            "service": service,
            "environment": environment,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=90)).isoformat(),
            "status": "active",
            "key_hash": hashlib.sha256(full_key.encode()).hexdigest(),
            "access_log": []
        }

        # Encrypt and store key
        encrypted_key = self._encrypt_key(full_key)
        key_record["encrypted_key"] = encrypted_key

        # Save key record
        self._save_key_record(key_record)

        # Log key creation (without exposing the key)
        self._log_access(key_record["id"], "created", f"Generated {key_type} for {service}")

        return {
            "key_id": key_record["id"],
            "key": full_key,  # Only return once for immediate use
            "expires_at": key_record["expires_at"]
        }

    def get_key(self, key_id, service_context=None):
        """Retrieve a key for use (with access logging)"""
        key_record = self._load_key_record(key_id)

        if key_record["status"] != "active":
            raise ValueError(f"Key {key_id} is not active")

        # Check expiration
        if datetime.fromisoformat(key_record["expires_at"]) < datetime.utcnow():
            raise ValueError(f"Key {key_id} has expired")

        # Verify service context (optional additional security)
        if service_context and key_record.get("service") != service_context:
            self._log_access(key_id, "access_denied", f"Service context mismatch: {service_context}")
            raise ValueError("Access denied: service context mismatch")

        # Decrypt and return key
        decrypted_key = self._decrypt_key(key_record["encrypted_key"])

        # Log access
        self._log_access(key_id, "accessed", f"Retrieved for {service_context or 'unknown'}")

        return decrypted_key

    def rotate_key(self, key_id):
        """Rotate an existing key"""
        old_record = self._load_key_record(key_id)

        # Generate new key of same type
        new_key_data = self.generate_key(
            key_type=old_record["type"],
            service=old_record["service"],
            environment=old_record["environment"]
        )

        # Mark old key as rotated
        old_record["status"] = "rotated"
        old_record["rotated_at"] = datetime.utcnow().isoformat()
        old_record["successor_key_id"] = new_key_data["key_id"]
        self._save_key_record(old_record)

        # Update service configuration
        self._update_service_config(
            old_record["service"],
            old_record["environment"],
            old_record["type"],
            new_key_data["key"]
        )

        self._log_access(key_id, "rotated", f"Rotated to key {new_key_data['key_id']}")

        return new_key_data

    def revoke_key(self, key_id, reason="manual_revoke"):
        """Revoke a key immediately"""
        key_record = self._load_key_record(key_id)
        key_record["status"] = "revoked"
        key_record["revoked_at"] = datetime.utcnow().isoformat()
        key_record["revoke_reason"] = reason

        self._save_key_record(key_record)
        self._log_access(key_id, "revoked", reason)

        # Notify services to stop using this key
        self._notify_key_revocation(key_record)

    def _encrypt_key(self, key):
        """Encrypt a key for storage"""
        f = Fernet(self.encryption_key)
        return f.encrypt(key.encode()).decode()

    def _decrypt_key(self, encrypted_key):
        """Decrypt a stored key"""
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted_key.encode()).decode()

    def _save_key_record(self, record):
        """Save key record to encrypted storage"""
        key_id = record["id"]
        filepath = os.path.join(self.storage_path, f"{key_id}.json")

        # Encrypt the entire record
        record_json = json.dumps(record, indent=2)
        encrypted_record = self._encrypt_key(record_json)

        with open(filepath, 'w') as f:
            json.dump({"encrypted_record": encrypted_record}, f, indent=2)

    def _load_key_record(self, key_id):
        """Load and decrypt key record"""
        filepath = os.path.join(self.storage_path, f"{key_id}.json")

        if not os.path.exists(filepath):
            raise ValueError(f"Key {key_id} not found")

        with open(filepath, 'r') as f:
            encrypted_data = json.load(f)

        decrypted_record = self._decrypt_key(encrypted_data["encrypted_record"])
        return json.loads(decrypted_record)

    def _log_access(self, key_id, action, details=""):
        """Log key access for audit purposes"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "key_id": key_id,
            "action": action,
            "details": details,
            "ip_address": os.getenv('REMOTE_ADDR', 'unknown'),
            "user_agent": os.getenv('HTTP_USER_AGENT', 'unknown')
        }

        # In production, send to centralized logging system
        print(f"AUDIT: {json.dumps(log_entry)}")

    def _update_service_config(self, service, environment, key_type, new_key):
        """Update service configuration with new key"""
        # Implementation depends on service configuration system
        # This could update Render env vars, Kubernetes secrets, etc.
        pass

    def _notify_key_revocation(self, key_record):
        """Notify services about key revocation"""
        # Send notifications to affected services
        pass

# Usage examples
if __name__ == "__main__":
    # Initialize key manager
    key_manager = SecureKeyManager()

    # Generate a new API key
    new_key = key_manager.generate_key("api_key", "paperclip", "production")
    print(f"Generated key: {new_key['key_id']}")
    print(f"Expires: {new_key['expires_at']}")

    # Later, retrieve the key for use
    retrieved_key = key_manager.get_key(new_key['key_id'], "paperclip")
    print(f"Retrieved key: {retrieved_key[:10]}...")  # Only show partial key

    # Rotate the key
    rotated_key = key_manager.rotate_key(new_key['key_id'])
    print(f"Rotated to: {rotated_key['key_id']}")
```

### Key Access Auditing
```python
import json
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

class KeyAuditLogger:
    def __init__(self, db_path="/var/log/paperclip/key_audit.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize audit database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS key_access (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    key_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    service_context TEXT
                )
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_key_access_key_id
                ON key_access(key_id)
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_key_access_timestamp
                ON key_access(timestamp)
            ''')

    def log_access(self, key_id, action, details="", ip_address="", user_agent="", service_context=""):
        """Log a key access event"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO key_access
                (timestamp, key_id, action, details, ip_address, user_agent, service_context)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.utcnow().isoformat(),
                key_id,
                action,
                details,
                ip_address,
                user_agent,
                service_context
            ))

    def get_access_log(self, key_id=None, days=30, action=None):
        """Retrieve access logs"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT * FROM key_access
                WHERE timestamp >= ?
            '''
            params = [(datetime.utcnow() - timedelta(days=days)).isoformat()]

            if key_id:
                query += ' AND key_id = ?'
                params.append(key_id)

            if action:
                query += ' AND action = ?'
                params.append(action)

            query += ' ORDER BY timestamp DESC'

            cursor = conn.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def generate_audit_report(self, days=30):
        """Generate comprehensive audit report"""
        logs = self.get_access_log(days=days)

        report = {
            "report_period": f"Last {days} days",
            "generated_at": datetime.utcnow().isoformat(),
            "total_events": len(logs),
            "events_by_action": defaultdict(int),
            "events_by_key": defaultdict(int),
            "events_by_service": defaultdict(int),
            "suspicious_activity": []
        }

        for log in logs:
            report["events_by_action"][log["action"]] += 1
            report["events_by_key"][log["key_id"]] += 1
            if log["service_context"]:
                report["events_by_service"][log["service_context"]] += 1

            # Detect suspicious patterns
            if self._is_suspicious(log):
                report["suspicious_activity"].append(log)

        return report

    def _is_suspicious(self, log):
        """Detect suspicious access patterns"""
        # Check for rapid access attempts
        recent_logs = self.get_access_log(
            key_id=log["key_id"],
            days=1,
            action="access_denied"
        )

        if len(recent_logs) > 10:
            return True

        # Check for access from unusual locations
        # This would integrate with GeoIP service
        if log["ip_address"] and self._is_unusual_location(log["ip_address"]):
            return True

        return False

    def _is_unusual_location(self, ip_address):
        """Check if IP is from unusual location"""
        # Placeholder - integrate with GeoIP service
        return False

    def cleanup_old_logs(self, days_to_keep=365):
        """Clean up old audit logs"""
        cutoff_date = (datetime.utcnow() - timedelta(days=days_to_keep)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM key_access WHERE timestamp < ?', (cutoff_date,))
            deleted_count = conn.total_changes

        print(f"Cleaned up {deleted_count} old audit log entries")
        return deleted_count

# Usage
audit_logger = KeyAuditLogger()

# Log key access
audit_logger.log_access(
    key_id="key-123",
    action="accessed",
    details="Retrieved for API call",
    ip_address="192.168.1.100",
    service_context="paperclip-api"
)

# Generate audit report
report = audit_logger.generate_audit_report(days=7)
print(json.dumps(report, indent=2))
```

## Security Best Practices

### Key Generation
- **Cryptographic Strength**: Use minimum 256-bit keys for symmetric encryption
- **Random Generation**: Always use cryptographically secure random number generators
- **Unique Keys**: Never reuse keys across different services or environments
- **Standard Formats**: Follow industry-standard key formats and naming conventions

### Key Storage
- **Encryption at Rest**: Encrypt all keys stored in databases or files
- **Access Control**: Implement strict access controls for key storage systems
- **Backup Security**: Securely backup keys with appropriate encryption
- **Key Separation**: Store different types of keys in separate secure locations

### Key Rotation
- **Regular Rotation**: Rotate keys regularly (90-180 days for API keys)
- **Automated Rotation**: Implement automated rotation for critical keys
- **Grace Periods**: Provide transition periods during key rotation
- **Emergency Rotation**: Have procedures for immediate key rotation when compromised

### Access Monitoring
- **Comprehensive Logging**: Log all key access, creation, and modification
- **Real-time Alerts**: Set up alerts for suspicious access patterns
- **Regular Audits**: Perform regular security audits of key management
- **Compliance Reporting**: Generate reports for regulatory compliance

## Integration Points

### Internal InfraForge AI
- **Security Agent**: Collaborates on key encryption and access control
- **Monitoring Agent**: Integrates with key access monitoring systems
- **Database Agent**: Works with database credential management

### Cross-Company Integration
- **DevForge AI**: Collaborates on application key requirements
- **PaperclipForge AI**: Works with project management for key lifecycle
- **QualityForge AI**: Partners on key security testing and validation

## Success Metrics

- **Key Security**: 100% of keys encrypted and securely stored
- **Rotation Compliance**: ≥95% of keys rotated within policy timelines
- **Access Audit**: 100% of key access events logged and monitored
- **Incident Response**: <1 hour average time to rotate compromised keys

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
