---
name: rocketsmith
description: Design 3D-printed hobby high-power rockets (NAR/TRA Class 2, certified commercial motors only) — airframe, nose cone and fin geometry, Barrowman stability with fin sizing to a target caliber, 1-D flight simulation (apogee, rail-exit speed, thrust-to-weight, descent rate), printed-part mass from wall/infill settings, measured-mass and flown-apogee calibration, and printable STEP/STL for nose cone and fin can. Based on RocketSmith (Barati Farimani Lab). Use for rocket design-for-AM, stability checks, flight prediction, or post-flight calibration.
---

# RocketSmith: design for AM of high-power rockets

RocketSmith (Pak et al., arXiv:2606.00097, 2026) designed four FDM-printed high-power rockets. All
four launched stably and two were recovered reflyable. Altimeter apogees came in at 80–84% of the
predictions.

Its key idea: **the LLM orchestrates and every number comes from a tool**, because LLMs that iterate
numbers themselves plateau. `scripts/rocket.py` provides those tools. It needs numpy and matplotlib,
plus CadQuery for parts. Details and the paper's flight data are in `references/paper-notes.md`.

**Scope and safety.** This skill covers airframe design for **certified commercial motors** within
the flyer's certification:
- H–I motors need L1 and J–L need L2; Class 2 ends at 40,960 N·s total impulse.
- Motor, propellant, igniter and ejection-charge design or sizing are out of scope. Point users to
  the motor manufacturer, their certification and the Range Safety Officer.
- Every design is a *candidate for review*, never a go-for-launch.

## Workflow (mirrors RocketSmith's skills)
1. **Motor selection.**
   - Use the manufacturer's RASP `.eng` file from thrustcurve.org (`--eng`).
   - `motors` lists the built-in certification summaries for the paper's motors, H100W and J425R.
   - Check that the motor letter matches the user's certification level.
2. **Design** in `design.json`, with the nose cone, body segments, fins, internal masses and print
   settings. Size parts to the user's printer build volume (the paper split HP2 into three parts to
   fit an Ender 3 and an Ender 5 Plus).
3. **Stability analysis:**
   - Run `check design.json` for CG and CP, stability at liftoff and burnout, rail-exit speed,
     thrust-to-weight, Mach and descent rate.
   - If stability is out of range, `fins design.json --target 1.25 [--lever span_mm|root_mm|tip_mm] --out sized.json`
     resizes the fins. When fins can't reach the target, move mass forward (avionics bay, nose
     weight) or lengthen the airframe.
4. **Predict the flight:**
   `simulate sized.json --plot flight.png [--cd 0.55 --rail 1.83]`.
   - Use Cd 0.45–0.55 for smooth airframes.
   - **Printed rockets flew at Cd ≈ 0.8** in the paper's data. Say which value you used.
5. **Generate structures:** `cad sized.json --out parts/` writes the nose cone (ogive or other
   shape, with shoulder) and the fin can (tube, fins and an integrated motor mount), as STEP and STL.
   - Then add the details the paper's agent added on request: shear-pin and heat-insert pilot holes,
     eyebolt holes, rail-button bosses, avionics slots. Use `cadsmith-text-to-cad` or edit the
     CadQuery code.
   - Print in **PETG or ABS, not PLA** (heat). Use 4–5 walls, gyroid infill and 0.2 mm layers.
6. **Mass calibration:** slice the parts, weigh them after printing, then
   `calibrate design.json --weighed nose=412,fincan=1265 [--cg 520]`. Re-check stability with the
   real masses; the paper's stability shifted with every manufactured part.
7. **After flight:** `calibrate design.json --weighed "" --apogee 276` fits the airframe's real Cd
   for the next prediction.

## Review checklist to hand the user (from the paper's failures)
- **HP1:** the eyebolt pulled out of the printed baffle and the lower airframe split. Make baffles
  and anchor points stronger than the printed walls, or anchor to the motor mount.
- **HP2:** the recovery bay didn't separate. Check shear-pin count against separation force, and
  check the fit.
- **HP3:** a friction-fit nose cone worked, at lower ejection resistance.
- Weathercocking: stability much above 2 cal in wind costs altitude and drift.

Cite: Pak et al., *RocketSmith*, arXiv:2606.00097 (2026).
