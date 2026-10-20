# DiaRemot - Project Structure

## Directory Organization

### Core Source Code (`src/diaremot/`)
```
src/diaremot/
├── affect/           # Emotion and paralinguistics analysis
├── io/              # Input/output utilities and model management
├── pipeline/        # Core pipeline orchestration and stages
├── summaries/       # Report generation and analysis
├── tools/           # Utility scripts and diagnostics
├── utils/           # Common utilities and helpers
├── __init__.py      # Package initialization
└── cli.py           # Command-line interface
```

### Pipeline Architecture (`pipeline/`)
- **stages/**: Modular pipeline components (ASR, diarization, affect analysis)
- **orchestrator.py**: Main pipeline coordinator with adaptive configuration
- **checkpoint_system.py**: State persistence and resumable execution
- **config.py**: Configuration management and validation
- **runtime_env.py**: Environment setup and model path resolution

### Affect Analysis (`affect/`)
- **emotion_analyzer.py**: Multi-modal emotion recognition engine
- **paralinguistics.py**: Speech feature extraction and analysis
- **ser_onnx.py**: ONNX-optimized speech emotion recognition
- **sed_panns.py**: Sound event detection using PANNs models
- **intent_defaults.py**: Intent classification configuration

### I/O Management (`io/`)
- **onnx_runtime_guard.py**: ONNX Runtime provider management
- **download_utils.py**: Model downloading and caching
- **speaker_registry_manager.py**: Speaker identification persistence
- **onnx_utils.py**: ONNX model utilities and optimization

### Summary Generation (`summaries/`)
- **html_summary_generator.py**: Interactive HTML report creation
- **pdf_summary_generator.py**: PDF report generation with charts
- **conversation_analysis.py**: Speaker interaction analysis
- **speakers_summary_builder.py**: Per-speaker statistics and insights

## Architectural Patterns

### Modular Pipeline Design
- **Stage-based Processing**: Each pipeline stage is independently testable
- **Dependency Injection**: Components receive dependencies through configuration
- **Provider Pattern**: Pluggable backends for different inference engines
- **Factory Pattern**: Dynamic component instantiation based on configuration

### Configuration Management
- **Hierarchical Config**: CLI args override environment vars override defaults
- **Validation Layer**: Type checking and constraint validation
- **Environment Adaptation**: Automatic fallback for cache and model directories
- **Runtime Tuning**: Adaptive parameter adjustment based on input characteristics

### State Management
- **Checkpoint System**: Granular state persistence at stage boundaries
- **Metadata Tracking**: Comprehensive logging of processing parameters
- **Error Recovery**: Graceful handling of partial failures with resume capability
- **Progress Monitoring**: Real-time pipeline progress and health metrics

## Core Components

### Pipeline Orchestrator
Central coordinator that manages:
- Stage execution order and dependencies
- Configuration merging and validation
- Checkpoint creation and restoration
- Error handling and recovery

### Model Management
Handles:
- ONNX model loading and optimization
- Cache directory resolution and fallback
- Model download and integrity verification
- Provider selection (CPU/GPU/specialized)

### Audio Processing Chain
Processes audio through:
1. **Preprocessing**: Normalization, resampling, format conversion
2. **VAD**: Voice activity detection and segmentation
3. **Diarization**: Speaker identification and clustering
4. **ASR**: Speech-to-text transcription
5. **Affect**: Emotion and paralinguistics analysis
6. **Summarization**: Report generation and insights

### Output Generation
Creates multiple output formats:
- **CSV**: Structured data for further analysis
- **JSONL**: Streaming format for real-time processing
- **HTML**: Interactive reports with visualizations
- **PDF**: Print-ready summaries with charts

## Data Flow

### Input Processing
1. Audio file validation and format detection
2. Preprocessing and normalization
3. Segmentation based on VAD results
4. Feature extraction for downstream analysis

### Analysis Pipeline
1. Speaker diarization creates speaker-segmented timeline
2. ASR transcribes speech segments with speaker attribution
3. Affect analysis processes both audio and text features
4. Intent classification analyzes transcribed content

### Output Generation
1. Results aggregation across all analysis stages
2. Statistical analysis and trend identification
3. Visualization generation for reports
4. Multi-format output creation (CSV, HTML, PDF)

## Integration Points

### External Dependencies
- **ONNX Runtime**: CPU-optimized inference engine
- **CTranslate2**: Optimized transformer inference
- **Faster-Whisper**: Efficient ASR implementation
- **Hugging Face**: Model hub integration

### Configuration Sources
- **CLI Arguments**: Runtime parameter overrides
- **Environment Variables**: System-level configuration
- **Config Files**: Persistent settings and defaults
- **Model Metadata**: Model-specific parameters