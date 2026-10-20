# DiaRemot - Development Guidelines

## Code Quality Standards

### Import Organization
- **Future Imports First**: Always use `from __future__ import annotations` for forward compatibility
- **Standard Library**: Group standard library imports (os, json, logging, threading, etc.)
- **Third-Party Libraries**: Separate third-party imports (numpy, librosa, transformers)
- **Local Imports**: Place local module imports last with relative imports
- **Conditional Imports**: Use try/except blocks for optional dependencies with graceful fallbacks

### Type Annotations
- **Comprehensive Typing**: Use type hints for all function parameters and return values
- **Union Types**: Use `|` syntax for union types (e.g., `str | None` instead of `Optional[str]`)
- **Generic Collections**: Use built-in generics (e.g., `list[str]` instead of `List[str]`)
- **Complex Types**: Define custom types using `TypeAlias` or dataclasses for complex structures
- **Runtime Safety**: Use `TYPE_CHECKING` imports for type-only imports

### Error Handling
- **Graceful Degradation**: Always provide fallback behavior for missing dependencies
- **Specific Exceptions**: Catch specific exceptions rather than bare `except:`
- **Logging Integration**: Use structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)
- **Resource Cleanup**: Use context managers and try/finally blocks for resource management
- **Validation**: Validate inputs early with clear error messages

### Documentation Standards
- **Module Docstrings**: Include purpose, key capabilities, and usage examples
- **Function Docstrings**: Document parameters, return values, and side effects
- **Inline Comments**: Explain complex algorithms and business logic
- **Type Documentation**: Document expected data structures and formats
- **Configuration Notes**: Document environment variables and configuration options

## Architectural Patterns

### Dependency Management
- **Lazy Loading**: Import heavy dependencies only when needed to reduce startup time
- **Backend Abstraction**: Use factory patterns to switch between different backends (ONNX, PyTorch, etc.)
- **Availability Checks**: Implement singleton classes to track available backends
- **Fallback Chains**: Provide multiple implementation options with automatic fallback

```python
# Pattern: Backend availability singleton
class BackendAvailability:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._check_backends()
        return cls._instance
```

### Configuration Management
- **Dataclass Configs**: Use frozen dataclasses for configuration objects
- **Environment Integration**: Support environment variables with sensible defaults
- **Validation**: Validate configuration values at initialization
- **Preset System**: Provide named presets for common use cases

```python
# Pattern: Configuration with presets
@dataclass(frozen=True)
class ProcessingConfig:
    model_size: str = "large-v3"
    compute_type: str = "float32"
    
def get_config_preset(preset_name: str) -> ProcessingConfig:
    presets = {
        "fast": ProcessingConfig(model_size="tiny", compute_type="int8"),
        "quality": ProcessingConfig(model_size="large-v3", compute_type="float32")
    }
    return presets.get(preset_name, ProcessingConfig())
```

### Async/Concurrency Patterns
- **Async Context Managers**: Use `@asynccontextmanager` for resource management
- **Semaphore Control**: Limit concurrent operations with semaphores
- **Thread Pool Integration**: Use `ThreadPoolExecutor` for CPU-bound tasks
- **Timeout Handling**: Implement timeouts with graceful degradation
- **Progress Tracking**: Provide progress callbacks for long-running operations

### State Management
- **Checkpoint System**: Implement resumable operations with state persistence
- **Thread Safety**: Use locks for shared state modification
- **Immutable Data**: Prefer immutable data structures where possible
- **State Validation**: Validate state transitions and handle invalid states

## Performance Optimization

### CPU Optimization
- **Vectorized Operations**: Use numpy vectorization over Python loops
- **Memory Efficiency**: Implement memory-mapped I/O for large files
- **Caching Strategies**: Use `@lru_cache` for expensive computations
- **Batch Processing**: Group operations to reduce overhead
- **Resource Pooling**: Reuse expensive resources like models and sessions

```python
# Pattern: Vectorized operations with caching
@lru_cache(maxsize=64)
def _get_optimized_frame_params(sr: int, frame_ms: int, hop_ms: int) -> tuple[int, int]:
    frame = max(64, int(sr * frame_ms / 1000.0))
    hop = max(32, int(sr * hop_ms / 1000.0))
    return frame, hop
```

### Memory Management
- **Lazy Initialization**: Initialize heavy objects only when needed
- **Context Managers**: Use context managers for automatic cleanup
- **Chunked Processing**: Process large data in chunks to control memory usage
- **Garbage Collection**: Explicitly clean up large objects when done

### Model Optimization
- **ONNX Preference**: Prefer ONNX models for CPU inference
- **Session Reuse**: Cache and reuse inference sessions
- **Batch Inference**: Process multiple inputs together when possible
- **Quantization**: Use quantized models for faster inference

## Testing and Validation

### Input Validation
- **Type Checking**: Validate input types and ranges
- **Boundary Conditions**: Handle edge cases like empty inputs
- **Format Validation**: Validate file formats and data structures
- **Graceful Failures**: Return sensible defaults for invalid inputs

### Error Recovery
- **Retry Logic**: Implement retry mechanisms for transient failures
- **Fallback Methods**: Provide alternative approaches when primary methods fail
- **Partial Results**: Return partial results when complete processing fails
- **Diagnostic Information**: Collect and report diagnostic information

### Performance Testing
- **Benchmarking**: Include performance benchmarks for critical paths
- **Memory Profiling**: Monitor memory usage in long-running operations
- **Timeout Testing**: Verify timeout handling works correctly
- **Load Testing**: Test with various input sizes and conditions

## Integration Patterns

### Pipeline Integration
- **Stage-Based Processing**: Organize processing into discrete stages
- **Data Flow**: Use consistent data structures between stages
- **Progress Reporting**: Provide progress updates throughout processing
- **Error Propagation**: Handle errors gracefully across stage boundaries

### External Dependencies
- **Version Pinning**: Pin exact versions for reproducible builds
- **Compatibility Layers**: Abstract differences between library versions
- **Feature Detection**: Detect available features at runtime
- **Graceful Degradation**: Reduce functionality when dependencies are missing

### File System Integration
- **Path Handling**: Use `pathlib.Path` for cross-platform compatibility
- **Directory Structure**: Follow consistent directory organization
- **Atomic Operations**: Use atomic file operations where possible
- **Cleanup**: Implement proper cleanup of temporary files

## Security and Reliability

### Input Sanitization
- **Path Validation**: Validate file paths to prevent directory traversal
- **Size Limits**: Enforce reasonable limits on input sizes
- **Format Validation**: Validate file formats before processing
- **Resource Limits**: Prevent resource exhaustion attacks

### Error Information
- **Sensitive Data**: Avoid logging sensitive information
- **Error Messages**: Provide helpful but not overly detailed error messages
- **Audit Trails**: Log important operations for debugging
- **Resource Monitoring**: Monitor resource usage and detect anomalies

### Dependency Security
- **Known Vulnerabilities**: Monitor dependencies for security issues
- **Minimal Dependencies**: Use minimal required dependencies
- **Isolation**: Isolate potentially unsafe operations
- **Validation**: Validate data from external sources

## Code Organization

### Module Structure
- **Single Responsibility**: Each module should have a clear, single purpose
- **Interface Consistency**: Maintain consistent interfaces across similar modules
- **Dependency Direction**: Avoid circular dependencies between modules
- **Public APIs**: Clearly define public vs private interfaces

### Class Design
- **Composition Over Inheritance**: Prefer composition to inheritance
- **Immutable Objects**: Use immutable objects where possible
- **Factory Methods**: Use factory methods for complex object creation
- **Context Managers**: Implement context managers for resource management

### Function Design
- **Pure Functions**: Prefer pure functions without side effects
- **Single Purpose**: Each function should do one thing well
- **Parameter Validation**: Validate parameters at function entry
- **Return Consistency**: Return consistent types and formats

## Development Workflow

### Code Style
- **Line Length**: Maximum 100 characters per line
- **Formatting**: Use black for code formatting
- **Linting**: Use ruff for linting and style checking
- **Type Checking**: Use mypy for static type checking

### Documentation
- **API Documentation**: Document all public APIs
- **Usage Examples**: Provide working examples
- **Configuration Guide**: Document configuration options
- **Troubleshooting**: Include common issues and solutions

### Version Control
- **Commit Messages**: Use clear, descriptive commit messages
- **Branch Strategy**: Use feature branches for development
- **Code Review**: Require code review for all changes
- **Testing**: Ensure all tests pass before merging