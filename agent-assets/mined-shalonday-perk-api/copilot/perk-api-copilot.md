# Perk API - Copilot Instructions

## Project Overview

Backend REST API for the Web Brain Project (WBP), serving a Neo4j Aura graph database that maps learning skills and educational resources. Powers the WBP frontend visualization and the RAG chatbot component.

## Tech Stack

- **Runtime:** Node.js v20.9.0+
- **Framework:** Express.js
- **Database:** Neo4j Aura (cloud-hosted graph database)
- **Key Dependencies:**
  - `neo4j-driver` v5.14.0 - Neo4j database driver
  - `cors` - Cross-origin resource sharing
  - `helmet` - Security headers
  - `express-rate-limit` - API rate limiting (20 req/min)
  - `compression` - Response compression
  - `dotenv` - Environment variable management

## Neo4j Database Schema

### Node Types

1. **Skill** - Learning skills/competencies
   - Properties: `id` (UUID), `name` (string), `embedding` (number[])
   - Type label for D3: `"skill"`

2. **URL** - Learning resources/materials
   - Properties: `id` (UUID), `name` (string), `embedding` (number[])
   - Type label for D3: `"url"`

### Relationships

- `(Skill)-[:IS_PREREQUISITE_TO]->(URL)` - Skill required before learning from URL
- `(URL)-[:TEACHES]->(Skill)` - URL teaches a specific skill

### Special Node

- **Entry Node "E"** - Starting point with `id: "E"`, represents no prerequisites

## Current Endpoints

### Active Routes

```
GET  /tree                         → readUniversalTree()
GET  /paths/:startNodeId/:targetNodeId → readPath()
POST /tree                         → mergeTree()
```

### Endpoint Details

**GET /tree**

- Returns complete graph structure (all nodes and links)
- Response: `{ nodes: [...], links: [...] }`
- Used by: WBP D3 visualization

**GET /paths/:startNodeId/:targetNodeId**

- Find learning path between two nodes
- Returns all nodes and relationships in the path
- Response: `{ nodes: [...], links: [...] }`

**POST /tree** (kept for future use)

- Bulk merge nodes and relationships
- Origin restricted: `https://shalonday.github.io`
- Body: `{ nodes: [...], links: [...] }`

## Development Setup

### Local Development (Current)

⚠️ **TEMPORARY:** Neo4j credentials are hardcoded in `service.js` lines 9-10 for local testing without `.env` file.

**To run locally:**

```bash
npm install
npm run devstart    # Uses nodemon for hot reload
```

## Known Issues & Security Concerns

### 🚨 Critical Security Issues

1. **SQL Injection Vulnerability** in `searchNodes()` (lines ~108-114)
   - Currently uses template strings with user input: `` `MATCH (s:Skill) where toLower(s.title) CONTAINS "${query.toLowerCase()}"` ``
   - **Fix:** Use parameterized queries
2. **CORS Wide Open**
   - Set to `origin: "*"` in app.js
   - **Fix:** Whitelist specific origins

3. **Hardcoded Credentials**
   - Credentials in source code
   - **Fix:** Move to `.env` and add `.env.example`

### ⚠️ Planned Improvements

- [ ] Add embedding-based semantic search
- [ ] Implement chatbot endpoints (`/chatbot/search`, `/chatbot/material-request`)
- [ ] Add input validation middleware
- [ ] Split service.js into smaller modules
- [ ] Add proper error handling and logging
- [ ] Document all Cypher queries

## Architecture Notes

### Neo4j Driver Pattern

- Single driver instance initialized on startup
- Sessions created per request, closed after use
- Uses `executeRead()` and `executeWrite()` for transactions

### Response Format

Most endpoints return:

```javascript
{
  nodes: [{ id, name, type, ... }],  // type: "skill" or "url"
  links: [{ id, source, target }]     // source/target are node UUIDs
}
```

### D3.js Compatibility

- Node types lowercase: `"skill"`, `"url"`
- Links use `source`/`target` properties (UUIDs, not Neo4j internal IDs)
- Helper function `getD3CompatibleLink()` converts Neo4j relationships

## Upcoming Features (Chatbot Integration)

### Endpoints to Add

1. **POST /chatbot/search**
   - Body: `{ query: string, limit: number }`
   - Vector similarity search using embeddings
   - Response: `[{ node: { id, name }, similarity: number }]`

2. **POST /chatbot/material-request**
   - Body: `{ embed: {...}, request: {...} }`
   - Submit material request to Discord webhook
   - Response: `{ success: boolean }`

### Embedding Strategy

- Store embeddings in `Skill.embedding` and `URL.embedding` properties as float arrays
- Use sentence-transformers model: `Xenova/all-MiniLM-L6-v2` (384-dimensional, optimized)
- Run the embedding generation script: `npm run generate-embeddings`

**Script Details:**

- Location: `scripts/generateEmbeddings.js`
- Fetches all nodes without embeddings
- Generates embeddings using @xenova/transformers (Hugging Face library)
- Updates nodes in batches of 10 for efficiency
- Takes ~5-15 minutes depending on node count
- Reports progress and final coverage statistics

## Code Style & Conventions

### Cypher Query Patterns

- Use parameterized queries for user input
- Session management: open → execute → close
- Prefer `executeRead()` / `executeWrite()` over raw `tx.run()`

### Error Handling

- Log errors to console (dev mode)
- Return generic error messages to client
- HTTP 500 for server errors, 404 for not found

### Naming Conventions

- Functions: camelCase (`readUniversalTree`)
- Variables: camelCase (`nodesArray`)
- Constants: UPPER_SNAKE_CASE (when added)

## External Dependencies & Integrations

### Neo4j Aura

- Cloud instance: `87dd45b4.databases.neo4j.io`
- Protocol: `neo4j+s://` (secure)
- Database: default

### Frontend Clients

- **WBP Main Site:** `https://www.webbrainproject.org`
- **GitHub Pages:** `https://shalonday.github.io`
- **Local Dev:** `http://localhost:5173` (Vite default)

### Future Integrations

- Discord webhook for material requests
- Embedding generation pipeline
- Potential vector database (if Neo4j embeddings insufficient)

## Testing & Deployment

### Current Deployment

- Platform: Railway (inferred from wbp-chatbot env: `perk-api-production.up.railway.app`)
- Auto-deploy on push to main branch (likely)

### Local Testing

```bash
npm start           # Production mode (port 3000)
npm run devstart    # Development mode with nodemon
npm run serverstart # Development mode with debug logs
```

### Manual Testing

Use tools like Postman, curl, or HTTPie to test endpoints:

```bash
curl http://localhost:3000/tree
curl http://localhost:3000/search/javascript
curl http://localhost:3000/paths/E/some-uuid
```

## Best Practices & Guidelines

### When Adding New Endpoints

1. Add route to `app.js`
2. Implement handler in `services/service.js`
3. Use parameterized Cypher queries
4. Add CORS restrictions if needed
5. Close Neo4j sessions in finally blocks
6. Return consistent response format

### When Modifying Queries

1. Test queries in Neo4j Browser first
2. Validate input parameters
3. Handle empty result sets
4. Log query execution for debugging
5. Consider query performance (use EXPLAIN/PROFILE)

### Security Checklist

- [ ] Never interpolate user input directly into Cypher
- [ ] Validate and sanitize all inputs
- [ ] Use HTTPS in production
- [ ] Rotate credentials regularly
- [ ] Audit CORS settings
- [ ] Monitor rate limit effectiveness

## Questions & TODOs

### Open Questions

1. Should embeddings be stored in Neo4j or separate vector DB?
2. Which embedding model to use? (Recommend: `all-MiniLM-L6-v2`)
3. Discord webhook URL - where to store?
4. Should we add authentication/API keys?

### Immediate TODOs

- [ ] Run embedding generation script: `npm run generate-embeddings`
- [ ] Fix SQL injection in `searchNodes()`
- [ ] Add proper error handling middleware
- [ ] Document API with OpenAPI/Swagger

## Contact & Resources

- **Frontend Repo:** github.com/shalonday/webbrainproject-ts
- **Chatbot Repo:** (local path: C:\Users\alond\Documents\wbp-chatbot)
- **Neo4j Docs:** https://neo4j.com/docs/
- **Neo4j Driver Docs:** https://neo4j.com/docs/javascript-manual/current/
