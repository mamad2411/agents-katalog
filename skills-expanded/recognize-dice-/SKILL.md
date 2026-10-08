# D6 Dice Recognition for Raspberry Pi 3 - Project Intelligence

## Development Environment - CRITICAL SETUP

### Development Platform: macOS (darwin 24.4.0)

- **Purpose**: Code development, editing, version control only
- **What works**: Framework testing with `test_fallback.py` ✅
- **What doesn't work**: Camera interface, full application (by design)
- **Applications**:
  - `python3 test_fallback.py` ✅ - Framework validation
  - `python3 install_deps.py` ✅ - Dependency management
  - Code editing, git operations, documentation

### Target Platform: Raspberry Pi 3

- **Purpose**: Complete application deployment and execution
- **What works**: Full application with camera + ML model + GUI
- **Applications**:
  - `python3 main.py` - Full dice recognition app
  - `python3 test_camera.py` - Hardware camera testing
  - `python3 install_deps.py` - Pi-specific dependencies

### Development Workflow (CRITICAL)

1. **Develop on macOS**: Edit code, test framework components
2. **Deploy to Pi**: Transfer via SSH/SCP for hardware testing
3. **Test on Pi**: Run full applications on actual hardware
4. **Iterate**: Make changes on macOS, redeploy to Pi

## Hardware Constraints (Critical)

- **Raspberry Pi 3**: ARM Cortex-A53 @ 1.2GHz, 1GB RAM only
- **Performance targets**: 3-5 FPS (not 5-15 like Pi 4)
- **Memory limit**: <800MB total application footprint
- **Resolution**: 320x320 (reduced from 640x640 for Pi 3)

## Key Architecture Decisions

### Performance Optimizations for Pi 3

- Frame skipping (process every 2nd frame by default)
- Tkinter instead of PyQt5 (lighter memory footprint)
- Aggressive model quantization required (INT8)
- No frame buffering - stream processing only
- Single-threaded processing to avoid overhead

### Camera Interface Strategy

- Dual compatibility: picamera2 (modern) with picamera (legacy) fallback
- Automatic detection and graceful degradation
- Pi 3 specific warm-up and configuration

### Model Strategy

- TensorFlow Lite with heavy quantization essential
- Fallback to simple CV (HoughCircles) when model unavailable
- Based on nell-byler/dice_detection but requires significant optimization

## Project Structure Patterns

### Memory Bank System

- Complete documentation in memory-bank/ directory
- Essential for context between sessions due to memory resets
- Always read ALL memory bank files at start of ANY task

### Module Organization

```
src/
├── camera/     # Pi camera interface with fallback support
├── detection/  # TensorFlow Lite + fallback CV detection
├── gui/        # Lightweight Tkinter interface
└── utils/      # Config, logging, performance monitoring
```

### Configuration Pattern

- Single Config class handles all Pi 3 optimizations
- Dynamic performance adjustment based on FPS/thermal
- Validation of required files and settings

## Development Workflow

### Testing Strategy

1. **On macOS**: Test framework with `python3 test_fallback.py`
2. **Deploy to Pi**: Transfer project files
3. **On Pi**: Test camera with `python3 test_camera.py`
4. **On Pi**: Run full app with `python3 main.py`
5. Monitor thermal/memory during development
6. Always test on actual Pi 3 hardware for performance validation

### Performance Monitoring

- Built-in FPS tracking and thermal monitoring
- Automatic frame skipping adjustment
- Memory usage tracking critical for Pi 3

### Error Handling Philosophy

- Graceful degradation everywhere
- Fallback methods for critical components
- Never crash on single component failure

## Known Challenges & Solutions

### Pi 3 Specific Issues

- **Memory pressure**: Use streaming, no buffering
- **CPU thermal**: Monitor /sys/class/thermal/thermal_zone0/temp
- **Frame rate**: Accept 3-5 FPS as normal, optimize for this

### Camera Compatibility

- Multiple Pi camera versions exist
- picamera2 vs picamera library differences
- Handle both RGB888 and RGBA formats

### Model Integration

- Reference model needs TensorFlow Lite conversion
- Heavy quantization required for Pi 3 performance
- Fallback CV must provide reasonable placeholder

## Cross-Platform Development Success

### macOS Development Testing ✅ CONFIRMED

- Core dependencies installed correctly
- Fallback detection working (detected 3 simulated dice)
- Framework logic validated
- GUI components functional
- Ready for Pi deployment

### Platform-Specific Dependencies

- **macOS**: Excludes camera libraries (correct behavior)
- **Pi 3**: Includes picamera2/picamera for hardware interface
- **Both**: Core CV and GUI libraries work identically

## User Experience Priorities

### Pi 3 User Expectations

- Startup time: <15 seconds acceptable
- Response time: <300ms detection latency OK
- Memory usage: Must stay under 800MB
- Reliability over speed

### GUI Design for Pi 3

- Minimal, lightweight Tkinter interface
- Reduced display resolution (480x360 max)
- Essential information only
- Performance stats visible

## Integration with Reference Project

### From nell-byler/dice_detection

- SSD MobileNet architecture basis
- Labelmap format: ???/one/two/three/four/five/six
- TensorFlow model conversion required
- Adaptation needed for Pi 3 constraints

### Model Conversion Process

1. Extract model from reference project
2. Convert to TensorFlow Lite
3. Apply INT8 quantization
4. Test on Pi 3 hardware
5. Adjust input resolution if needed

## Critical Success Factors

### For Pi 3 Viability

- Memory management is everything
- Thermal management essential
- Frame skipping/dynamic adjustment required
- Fallback methods must work well

### Development Efficiency

- Always read memory bank before starting work
- Test framework on macOS, deploy to Pi for hardware testing
- Monitor performance continuously on Pi
- Document Pi 3 specific patterns

### User Adoption

- Make it "just work" despite Pi 3 limitations
- Clear performance expectations
- Good error messages and troubleshooting
- Easy setup process

## Future Enhancement Priorities

1. Model optimization for Pi 3
2. Better fallback detection algorithms
3. Advanced thermal management
4. Multiple dice tracking improvements

## Development Environment Commands Reference

### macOS Development

```bash
python3 test_fallback.py    # Framework validation ✅
python3 install_deps.py     # Dev dependencies ✅
# Edit code, commit, push to Pi
```

### Raspberry Pi 3 Production

```bash
python3 install_deps.py     # Pi-specific dependencies
python3 test_camera.py      # Hardware camera test
python3 main.py            # Full application
```

Remember: This project's success depends on embracing Pi 3 limitations rather than fighting them. The cross-platform development approach allows rapid iteration while ensuring Pi 3 optimization.
