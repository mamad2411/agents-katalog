---
name: security-best-practices
description: Implement security best practices including authentication, authorization, input validation, and security patterns. Use when implementing security features, handling authentication, or when the user asks about security, authentication, authorization, or security vulnerabilities.
---

# Security Best Practices

Implement comprehensive security measures to protect applications and user data.

## Authentication

### Password Hashing

```typescript
import bcrypt from "bcrypt";

// Hash password
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
}

// Verify password
async function verifyPassword(
  password: string,
  hash: string,
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Usage
const hashedPassword = await hashPassword("userPassword123");
const isValid = await verifyPassword("userPassword123", hashedPassword);
```

### JWT Tokens

```typescript
import jwt from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET!;
const JWT_EXPIRES_IN = "15m";
const REFRESH_TOKEN_EXPIRES_IN = "7d";

// Generate tokens
function generateTokens(userId: number) {
  const accessToken = jwt.sign({ userId, type: "access" }, JWT_SECRET, {
    expiresIn: JWT_EXPIRES_IN,
  });

  const refreshToken = jwt.sign({ userId, type: "refresh" }, JWT_SECRET, {
    expiresIn: REFRESH_TOKEN_EXPIRES_IN,
  });

  return { accessToken, refreshToken };
}

// Verify token
function verifyToken(token: string): { userId: number } {
  try {
    return jwt.verify(token, JWT_SECRET) as { userId: number };
  } catch (error) {
    throw new UnauthorizedError("Invalid token");
  }
}
```

### Refresh Token Rotation

```typescript
async function refreshAccessToken(refreshToken: string) {
  // Verify refresh token
  const decoded = verifyToken(refreshToken);

  // Check if token exists in database
  const tokenRecord = await RefreshToken.findOne({
    where: { token: refreshToken, userId: decoded.userId },
  });

  if (!tokenRecord || tokenRecord.expiresAt < new Date()) {
    throw new UnauthorizedError("Invalid refresh token");
  }

  // Generate new tokens
  const { accessToken, refreshToken: newRefreshToken } = generateTokens(
    decoded.userId,
  );

  // Revoke old refresh token
  await tokenRecord.destroy();

  // Store new refresh token
  await RefreshToken.create({
    userId: decoded.userId,
    token: newRefreshToken,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  });

  return { accessToken, refreshToken: newRefreshToken };
}
```

## Authorization

### Role-Based Access Control (RBAC)

```typescript
// Middleware for role checking
export const requireRole = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = (req as AuthenticatedRequest).user;

    if (!user) {
      throw new UnauthorizedError();
    }

    if (!roles.includes(user.role)) {
      throw new ForbiddenError("Insufficient permissions");
    }

    next();
  };
};

// Usage
router.get("/admin/users", requireRole("admin"), getUsers);
router.delete("/users/:id", requireRole("admin", "moderator"), deleteUser);
```

### Permission-Based Access Control

```typescript
interface Permission {
  resource: string;
  action: string;
}

// Check permissions
async function hasPermission(
  userId: number,
  permission: Permission,
): Promise<boolean> {
  const user = await User.findByPk(userId, {
    include: [{ model: Role, include: [{ model: Permission }] }],
  });

  if (!user) return false;

  return user.roles.some((role) =>
    role.permissions.some(
      (p) =>
        p.resource === permission.resource && p.action === permission.action,
    ),
  );
}

// Middleware
export const requirePermission = (resource: string, action: string) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = (req as AuthenticatedRequest).user;

    if (!user) {
      throw new UnauthorizedError();
    }

    const hasAccess = await hasPermission(user.id, { resource, action });
    if (!hasAccess) {
      throw new ForbiddenError("Insufficient permissions");
    }

    next();
  };
};
```

## Input Validation & Sanitization

### Validate All Inputs

```typescript
import { z } from "zod";

// Define schema
const createUserSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain uppercase letter")
    .regex(/[a-z]/, "Password must contain lowercase letter")
    .regex(/[0-9]/, "Password must contain number"),
  name: z.string().min(1, "Name is required").max(100, "Name too long"),
  age: z.number().int().min(0).max(150).optional(),
});

// Validate
function validateCreateUser(data: unknown) {
  return createUserSchema.parse(data);
}
```

### Sanitize Inputs

```typescript
import DOMPurify from "isomorphic-dompurify";

// Sanitize HTML
function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html);
}

// Sanitize user input
function sanitizeInput(input: string): string {
  return input
    .trim()
    .replace(/[<>]/g, "") // Remove HTML brackets
    .substring(0, 1000); // Limit length
}
```

### SQL Injection Prevention

```typescript
// ✅ Good - Use parameterized queries (Sequelize does this automatically)
const user = await User.findOne({
  where: { email: userEmail }, // Safe - parameterized
});

// ❌ Bad - Never use string concatenation
// const query = `SELECT * FROM users WHERE email = '${userEmail}'`; // DANGEROUS
```

## Security Headers

### Set Security Headers

```typescript
import helmet from "helmet";

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", "data:", "https:"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true,
    },
  }),
);
```

## Rate Limiting

### Implement Rate Limiting

```typescript
import rateLimit from "express-rate-limit";

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again later",
});

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Limit each IP to 5 requests per windowMs
  skipSuccessfulRequests: true,
});

// Apply
app.use("/api/", apiLimiter);
app.use("/api/auth/", authLimiter);
```

## CORS Configuration

### Secure CORS Setup

```typescript
import cors from "cors";

app.use(
  cors({
    origin: (origin, callback) => {
      const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(",") || [];
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true,
    optionsSuccessStatus: 200,
  }),
);
```

## Secrets Management

### Environment Variables

```typescript
// Never commit secrets
// Use .env file (in .gitignore)
// JWT_SECRET=your-secret-key
// DB_PASSWORD=your-db-password

// Validate required env vars
function validateEnv() {
  const required = ["JWT_SECRET", "DB_PASSWORD", "API_KEY"];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}`,
    );
  }
}
```

### Secure Configuration

```typescript
// config/security.ts
export const securityConfig = {
  jwt: {
    secret: process.env.JWT_SECRET!,
    expiresIn: process.env.JWT_EXPIRES_IN || "15m",
  },
  bcrypt: {
    saltRounds: parseInt(process.env.BCRYPT_SALT_ROUNDS || "12"),
  },
  cors: {
    allowedOrigins: process.env.ALLOWED_ORIGINS?.split(",") || [],
  },
};
```

## XSS Prevention

### Sanitize Output

```typescript
// Escape HTML in responses
function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

// Use in templates
const safeOutput = escapeHtml(userInput);
```

## CSRF Protection

### CSRF Tokens

```typescript
import csrf from "csurf";

const csrfProtection = csrf({ cookie: true });

// Generate token
app.get("/api/csrf-token", csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Protect routes
app.post("/api/users", csrfProtection, createUser);
```

## Best Practices

1. **Hash passwords** - Never store plain text passwords
2. **Use HTTPS** - Encrypt data in transit
3. **Validate all inputs** - Never trust client data
4. **Sanitize outputs** - Prevent XSS attacks
5. **Use parameterized queries** - Prevent SQL injection
6. **Implement rate limiting** - Prevent abuse
7. **Set security headers** - Use Helmet.js
8. **Rotate secrets** - Change keys regularly
9. **Use least privilege** - Grant minimum necessary permissions
10. **Log security events** - Monitor for suspicious activity
11. **Keep dependencies updated** - Patch vulnerabilities
12. **Use secure session management** - HttpOnly, Secure cookies

## When Implementing Security

1. **Authenticate users** - Verify identity
2. **Authorize actions** - Check permissions
3. **Validate inputs** - Check all user data
4. **Sanitize outputs** - Escape dangerous content
5. **Use HTTPS** - Encrypt communications
6. **Set security headers** - Protect against common attacks
7. **Implement rate limiting** - Prevent abuse
8. **Log security events** - Monitor for threats
9. **Keep secrets secure** - Use environment variables
10. **Update dependencies** - Patch vulnerabilities regularly
