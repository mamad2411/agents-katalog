// Command: /optimize-performance
// Description: Analyze and optimize performance bottlenecks

You are optimizing performance in OrdnungsHub. Follow these steps:

1. **Performance Analysis**
   - Profile current performance
   - Identify bottlenecks with data
   - Measure baseline metrics
   - Set optimization targets

2. **Backend Optimization**
   ```python
   # Common optimizations:
   - Use async/await for I/O operations
   - Implement caching for repeated operations
   - Batch database queries
   - Use connection pooling
   - Optimize file scanning algorithms
   ```

3. **Frontend Optimization**
   ```typescript
   // Common optimizations:
   - React.memo for expensive components
   - useMemo/useCallback for computed values
   - Virtualization for long lists
   - Code splitting with lazy loading
   - Optimize bundle size
   ```

4. **Measurement & Validation**
   - Before: Document current metrics
   - After: Measure improvement
   - Run performance tests
   - Check memory usage
   - Verify no functionality regression

Example optimization for file scanning:
```python
# Before: Sequential scanning
for file in files:
    result = await scan_file(file)

# After: Concurrent scanning with limit
async def scan_batch(batch):
    return await asyncio.gather(*[scan_file(f) for f in batch])

# Process in batches of 10
for i in range(0, len(files), 10):
    batch = files[i:i+10]
    results.extend(await scan_batch(batch))
```

Key metrics to track:
- File scan time per 1000 files
- API response time (p50, p95, p99)
- Memory usage (idle and peak)
- UI frame rate during operations
- Bundle size and load time

Tools:
- Python: cProfile, memory_profiler
- JavaScript: Chrome DevTools, Lighthouse
- Monitoring: Custom metrics logging
