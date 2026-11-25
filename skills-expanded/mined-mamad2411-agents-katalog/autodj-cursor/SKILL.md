# AutoDJ Project Rules

## Project Overview
AutoDJ is an application that automatically mixes songs together by analyzing DJ mixes, extracting transitions, and building a graph of song relationships.

# KEEP THINGS SIMPLE
NO OVERENGINEERING EVERYTHING
this is for a 36 hour hackathon


## Architecture & Pipeline
The project follows an 8-stage pipeline:
1. Get Source Song (YouTube/multi-source search)
2. Find Related Mixes (preset queries → LLM-generated queries)
3. Store in Blob Storage (Azure Blob Storage)
4. Fingerprinting (DejaVu audio fingerprinting)
5. Song-in-Mix Recognition (DejaVu + AUDAlign)
6. Transition Detection (deterministic rules → quality metrics)
7. Transition Extraction (local → Azure Functions)
8. Transition Graph (directed graph with nodes=songs, edges=transitions)

## Development Phases
- **MVP**: Single-process, YouTube-only, local processing
- **Full**: Multi-source, Azure Functions, advanced features

## Code Standards

### Python Standards
- Use type hints for all function parameters and return values
- Follow PEP 8 with Black formatter (88 character line length)
- Use pydantic for data structures (see graph.py example)
- Prefer async/await for I/O operations
- Use pathlib for file operations
- Use logging instead of print statements

### File Organization
- Keep MVP and Full implementations in separate modules when possible
- Use clear module names: `song_search.py`, `fingerprinting.py`, `transition_graph.py`
- Place Azure-specific code in `azure/` subdirectory
- Keep configuration in `config/` directory

### Error Handling
- Always handle network timeouts and retries
- Use specific exception types, not bare `except:`
- Log errors with context (song_id, mix_id, etc.)
- Implement graceful degradation for MVP features

### Data Models
- Use pydantic for structured data (SongNode, TransitionEdge pattern)
- Include metadata fields for extensibility
- Use UUIDs for unique identifiers
- Store timestamps as datetime objects

### Audio Processing
- Always validate audio file formats before processing
- Use FFmpeg for audio conversion and manipulation
- Implement proper audio chunking for large files (>20-30 min)
- Add micro-fades (2-5ms) to prevent audio clicks
- Normalize loudness using EBU R128 standards

### Database & Storage
- Use PostgreSQL for structured data
- Use Azure Blob Storage for audio files
- Implement proper indexing for graph queries
- Use connection pooling for database operations
- Store file hashes for integrity checking

### API Design
- RESTful endpoints for graph operations
- Use proper HTTP status codes
- Implement pagination for large result sets
- Include confidence scores in responses
- Version your APIs

## Testing Requirements
- Unit tests for all core functions
- Integration tests for pipeline stages
- Mock external services (YouTube, Azure)
- Test both MVP and Full implementations
- Include performance benchmarks

## Security Considerations
- Never commit API keys or secrets
- Use environment variables for configuration
- Implement rate limiting for external APIs
- Validate all user inputs
- Use signed URLs for blob access

## Performance Guidelines
- Implement parallel processing where possible
- Use queues for long-running tasks
- Cache frequently accessed data
- Monitor memory usage for large audio files
- Implement proper cleanup of temporary files

## Documentation
- Include docstrings for all public functions
- Document API endpoints with examples
- Keep README updated with setup instructions
- Document configuration options
- Include troubleshooting guides

## Dependencies
- Core: yt-dlp, dejavu, audalign, ffmpeg-python
- Azure: azure-storage-blob, azure-functions
- Database: psycopg2, sqlalchemy
- Web: fastapi, uvicorn
- Testing: pytest, pytest-asyncio
- Utilities: python-dotenv, requests, aiohttp
