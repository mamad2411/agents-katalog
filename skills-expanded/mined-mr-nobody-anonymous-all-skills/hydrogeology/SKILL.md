---
name: hydrogeology
description: "Groundwater flow, Darcy's law, aquifer test analysis, contaminant transport, and numerical groundwater modeling"
category: earth-science
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/earth-science/hydrogeology/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Hydrogeology

## Scope
Hydrogeology studies the distribution and movement of groundwater in soil, rock, and aquifers of the upper crust.

## Core Formulations & Equations
- **Darcy's Law**:
  $$Q = -K A \frac{dh}{dl} \implies q = \frac{Q}{A} = -K \frac{dh}{dl}$$
  where $K$ is hydraulic conductivity ($m/s$), $dh/dl$ hydraulic gradient.
- **Confined Aquifer Flow Equation**:
  $$S_s \frac{\partial h}{\partial t} = \nabla \cdot (K \nabla h)$$
- **Theis Solution (Pumping Test Analysis)**:
  $$s = \frac{Q}{4\pi T} W(u), \quad u = \frac{r^2 S}{4 T t}$$

## Tools & Standards
- **Software**: MODFLOW, FloPy (Python), MT3DMS, FEFLOW.
- **Canonical References**: Freeze & Cherry — *Groundwater*; Fetter — *Applied Hydrogeology*.
