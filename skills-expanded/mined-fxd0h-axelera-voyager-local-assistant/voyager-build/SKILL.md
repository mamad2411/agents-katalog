---
name: voyager-build
description: Build GStreamer operators, trackers, and C/C++ examples for Axelera AI hardware. Use when the user wants to compile native Voyager SDK components.
argument-hint: "<component> [options]"
allowed-tools: Read, Bash, Glob, Grep, mcp__voyager__*
---

# Build Native Components

Build GStreamer operators, trackers, and C/C++ examples for Axelera AI hardware

## Instructions

Build the specified components: **$ARGUMENTS**

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 0.5: Axelera Voyager Project & Task Integration

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Environment Verification

- Read `.voyager-runtime.json`. Native component builds require a supported
  Linux Voyager SDK host. In `package_for_linux` mode, provide build commands
  and caveats instead of claiming the build ran.
- Verify Axelera environment is activated:
  ```bash
  if [ -z "$AXELERA_RUNTIME_DIR" ]; then
      echo "Please activate environment: source venv/bin/activate"
      exit 1
  fi
  ```

### Step 2: Component Identification

Parse build target from arguments:

- `all`: Build everything (operators, trackers, examples)
- `operators`: Build GStreamer pipeline operators
- `trackers`: Build object tracking algorithms
- `examples`: Build C/C++ example applications
- `clean`: Clean all build artifacts

### Step 3: Build Operators

GStreamer operators provide pipeline processing capabilities:

```bash
# Build all operators
make operators

# Or build directly from operators directory
cd operators && make

# Clear CMake cache if needed (target lives in operators/)
make -C operators clear-cmake-cache
```

Operators built:

- `axstreamer`: Core streaming operator
- `gstaxstreamer`: GStreamer integration
- `PillowResize`: Image resizing operator

### Step 4: Build Trackers

Object tracking algorithms:

```bash
# Build all trackers
make trackers

# Or build directly
cd trackers && make
```

Trackers built:

- `ByteTrack`: Fast multi-object tracker
- `OC-SORT`: Observation-centric SORT tracker
- `TrackTrack`: Tracker under `trackers/algorithms/tracktrack`

### Step 5: Build Examples

C/C++ example applications:

```bash
# Build all examples
make examples

# Requires operators to be built first
make operators && make examples

# Or build directly
cd examples && make
```

Example categories:

- `axinferencenet/`: AxInferenceNet API examples
- `axruntime/`: Low-level runtime API examples

### Step 6: Build Everything

```bash
# Build all components
make operators
make trackers
make examples
```

### Step 7: CMake Build Options

For more control, use CMake directly:

```bash
cd operators

# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build -j$(nproc)

# Install
cmake --install build --prefix $AXELERA_FRAMEWORK/operators
```

### Step 8: Debug Builds

```bash
# Build with debug symbols
cd operators
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

### Step 9: Clean Build Artifacts

```bash
# Clean all libraries (make clean is an alias for clean-libs)
make clean-libs

# Clobber (deep clean; make clobber is an alias for clobber-libs)
make clobber-libs

# Clean specific component
cd operators && make clean
cd trackers && make clean
cd examples && make clean

# Clear CMake cache (target lives in operators/)
make -C operators clear-cmake-cache
```

### Step 10: Verify Build Success

Check that libraries are installed:

```bash
# Check operator libraries
ls -la $AXELERA_FRAMEWORK/operators/lib/

# Check tracker libraries
ls -la $AXELERA_FRAMEWORK/trackers/lib/

# Check GStreamer plugins
gst-inspect-1.0 axstreamer

# Check dynamic library loading when a plugin path is known
ldd "$AXELERA_FRAMEWORK/operators/lib/"*.so
```

Also run the relevant operator/tracker/example smoke test when the current
SDK provides one. Report exact commands, exit status, library/plugin paths,
and any hardware coverage skipped by the runtime mode.

### Step 11: Troubleshooting Build Issues

**Missing runtime directory:**

```
Error: Please set AXELERA_RUNTIME_DIR
Solution: source venv/bin/activate
```

**CMake configuration errors:**

```bash
# Clear cache and reconfigure
make -C operators clear-cmake-cache
make operators
```

**Missing dependencies:**

```bash
# Install build dependencies
sudo apt install build-essential cmake
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

**Linker errors:**

```bash
# Check library paths
echo $LD_LIBRARY_PATH
# Add runtime library path
export LD_LIBRARY_PATH=$AXELERA_RUNTIME_DIR/lib:$LD_LIBRARY_PATH
```

### Step 12: Build Configuration

The build uses these configuration files:

- `operators/CMakeLists.txt`: Operator build config
- `trackers/CMakeLists.txt`: Tracker build config
- `examples/CMakeLists.txt`: Examples build config
- `Makefile`: Top-level build orchestration

### Step 13: Top-Level Make Targets

The top-level Makefile provides these targets (there is no `NN=` variable and
no `info` target):

```bash
make help                     # Default target; prints per-model help
make operators                # Build GStreamer operators
make trackers                 # Build trackers
make examples                 # Build C/C++ examples (builds operators first)
make clean / clean-libs       # Clean operators, trackers, examples
make clobber / clobber-libs   # Deep clean
make operators-docker         # Operators build path used by Docker installs
make operators-containerless  # Operators build with stale-CMake-cache repair
```

### Step 14: Docker Build (Alternative)

Use Docker only when the current SDK documentation or local repo scripts
support it for this host:

```bash
./launch-docker.sh
# Inside container:
make operators
make trackers
```
