# Backend Security Cursor Rules

## Injection Attack Prevention

### SQL Injection Prevention
```javascript
// ❌ NEVER concatenate user input into SQL
const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
db.query(query);

// ✅ Use parameterized queries
const query = "SELECT * FROM users WHERE username = ? AND password = ?";
db.query(query, [username, password]);

// ✅ Use ORM with proper escaping
const user = await User.findOne({
	where: { username: username, password: password },
});

// ✅ Additional validation
function validateUserInput(input) {
	if (typeof input !== "string") {
		throw new Error("Invalid input type");
	}
	if (input.length > 100) {
		throw new Error("Input too long");
	}
	return input.trim();
}
```

### NoSQL Injection Prevention
```;
javascript;
// ❌ Vulnerable to NoSQL injection
const { username, password } = req.body;
const user = await db.collection("users").findOne({ username, password });

// ✅ Secure - Type validation and explicit operators
const username = String(req.body.username ?? "");
const password = String(req.body.password ?? "");
const user = await db.collection("users").findOne({
	username: { $eq: username },
	password: { $eq: password },
});

// ✅ Additional validation
function sanitizeMongoQuery(query) {
	// Remove dangerous operators
	const dangerousOps = ["$where", "$regex", "$ne", "$gt", "$lt", "$in", "$nin"];
	for (const op of dangerousOps) {
		if (query[op]) {
			throw new Error(`Dangerous operator ${op} not allowed`);
		}
	}
	return query;
}
```

### Command Injection Prevention
```;
javascript;
// ❌ Dangerous - user input in system commands
exec(`cat ${filename}`, callback);

// ✅ Secure - Input validation + no shell
const validName = /^[\w.-]+$/;
if (!validName.test(filename)) {
	throw new Error("Invalid filename");
}
const cat = spawn("cat", [filename], { shell: false });

// ✅ Use whitelist approach
const ALLOWED_COMMANDS = ["ls", "cat", "grep"];
function executeCommand(command, args) {
	if (!ALLOWED_COMMANDS.includes(command)) {
		throw new Error("Command not allowed");
	}
	return spawn(command, args, { shell: false });
}
```

## Authentication & Authorization

### JWT Security Implementation
```;
javascript;
// ✅ Secure JWT implementation
const jwt = require("jsonwebtoken");

function generateJWT(payload) {
	return jwt.sign(payload, process.env.JWT_SECRET, {
		algorithm: "HS256", // Never use 'none'
		expiresIn: "1h",
		issuer: "your-app",
		audience: "your-api",
	});
}

function verifyJWT(token) {
	try {
		const decoded = jwt.verify(token, process.env.JWT_SECRET, {
			algorithms: ["HS256"], // Whitelist algorithms
			issuer: "your-app",
			audience: "your-api",
		});
		return decoded;
	} catch (error) {
		throw new Error("Invalid token");
	}
}

// ✅ JWT middleware
function authenticateToken(req, res, next) {
	const authHeader = req.headers["authorization"];
	const token = authHeader && authHeader.split(" ")[1];

	if (!token) {
		return res.status(401).json({ error: "Access token required" });
	}

	try {
		const user = verifyJWT(token);
		req.user = user;
		next();
	} catch (error) {
		return res.status(403).json({ error: "Invalid token" });
	}
}
```

### Session Management
```;
javascript;
// ✅ Secure session configuration
const session = require("express-session");
const RedisStore = require("connect-redis")(session);

app.use(
	session({
		store: new RedisStore({ client: redisClient }),
		secret: process.env.SESSION_SECRET,
		resave: false,
		saveUninitialized: false,
		cookie: {
			secure: process.env.NODE_ENV === "production",
			httpOnly: true,
			maxAge: 30 * 60 * 1000, // 30 minutes
			sameSite: "lax",
		},
	}),
);

// ✅ Session regeneration after login
app.post("/login", async (req, res) => {
	// Validate credentials
	const user = await validateCredentials(req.body);

	if (user) {
		// Regenerate session to prevent fixation
		req.session.regenerate((err) => {
			if (err) throw err;

			req.session.userId = user.id;
			req.session.save((err) => {
				if (err) throw err;
				res.json({ success: true });
			});
		});
	} else {
		res.status(401).json({ error: "Invalid credentials" });
	}
});
```

### Authorization Patterns
```;
javascript;
// ✅ Resource-based access control
class AuthorizationService {
	static async canAccess(user, resource, action) {
		if (!user || !user.permissions) return false;

		// Check resource ownership
		if (resource.ownerId && resource.ownerId !== user.id) {
			if (!user.permissions.includes("admin")) return false;
		}

		// Check specific action permissions
		const requiredPermission = `${resource.type}:${action}`;
		return user.permissions.includes(requiredPermission);
	}
}

// ✅ Usage in API endpoints
app.get("/api/documents/:id", authenticateToken, async (req, res) => {
	const document = await Document.findById(req.params.id);
	if (!document) return res.status(404).end();

	const canRead = await AuthorizationService.canAccess(
		req.user,
		document,
		"read",
	);

	if (!canRead) return res.status(403).end();

	res.json(document);
});
```

## Input Validation & Sanitization

### Comprehensive Input Validation
```;
javascript;
const Joi = require("joi");

// ✅ Define validation schemas
const userSchema = Joi.object({
	username: Joi.string().alphanum().min(3).max(30).required(),
	email: Joi.string().email().required(),
	password: Joi.string()
		.min(8)
		.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
		.required(),
	age: Joi.number().integer().min(13).max(120),
});

// ✅ Validation middleware
function validateInput(schema) {
	return (req, res, next) => {
		const { error, value } = schema.validate(req.body);
		if (error) {
			return res.status(400).json({
				error: "Validation failed",
				details: error.details,
			});
		}
		req.body = value; // Use validated data
		next();
	};
}

// ✅ Usage
app.post("/api/users", validateInput(userSchema), createUser);
```

### File Upload Security
```;
javascript;
const multer = require("multer");
const path = require("path");
const { v4: uuidv4 } = require("uuid");

// ✅ Secure file upload configuration
const storage = multer.diskStorage({
	destination: "/var/app/uploads", // Outside webroot
	filename: (req, file, cb) => {
		const ext = path.extname(file.originalname);
		cb(null, `${uuidv4()}${ext}`); // Randomize filename
	},
});

const upload = multer({
	storage,
	limits: {
		fileSize: 10 * 1024 * 1024, // 10MB max
		files: 5, // Max 5 files per request
	},
	fileFilter: (req, file, cb) => {
		const allowedTypes = [
			"image/jpeg",
			"image/png",
			"image/gif",
			"application/pdf",
			"text/plain",
		];

		if (allowedTypes.includes(file.mimetype)) {
			cb(null, true);
		} else {
			cb(new Error("File type not allowed"), false);
		}
	},
});

// ✅ Additional server-side validation
async function validateUploadedFile(filePath) {
	const fileType = await import("file-type");
	const type = await fileType.fromFile(filePath);

	const ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"];
	if (!type || !ALLOWED_TYPES.includes(type.mime)) {
		throw new Error("File type mismatch");
	}

	return true;
}
```

## Directory Traversal Prevention

### Secure Path Handling
```;
javascript;
const path = require("path");

const SAFE_BASE = path.resolve("/var/app/uploads");

function securePath(userPath) {
	// Resolve against base directory
	const fullPath = path.resolve(SAFE_BASE, userPath);

	// Ensure result is within safe directory
	if (!fullPath.startsWith(SAFE_BASE + path.sep)) {
		throw new Error("Path traversal attempt detected");
	}

	return fullPath;
}

// ✅ Additional validation
const ALLOWED_EXTENSIONS = new Set([".jpg", ".png", ".pdf"]);
function validateFileExtension(filename) {
	const ext = path.extname(filename).toLowerCase();
	return ALLOWED_EXTENSIONS.has(ext);
}

// ✅ Usage
app.get("/api/files/:filename", (req, res) => {
	try {
		const safePath = securePath(req.params.filename);
		const ext = path.extname(safePath);

		if (!validateFileExtension(safePath)) {
			return res.status(400).json({ error: "Invalid file type" });
		}

		res.sendFile(safePath);
	} catch (error) {
		res.status(400).json({ error: "Invalid file path" });
	}
});
```

## Rate Limiting & DDoS Protection

### Multi-tier Rate Limiting
```;
javascript;
const rateLimit = require("express-rate-limit");
const slowDown = require("express-slow-down");

// ✅ Global rate limiting
const globalLimit = rateLimit({
	windowMs: 15 * 60 * 1000, // 15 minutes
	max: 1000, // Limit each IP to 1000 requests per windowMs
	message: "Too many requests from this IP",
	standardHeaders: true,
	legacyHeaders: false,
});

// ✅ API-specific stricter limits
const apiLimit = rateLimit({
	windowMs: 15 * 60 * 1000,
	max: 100,
	keyGenerator: (req) => `${req.ip}:${req.user?.id || "anonymous"}`,
	message: "API rate limit exceeded",
});

// ✅ Progressive delays for suspicious behavior
const speedLimiter = slowDown({
	windowMs: 15 * 60 * 1000,
	delayAfter: 50, // Allow 50 requests at full speed
	delayMs: 500, // Add 500ms delay per request after delayAfter
});

// ✅ Apply to routes
app.use("/api/", globalLimit, apiLimit, speedLimiter);
```

## Error Handling & Information Disclosure

### Secure Error Handling
```;
javascript;
// ❌ Dangerous - leaks internal information
app.use((err, req, res, next) => {
	res.status(500).json({
		error: err.message,
		stack: err.stack,
		query: req.query,
	});
});

// ✅ Secure error handling
app.use((err, req, res, next) => {
	// Log detailed error internally
	logger.error("Application error", {
		error: err.message,
		stack: err.stack,
		userId: req.user?.id,
		ip: req.ip,
		url: req.url,
		timestamp: new Date().toISOString(),
	});

	// Return generic error to client
	const isDevelopment = process.env.NODE_ENV === "development";

	res.status(err.status || 500).json({
		error: "An error occurred while processing your request",
		requestId: req.id, // For support correlation
		...(isDevelopment && { details: err.message }), // Only in dev
	});
});
```

## Security Headers

### Comprehensive Security Headers
```;
javascript;
const helmet = require("helmet");

// ✅ Use helmet for security headers
app.use(
	helmet({
		contentSecurityPolicy: {
			directives: {
				defaultSrc: ["'self'"],
				styleSrc: ["'self'", "'unsafe-inline'"],
				scriptSrc: ["'self'"],
				imgSrc: ["'self'", "data:", "https:"],
				connectSrc: ["'self'"],
				fontSrc: ["'self'"],
				objectSrc: ["'none'"],
				mediaSrc: ["'self'"],
				frameSrc: ["'none'"],
			},
		},
		crossOriginEmbedderPolicy: false,
		hsts: {
			maxAge: 31536000,
			includeSubDomains: true,
			preload: true,
		},
	}),
);

// ✅ Additional custom headers
app.use((req, res, next) => {
	res.setHeader("X-Content-Type-Options", "nosniff");
	res.setHeader("X-Frame-Options", "DENY");
	res.setHeader("X-XSS-Protection", "1; mode=block");
	res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
	res.setHeader(
		"Permissions-Policy",
		"camera=(), microphone=(), geolocation=()",
	);
	next();
});
```

## Database Security

### Connection Security
```;
javascript;
// ✅ Secure database connection
const { Pool } = require("pg");

const pool = new Pool({
	host: process.env.DB_HOST,
	port: process.env.DB_PORT,
	database: process.env.DB_NAME,
	user: process.env.DB_USER,
	password: process.env.DB_PASSWORD,
	ssl: {
		rejectUnauthorized: true,
		ca: process.env.DB_SSL_CA,
	},
	max: 20, // Connection pool size
	idleTimeoutMillis: 30000,
	connectionTimeoutMillis: 2000,
});

// ✅ Connection error handling
pool.on("error", (err) => {
	logger.error("Unexpected error on idle client", err);
	process.exit(-1);
});
```

### Query Security
```;
javascript;
// ✅ Always use parameterized queries
async function getUserById(id) {
	const query = "SELECT id, username, email FROM users WHERE id = $1";
	const result = await pool.query(query, [id]);
	return result.rows[0];
}

// ✅ Input validation for database queries
function validateId(id) {
	const numId = Number.parseInt(id);
	if (isNaN(numId) || numId <= 0) {
		throw new Error("Invalid ID");
	}
	return numId;
}
```

## Logging & Monitoring

### Security Event Logging
```;
javascript;
const winston = require("winston");

// ✅ Configure security logging
const securityLogger = winston.createLogger({
	level: "info",
	format: winston.format.combine(
		winston.format.timestamp(),
		winston.format.json(),
	),
	transports: [
		new winston.transports.File({ filename: "security.log" }),
		new winston.transports.Console(),
	],
});

// ✅ Log security events
function logSecurityEvent(event, details, req) {
	securityLogger.info("Security event", {
		event,
		details,
		ip: req.ip,
		userAgent: req.get("User-Agent"),
		userId: req.user?.id,
		timestamp: new Date().toISOString(),
		url: req.url,
		method: req.method,
	});
}

// ✅ Usage
app.post("/api/login", (req, res) => {
	// ... authentication logic
	if (success) {
		logSecurityEvent("login_success", { userId: user.id }, req);
	} else {
		logSecurityEvent("login_failed", { username: req.body.username }, req);
	}
});
```

## CORS Configuration

### Secure CORS Setup
```;
javascript;
const cors = require("cors");

// ✅ Secure CORS configuration
const corsOptions = {
	origin: (origin, callback) => {
		const allowedOrigins = [
			"https://app.example.com",
			"https://admin.example.com",
		];

		// Allow requests with no origin (mobile apps, etc.)
		if (!origin) return callback(null, true);

		if (allowedOrigins.includes(origin)) {
			callback(null, true);
		} else {
			callback(new Error("Not allowed by CORS"));
		}
	},
	credentials: true,
	optionsSuccessStatus: 200,
	methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
	allowedHeaders: ["Content-Type", "Authorization", "X-CSRF-Token"],
	exposedHeaders: ["X-Total-Count"],
};

app.use(cors(corsOptions));
```

## WebSocket Security

### Secure WebSocket Implementation
```;
javascript;
const WebSocket = require("ws");

// ✅ Secure WebSocket server
const wss = new WebSocket.Server({
	port: 8080,
	verifyClient: (info) => {
		// Validate origin
		const allowedOrigins = ["https://app.example.com"];
		return allowedOrigins.includes(info.origin);
	},
});

wss.on("connection", (ws, req) => {
	// Validate authentication
	const token = req.url.split("token=")[1];
	if (!verifyJWT(token)) {
		ws.close(1008, "Authentication required");
		return;
	}

	// Set up message validation
	ws.on("message", (data) => {
		try {
			const message = JSON.parse(data);
			validateWebSocketMessage(message);
			// Process message
		} catch (error) {
			ws.send(JSON.stringify({ error: "Invalid message format" }));
		}
	});

	// Set idle timeout
	ws.idleTimeout = setTimeout(
		() => {
			ws.close(1000, "Idle timeout");
		},
		30 * 60 * 1000,
	); // 30 minutes
});
```

## Environment & Configuration Security

### Secure Configuration Management
```;
javascript;
const dotenv = require("dotenv");
const joi = require("joi");

// ✅ Load and validate environment variables
dotenv.config();

const envSchema = joi
	.object({
		NODE_ENV: joi
			.string()
			.valid("development", "production", "test")
			.required(),
		PORT: joi.number().port().default(3000),
		JWT_SECRET: joi.string().min(32).required(),
		DB_PASSWORD: joi.string().min(8).required(),
		REDIS_URL: joi.string().uri().required(),
	})
	.unknown();

const { error, value: envVars } = envSchema.validate(process.env);
if (error) {
	throw new Error(`Config validation error: ${error.message}`);
}

// ✅ Use validated environment variables
const config = {
	env: envVars.NODE_ENV,
	port: envVars.PORT,
	jwtSecret: envVars.JWT_SECRET,
	dbPassword: envVars.DB_PASSWORD,
	redisUrl: envVars.REDIS_URL,
};
```

## Dependency Security

### Secure Dependency Management
```;
javascript;
// ✅ Regular security audits
// npm audit
// npm audit fix

// ✅ Use package-lock.json
// ✅ Pin dependency versions
// ✅ Use trusted package sources only

// ✅ Monitor for vulnerabilities
const audit = require("npm-audit");

async function checkDependencies() {
	try {
		const results = await audit({ auditLevel: "moderate" });
		if (results.vulnerabilities.length > 0) {
			logger.warn("Dependencies have vulnerabilities", results);
		}
	} catch (error) {
		logger.error("Failed to audit dependencies", error);
	}
}
```
