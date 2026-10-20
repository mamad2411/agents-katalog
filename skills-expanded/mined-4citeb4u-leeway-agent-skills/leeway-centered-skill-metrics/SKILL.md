---

name: leeway-centered-skill-metrics

description: Governance for centered multidimensional skill/release evaluation using zero-centered deviation vectors, positive-definite weighted quadratic potentials, admissible ellipsoids, and evidence-bound measurements. Compatible with LeeWay Formula staging without inventing canonical Formula constants or mappings.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards

  mode: centered-evaluation-geometry

  stage: measurement-and-shiproom-evaluation

---

# LeeWay Centered Skill Metrics

## Boundary

This skill formalizes an evaluation geometry proposed by the Creator. It is not a claim that the canonical LeeWay Formula already uses these exact dimensions, weights, constants, or equations. Bind to canonical Formula only when its real implementation/version/hash supplies the mapping.

## General model

Let x be a measured deviation vector from an explicitly defined target/equilibrium x*=0. Let W be symmetric positive-definite. Define E(x)=x^T W x and a bounded score S(x)=exp(-E(x)) when that transform is appropriate. An admissible gate may use x^T W x <= R^2.

## Measurement law

Zero must mean a defined target deviation, not an impossible fantasy. Normalize asymmetric or one-sided objectives before centering. Example: latency below an SLA is not naturally zero latency; define deviation from the target/envelope. Availability, coverage, security risk, cost, capacity, accessibility, delivery value and human factors require explicit units and normalization.

## Coupling law

Off-diagonal W terms are allowed only when measured/justified coupling exists. Do not invent covariance/coupling weights. If dimensions lack comparable evidence, preserve them separately rather than hiding uncertainty inside one score.

## Department families

SWE: correctness/coverage/determinism/latency/complexity/reliability. SRE: drift/burn/MTTD/MTTR/availability/capacity. Product: scope/delivery/value/experiment evidence/dependency risk. Security: residual threat/control coverage/exploitability/remediation. UX: accessibility/friction/error rate/task success/research evidence. Leadership: demand-capacity/risk/cost/dependency volatility/continuity.

## Shiproom geometry

Concatenate normalized department deviation vectors into X. A block-diagonal or evidence-supported coupled Omega may define X^T Omega X <= R^2. Passing the aggregate gate never erases hard constraints: a critical security, legal, authority, safety, or reliability failure can remain independently blocking.

## Veritas

Every metric must bind definition, unit, source, timestamp/window, target, transformation, uncertainty, weight provenance, and acceptance threshold. Generated numbers are not measurements.

## Formula handoff

Context Engineering prepares measured state; Formula Governance may use the canonical implementation if available; Centered Skill Metrics supplies an evidence-bound geometric evaluation representation; Veritas validates measurements and gate claims.