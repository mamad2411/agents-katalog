-----
name: functional-analysis
description: >
  Expert in functional analysis, operator theory, and spectral methods. Use this 
  skill for understanding infinite-dimensional vector spaces, Banach and Hilbert 
  spaces, linear operators, spectral theory, and applications to quantum mechanics 
  and differential equations. Covers normed spaces, bounded operators, Fourier 
  analysis, and functional calculus.
license: MIT
compatibility: opencode
metadata:
  audience: students
  category: mathematics
  tags: [functional-analysis, banach-spaces, hilbert-spaces, operator-theory, spectral-theory]

# Functional Analysis

Covers: **Normed Spaces · Banach Spaces · Hilbert Spaces · Linear Operators · Bounded Operators · Spectral Theory · Fourier Analysis · Functional Calculus**

-----

## Normed Vector Spaces

### Definitions and Properties

A **normed vector space** (X, ||·||) is a vector space X equipped with a norm that satisfies:
- **Positivity**: ||x|| ≥ 0, with equality only if x = 0
- **Absolute homogeneity**: ||αx|| = |α| ||x|| for all scalars α
- **Triangle inequality**: ||x + y|| ≤ ||x|| + ||y||

```python
import numpy as np
from typing import Callable, List, Tuple
from abc import ABC, abstractmethod

class NormedSpace(ABC):
    """Abstract base for normed vector spaces"""
    
    @abstractmethod
    def norm(self, x: np.ndarray) -> float:
        """Compute the norm of a vector"""
        pass
    
    def distance(self, x: np.ndarray, y: np.ndarray) -> float:
        """Distance induced by norm"""
        return self.norm(x - y)
    
    def is_cauchy(self, sequence: List[np.ndarray], tolerance: float = 1e-6) -> bool:
        """Check if sequence is Cauchy"""
        for i in range(len(sequence) - 1):
            if self.distance(sequence[i], sequence[i+1]) > tolerance:
                return False
        return True


class LpSpace(NormedSpace):
    """L^p normed space"""
    
    def __init__(self, p: float = 2):
        if p < 1:
            raise ValueError("p must be >= 1")
        self.p = p
    
    def norm(self, x: np.ndarray) -> float:
        """L^p norm: (Σ|x_i|^p)^(1/p)"""
        return np.sum(np.abs(x) ** self.p) ** (1 / self.p)
    
    def __repr__(self):
        return f"L^{self.p} space"


class LInfSpace(NormedSpace):
    """L^∞ (essential supremum) space"""
    
    def norm(self, x: np.ndarray) -> float:
        """Supremum norm"""
        return np.max(np.abs(x))


class WeightedSpace(NormedSpace):
    """Weighted L^p space"""
    
    def __init__(self, weight: Callable, p: float = 2):
        self.weight = weight
        self.p = p
    
    def norm(self, x: np.ndarray) -> float:
        """Weighted norm"""
        weighted = x * np.array([self.weight(i) for i in range(len(x))])
        return np.sum(np.abs(weighted) ** self.p) ** (1 / self.p)
```

### Banach Spaces

A **Banach space** is a complete normed vector space. Every Cauchy sequence converges to a limit within the space.

```python
class BanachSpace(ABC):
    """Abstract Banach space"""
    
    @abstractmethod
    def norm(self, x: np.ndarray) -> float:
        pass
    
    @abstractmethod
    def complete(self) -> bool:
        """Check if space is complete"""
        pass


class SequenceSpace(BanachSpace):
    """Space of bounded sequences l^∞"""
    
    def __init__(self):
        self.space = LInfSpace()
    
    def norm(self, x: np.ndarray) -> float:
        return self.space.norm(x)
    
    def complete(self) -> bool:
        """l^∞ is complete"""
        return True


class ContinuousFunctionSpace(BanachSpace):
    """Space of continuous functions C[a,b] with sup norm"""
    
    def __init__(self, a: float = 0, b: float = 1):
        self.a = a
        self.b = b
    
    def norm(self, f: Callable) -> float:
        """Supremum norm"""
        x = np.linspace(self.a, self.b, 1000)
        return np.max(np.abs(f(x)))
    
    def complete(self) -> bool:
        """C[a,b] with sup norm is complete"""
        return True


# Common Banach spaces
banach_spaces = {
    'l1': 'Absolute summable sequences',
    'l2': 'Square summable sequences (Hilbert space)',
    'lp': 'p-power summable sequences',
    'L1': 'Lebesgue integrable functions',
    'L2': 'Square integrable functions (Hilbert space)',
    'L^p': 'p-power Lebesgue integrable functions',
    'C[a,b]': 'Continuous functions on [a,b]',
    'C^k': 'k-times continuously differentiable functions'
}
```

-----

## Hilbert Spaces

### Inner Product Spaces

A **Hilbert space** is a complete inner product space. The inner product induces the norm:

```python
class HilbertSpace(ABC):
    """Abstract Hilbert space"""
    
    @abstractmethod
    def inner_product(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute inner product"""
        pass
    
    @abstractmethod
    def norm(self, x: np.ndarray) -> float:
        """Norm induced by inner product"""
        pass
    
    def cauchy_schwarz(self, x: np.ndarray, y: np.ndarray) -> bool:
        """Verify Cauchy-Schwarz inequality"""
        lhs = abs(self.inner_product(x, y))
        rhs = self.norm(x) * self.norm(y)
        return lhs <= rhs + 1e-10
    
    def angle(self, x: np.ndarray, y: np.ndarray) -> float:
        """Angle between vectors"""
        cos_angle = self.inner_product(x, y) / (self.norm(x) * self.norm(y))
        return np.arccos(np.clip(cos_angle, -1, 1))


class EuclideanSpace(HilbertSpace):
    """Standard Euclidean space R^n"""
    
    def __init__(self, n: int):
        self.n = n
    
    def inner_product(self, x: np.ndarray, y: np.ndarray) -> float:
        return np.dot(x, y)
    
    def norm(self, x: np.ndarray) -> float:
        return np.linalg.norm(x)
    
    def orthogonal_projection(self, x: np.ndarray, subspace: List[np.ndarray]) -> np.ndarray:
        """Project onto subspace spanned by given vectors"""
        coeffs = np.array([self.inner_product(x, v) for v in subspace])
        return sum(c * v for c, v in zip(coeffs, subspace))


class L2Space(HilbertSpace):
    """L^2 space of square-integrable functions"""
    
    def inner_product(self, f: Callable, g: Callable, a: float = 0, b: float = 1) -> float:
        """L^2 inner product: ∫ f(x)g(x) dx"""
        x = np.linspace(a, b, 1000)
        return np.trapz(f(x) * g(x), x)
    
    def norm(self, f: Callable, a: float = 0, b: float = 1) -> float:
        """L^2 norm: √(∫ |f(x)|^2 dx)"""
        x = np.linspace(a, b, 1000)
        return np.sqrt(np.trapz(f(x) ** 2, x))
```

### Orthonormal Bases

```python
class OrthonormalBasis:
    """Orthonormal basis for Hilbert space"""
    
    def __init__(self, vectors: List[np.ndarray]):
        self.vectors = vectors
        self._verify_orthonormality()
    
    def _verify_orthonormality(self):
        """Verify vectors form orthonormal basis"""
        n = len(self.vectors)
        for i in range(n):
            for j in range(n):
                if i == j:
                    assert abs(np.dot(self.vectors[i], self.vectors[j]) - 1) < 1e-10
                else:
                    assert abs(np.dot(self.vectors[i], self.vectors[j])) < 1e-10
    
    def expand(self, x: np.ndarray) -> Tuple[List[float], np.ndarray]:
        """Expand vector in orthonormal basis"""
        coefficients = [np.dot(x, v) for v in self.vectors]
        reconstruction = sum(c * v for c, v in zip(coefficients, self.vectors))
        return coefficients, reconstruction
    
    def parseval_identity(self, x: np.ndarray) -> bool:
        """Verify Parseval's identity: ||x||² = Σ|c_n|²"""
        coeffs, _ = self.expand(x)
        lhs = np.dot(x, x)
        rhs = sum(c ** 2 for c in coeffs)
        return abs(lhs - rhs) < 1e-10


# Fourier basis
class FourierBasis(OrthonormalBasis):
    """Fourier basis for L²[0, 2π]"""
    
    def __init__(self, n_harmonics: int):
        vectors = []
        
        # DC component
        vectors.append(np.ones(2 * np.pi) / np.sqrt(2 * np.pi))
        
        # Cosine and sine terms
        for k in range(1, n_harmonics + 1):
            vectors.append(np.cos(k * np.linspace(0, 2*np.pi, 1000)) / np.sqrt(np.pi))
            vectors.append(np.sin(k * np.linspace(0, 2*np.pi, 1000)) / np.sqrt(np.pi))
        
        super().__init__(vectors)
```

-----

## Linear Operators

### Bounded Linear Operators

An operator T: X → Y is **bounded** if there exists M ≥ 0 such that ||Tx|| ≤ M||x|| for all x. The operator norm is:

```python
class BoundedOperator:
    """Bounded linear operator between normed spaces"""
    
    def __init__(self, matrix: np.ndarray = None, 
                 linear_map: Callable = None):
        if matrix is not None:
            self.matrix = matrix
            self.linear_map = lambda x: matrix @ x
        elif linear_map is not None:
            self.linear_map = linear_map
            self.matrix = None
        else:
            raise ValueError("Provide either matrix or linear_map")
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.linear_map(x)
    
    def operator_norm(self, num_samples: int = 1000) -> float:
        """Compute operator norm approximately"""
        max_norm = 0
        for _ in range(num_samples):
            x = np.random.randn(len(x))
            x = x / np.linalg.norm(x)
            y = self(x)
            norm_ratio = np.linalg.norm(y) / np.linalg.norm(x)
            max_norm = max(max_norm, norm_ratio)
        return max_norm
    
    def adjoint(self) -> 'BoundedOperator':
        """Adjoint operator (Hermitian transpose for matrices)"""
        if self.matrix is not None:
            return BoundedOperator(matrix=self.matrix.T.conj())
        raise NotImplementedError("Adjoint only implemented for matrix operators")
    
    def is_self_adjoint(self, tolerance: float = 1e-10) -> bool:
        """Check if operator is self-adjoint (Hermitian)"""
        return np.allclose(self.matrix, self.matrix.T.conj(), atol=tolerance)
    
    def is_unitary(self, tolerance: float = 1e-10) -> bool:
        """Check if operator is unitary"""
        identity = np.eye(self.matrix.shape[0])
        return np.allclose(self.matrix @ self.matrix.T.conj(), identity, atol=tolerance) and \
               np.allclose(self.matrix.T.conj() @ self.matrix, identity, atol=tolerance)
```

### Compact Operators

```python
class CompactOperator(BoundedOperator):
    """Compact operator (maps bounded sets to relatively compact sets)"""
    
    def __init__(self, kernel: Callable = None, matrix: np.ndarray = None):
        super().__init__(matrix=matrix)
        self.kernel = kernel
    
    @staticmethod
    def is_compact(matrix: np.ndarray, tolerance: float = 1e-10) -> bool:
        """Check if matrix operator is compact (all finite rank or approximated)"""
        # For finite-dimensional, all linear operators are compact
        return True


class HilbertSchmidtOperator(CompactOperator):
    """Hilbert-Schmidt operator (square-summable kernel)"""
    
    def __init__(self, kernel: Callable):
        self.kernel = kernel
    
    def hilbert_schmidt_norm(self, n: int = 100) -> float:
        """Compute Hilbert-Schmidt norm: √(∫|K(x,y)|² dxdy)"""
        # Approximate numerical computation
        x = np.linspace(0, 1, n)
        y = np.linspace(0, 1, n)
        X, Y = np.meshgrid(x, y)
        
        K_vals = np.array([[self.kernel(xi, yi) for xi, yi in zip(Xi, Yi)] 
                          for Xi, Yi in zip(X, Y)])
        
        return np.sqrt(np.sum(K_vals ** 2) * (1/n) ** 2)
    
    def is_hilbert_schmidt(self, tolerance: float = 1e-10) -> bool:
        """Check if operator is Hilbert-Schmidt"""
        return np.isfinite(self.hilbert_schmidt_norm())
```

-----

## Spectral Theory

### Eigenvalues and Eigenvectors

```python
class SpectralAnalysis:
    """Spectral analysis for operators"""
    
    @staticmethod
    def eigenvalues(matrix: np.ndarray) -> np.ndarray:
        """Compute eigenvalues"""
        return np.linalg.eigvals(matrix)
    
    @staticmethod
    def eigenvectors(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute eigenvalues and eigenvectors"""
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return eigenvalues, eigenvectors
    
    @staticmethod
    def spectral_radius(matrix: np.ndarray) -> float:
        """Spectral radius: max(|λ|)"""
        return np.max(np.abs(np.linalg.eigvals(matrix)))
    
    @staticmethod
    def spectral_norm(matrix: np.ndarray) -> float:
        """Spectral norm (largest singular value)"""
        return np.linalg.norm(matrix, ord=2)
    
    @staticmethod
    def is_spectral_bounded(matrix: np.ndarray) -> bool:
        """Check if spectral radius ≤ 1 for stability"""
        return SpectralAnalysis.spectral_radius(matrix) <= 1
    
    @staticmethod
    def spectral_decomposition(matrix: np.ndarray) -> dict:
        """Spectral decomposition for diagonalizable matrix"""
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        # Check if diagonalizable
        if np.linalg.matrix_rank(eigenvectors) < len(eigenvalues):
            return {'diagonalizable': False}
        
        # Construct spectral decomposition
        spectral_proj = {}
        for i, lam in enumerate(eigenvalues):
            v = eigenvectors[:, i]
            P = np.outer(v, v.conj()) / np.dot(v.conj(), v)
            spectral_proj[lam] = P
        
        return {
            'diagonalizable': True,
            'eigenvalues': eigenvalues,
            'projectors': spectral_proj
        }
```

### Spectrum of Operators

```python
class Spectrum:
    """Spectrum of a bounded operator"""
    
    @staticmethod
    def point_spectrum(operator: BoundedOperator) -> np.ndarray:
        """Point spectrum (eigenvalues)"""
        matrix = operator.matrix
        return np.linalg.eigvals(matrix)
    
    @staticmethod
    def resolvent_set(operator: BoundedOperator) -> List[complex]:
        """Resolvent set: λ where (λI - T) is invertible"""
        matrix = operator.matrix
        eigenvalues = np.linalg.eigvals(matrix)
        
        # Approximate: check if near-zero eigenvalues exist
        resolvent = [lam for lam in eigenvalues if abs(lam) > 1e-10]
        return resolvent
    
    @staticmethod
    def approximate_point_spectrum(operator: BoundedOperator, 
                                   num_vectors: int = 100) -> List[float]:
        """Approximate point spectrum using numerical methods"""
        spectrum = []
        
        for _ in range(num_vectors):
            x = np.random.randn(operator.matrix.shape[0])
            x = x / np.linalg.norm(x)
            
            Tx = operator(x)
            rayleigh_quotient = np.dot(x.conj(), Tx) / np.dot(x.conj(), x)
            spectrum.append(rayleigh_quotient)
        
        return spectrum


class SpectralTheorem:
    """Spectral theorem for self-adjoint operators"""
    
    @staticmethod
    def spectral_theorem_real(matrix: np.ndarray) -> dict:
        """Spectral theorem for real symmetric matrices"""
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        
        # Diagonalize: A = QΛQ^T
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'diagonalization': 'A = QΛQ^T',
            'is_positive_definite': all(eigenvalues > 0),
            'is_positive_semidefinite': all(eigenvalues >= 0)
        }
    
    @staticmethod
    def spectral_theorem_complex(matrix: np.ndarray) -> dict:
        """Spectral theorem for complex Hermitian matrices"""
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        
        # Diagonalize: A = UΛU^*
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'diagonalization': 'A = UΛU*',
            'is_positive_definite': all(eigenvalues > 0)
        }
```

-----

## Fourier Analysis

### Fourier Series

```python
class FourierSeries:
    """Fourier series expansion"""
    
    def __init__(self, n_harmonics: int = 10):
        self.n_harmonics = n_harmonics
        self.a_coefficients = []
        self.b_coefficients = []
    
    def fit(self, f: Callable, a: float = 0, b: float = 2*np.pi) -> 'FourierSeries':
        """Compute Fourier coefficients"""
        self.a0 = (2 / (b - a)) * np.trapz([f(x) for x in np.linspace(a, b, 1000)], 
                                           np.linspace(a, b, 1000))
        
        self.a_coefficients = []
        self.b_coefficients = []
        
        for n in range(1, self.n_harmonics + 1):
            a_n = (2 / (b - a)) * np.trapz([f(x) * np.cos(n * x) for x in np.linspace(a, b, 1000)],
                                          np.linspace(a, b, 1000))
            b_n = (2 / (b - a)) * np.trapz([f(x) * np.sin(n * x) for x in np.linspace(a, b, 1000)],
                                          np.linspace(a, b, 1000))
            
            self.a_coefficients.append(a_n)
            self.b_coefficients.append(b_n)
        
        return self
    
    def predict(self, x: float) -> float:
        """Evaluate Fourier series"""
        result = self.a0 / 2
        
        for n in range(1, self.n_harmonics + 1):
            result += self.a_coefficients[n-1] * np.cos(n * x)
            result += self.b_coefficients[n-1] * np.sin(n * x)
        
        return result
    
    def convergence_check(self, f: Callable, x: float, tolerance: float = 1e-6) -> bool:
        """Check pointwise convergence"""
        max_harmonics = 50
        prev_result = 0
        
        for n in range(1, max_harmonics + 1):
            temp_fourier = FourierSeries(n_harmonics=n)
            temp_fourier.fit(f)
            result = temp_fourier.predict(x)
            
            if abs(result - prev_result) < tolerance:
                return True
            prev_result = result
        
        return False
```

### Fourier Transform

```python
class FourierTransform:
    """Continuous Fourier transform"""
    
    @staticmethod
    def fft(signal: np.ndarray, sampling_rate: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """Fast Fourier Transform"""
        n = len(signal)
        freqs = np.fft.fftfreq(n, 1/sampling_rate)
        fft_vals = np.fft.fft(signal)
        
        # Only positive frequencies
        positive_freqs = freqs[:n//2]
        positive_fft = np.abs(fft_vals[:n//2])
        
        return positive_freqs, positive_fft
    
    @staticmethod
    def inverse_fft(freq_domain: np.ndarray, 
                   sampling_rate: float = 1.0) -> np.ndarray:
        """Inverse FFT"""
        return np.fft.ifft(freq_domain).real
    
    @staticmethod
    def power_spectrum(signal: np.ndarray) -> np.ndarray:
        """Compute power spectrum"""
        fft_vals = np.fft.fft(signal)
        return np.abs(fft_vals) ** 2
    
    @staticmethod
    def convolution_theorem(f: np.ndarray, g: np.ndarray) -> np.ndarray:
        """Convolution via Fourier transform"""
        return np.fft.ifft(np.fft.fft(f) * np.fft.fft(g)).real
```

-----

## Functional Calculus

### Borel Functional Calculus

```python
class FunctionalCalculus:
    """Functional calculus for operators"""
    
    @staticmethod
    def polynomial_calculus(matrix: np.ndarray, coeffs: List[float]) -> np.ndarray:
        """Evaluate polynomial p(T) = a₀I + a₁T + a₂T² + ..."""
        result = coeffs[0] * np.eye(matrix.shape[0])
        power = np.eye(matrix.shape[0])
        
        for a in coeffs[1:]:
            power = power @ matrix
            result = result + a * power
        
        return result
    
    @staticmethod
    def spectral_mapping(matrix: np.ndarray, f: Callable) -> np.ndarray:
        """Apply function to spectrum: f(T) = Qf(Λ)Q^*"""
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        
        # Apply function to eigenvalues
        f_eigenvalues = np.array([f(lam) for lam in eigenvalues])
        
        # Reconstruct
        return eigenvectors @ np.diag(f_eigenvalues) @ eigenvectors.T
    
    @staticmethod
    def exponential(matrix: np.ndarray) -> np.ndarray:
        """Matrix exponential e^T"""
        return FunctionalCalculus.spectral_mapping(matrix, np.exp)
    
    @staticmethod
    def logarithm(matrix: np.ndarray) -> np.ndarray:
        """Matrix logarithm log(T)"""
        return FunctionalCalculus.spectral_mapping(matrix, np.log)
    
    @staticmethod
    def square_root(matrix: np.ndarray) -> np.ndarray:
        """Matrix square root T^(1/2)"""
        return FunctionalCalculus.spectral_mapping(matrix, np.sqrt)
```

-----

## Applications

### Quantum Mechanics

```python
class QuantumState:
    """Quantum state in Hilbert space"""
    
    def __init__(self, vector: np.ndarray):
        # Normalize
        self.vector = vector / np.linalg.norm(vector)
    
    def expectation(self, operator: np.ndarray) -> float:
        """Expectation value ⟨ψ|A|ψ⟩"""
        return np.vdot(self.vector, operator @ self.vector).real
    
    def probability(self, projector: np.ndarray) -> float:
        """Probability of measurement outcome"""
        return abs(np.vdot(self.vector, projector @ self.vector)) ** 2
    
    def evolve(self, hamiltonian: np.ndarray, time: float) -> 'QuantumState':
        """Time evolution under Hamiltonian: e^(-iHt)|ψ⟩"""
        from scipy.linalg import expm
        evolution = expm(-1j * hamiltonian * time)
        new_vector = evolution @ self.vector
        return QuantumState(new_vector)


class QuantumOperator:
    """Common quantum operators"""
    
    @staticmethod
    def pauli_x(n: int = 2) -> np.ndarray:
        """Pauli-X (NOT) gate"""
        return np.array([[0, 1], [1, 0]])
    
    @staticmethod
    def pauli_y(n: int = 2) -> np.ndarray:
        """Pauli-Y gate"""
        return np.array([[0, -1j], [1j, 0]])
    
    @staticmethod
    def pauli_z(n: int = 2) -> np.ndarray:
        """Pauli-Z gate"""
        return np.array([[1, 0], [0, -1]])
    
    @staticmethod
    def hadamard(n: int = 2) -> np.ndarray:
        """Hadamard gate"""
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
```

### Sturm-Liouville Theory

```python
class SturmLiouvilleProblem:
    """Sturm-Liouville eigenvalue problem"""
    
    def __init__(self, p: Callable, q: Callable, w: Callable = None,
                 a: float = 0, b: float = np.pi):
        self.p = p  # Weight function coefficient
        self.q = q  # Potential
        self.w = w if w else lambda x: 1  # Weight function
        self.a = a
        self.b = b
    
    def eigenvalues(self, n: int = 5) -> List[float]:
        """Approximate eigenvalues"""
        # For simple cases, use analytical solutions
        # General case requires numerical methods
        return [n**2 for n in range(1, n+1)]
    
    def eigenfunctions(self, n: int = 5) -> List[Callable]:
        """Eigenfunctions"""
        return [lambda x, k=k: np.sin(k * x) for k in range(1, n+1)]
    
    def orthogonality_check(self, i: int, j: int) -> bool:
        """Check orthogonality of eigenfunctions"""
        if i == j:
            return True
        
        xi = np.linspace(self.a, self.b, 1000)
        fi = np.sin(i * xi)
        fj = np.sin(j * xi)
        
        inner_product = np.trapz(fi * fj * self.w(xi), xi)
        return abs(inner_product) < 1e-10
```

-----

## Key Theorems

| Theorem | Statement | Application |
|---------|-----------|--------------|
| **Hahn-Banach** | Extend linear functionals | Functional extension |
| **Uniform Boundedness** | Pointwise bounded ⇒ uniformly bounded | Baire category |
| **Open Mapping** | Open continuous linear maps | Inverse operator |
| **Closed Graph** | Graph closed ⇔ operator bounded | Boundedness |
| **Riesz Representation** | Hilbert space duality | Dual spaces |
| **Spectral** | A = ∫ λ dE_λ | Operator decomposition |
