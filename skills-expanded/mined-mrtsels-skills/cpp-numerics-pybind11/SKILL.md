---
name: cpp-numerics-pybind11
description: Use for C++ pybind11 num algos. CMake, power method, SVD.
---

# C++ Numerical Algorithms with pybind11

Use when implementing a C++ numerical algorithm that Python calls via pybind11. Covers project setup, algorithm implementation patterns, convergence handling, and numerical validation.

## Project Setup

### Directory Structure

```
project/
├── cpp/
│   ├── algorithm.hpp           # Header-only or header + .cpp
│   ├── pybind_wrapper.cpp      # pybind11 binding code
│   └── CMakeLists.txt          # CMake build config
├── python/
│   ├── wrapper.py              # Python interface layer
│   ├── test_algorithm.py       # Correctness + performance tests
│   └── validation_report.md    # Test results document
└── README.md                   # Build/run instructions
```

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.14)
project(my_project LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(my_module pybind_wrapper.cpp algorithm.hpp)

target_include_directories(my_module PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
set_target_properties(my_module PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../python"
)
```

### Build Commands

```bash
cd cpp/
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=$(python3 -c "import pybind11; print(pybind11.get_cmake_dir())")
cmake --build .
```

### pybind11 Wrapper Patterns

```cpp
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Convert numpy array -> C++ Matrix (row-major)
Matrix numpy_to_matrix(py::array_t<double, py::array::c_style | py::array::forcecast> arr) {
    py::buffer_info buf = arr.request();
    double* ptr = (double*)buf.ptr;
    return Matrix(buf.shape[0], buf.shape[1],
                  std::vector<double>(ptr, ptr + buf.shape[0] * buf.shape[1]));
}

// Convert C++ Matrix -> numpy array
py::array_t<double> matrix_to_numpy(const Matrix& M) {
    py::array_t<double> result({M.rows, M.cols});
    std::copy(M.data.begin(), M.data.end(), (double*)result.request().ptr);
    return result;
}

// Module definition
PYBIND11_MODULE(my_module, m) {
    m.def("my_function", &my_function, py::arg("A"), py::arg("k") = py::none(),
          "Description of the function");
}
```

### Python Wrapper

```python
def my_function(A: np.ndarray, k: int = None):
    """Wrapper with input validation."""
    if not isinstance(A, np.ndarray):
        raise TypeError(...)
    if A.ndim != 2:
        raise TypeError(...)
    if A.dtype != np.float64:
        A = A.astype(np.float64)
    # Call C++ via pybind11
    return _cpp_module.my_function(A, k)
```

## Power Iteration -- Common Pitfalls

### 1. Sign-Flip Convergence (Critical)

Eigenvectors can flip sign between iterations (`b` vs `-b`). The naive convergence check `||b_next - b|| < tol` misses converged vectors that flipped sign.

**Fix:** Check both difference and sum:

```cpp
double diff = 0.0, sum = 0.0;
for (int i = 0; i < n; ++i) {
    double d = b_next[i] - b[i];
    double s = b_next[i] + b[i];
    diff += d * d;
    sum += s * s;
}
diff = std::sqrt(std::min(diff, sum));
```

### 2. RNG Re-Seeding (Easy to Miss)

Calling `srand(seed)` inside `power_iteration` resets the RNG every call, generating the **same** random vector each time. For matrices with degenerate eigenspaces (e.g., identity matrix), this causes the second call to find zero after deflation.

**Fix:** Seed once at the program level (`srand(42)` in `main()`), never inside the iterative call.

### 3. Eigenvalue Stagnation Detector

If the vector isn't converging but the eigenvalue has stabilized (e.g., near-degenerate eigenvalues), add a secondary exit:

```cpp
double lambda = vec_dot(b, AtA_b);
if (iter > 0 && std::abs(lambda - prev_lambda) < 1e-12)
    stalled++;
else
    stalled = 0;
if (stalled > 10) break;
prev_lambda = lambda;
```

### 4. Zero-Vector Protection

When `AtA` has a nullspace, `A * b` can become all-zero. Check norm before normalizing:

```cpp
double norm = vec_norm(b_next);
if (norm < 1e-15) break;  // converged to zero
for (auto& val : b_next) val /= norm;
```

## SVD Construction

### Deflation
```cpp
// Subtract rank-1 component: A <- A - sigma*u*v^T
for (int i = 0; i < A.rows; ++i)
    for (int j = 0; j < A.cols; ++j)
        A(i, j) -= sigma * u[i] * v[j];
```

Handle `sigma=0` by skipping deflation (no component to remove):
```cpp
if (sigma > 1e-15) deflate(A_cur, sigma, u, v);
```

### Matrix Dimension Ordering

SVD signature: `(U, s, Vt)` where:
- `U`: m x k -- orthonormal **columns** -> check `U^T U - I`
- `Vt`: k x n -- orthonormal **rows** (it's V^T) -> check `Vt Vt^T - I`

## Numerical Validation Patterns

### Test Matrix Types

| Type | Purpose | Expected |
|------|---------|----------|
| Random square | General case | Singular values match NumPy |
| Random thin (m>n) | Tall matrix | Full reconstruction < 1e-12 |
| Random wide (m<n) | Short matrix | Full reconstruction < 1e-12 |
| Diagonal | Known eigenvalues | Exact recovery |
| All-ones (rank 1) | Rank deficiency | One non-zero sv, rest ~0 |
| Zero matrix | Edge case | All sv = 0 |
| Identity | Degenerate eigenspace | All sv = 1 |
| k=1 only | Partial SVD | Returns top sv only |

### Handling Partial SVD in Validation

For a rank-k approximation of a full-rank matrix, reconstruction error is **naturally large** (the missing singular values). Only check reconstruction error for full SVD (`k >= min(m, n)`).

### Handling Rank-Deficient Matrices

When rank < k, deflated zero vectors aren't orthogonal. Only check orthogonality on non-zero singular vector columns:
```python
effective_rank = np.sum(s > 1e-12 * max(s[0], 1.0))
if effective_rank > 0:
    orth_err = orthogonality_error(U[:, :effective_rank])
```

### Metrics to Check

- Reconstruction error: `||A - U Sigma V^T||_F / ||A||_F < 1e-6`
- Left orthogonality: `||U^T U - I||_F < 1e-6`
- Right orthogonality: `||Vt Vt^T - I||_F < 1e-6` (note: Vt @ Vt.T, not Vt.T @ Vt)
- Singular values non-negative and decreasing
- vs NumPy: relative error < 1e-4

## Reference: Full Implementation Transcript

See `references/power-method-svd-implementation.md` for the complete implementation transcript from a real Power Method SVD project — including all bug fixes encountered, build commands, and validation results.

## Review Checklist

- [ ] No `srand()` inside iterative functions (seed at program level)
- [ ] Sign-flip convergence check (min of diff and sum)
- [ ] Zero-vector protection before normalization
- [ ] `sigma=0` skips deflation -- no division by zero
- [ ] `max_iter` exhaustion prints warning, doesn't crash
- [ ] All `std::vector` (RAII) -- no raw `new`/`delete`
- [ ] `const` on unmodified parameters
- [ ] `extern "C"` guard or pybind11 wrapper exposes correct API
- [ ] Compiles with `-Wall -Wextra -Wpedantic` zero warnings
- [ ] Validation tests pass for all matrix shapes and edge cases
