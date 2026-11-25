---
name: desktop-dashboard-connectivity
description: >
  Use this skill when the task involves establishing secure communication channels between desktop
  applications and cloud-deployed dashboards, configuring real-time data synchronization, or setting
  up bidirectional communication protocols between local and remote systems.
  
  Use when: Desktop applications need access to cloud dashboards; real-time data sync is required;
  bidirectional communication needs setup; secure desktop-to-cloud channels are needed; dashboard
  connectivity troubleshooting is required.
  
  Don't use when: The task is about network tunneling only (use network-tunneling-configuration instead);
  the task requires general API communication (use hermes-communication-setup instead).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Desktop Dashboard Connectivity Skill

## Overview

The Desktop Dashboard Connectivity skill enables the Render Deployment Specialist agent to establish and manage secure, bidirectional communication channels between desktop applications and cloud-deployed dashboards. This skill covers real-time data synchronization, secure authentication, connection management, and troubleshooting connectivity issues.

## Capabilities

### Real-time Communication Setup
- **WebSocket Configuration**: Set up WebSocket connections for real-time updates
- **Server-Sent Events**: Configure SSE for one-way real-time communication
- **Long Polling**: Implement fallback polling mechanisms
- **Connection Pooling**: Manage multiple concurrent connections efficiently

### Authentication and Security
- **Token-based Authentication**: Implement JWT tokens for secure connections
- **Session Management**: Handle connection sessions and reconnections
- **Secure Channels**: Ensure all communication uses encrypted protocols
- **Access Control**: Implement role-based access to dashboard features

### Data Synchronization
- **Bidirectional Sync**: Set up two-way data synchronization
- **Conflict Resolution**: Handle data conflicts between desktop and cloud
- **Offline Support**: Implement offline data queuing and sync on reconnection
- **Delta Updates**: Send only changed data to minimize bandwidth

### Connection Management
- **Connection Monitoring**: Monitor connection health and performance
- **Automatic Reconnection**: Implement automatic reconnection on failures
- **Load Balancing**: Distribute connections across multiple servers
- **Connection Limits**: Manage connection limits and throttling

## Common Patterns

### Real-time Dashboard Connection
```javascript
// desktop-dashboard-connection.js - Real-time dashboard connectivity
class DesktopDashboardConnection {
    constructor(dashboardUrl, authToken) {
        this.dashboardUrl = dashboardUrl;
        this.authToken = authToken;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
        this.heartbeatInterval = null;
        this.messageHandlers = new Map();
        this.pendingMessages = [];
        this.isConnected = false;

        // Set up event handlers
        this.setupMessageHandlers();
    }

    setupMessageHandlers() {
        // Handle different message types
        this.messageHandlers.set('dashboard_update', this.handleDashboardUpdate.bind(this));
        this.messageHandlers.set('agent_status', this.handleAgentStatus.bind(this));
        this.messageHandlers.set('task_complete', this.handleTaskComplete.bind(this));
        this.messageHandlers.set('error', this.handleError.bind(this));
        this.messageHandlers.set('heartbeat_ack', this.handleHeartbeatAck.bind(this));
    }

    async connect() {
        try {
            const wsUrl = this.dashboardUrl.replace(/^http/, 'ws') + '/ws';
            this.ws = new WebSocket(wsUrl);

            return new Promise((resolve, reject) => {
                this.ws.onopen = () => {
                    console.log('Connected to dashboard');
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this.startHeartbeat();
                    this.authenticate();
                    resolve();
                };

                this.ws.onmessage = (event) => {
                    this.handleMessage(event.data);
                };

                this.ws.onclose = (event) => {
                    console.log('Dashboard connection closed:', event.code, event.reason);
                    this.isConnected = false;
                    this.stopHeartbeat();

                    if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
                        this.scheduleReconnect();
                    }
                };

                this.ws.onerror = (error) => {
                    console.error('Dashboard connection error:', error);
                    reject(error);
                };

                // Connection timeout
                setTimeout(() => {
                    if (!this.isConnected) {
                        reject(new Error('Connection timeout'));
                    }
                }, 10000);
            });

        } catch (error) {
            console.error('Failed to connect to dashboard:', error);
            throw error;
        }
    }

    authenticate() {
        // Send authentication message
        this.send({
            type: 'authenticate',
            token: this.authToken,
            client_type: 'desktop',
            client_version: '1.0.0'
        });
    }

    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.isConnected) {
                this.send({ type: 'heartbeat', timestamp: Date.now() });
            }
        }, 30000); // 30 seconds
    }

    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    send(message) {
        if (this.isConnected && this.ws.readyState === WebSocket.OPEN) {
            const messageStr = JSON.stringify(message);
            this.ws.send(messageStr);
        } else {
            // Queue message for later sending
            this.pendingMessages.push(message);
        }
    }

    handleMessage(data) {
        try {
            const message = JSON.parse(data);
            const handler = this.messageHandlers.get(message.type);

            if (handler) {
                handler(message);
            } else {
                console.warn('Unknown message type:', message.type);
            }
        } catch (error) {
            console.error('Failed to parse message:', error, data);
        }
    }

    handleDashboardUpdate(message) {
        // Update local dashboard state
        console.log('Dashboard update received:', message.data);

        // Emit event for UI update
        this.emit('dashboardUpdate', message.data);
    }

    handleAgentStatus(message) {
        // Update agent status in UI
        console.log('Agent status update:', message.agent_id, message.status);

        this.emit('agentStatusUpdate', {
            agentId: message.agent_id,
            status: message.status,
            lastSeen: message.last_seen
        });
    }

    handleTaskComplete(message) {
        // Handle task completion notification
        console.log('Task completed:', message.task_id);

        this.emit('taskCompleted', {
            taskId: message.task_id,
            result: message.result,
            duration: message.duration
        });
    }

    handleError(message) {
        console.error('Dashboard error:', message.error);

        this.emit('error', {
            type: message.error.type,
            message: message.error.message,
            details: message.error.details
        });
    }

    handleHeartbeatAck(message) {
        // Heartbeat acknowledged - connection is healthy
        // Could implement connection quality monitoring here
    }

    scheduleReconnect() {
        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts), 30000);

        console.log(`Scheduling reconnect attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);

        setTimeout(() => {
            this.connect().then(() => {
                // Send any pending messages
                while (this.pendingMessages.length > 0) {
                    const message = this.pendingMessages.shift();
                    this.send(message);
                }
            }).catch(error => {
                console.error('Reconnect failed:', error);
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.scheduleReconnect();
                }
            });
        }, delay);
    }

    disconnect() {
        this.isConnected = false;
        this.stopHeartbeat();

        if (this.ws) {
            this.ws.close(1000, 'Client disconnecting');
        }
    }

    // Event emitter functionality
    emit(event, data) {
        // Simple event emitter - in real app, use a proper event library
        if (this.eventListeners && this.eventListeners[event]) {
            this.eventListeners[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('Event listener error:', error);
                }
            });
        }
    }

    on(event, callback) {
        if (!this.eventListeners) {
            this.eventListeners = {};
        }
        if (!this.eventListeners[event]) {
            this.eventListeners[event] = [];
        }
        this.eventListeners[event].push(callback);
    }
}

// Usage
const dashboard = new DesktopDashboardConnection(
    'https://your-app.onrender.com',
    'your-jwt-token'
);

// Set up event listeners
dashboard.on('dashboardUpdate', (data) => {
    updateDashboardUI(data);
});

dashboard.on('agentStatusUpdate', (data) => {
    updateAgentStatus(data);
});

dashboard.on('taskCompleted', (data) => {
    showTaskCompletion(data);
});

dashboard.on('error', (error) => {
    showErrorNotification(error);
});

// Connect to dashboard
dashboard.connect().then(() => {
    console.log('Successfully connected to dashboard');
}).catch(error => {
    console.error('Failed to connect:', error);
});
```

### Secure Authentication Flow
```python
# secure_auth.py - Secure desktop authentication
import jwt
import time
import secrets
from typing import Dict, Optional
import hashlib
import hmac

class DesktopAuthenticator:
    def __init__(self, jwt_secret: str, token_expiry: int = 3600):
        self.jwt_secret = jwt_secret.encode()
        self.token_expiry = token_expiry
        self.active_sessions = {}

    def generate_desktop_token(self, desktop_id: str, permissions: list = None) -> str:
        """Generate a JWT token for desktop authentication"""
        if permissions is None:
            permissions = ['read', 'dashboard']

        payload = {
            'iss': 'paperclip-dashboard',
            'sub': desktop_id,
            'iat': int(time.time()),
            'exp': int(time.time()) + self.token_expiry,
            'type': 'desktop',
            'permissions': permissions,
            'session_id': secrets.token_hex(16)
        }

        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')

        # Store session info
        self.active_sessions[payload['session_id']] = {
            'desktop_id': desktop_id,
            'permissions': permissions,
            'created_at': payload['iat'],
            'expires_at': payload['exp']
        }

        return token

    def validate_desktop_token(self, token: str) -> Optional[Dict]:
        """Validate a desktop JWT token"""
        try:
            # Decode and verify token
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])

            # Check token type
            if payload.get('type') != 'desktop':
                return None

            # Check if session is still active
            session_id = payload.get('session_id')
            if session_id not in self.active_sessions:
                return None

            session = self.active_sessions[session_id]

            # Check if session hasn't expired
            if time.time() > session['expires_at']:
                del self.active_sessions[session_id]
                return None

            return {
                'desktop_id': payload['sub'],
                'permissions': payload.get('permissions', []),
                'session_id': session_id,
                'valid': True
            }

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def revoke_desktop_session(self, session_id: str) -> bool:
        """Revoke a desktop session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False

    def get_active_sessions(self) -> Dict:
        """Get all active desktop sessions"""
        # Clean up expired sessions
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if current_time > session['expires_at']
        ]

        for session_id in expired_sessions:
            del self.active_sessions[session_id]

        return self.active_sessions.copy()

class WebSocketAuthenticator:
    def __init__(self, auth_service: DesktopAuthenticator):
        self.auth_service = auth_service
        self.connections = {}

    def authenticate_connection(self, websocket, auth_header: str) -> Optional[Dict]:
        """Authenticate a WebSocket connection"""
        try:
            # Extract token from header
            if not auth_header.startswith('Bearer '):
                return None

            token = auth_header[7:]  # Remove 'Bearer ' prefix

            # Validate token
            auth_data = self.auth_service.validate_desktop_token(token)

            if not auth_data:
                return None

            # Store connection info
            connection_id = secrets.token_hex(8)
            self.connections[connection_id] = {
                'websocket': websocket,
                'auth_data': auth_data,
                'connected_at': time.time()
            }

            return {
                'connection_id': connection_id,
                **auth_data
            }

        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def check_permission(self, connection_id: str, required_permission: str) -> bool:
        """Check if connection has required permission"""
        if connection_id not in self.connections:
            return False

        permissions = self.connections[connection_id]['auth_data']['permissions']
        return required_permission in permissions

    def remove_connection(self, connection_id: str):
        """Remove a connection"""
        if connection_id in self.connections:
            del self.connections[connection_id]

# Flask-SocketIO authentication middleware
def authenticate_socket(socketio):
    @socketio.on('connect')
    def handle_connect(auth):
        if not auth or 'token' not in auth:
            return False

        token = auth['token']
        auth_result = ws_auth.authenticate_connection(request.sid, f"Bearer {token}")

        if not auth_result:
            return False

        # Store auth data in session
        session['auth'] = auth_result
        return True

    @socketio.on('disconnect')
    def handle_disconnect():
        connection_id = session.get('auth', {}).get('connection_id')
        if connection_id:
            ws_auth.remove_connection(connection_id)

# Usage
auth_service = DesktopAuthenticator('your-jwt-secret-key')
ws_auth = WebSocketAuthenticator(auth_service)

# Generate token for desktop app
desktop_token = auth_service.generate_desktop_token('desktop-123', ['read', 'write', 'dashboard'])

# In desktop app, use token for WebSocket connection
# const socket = io('https://your-app.onrender.com', {
#   auth: { token: desktop_token }
# });
```

### Data Synchronization Manager
```python
# data_sync.py - Bidirectional data synchronization
import json
import time
import threading
from typing import Dict, List, Callable, Any
from enum import Enum

class SyncDirection(Enum):
    DESKTOP_TO_CLOUD = "desktop_to_cloud"
    CLOUD_TO_DESKTOP = "cloud_to_desktop"
    BIDIRECTIONAL = "bidirectional"

class ConflictResolution(Enum):
    DESKTOP_WINS = "desktop_wins"
    CLOUD_WINS = "cloud_wins"
    MANUAL = "manual"
    TIMESTAMP = "timestamp"

class DataSynchronizationManager:
    def __init__(self, connection_manager, conflict_resolution=ConflictResolution.TIMESTAMP):
        self.connection_manager = connection_manager
        self.conflict_resolution = conflict_resolution
        self.sync_handlers = {}
        self.pending_changes = {}
        self.last_sync_timestamps = {}
        self.sync_lock = threading.Lock()

        # Set up sync message handlers
        self.setup_sync_handlers()

    def setup_sync_handlers(self):
        """Set up handlers for sync messages"""
        self.connection_manager.on('sync_request', self.handle_sync_request)
        self.connection_manager.on('sync_response', self.handle_sync_response)
        self.connection_manager.on('data_change', self.handle_data_change)

    def register_sync_handler(self, data_type: str, handler: Callable, direction: SyncDirection = SyncDirection.BIDIRECTIONAL):
        """Register a data synchronization handler"""
        self.sync_handlers[data_type] = {
            'handler': handler,
            'direction': direction
        }

    def sync_data(self, data_type: str, data: Any, source: str = 'desktop'):
        """Sync data between desktop and cloud"""
        with self.sync_lock:
            timestamp = time.time()

            sync_message = {
                'type': 'data_change',
                'data_type': data_type,
                'data': data,
                'timestamp': timestamp,
                'source': source,
                'change_id': f"{data_type}_{timestamp}_{hash(str(data))}"
            }

            # Store pending change
            if data_type not in self.pending_changes:
                self.pending_changes[data_type] = []

            self.pending_changes[data_type].append(sync_message)

            # Send to cloud if connected
            if self.connection_manager.is_connected:
                self.connection_manager.send(sync_message)
            else:
                # Queue for later when connection is restored
                self.queue_offline_change(sync_message)

    def handle_data_change(self, message):
        """Handle incoming data change from other side"""
        data_type = message['data_type']
        source = message['source']
        timestamp = message['timestamp']

        # Check for conflicts
        if self.has_conflict(data_type, timestamp):
            resolved_data = self.resolve_conflict(data_type, message)
        else:
            resolved_data = message['data']

        # Apply the change locally
        if data_type in self.sync_handlers:
            handler = self.sync_handlers[data_type]['handler']
            try:
                handler(resolved_data, source)
                self.last_sync_timestamps[data_type] = timestamp
            except Exception as e:
                print(f"Error applying sync change for {data_type}: {e}")

    def has_conflict(self, data_type: str, incoming_timestamp: float) -> bool:
        """Check if there's a conflict with incoming change"""
        last_sync = self.last_sync_timestamps.get(data_type, 0)
        return incoming_timestamp > last_sync and data_type in self.pending_changes

    def resolve_conflict(self, data_type: str, incoming_message: Dict) -> Any:
        """Resolve data conflicts based on strategy"""
        pending_changes = self.pending_changes.get(data_type, [])

        if self.conflict_resolution == ConflictResolution.DESKTOP_WINS:
            # Keep local changes, ignore incoming
            return None
        elif self.conflict_resolution == ConflictResolution.CLOUD_WINS:
            # Accept incoming changes, discard local
            self.pending_changes[data_type] = []
            return incoming_message['data']
        elif self.conflict_resolution == ConflictResolution.TIMESTAMP:
            # Use most recent change
            incoming_time = incoming_message['timestamp']
            local_time = max([c['timestamp'] for c in pending_changes]) if pending_changes else 0

            if incoming_time > local_time:
                self.pending_changes[data_type] = []
                return incoming_message['data']
            else:
                return None  # Keep local
        else:  # MANUAL
            # Queue for manual resolution
            self.queue_conflict_for_resolution(data_type, incoming_message)
            return None

    def handle_sync_request(self, message):
        """Handle sync request from other side"""
        requested_types = message.get('data_types', list(self.sync_handlers.keys()))

        sync_data = {}
        for data_type in requested_types:
            if data_type in self.last_sync_timestamps:
                # Get current state for this data type
                current_data = self.get_current_data_state(data_type)
                sync_data[data_type] = {
                    'data': current_data,
                    'timestamp': self.last_sync_timestamps[data_type]
                }

        # Send sync response
        self.connection_manager.send({
            'type': 'sync_response',
            'request_id': message.get('request_id'),
            'sync_data': sync_data
        })

    def handle_sync_response(self, message):
        """Handle sync response with current state"""
        sync_data = message.get('sync_data', {})

        for data_type, data_info in sync_data.items():
            incoming_timestamp = data_info['timestamp']

            # Check if we need to update
            if incoming_timestamp > self.last_sync_timestamps.get(data_type, 0):
                # Apply the data
                if data_type in self.sync_handlers:
                    handler = self.sync_handlers[data_type]['handler']
                    try:
                        handler(data_info['data'], 'sync_response')
                        self.last_sync_timestamps[data_type] = incoming_timestamp
                    except Exception as e:
                        print(f"Error applying sync response for {data_type}: {e}")

    def request_full_sync(self, data_types: List[str] = None):
        """Request full synchronization from cloud"""
        if data_types is None:
            data_types = list(self.sync_handlers.keys())

        self.connection_manager.send({
            'type': 'sync_request',
            'request_id': f"sync_{int(time.time())}",
            'data_types': data_types
        })

    def queue_offline_change(self, change_message):
        """Queue changes made while offline"""
        # In a real implementation, this would persist to disk
        # For now, just keep in memory
        pass

    def process_offline_changes(self):
        """Process queued offline changes when connection is restored"""
        # Send all queued changes
        for data_type, changes in self.pending_changes.items():
            for change in changes:
                self.connection_manager.send(change)

        # Clear processed changes
        self.pending_changes.clear()

    def get_current_data_state(self, data_type: str) -> Any:
        """Get current local state for a data type"""
        # This would be implemented by the application
        # to return current state of specific data types
        return None

    def queue_conflict_for_resolution(self, data_type: str, incoming_message: Dict):
        """Queue conflict for manual resolution"""
        # In a real app, this would notify the user
        print(f"CONFLICT: Manual resolution needed for {data_type}")
        print(f"Incoming: {incoming_message}")

# Usage
sync_manager = DataSynchronizationManager(dashboard_connection)

# Register sync handlers for different data types
sync_manager.register_sync_handler('agents', handle_agent_sync)
sync_manager.register_sync_handler('tasks', handle_task_sync)
sync_manager.register_sync_handler('companies', handle_company_sync)

# Sync data changes
def on_agent_updated(agent_data):
    sync_manager.sync_data('agents', agent_data)

def on_task_completed(task_data):
    sync_manager.sync_data('tasks', task_data)

# Handle incoming sync messages
def handle_agent_sync(agent_data, source):
    # Update local agent data
    update_local_agents(agent_data)

def handle_task_sync(task_data, source):
    # Update local task data
    update_local_tasks(task_data)

def handle_company_sync(company_data, source):
    # Update local company data
    update_local_companies(company_data)
```

## Troubleshooting Common Issues

### Connection Failures
1. **Network Issues**
   ```bash
   # Check network connectivity
   ping your-app.onrender.com
   traceroute your-app.onrender.com
   ```

2. **Firewall Blocking**
   ```bash
   # Check firewall rules
   sudo ufw status
   sudo iptables -L
   ```

3. **SSL Certificate Problems**
   ```bash
   # Verify SSL certificate
   openssl s_client -connect your-app.onrender.com:443
   ```

### Authentication Issues
1. **Token Expiration**
   ```bash
   # Check token expiry
   jwt decode your-token --json | jq '.exp'
   ```

2. **Invalid Permissions**
   ```bash
   # Verify token permissions
   jwt decode your-token | jq '.permissions'
   ```

3. **Session Management**
   ```bash
   # Check active sessions
   curl https://your-app.onrender.com/api/sessions
   ```

### Synchronization Problems
1. **Data Conflicts**
   ```bash
   # Check conflict resolution strategy
   # Implement proper conflict handling
   ```

2. **Network Latency**
   ```bash
   # Monitor connection latency
   ping -c 10 your-app.onrender.com
   ```

3. **Offline Queue**
   ```bash
   # Check offline change queue
   # Implement proper offline handling
   ```

## Security Considerations

### Communication Security
- **End-to-End Encryption**: Ensure all communication is encrypted
- **Certificate Validation**: Validate SSL certificates properly
- **Secure WebSocket**: Use WSS (WebSocket Secure) for WebSocket connections
- **Token Security**: Implement proper JWT token handling

### Access Control
- **Role-Based Permissions**: Implement granular access control
- **Session Limits**: Limit concurrent sessions per user
- **Rate Limiting**: Implement rate limiting for API calls
- **Audit Logging**: Log all connection and data access events

## Integration Points

### Internal InfraForge AI
- **Database Agent**: Coordinates data synchronization
- **Security Agent**: Works with authentication and encryption
- **Monitoring Agent**: Integrates with connection monitoring

### Cross-Company Integration
- **DevForge AI**: Collaborates on desktop application connectivity
- **PaperclipForge AI**: Works with dashboard communication requirements
- **QualityForge AI**: Partners on connectivity testing and validation

## Success Metrics

- **Connection Success**: ≥99% successful desktop-to-dashboard connections
- **Data Sync Accuracy**: ≥99.9% data synchronization accuracy
- **Real-time Latency**: <500ms average real-time update latency
- **Offline Recovery**: ≥95% successful offline data synchronization

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
