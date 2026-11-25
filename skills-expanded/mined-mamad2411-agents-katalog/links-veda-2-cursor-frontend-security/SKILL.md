# Frontend Security Cursor Rules

## Cross-Site Scripting (XSS) Prevention

### Input Sanitization
```javascript
// ❌ NEVER use dangerouslySetInnerHTML with user input
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Use textContent for plain text
<div>{userInput}</div>

// ✅ Sanitize HTML if needed
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### React Security Patterns
```javascript
// ✅ React automatically escapes by default
function UserProfile({ user }) {
  return (
    <div>
      <h1>{user.name}</h1> {/* Safe - React escapes */}
      <p>{user.bio}</p>     {/* Safe - React escapes */}
    </div>
  );
}

// ❌ Avoid direct DOM manipulation
useEffect(() => {
  element.innerHTML = userInput; // Dangerous
}, []);

// ✅ Use React patterns
useEffect(() => {
  element.textContent = userInput; // Safe
}, []);
```

### Content Security Policy (CSP)
```html
<!-- Implement strict CSP -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' data: https:;">
```

## Cross-Site Request Forgery (CSRF) Protection

### SameSite Cookie Configuration
```javascript
// ✅ Secure cookie settings
document.cookie = "sessionId=abc123; SameSite=Lax; Secure; HttpOnly";

// For API calls, use SameSite=Strict for sensitive operations
document.cookie = "csrfToken=xyz789; SameSite=Strict; Secure; HttpOnly";
```

### CSRF Token Implementation
```javascript
// ✅ Include CSRF token in forms
function LoginForm() {
  const [csrfToken, setCsrfToken] = useState('');
  
  useEffect(() => {
    // Fetch CSRF token from server
    fetch('/api/csrf-token')
      .then(res => res.json())
      .then(data => setCsrfToken(data.token));
  }, []);
  
  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="csrfToken" value={csrfToken} />
      {/* other form fields */}
    </form>
  );
}

// ✅ Include CSRF token in API calls
const apiCall = async (data) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrfToken='))
    ?.split('=')[1];
    
  return fetch('/api/endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify(data)
  });
};
```

## Authentication & Session Security

### Secure Token Storage
```javascript
// ❌ NEVER store sensitive tokens in localStorage
localStorage.setItem('jwt', token); // Vulnerable to XSS

// ✅ Use httpOnly cookies for sensitive tokens
// Set by server: Set-Cookie: jwt=token; HttpOnly; Secure; SameSite=Lax

// ✅ For client-side tokens, use memory storage
class TokenManager {
  constructor() {
    this.token = null;
  }
  
  setToken(token) {
    this.token = token;
  }
  
  getToken() {
    return this.token;
  }
  
  clearToken() {
    this.token = null;
  }
}
```

### JWT Security
```javascript
// ✅ Validate JWT properly
function validateJWT(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    
    // Check expiration
    if (payload.exp < Date.now() / 1000) {
      throw new Error('Token expired');
    }
    
    // Check issuer
    if (payload.iss !== 'your-app') {
      throw new Error('Invalid issuer');
    }
    
    // Check audience
    if (payload.aud !== 'your-api') {
      throw new Error('Invalid audience');
    }
    
    return payload;
  } catch (error) {
    throw new Error('Invalid token');
  }
}
```

## Input Validation & Sanitization

### Client-Side Validation
```javascript
// ✅ Validate all inputs
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePassword(password) {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
}

function sanitizeInput(input) {
  return input
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .trim()
    .substring(0, 1000); // Limit length
}
```

### File Upload Security
```javascript
// ✅ Secure file upload validation
function validateFile(file) {
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (!allowedTypes.includes(file.type)) {
    throw new Error('File type not allowed');
  }
  
  if (file.size > maxSize) {
    throw new Error('File too large');
  }
  
  // Additional validation
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.pdf'];
  const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
  
  if (!allowedExtensions.includes(fileExtension)) {
    throw new Error('Invalid file extension');
  }
  
  return true;
}
```

## HTTPS & Transport Security

### Force HTTPS
```javascript
// ✅ Redirect HTTP to HTTPS
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
  location.replace('https:' + window.location.href.substring(window.location.protocol.length));
}

// ✅ Use secure WebSocket connections
const ws = new WebSocket('wss://api.example.com/ws');
```

### Mixed Content Prevention
```javascript
// ❌ Never load HTTP resources over HTTPS
<img src="http://example.com/image.jpg" /> // Mixed content

// ✅ Always use HTTPS
<img src="https://example.com/image.jpg" />
```

## CORS & Cross-Origin Security

### CORS Configuration
```javascript
// ✅ Proper CORS handling
const corsOptions = {
  origin: ['https://app.example.com', 'https://admin.example.com'],
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token']
};
```

### PostMessage Security
```javascript
// ✅ Secure postMessage communication
function handleMessage(event) {
  // Always validate origin
  const allowedOrigins = ['https://trusted-site.com'];
  
  if (!allowedOrigins.includes(event.origin)) {
    console.warn('Rejected message from untrusted origin:', event.origin);
    return;
  }
  
  // Validate message structure
  if (typeof event.data !== 'object' || !event.data.type) {
    console.warn('Invalid message format');
    return;
  }
  
  // Process message
  processMessage(event.data);
}

window.addEventListener('message', handleMessage);
```

## iframe Security

### Clickjacking Protection
```javascript
// ✅ Prevent clickjacking
function preventClickjacking() {
  if (window !== window.top) {
    // Running in iframe - check if allowed
    const allowedFraming = window.location.search.includes('allowFraming=true');
    if (!allowedFraming) {
      document.body.innerHTML = 'This page cannot be displayed in a frame.';
    }
  }
}

// ✅ Secure iframe sandboxing
<iframe 
  src="https://trusted-site.com" 
  sandbox="allow-scripts allow-same-origin"
  allow="camera; microphone"
/>
```

## Error Handling & Information Disclosure

### Secure Error Messages
```javascript
// ❌ Don't expose sensitive information
function handleError(error) {
  console.error('Database error:', error.sql); // Exposes SQL
  return { error: error.message }; // Exposes internal details
}

// ✅ Generic error messages for users
function handleError(error) {
  // Log detailed error internally
  console.error('Application error:', {
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString()
  });
  
  // Return generic message to user
  return { 
    error: 'An error occurred. Please try again.',
    requestId: generateRequestId() // For support correlation
  };
}
```

## Security Headers

### Implement Security Headers
```javascript
// ✅ Set security headers
const securityHeaders = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()'
};

// Apply headers to responses
Object.entries(securityHeaders).forEach(([key, value]) => {
  response.setHeader(key, value);
});
```

## Rate Limiting & DDoS Protection

### Client-Side Rate Limiting
```javascript
// ✅ Implement client-side rate limiting
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }
  
  canMakeRequest() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.windowMs);
    
    if (this.requests.length >= this.maxRequests) {
      return false;
    }
    
    this.requests.push(now);
    return true;
  }
}

const apiLimiter = new RateLimiter(10, 60000); // 10 requests per minute

function makeAPICall() {
  if (!apiLimiter.canMakeRequest()) {
    throw new Error('Rate limit exceeded');
  }
  // Make API call
}
```

## Dependency Security

### Secure Package Management
```javascript
// ✅ Use package-lock.json
// ✅ Regular security audits
// npm audit
// npm audit fix

// ✅ Use trusted packages only
// Check package reputation, maintenance, and security history
// Avoid packages with known vulnerabilities
```

## Monitoring & Logging

### Security Event Logging
```javascript
// ✅ Log security events
function logSecurityEvent(event, details) {
  const securityLog = {
    timestamp: new Date().toISOString(),
    event: event,
    details: details,
    userAgent: navigator.userAgent,
    url: window.location.href,
    userId: getCurrentUserId()
  };
  
  // Send to security monitoring system
  fetch('/api/security-log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(securityLog)
  });
}

// Usage
logSecurityEvent('login_attempt', { success: true });
logSecurityEvent('suspicious_activity', { action: 'multiple_failed_logins' });
```

## React-Specific Security Patterns

### Props Validation
```javascript
// ✅ Use PropTypes for runtime validation
import PropTypes from 'prop-types';

function UserCard({ user, onEdit }) {
  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}

UserCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired
  }).isRequired,
  onEdit: PropTypes.func.isRequired
};
```

### State Management Security
```javascript
// ✅ Secure state updates
const [userData, setUserData] = useState(null);

// ❌ Don't directly mutate state
userData.name = newName; // Dangerous

// ✅ Use immutable updates
setUserData(prevData => ({
  ...prevData,
  name: newName
}));
```

### Event Handler Security
```javascript
// ✅ Secure event handlers
function handleFormSubmit(event) {
  event.preventDefault();
  
  // Validate form data
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  
  // Sanitize inputs
  const sanitizedData = {
    username: sanitizeInput(data.username),
    email: sanitizeInput(data.email)
  };
  
  // Submit data
  submitUserData(sanitizedData);
}
```

## URL Security

### URL Validation
```javascript
// ✅ Validate URLs before using
function isValidUrl(string) {
  try {
    const url = new URL(string);
    return ['http:', 'https:'].includes(url.protocol);
  } catch (_) {
    return false;
  }
}

// ✅ Sanitize URLs
function sanitizeUrl(url) {
  try {
    const parsed = new URL(url);
    // Only allow specific protocols
    if (!['https:', 'http:'].includes(parsed.protocol)) {
      throw new Error('Invalid protocol');
    }
    return parsed.toString();
  } catch (error) {
    throw new Error('Invalid URL');
  }
}
```

## Local Storage Security

### Secure Local Storage Usage
```javascript
// ✅ Encrypt sensitive data before storing
import CryptoJS from 'crypto-js';

const SECRET_KEY = process.env.REACT_APP_STORAGE_SECRET;

function setSecureStorage(key, value) {
  const encrypted = CryptoJS.AES.encrypt(JSON.stringify(value), SECRET_KEY).toString();
  localStorage.setItem(key, encrypted);
}

function getSecureStorage(key) {
  const encrypted = localStorage.getItem(key);
  if (!encrypted) return null;
  
  try {
    const decrypted = CryptoJS.AES.decrypt(encrypted, SECRET_KEY);
    return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
  } catch (error) {
    console.error('Failed to decrypt storage data:', error);
    return null;
  }
}
```

## Content Security Policy Implementation

### CSP Meta Tag
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' 'unsafe-eval';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;
               font-src 'self' data:;
               connect-src 'self' https://api.example.com;
               frame-ancestors 'none';
               base-uri 'self';
               form-action 'self';">
```

### CSP Nonce Implementation
```javascript
// ✅ Use nonces for inline scripts
const nonce = generateNonce(); // Generate server-side

// Inline script with nonce
<script nonce={nonce}>
  // Inline JavaScript code
</script>

// External script with nonce
<script src="/script.js" nonce={nonce}></script>
```

## WebSocket Security

### Secure WebSocket Connection
```javascript
// ✅ Secure WebSocket implementation
class SecureWebSocket {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.ws = null;
  }
  
  connect() {
    // Validate URL
    if (!isValidUrl(this.url)) {
      throw new Error('Invalid WebSocket URL');
    }
    
    // Add authentication token to URL
    const wsUrl = `${this.url}?token=${this.token}`;
    
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (error) {
        console.error('Invalid WebSocket message:', error);
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
  
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}
```
