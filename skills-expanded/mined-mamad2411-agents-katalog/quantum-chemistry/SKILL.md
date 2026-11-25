---

## name: quantum-chemistry
description: >
  Expert quantum chemistry assistant for computational chemists and researchers. Use this skill whenever the user needs:
  understanding molecular orbital theory, wave function methods, density functional theory, computational chemistry calculations,
  or any rigorous academic treatment of quantum chemistry. Covers electronic structure theory, molecular properties, and spectroscopy.
license: MIT
compatibility: opencode
metadata:
  audience: computational chemists, researchers
  category: chemistry

# Quantum Chemistry — Academic Research Assistant

Covers: **Wave Function Theory · Molecular Orbital Theory · Hartree-Fock · Density Functional Theory · Basis Sets · Molecular Properties · Computational Methods**

---

## Fundamental Concepts

### Schrödinger Equation

```
Time-independent: ĤΨ = EΨ

Where:
- Ĥ = Hamiltonian operator
- Ψ = Wave function (electronic)
- E = Energy

Hamiltonian for N-electron system:
Ĥ = Σᵢ(-½∇ᵢ²) + Σᵢ₍ᵣ₎ Σⱼ₍ᵣ₎(Zᵣ/|rᵢ-rᵣ|) + Σᵢ<ⱼ(1/|rᵢ-rⱼ|)
     Kinetic     Nuclear-electron     Electron-electron
```

### Born-Oppenheimer Approximation

- Separate nuclear and electronic motion
- Fix nuclei, solve electronic problem
- Potential energy surface (PES)

```python
class QuantumChemistryBasics:
    """Fundamental quantum chemistry calculations"""
    
    def hydrogen_atom_solutions(self, n, l, m):
        """
        Hydrogen atom wave functions
        n: principal quantum number (1,2,3,...)
        l: angular momentum (0 to n-1)
        m: magnetic quantum number (-l to l)
        """
        # Solutions include associated Laguerre polynomials
        # and spherical harmonics
        pass
    
    def calculate_scf_energy(self, one_electron, two_electron, density):
        """
        Calculate SCF energy
        E = Σᵢⱼ Pᵢⱼ Hᵢⱼ + ½ Σᵢⱼ Σₖₗ Pᵢⱼ Pₖₗ(ij|kl) - ½ Σᵢₖ Σⱼₗ Pᵢₖ Pⱼₗ(ij|kl)
        """
        one_electron_term = sum(one_electron[i][j] * density[i][j] 
                               for i in range(len(density)) 
                               for j in range(len(density)))
        
        return one_electron_term
    
    # Units
    def eV_to_hartree(self, eV):
        """Convert electronvolts to Hartree"""
        return eV / 27.2114
    
    def angstrom_to_bohr(self, angstrom):
        """Convert Angstrom to Bohr"""
        return angstrom * 1.8897259886
```

---

## Molecular Orbital Theory

### LCAO-MO Approximation

```
Ψᵢ(r) = Σᵣ Cᵣᵢ φᵣ(r)

Where:
- Ψᵢ = molecular orbital i
- Cᵣᵢ = molecular orbital coefficient
- φᵣ = atomic orbital
```

### Orbital Types

|Orbital Type|Bonding Character|Energy|
|------------|-----------------|-------|
|σ|Symmetric (head-on)|Bonding < antibonding|
|π|Asymmetric (side-on)|Bonding < antibonding|
|δ|4-lobed|Delocalized systems|

```python
class MolecularOrbitals:
    """Molecular orbital calculations"""
    
    def calculate_mo_coefficients(self, huckel_matrix):
        """
        Solve secular determinant
        |H - ES| = 0
        """
        import numpy as np
        
        eigenvalues, eigenvectors = np.linalg.eig(huckel_matrix)
        
        # Sort by energy
        idx = eigenvalues.argsort()
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        return eigenvalues, eigenvectors
    
    def assign_orbital_occupancy(self, num_electrons, mo_energies):
        """
        Assign electrons to MOs (Aufbau principle)
        """
        import numpy as np
        
        n = num_electrons
        
        # Sort orbitals by energy
        sorted_indices = np.argsort(mo_energies)
        
        # Fill with 2 electrons each
        occupancy = np.zeros(len(mo_energies))
        
        for i, idx in enumerate(sorted_indices):
            if n >= 2:
                occupancy[idx] = 2
                n -= 2
            elif n == 1:
                occupancy[idx] = 1
                n -= 1
            else:
                break
        
        return occupancy
    
    def calculate_homo_lumo(self, mo_energies, occupancy):
        """
        Identify HOMO and LUMO orbitals
        """
        n_electrons = sum(occupancy)
        
        homo_idx = int(n_electrons / 2) - 1
        lumo_idx = homo_idx + 1
        
        return {
            "homo_energy": mo_energies[homo_idx],
            "lumo_energy": mo_energies[lumo_idx],
            "gap": mo_energies[lumo_idx] - mo_energies[homo_idx]
        }
```

---

## Hartree-Fock Theory

### Self-Consistent Field Method

```
1. Guess initial density matrix
2. Calculate Fock matrix: F = H + G(P)
3. Solve eigenvalue problem: FC = SCE
4. Form new density: P = 2Σ|Cᵢ|²
5. Check convergence; repeat if needed
```

### Electron Correlation

|Method|Description|Accuracy|
|-------|-----------|--------|
|Hartree-Fock|Mean field only|~0.5-1.0 Hartree error|
|MP2|Møller-Plesset perturbation|Mild correlation|
|CCSD|Toupled-cluster singles/doubles|Very good|
|CCSD(T)|"Gold standard"|Excellent|

```python
class HartreeFock:
    """Hartree-Fock implementation"""
    
    def initialize_density(self, num_electrons, num_basis):
        """
        Initial guess: core Hamiltonian
        """
        import numpy as np
        
        # Superposition of atomic densities
        density = np.zeros((num_basis, num_basis))
        
        # Simple guess: diagonal elements
        for i in range(num_electrons // 2):
            density[i, i] = 2
        
        return density
    
    def compute_fock_matrix(self, h_core, two_electron, density):
        """
        F = H + G(P)
        Gᵢⱼ = Σₖₗ Pₖₗ[(ij|kl) - ½(ik|jl)]
        """
        import numpy as np
        
        n = len(h_core)
        g_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        g_matrix[i,j] += density[k,l] * (
                            two_electron[i,j,k,l] - 
                            0.5 * two_electron[i,k,j,l]
                        )
        
        fock = h_core + g_matrix
        
        return fock
    
    def scf_iteration(self, h_core, two_electron, max_iter=100, tol=1e-6):
        """
        Self-consistent field iterations
        """
        import numpy as np
        
        # Initial guess
        density = self.initialize_density(8, len(h_core))
        
        for iteration in range(max_iter):
            # Compute Fock
            fock = self.compute_fock_matrix(h_core, two_electron, density)
            
            # Diagonalize
            mo_coeffs = np.linalg.eigvalsh(fock)
            
            # New density
            new_density = self.construct_density(mo_coeffs, 8)
            
            # Check convergence
            diff = np.max(np.abs(new_density - density))
            
            if diff < tol:
                print(f"Converged in {iteration} iterations")
                return mo_coeffs, new_density
            
            density = new_density
        
        print("Failed to converge")
        return None, None
```

---

## Density Functional Theory

### Exchange-Correlation Functionals

|Functional|Type|Performance|
|-----------|-----|-----------|
|LDA|Local density|Limited accuracy|
|GGA|Gradient corrected|Better for molecules|
|Hybrid|Mixture of HF/DFT|Very good|
|Range-separated|Long-range corrected|Best for properties|

```python
class DensityFunctionalTheory:
    """DFT calculations"""
    
    # Common functionals
    FUNCTIONALS = {
        "B3LYP": {
            "type": "Hybrid GGA",
            "exchange": "20% HF + 80% GGA",
            "recommended_for": "Organic molecules"
        },
        "PBE0": {
            "type": "Hybrid GGA", 
            "exchange": "25% HF + 75% GGA",
            "recommended_for": "General purpose"
        },
        "M06-2X": {
            "type": "Meta-hybrid",
            "recommended_for": "Non-covalent interactions"
        },
        "wB97X-D": {
            "type": "Range-separated hybrid",
            "recommended_for": "Dispersion"
        }
    }
    
    # Basis sets
    BASIS_SETS = {
        "STO-3G": {"description": "Minimal basis, 3 Gaussians per STO"},
        "6-31G": {"description": "Double-zeta, polarization on heavy"},
        "6-311G": {"description": "Triple-zeta, polarization"},
        "cc-pVTZ": {"description": "Correlation-consistent, triple-zeta"},
        "def2-TZVP": {"description": "Def2, good balance speed/accuracy"}
    }
```

---

## Basis Sets

### Gaussian-Type Orbitals

```
φ(r) = N × x^l y^m z^n × exp(-αr²)

Where:
- l,m,n = angular momentum
- α = exponent (controls width)
- N = normalization constant
```

### Effective Core Potentials

- Replace core electrons
- Relativistic effects for heavy atoms
- LANL2DZ, Stuttgart-Copenhagen

---

## Molecular Properties

### Dipole Moment

```python
class MolecularProperties:
    """Calculate molecular properties"""
    
    def calculate_dipole_moment(self, charges, coordinates):
        """
        μ = Σᵢ qᵢ rᵢ
        """
        import numpy as np
        
        dipole = np.zeros(3)
        
        for q, r in zip(charges, coordinates):
            dipole += q * r
        
        return {
            "dipole_vector": dipole,
            "dipole_magnitude": np.linalg.norm(dipole),
            "units": "Debye"
        }
    
    def calculate_polarizability(self, fock_ao, mo_coeffs):
        """
        Polarizability tensor from finite field
        """
        pass
    
    def calculate_nmr_shielding(self, density, gauge_origin):
        """
        NMR chemical shifts
        """
        pass
    
    def calculate_vibrational_frequencies(self, hessian, masses):
        """
        Frequency calculation from Hessian
        """
        import numpy as np
        
        # Mass-weighted Hessian
        # Diagonalize
        # Convert to cm⁻¹
        
        frequencies = np.linalg.eigvalsh(hessian)
        
        return frequencies * 0.529177  # Convert
```

---

## Computational Methods

### Geometry Optimization

|Method|Description|Use Case|
|-------|-----------|--------|
|Steepest descent|Follow gradient|Simple, slow|
|Conjugate gradient|Better than steepest|Medium systems|
|Newton-Raphson|Use Hessian|Fast near minimum|
|BFGS|Quasi-Newton|Default for molecules|

### Transition States

|Method|Description|
|-------|-----------|
|QST2|Interpolate between reactants/products|
|GRRM|Automated reaction path|
|String method|String method for MEP|

---

## Common Errors to Avoid

1. **Wrong basis set** — Too small = inaccurate, too large = slow
2. **Neglecting relativity** — Heavy atoms need it
3. **Ignoring dispersion** — Use dispersion-corrected DFT
4. **Not verifying convergence** — SCF and geometry must converge
5. **Wrong functional choice** — Different functionals for different properties
6. **Single-point energies alone** — Always verify with frequency calculation
7. **Basis set superposition error** — Use counterpoise correction for complexes
8. **Confusion about units** — Atomic units internally, convert for output

