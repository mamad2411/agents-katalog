# DiaRemot - Technology Stack

## Programming Language
- **Python 3.9-3.11**: Core implementation language with strict version compatibility
- **Type Hints**: Comprehensive type annotations for better code maintainability
- **Async/Await**: Asynchronous processing for I/O-bound operations

## Core Dependencies (Pinned Versions)

### Machine Learning & Inference
- **onnxruntime==1.17.1**: CPU-optimized inference engine
- **torch==2.4.1+cpu**: PyTorch CPU-only build for model compatibility
- **transformers==4.38.2**: Hugging Face transformers library
- **tokenizers==0.15.2**: Fast tokenization for NLP models
- **ctranslate2==4.6.0**: Optimized transformer inference
- **faster-whisper==1.1.0**: Efficient Whisper ASR implementation

### Audio Processing
- **librosa==0.10.2.post1**: Audio analysis and feature extraction
- **soundfile==0.12.1**: Audio file I/O operations
- **av==11.0.0**: FFmpeg Python bindings
- **pydub==0.25.1**: Audio manipulation utilities
- **praat-parselmouth==0.4.3**: Phonetic analysis tools

### Scientific Computing
- **numpy==1.24.4**: Numerical computing foundation
- **scipy==1.10.1**: Scientific computing algorithms
- **pandas==2.0.3**: Data manipulation and analysis
- **scikit-learn==1.3.2**: Machine learning utilities
- **numba==0.59.1**: JIT compilation for performance
- **llvmlite==0.42.0**: LLVM bindings for Numba

### Specialized Models
- **panns-inference==0.1.1**: Pre-trained audio neural networks
- **huggingface_hub==0.24.6**: Model hub integration

### Visualization & Reporting
- **matplotlib==3.7.5**: Plotting and visualization
- **seaborn==0.13.2**: Statistical data visualization
- **reportlab==4.1.0**: PDF generation
- **jinja2==3.1.6**: Template engine for HTML reports
- **beautifulsoup4==4.12.3**: HTML parsing and manipulation

### CLI & Utilities
- **click==8.1.7**: Command-line interface framework
- **typer==0.9.0**: Modern CLI framework with type hints
- **tqdm==4.66.4**: Progress bars and monitoring
- **psutil==5.9.8**: System and process utilities

## Build System

### Package Management
- **setuptools>=65**: Modern Python packaging
- **wheel**: Binary distribution format
- **pip**: Package installer with exact version pinning

### Configuration Files
- **pyproject.toml**: Modern Python project configuration
- **requirements.txt**: Exact dependency specifications
- **pytest.ini**: Test configuration and options

### Development Tools
- **ruff**: Fast Python linter and formatter
- **black**: Code formatting with 100-character line length
- **mypy**: Static type checking
- **pytest**: Testing framework with coverage

## Environment Management

### Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Environment Variables
```bash
# Model and cache directories
DIAREMOT_MODEL_DIR=/srv/models
HF_HOME=/srv/.cache/hf
TRANSFORMERS_CACHE=/srv/.cache/transformers
TORCH_HOME=/srv/.cache/torch

# Performance tuning
OMP_NUM_THREADS=4
MKL_NUM_THREADS=4
NUMEXPR_MAX_THREADS=4
TOKENIZERS_PARALLELISM=false

# CPU-only execution
CUDA_VISIBLE_DEVICES=""
TORCH_DEVICE=cpu
```

## Development Commands

### Setup and Installation
```bash
# Initial setup
chmod +x ./setup.sh
./setup.sh

# Manual installation
python -m pip install -r requirements.txt

# Development installation
pip install -e .
```

### Testing and Validation
```bash
# Run test suite
pytest

# Dependency validation
python -m diaremot.pipeline.audio_pipeline_core --verify_deps --strict_dependency_versions

# Smoke test
python -m diaremot.cli run --input data/sample.wav --outdir ./outputs
```

### Code Quality
```bash
# Linting and formatting
ruff check src/
ruff format src/

# Type checking
mypy src/

# Dependency check
diaremot-deps-check
```

### Pipeline Execution
```bash
# Basic run
diaremot run --input audio.wav --outdir results/

# Advanced configuration
diaremot run \
  --input audio.wav \
  --outdir results/ \
  --asr-compute-type float32 \
  --vad-threshold 0.35 \
  --enable-affect-analysis \
  --generate-summary
```

## Model Architecture

### ONNX Optimization
- **CPU Execution Provider**: Optimized for CPU-only inference
- **Model Quantization**: Reduced precision for faster inference
- **Memory Optimization**: Efficient memory usage patterns
- **Batch Processing**: Optimized batch sizes for throughput

### Inference Engines
- **CTranslate2**: Transformer model optimization
- **ONNX Runtime**: Cross-platform inference
- **PyTorch**: Fallback for unsupported operations
- **Hugging Face**: Model loading and tokenization

## Performance Considerations

### CPU Optimization
- Thread pool management for parallel processing
- Memory-mapped file I/O for large audio files
- Lazy loading of heavy dependencies
- Efficient numpy operations with vectorization

### Caching Strategy
- Model caching with integrity verification
- Intermediate result caching for resumable execution
- Hugging Face hub caching for model downloads
- Local cache fallback for restricted environments

### Memory Management
- Streaming audio processing for large files
- Garbage collection optimization
- Memory profiling and leak detection
- Resource cleanup and context management