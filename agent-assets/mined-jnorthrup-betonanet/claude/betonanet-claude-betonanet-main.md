## Essential Development Commands

### Core Build Commands
```bash
# Build HTX bounty crate (main target)
cargo build --release --manifest-path bounty/htx/Cargo.toml

# Build all bounties
cargo build --release --manifest-path bounty/htx/Cargo.toml
cargo build --release --manifest-path bounty/nym-mixnode/Cargo.toml
cargo build --release --manifest-path bounty/c-bindings/Cargo.toml
cargo build --release --manifest-path bounty/spec-linter/Cargo.toml
cargo build --release --manifest-path bounty/utls-template/Cargo.toml

# Build literbike (core library)
cargo build --release --manifest-path literbike/Cargo.toml
```

### Testing
```bash
# Run HTX bounty tests
cargo test --manifest-path bounty/htx/Cargo.toml

# Run tests with coverage
cargo tarpaulin --manifest-path bounty/htx/Cargo.toml --out Html

# Run fuzz tests
cd bounty/htx && cargo fuzz run fuzz_handshake

# Run parallel build script
./bounty/htx/parallel_build.sh
```

### Development Workflow
```bash
# Lint and format
cargo clippy --manifest-path bounty/htx/Cargo.toml
cargo fmt --manifest-path bounty/htx/Cargo.toml

# Run compliance checks
cargo run --manifest-path bounty/spec-linter/Cargo.toml

# Generate SBOM
cargo run --manifest-path bounty/spec-linter/Cargo.toml -- --sbom
```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Betanet Bounty Program - $32,000 USD Total

These bounties were made possible by sponsors: ziruem ($500 USD) and THESLAMMERRRRRR with the broader community (bags.fm fund, $50,000+ USD).

**ALL SUBMISSIONS MUST BE SENT VIA EMAIL TO PROJECT MAINTAINERS**

## Bounty #1: HTX Client/Server Crate - $12,000 USD 🥇

**Core Deliverables:**

- `dial()`, `accept()`, `stream()` APIs for TCP-443 & QUIC-443
- ChaCha20-Poly1305 AEAD encryption
- Noise XK handshake implementation  
- ECH (Encrypted Client Hello) stub
- ≥80% line/branch fuzz coverage

**Implementation Requirements (§5 Cover Transport):**

1. **Origin Mirroring**: Mirror target origin's JA3/JA4, ALPN, extensions exactly
2. **Access Tickets**: X25519 + HKDF with cookie/query/body carriers, 24-64B padding
3. **Noise XK**: Inner handshake over TLS tunnel with rekeying (≥8GiB/2¹⁶frames/1h)
4. **HTTP/2/3 Emulation**: Random PING cadence [10s,60s], origin-matched SETTINGS
5. **Anti-Correlation**: Cover connections on UDP→TCP fallback

### Build Commands

```bash
cargo build --manifest-path htx/Cargo.toml
cargo test --manifest-path htx/Cargo.toml  
cargo fuzz run fuzz_handshake --manifest-path htx/Cargo.toml
cargo tarpaulin --manifest-path htx/Cargo.toml --out Html
```

## Bounty #2: High-Performance Nym Mixnode - $8,000 USD 🥈

**Core Deliverables:**

- Process Sphinx packets with VRF hop-selection
- ≥25k pkt/s sustained on 4-core VPS
- Basic cover-traffic padding and rate-limiting
- BeaconSet randomness integration (§7.2)

**Implementation Requirements:**

- Sphinx packet processing with constant-time crypto
- VRF-based hop selection using BeaconSet entropy
- Traffic analysis resistance with cover patterns
- Per-stream entropy diversity (≥8 distinct hop sets)

## Bounty #3: C Library Implementation - $4,000 USD 🥉

**Core Deliverables:**

- Complete C API for Betanet protocol stack
- Thread-safe, memory-safe implementation
- Cross-platform compatibility (Linux, macOS, Windows)
- Comprehensive documentation and examples

## Bounty #4: Spec-Compliance Linter CLI - $4,000 USD

**Core Deliverables:**

- Run all 11 compliance checks from §11 against binaries
- Generate SBOM (Software Bill of Materials)
- Ready-made GitHub Action template
- Pass/fail report with detailed diagnostics

**The 11 Mandatory Compliance Checks:**

1. HTX over TCP-443/QUIC-443 with ECH + calibration
2. Negotiated-carrier access tickets with replay protection
3. Noise XK with hybrid X25519-Kyber768 (from 2027-01-01)
4. HTTP/2/3 behavior emulation
5. HTX-tunneled SCION transitions (no public wire headers)
6. Standard transport endpoints (/betanet/htx/1.1.0)
7. BeaconSet bootstrap with PoW rate-limits
8. BeaconSet mixnode selection with entropy
9. 2-of-3 blockchain alias verification
10. 128-B Cashu voucher support
11. Anti-correlation fallback + SLSA 3 builds

## Bounty #5: Chrome uTLS Template Generator - $4,000 USD

**Core Deliverables:**

- Deterministic ClientHello blob matching Chrome Stable (N-2)
- JA3 self-test CLI with fingerprint verification
- Auto-refresh when new Chromium stable tags appear
- Perfect indistinguishability from real Chrome traffic

## Reference Architecture

**Kotlin KMP Reference Implementations:**

- `~/work/superbikeshed/Trikeshed/` - QUIC engine with Indexed<T> types
- `~/work/v2superbikeshed/trikeshed-http/` - HTTP/3 server
- `~/work/literbike/src/rbcursive/` - RbCursive protocol combinators

**Key Patterns:**

- `Indexed<T> = Join<Int, Int->T>` for zero-allocation data structures
- SIMD-accelerated protocol detection with constant-time anchors
- Functional composition with categorical pairwise atoms

## Testing & Submission Requirements

**For HTX Bounty:**

- ≥80% line/branch coverage mandatory
- Fuzz testing for all parsers
- Performance benchmarks for sustained throughput

**For Nym Bounty:**

- ≥25k pkt/s sustained performance proof on 4-core VPS
- Latency distribution analysis
- Cover traffic effectiveness metrics

**All Bounties:**

- Complete source code + documentation
- SBOM generation where applicable
- Email submission to project maintainers
- Reproducible builds with SLSA 3 provenance

---


## Architecture Overview

### High-Level Structure

**Betanet** is a censorship-resistant network protocol designed to replace HTTPS. The codebase implements a layered architecture:

- **Layer 2**: HTX (Cover Transport) - Encrypted transport that mimics regular HTTPS traffic
- **Layer 3**: Overlay mesh using libp2p-v2 for object relay
- **Layer 4**: Optional privacy hop through Nym mixnet
- **Layer 5**: Naming & trust with self-certifying IDs and alias ledger
- **Layer 6**: Payments via federated Cashu + Lightning

### Key Components

#### Core Libraries
- **`bounty/htx/`** - Main HTX protocol implementation with QUIC and TCP-443 transport
- **`literbike/`** - Core networking utilities and protocol detection library
- **`platform/couchduck/`** - High-performance database with MLIR acceleration
- **`platform/rbcursive/`** - Protocol parsing combinators with SIMD optimizations

#### Bounty Implementations
- **`bounty/htx/`** - HTX Client/Server crate ($12k bounty)
- **`bounty/nym-mixnode/`** - High-performance Nym mixnode ($8k bounty)
- **`bounty/c-bindings/`** - C library implementation ($4k bounty)
- **`bounty/spec-linter/`** - Spec compliance linter ($4k bounty)
- **`bounty/utls-template/`** - Chrome uTLS template generator ($4k bounty)

### Key Patterns

#### Zero-Allocation Design
The codebase uses `Indexed<T> = Join<Int, Int->T>` types for zero-allocation data structures throughout. This pattern enables high-performance protocol processing without heap allocations.

#### MLIR Integration
Many components integrate with MLIR (Multi-Level Intermediate Representation) for compile-time optimization and constraint verification. This enables performance acceleration and formal verification.

#### Feature Gating
Complex features are progressively unlocked through Cargo feature flags:
- **basic**: Core dial/accept/stream APIs
- **crypto**: Full encryption support
- **optimization**: WAM + MLIR integration
- **vectorization**: SIMD + advanced optimization
- **full-stack**: Complete Betanet integration
