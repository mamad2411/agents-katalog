---
name: outdoor-gps
description: "Use when building outdoor robot navigation with GPS/GNSS — choosing receivers, setting up RTK/NTRIP corrections, fusing GPS with IMU and wheel odometry, handling dropouts, implementing geofences, or debugging heading/position errors. Provides accuracy budgets, UTM vs lat/lon code patterns, robot_localization configuration, point-in-polygon geofencing with hysteresis, and compass calibration procedures near motors."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Outdoor GPS/GNSS Navigation

Expert knowledge for GPS-based outdoor robot navigation: what accuracy you actually get, how to get centimeter accuracy with RTK, how to survive GPS dropout, and how to not let coordinate-frame bugs drive your robot into a fence.

---

## 1. GPS Accuracy Reality Check

The single most common outdoor-nav failure is designing around a fantasy accuracy number. Here is what you actually get:

| Receiver class | Horizontal accuracy (typical, open sky) | Update rate | Cost | Examples |
|---|---|---|---|---|
| Consumer / phone-grade | 3–5 m CEP, 10–30 m in multipath | 1 Hz | $10–30 | NEO-M8N, phone GNSS |
| Multi-band standalone | 1–2 m | 5–25 Hz | $50–150 | u-blox NEO-M9N, ZED-F9P (no corrections) |
| SBAS (WAAS/EGNOS) | 1–2 m | 1–10 Hz | same hardware | Free correction over satellite |
| DGPS / code corrections | 0.5–1 m | 1–10 Hz | varies | NTRIP DGPS streams |
| RTK Float | 0.1–0.5 m | 5–20 Hz | $200–600 | ZED-F9P + NTRIP, float solution |
| RTK Fixed | 1–2 cm + 1 ppm baseline | 5–20 Hz | $200–600 | ZED-F9P, Septentrio Mosaic, Trimble BD990 |
| PPP (Point Precise Positioning) | 2–10 cm after 10–30 min convergence | 1–5 Hz | service fee | u-blox PointPerfect, Trimble RTX |

Critical implications:

- **A consumer GPS cannot follow a 1 m wide path.** With 3–5 m error, the robot doesn't know which side of a sidewalk it's on. Row crops, sidewalks, mowing patterns → you need RTK Fixed, full stop.
- **Vertical error is 1.5–3× horizontal.** Never use GPS altitude for terrain decisions on consumer receivers.
- **RTK degrades 1 ppm per km of baseline** to the base station. At 20 km from the NTRIP base: 1 cm + 2 cm = ~3 cm. Beyond ~35 km, fixed solutions become unreliable; expect float.
- **"RTK Float" is not "almost fixed."** Float means the integer ambiguities are unresolved — error is 10–50 cm and can jump when the ambiguity estimate shifts. Treat float as a *different, worse sensor* in your fusion, not as slightly-noisy fixed.
- **Multipath near buildings/trees adds meters, not centimeters**, and it is *biased* (not zero-mean) — averaging does not remove it. The reported covariance from the receiver typically *underestimates* multipath error by 2–5×.

### Reading fix quality (NMEA GGA field 6 / u-blox carrSoln)

| GGA quality | Meaning | Trust for navigation |
|---|---|---|
| 0 | No fix | None |
| 1 | GPS fix (SPS) | 3–5 m |
| 2 | DGPS | 0.5–1 m |
| 4 | RTK Fixed | 1–2 cm |
| 5 | RTK Float | 10–50 cm, jumpy |

Your fusion stack MUST switch covariance based on this field. Hardcoding one GPS covariance is the #1 fusion bug in outdoor robots.

```python
# Covariance selection by fix type — values are variance (m^2), per axis
GPS_COVARIANCE = {
    0: None,            # no fix: do NOT publish, do NOT fuse
    1: 25.0,            # SPS: sigma ~5 m
    2: 1.0,             # DGPS: sigma ~1 m
    4: 0.0004,          # RTK fixed: sigma ~2 cm
    5: 0.09,            # RTK float: sigma ~30 cm (and it's biased; inflate!)
}
```

Also monitor:
- **HDOP** > 2.0 → geometry is poor, inflate covariance ×HDOP².
- **Satellite count** < 6 → expect degradation; < 4 → no 3D fix possible.
- **Age of differential corrections** (GGA field 13): > 10 s, RTK will fall to float; > 60 s, falls to SPS on most receivers.

---

## 2. RTK + NTRIP Setup

RTK works by streaming raw corrections (RTCM 3.x messages) from a base station at a *surveyed, known position* to your rover over the internet (NTRIP) or radio.

### Correction sources, in order of preference

1. **State/national CORS networks** — many are free (e.g., US state DOT networks, EUREF in Europe). Search "[your state] CORS NTRIP".
2. **Commercial networks** — PointOneNav, Skylark (Swift), u-blox PointPerfect, Hexagon SmartNet. ~$50–100/mo, dense coverage, VRS (virtual reference station) so baseline is always short.
3. **Your own base** — second ZED-F9P + antenna on a surveyed point, running an NTRIP caster (SNIP, RTK2go for testing). Required for remote sites. Survey-in the base for ≥24 h or use a known mark; **every cm of base position error becomes a cm of systematic rover error.**

### RTCM messages you need

Minimum for GPS+GLONASS+Galileo+BeiDou RTK:
- **1005/1006** — base station position (without this, no fix ever)
- **1074/1084/1094/1124** — MSM4 observables per constellation (or MSM7: 1077/1087/1097/1127)
- **1230** — GLONASS code-phase biases
- Rate: observables at 1 Hz, 1005 at 0.1 Hz is fine.

### NTRIP client (Python, production pattern)

```python
import socket, base64, serial, time

def ntrip_client(caster, port, mountpoint, user, pwd, gps_serial: serial.Serial):
    """Stream RTCM from NTRIP caster into the receiver's UART.
    Reconnects on failure. Sends GGA upstream every 10 s (required by
    VRS networks to position the virtual base near you)."""
    auth = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    req = (f"GET /{mountpoint} HTTP/1.1\r\n"
           f"Host: {caster}\r\n"
           f"Ntrip-Version: Ntrip/2.0\r\n"
           f"User-Agent: NTRIP robot-client/1.0\r\n"
           f"Authorization: Basic {auth}\r\n\r\n")
    while True:
        try:
            s = socket.create_connection((caster, port), timeout=10)
            s.sendall(req.encode())
            hdr = s.recv(4096)
            if b"200" not in hdr.split(b"\r\n")[0]:
                raise ConnectionError(f"Caster refused: {hdr[:80]!r}")
            s.settimeout(5)
            last_gga = 0.0
            while True:
                data = s.recv(4096)
                if not data:
                    raise ConnectionError("caster closed stream")
                gps_serial.write(data)          # RTCM -> receiver UART2/USB
                if time.time() - last_gga > 10:
                    gga = read_latest_gga()      # from receiver NMEA stream
                    if gga:
                        s.sendall((gga + "\r\n").encode())
                    last_gga = time.time()
        except (OSError, ConnectionError) as e:
            print(f"NTRIP reconnect after error: {e}")
            time.sleep(5)   # backoff; do NOT hammer the caster
```

Production gotchas:
- **VRS mountpoints require GGA upstream** or they send nothing / disconnect. The silent symptom is "connected but never gets RTK fix."
- **Cellular dead zones**: buffer is pointless — corrections older than ~10 s are useless. Instead, design the *robot behavior* for correction loss (Section 4).
- **Time to first fix**: cold RTK fix takes 30 s–5 min with good sky. If it takes longer: check baseline length, check 1230 message presence (GLONASS ambiguities won't resolve without it), check antenna.
- **Antenna matters more than receiver.** A $50 helical or survey-grade antenna with a ground plane (≥10 cm metal disc) outperforms a patch antenna taped to plastic by a full accuracy class. Mount it at the highest point, away from RF emitters (telemetry radios, companion computer USB3 — **USB3 radiates exactly in the GPS L1 band**; shield or separate by >30 cm).

### ROS2 wiring (ZED-F9P)

Use `ublox_gps` or `ublox_dgnss` driver + `ntrip_client` package:

```yaml
# ntrip_client params
host: "rtk2go.com"
port: 2101
mountpoint: "YOUR_MOUNT"
authenticate: true
username: "you@example.com"
password: "none"
# Subscribes /nmea (GGA from driver), publishes /rtcm -> driver fuses it
```

Verify with: `ros2 topic echo /ublox_gps_node/navpvt --field carr_soln` → want `2` (fixed).

---

## 3. Coordinates: UTM vs Lat/Lon in Code

**Rule: lat/lon at the system boundary only (GPS in, telemetry/maps out). All navigation math in a local metric frame.**

Why never do math in lat/lon:
- 1° longitude = 111,320 m × cos(latitude). It varies with latitude; naive `dx = lon2 - lon1` is wrong everywhere and *differently wrong* at different latitudes.
- Floating-point: a `float32` lat has ~1 m resolution. Storing lat/lon in float32 (common when stuffing into a `geometry_msgs/Point`) silently destroys RTK accuracy. **Always float64 for lat/lon.**

### Option A — UTM (standard, use this)

UTM projects to a metric grid in 6°-wide zones. Use `pyproj` or `utm`:

```python
from pyproj import Transformer

# Determine zone ONCE at startup from the datum point; lock it.
def utm_transformer(lat: float, lon: float):
    zone = int((lon + 180) / 6) + 1
    epsg = 32600 + zone if lat >= 0 else 32700 + zone
    return Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)

tf = utm_transformer(datum_lat, datum_lon)
easting, northing = tf.transform(lon, lat)   # NOTE: always_xy => (lon, lat) order!
```

Failure modes that kill robots:
- **Zone boundary crossing**: easting jumps by ~800 km mid-mission. If your operation area is within ~50 km, lock the zone at startup and *force* all conversions through that zone (UTM tolerates modest overrange). Never re-derive the zone per-fix.
- **Argument order**: pyproj default is (lat, lon); with `always_xy=True` it's (lon, lat). Mixing these puts you in the ocean. Always pass `always_xy=True` and write a unit test with a known landmark.
- **Grid convergence**: UTM grid north ≠ true north, by up to ±3° at zone edges. For heading-critical work (mowing stripes), compute convergence: `gamma ≈ (lon - lon_central_meridian) * sin(lat)` and correct, or use Option B.

### Option B — Local tangent plane (ENU), best for robot-local nav

Pick a datum (first RTK fix, or surveyed point), convert everything to East-North-Up meters relative to it. No zone issues, north is true north at the datum:

```python
import math
A = 6378137.0          # WGS84 semi-major
E2 = 6.69437999014e-3  # first eccentricity squared

def lla_to_enu(lat, lon, alt, lat0, lon0, alt0):
    """Sufficiently exact for areas < ~10 km across (error < cm)."""
    lat_r, lat0_r = math.radians(lat), math.radians(lat0)
    dlat = lat_r - lat0_r
    dlon = math.radians(lon - lon0)
    # Radii of curvature at datum
    s = math.sin(lat0_r)
    rn = A / math.sqrt(1 - E2 * s * s)            # prime vertical
    rm = rn * (1 - E2) / (1 - E2 * s * s)         # meridional
    east  = dlon * (rn + alt0) * math.cos(lat0_r)
    north = dlat * (rm + alt0)
    up    = alt - alt0
    return east, north, up
```

Worked example: datum at 51.5000°N. One RTK fix at 51.50010°N, same lon. dlat = 1.0e-4° = 1.745e-6 rad; rm ≈ 6,373,000 m → north ≈ 11.12 m. Sanity check: ~111.2 m per 0.001° lat. If your code says anything else, you have a radians/degrees bug.

**Persist the datum.** If the datum is "first fix after boot," every reboot shifts your saved waypoints and geofence. Store datum lat/lon/alt in config; saved maps and fences are then stable across power cycles.

In ROS2: `robot_localization`'s `navsat_transform_node` does exactly this — it builds a `utm`→`map` transform from the datum. Set `wait_for_datum: true` + a `datum:` parameter for repeatable frames.

---

## 4. GPS + IMU + Wheel Odometry Fusion (Canyon/Dropout Survival)

GPS alone is unusable for control: 1–10 Hz, latency 100–300 ms, jumps on fix-type change, dies under trees/bridges/urban canyons. Standard architecture is dual-EKF (this is the `robot_localization` reference pattern):

```
                       ┌────────────────────────────┐
 wheel odom (50 Hz) ──►│ EKF #1 (odom frame)        │──► odom→base_link
 IMU (100–200 Hz)   ──►│ continuous, smooth,        │    (use for control:
                       │ drifts, never jumps        │     path tracking, PID)
                       └────────────────────────────┘
 wheel odom ──────────►┌────────────────────────────┐
 IMU ─────────────────►│ EKF #2 (map frame)         │──► map→odom
 GPS (as odom from  ──►│ globally accurate,         │    (use for planning,
 navsat_transform)     │ MAY jump on fix change     │     waypoints, geofence)
                       └────────────────────────────┘
```

The split exists because **controllers must never see position jumps** (a 30 cm RTK float→fixed jump through a pure-pursuit controller = steering twitch; a 3 m jump = lunge into a ditch). Control runs on the smooth odom-frame estimate; global goals live in the map frame and the map→odom transform absorbs the jumps.

### Starting configuration (robot_localization, ground robot)

```yaml
# EKF #2 (map). EKF #1 identical minus the GPS input.
ekf_filter_node_map:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true                  # ground robot: pitch/roll/z not estimated
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link
    world_frame: map

    odom0: /wheel/odometry            # config: [x,y,z, r,p,y, vx,vy,vz, vr,vp,vy, ax,ay,az]
    odom0_config: [false, false, false,
                   false, false, false,
                   true,  true,  false,   # fuse vx, vy (velocities, not pose!)
                   false, false, true,    # fuse yaw rate
                   false, false, false]
    odom0_differential: false

    imu0: /imu/data
    imu0_config: [false, false, false,
                  false, false, true,     # absolute yaw ONLY if magnetometer is trustworthy (see §6)
                  false, false, false,
                  false, false, true,     # yaw rate
                  true,  false, false]    # ax for slip detection (optional)
    imu0_remove_gravitational_acceleration: true

    odom1: /odometry/gps              # from navsat_transform_node
    odom1_config: [true,  true,  false,   # fuse x, y position only
                   false, false, false,
                   false, false, false,
                   false, false, false,
                   false, false, false]
    odom1_differential: false
```

Fusion rules that matter:
- **Fuse wheel odometry as VELOCITY, not position.** Wheel position drifts unboundedly; fusing it as pose fights the GPS. Velocity is locally honest.
- **Fuse GPS as position only**, with covariance switched per fix type (§1 table). When fix quality is 0 or corrections age out, **stop publishing** — don't publish with huge covariance; some filter configs still get dragged.
- **Gate GPS innovations.** Before fusing, compute Mahalanobis distance of the GPS measurement vs the filter prediction; reject if > 3σ. Multipath produces confident-looking 5 m outliers that pass covariance checks because the receiver under-reports. `robot_localization`: not built-in for this — wrap the GPS topic in a gating node.

```python
def gate_gps(z_xy, x_pred_xy, P_pred_2x2, R_2x2, chi2_thresh=9.21):  # 99% for 2 DOF
    import numpy as np
    nu = np.asarray(z_xy) - np.asarray(x_pred_xy)
    S = P_pred_2x2 + R_2x2
    d2 = float(nu @ np.linalg.solve(S, nu))
    return d2 < chi2_thresh   # False => drop this GPS fix
```

### Dropout (canyon, tree canopy, under bridge) behavior

Expected drift rates during dropout, well-calibrated system:

| Dead-reckoning source | Drift |
|---|---|
| Wheel odom only | 2–10% of distance traveled; worse on slip (grass, gravel) |
| Wheel + gyro yaw | 1–2% of distance (heading is what kills wheel-only DR) |
| Wheel + tactical IMU + good cal | 0.2–0.5% of distance |

Design the behavior budget: at 1 m/s with wheel+gyro DR (1.5%), you accumulate ~1 m error in 65 s. So:
1. **< 30 s dropout**: continue mission on dead reckoning, inflate position uncertainty.
2. **30 s–N**: slow down (error budget is per-meter, not per-second — slowing buys time), shrink geofence margin (§5).
3. **Uncertainty exceeds safety margin** (e.g., 1σ position error > half the distance to the nearest fence edge): **stop and wait** for fix recovery. Never keep driving on hope.
4. **On reacquisition**: the map-frame estimate jumps to truth. The odom-frame estimate does not — controllers stay smooth, and the planner replans from the corrected map pose.

**RTK float↔fixed oscillation** under partial canopy is a special hell: position hops 20–40 cm at 1 Hz. Mitigate by (a) hysteresis — require 5 s of continuous fixed before tightening covariance back down, (b) rate-limit how fast you shrink the fused covariance.

---

## 5. Geofencing (Point-in-Polygon with Hysteresis)

A geofence is a safety function. It must be: evaluated on the *fused* pose (map frame, meters — never raw lat/lon floats), independent of the mission planner, and fail-safe on estimator divergence.

### Point-in-polygon: ray casting

```python
def point_in_polygon(px, py, poly):   # poly: [(x0,y0), (x1,y1), ...] in METERS (ENU/UTM)
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > py) != (yj > py):
            x_int = (xj - xi) * (py - yi) / (yj - yi) + xi
            if px < x_int:
                inside = not inside
        j = i
    return inside
```

O(n) per check; fine for fences < 1000 vertices at 50 Hz. **Convert fence vertices from lat/lon to ENU once at load time** using the persisted datum — never per-check.

### Signed distance + hysteresis (the part everyone skips)

A raw inside/outside boolean with 2 cm RTK noise at the boundary chatters; with 30 cm float noise it chatters violently — robot oscillates between "stop" and "resume" at the fence line. Use signed distance to the polygon boundary and two thresholds:

```python
import math

def dist_to_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy + 1e-12)))
    return math.hypot(px - (ax + t*dx), py - (ay + t*dy))

def signed_distance(px, py, poly):
    """Positive inside, negative outside."""
    d = min(dist_to_segment(px, py, *poly[i], *poly[(i+1) % len(poly)])
            for i in range(len(poly)))
    return d if point_in_polygon(px, py, poly) else -d

class Geofence:
    """States: OK -> WARN -> BREACH, with hysteresis on re-entry."""
    def __init__(self, poly, warn_margin=2.0, stop_margin=0.5, reentry_margin=1.0):
        self.poly = poly
        self.warn, self.stop, self.reentry = warn_margin, stop_margin, reentry_margin
        self.state = "OK"

    def update(self, px, py, pos_sigma):
        # Inflate margins by current position uncertainty (3-sigma)
        eff_stop = self.stop + 3.0 * pos_sigma
        d = self.signed_d = signed_distance(px, py, self.poly)
        if self.state == "BREACH":
            if d > self.reentry + 3.0 * pos_sigma:   # hysteresis: must come WELL inside
                self.state = "OK"
        elif d < eff_stop:
            self.state = "BREACH"
        elif d < self.warn + 3.0 * pos_sigma:
            self.state = "WARN"
        else:
            self.state = "OK"
        return self.state
```

Non-negotiable geofence rules:
- **Inflate margins by estimator uncertainty** (`3 * sigma` from the EKF covariance). During GPS dropout the effective fence shrinks automatically — this is the mechanism behind §4 rule 3.
- **Size the stop margin for stopping distance**: margin ≥ v²/(2·a_brake) + v·t_react + position error. A 2 m/s robot with 1 m/s² braking and 200 ms reaction needs ≥ 2.4 m before counting GPS error. Velocity-dependent margins are better than static ones.
- **WARN should slow the robot**, not just log. BREACH = controlled stop (not E-stop torque-off on a slope — a dead motor on a hill rolls).
- **Fail-safe on bad data**: no fused pose for > 500 ms, or covariance > threshold → treat as BREACH.
- Holes (keep-out islands inside the fence) are just additional polygons with inverted sign: must be *outside* all keep-outs AND *inside* the boundary.
- Test the fence by **walking the robot to the line under joystick** before trusting it autonomously. Log signed distance continuously.

---

## 6. Heading: Magnetic vs True, and Compass Near Motors

### The three norths

- **True north**: direction to the geographic pole. What your map/ENU frame uses.
- **Magnetic north**: what a magnetometer measures. Differs from true by **declination**: −15° to +20° depending on location (e.g., Seattle ≈ +15.5°E, London ≈ +0.5°, varies ~0.1°/yr). Get it from the World Magnetic Model (`pygeomag`, or `geographiclib`), keyed by lat/lon/date — never hardcode.
- **Grid north** (UTM): differs from true by grid convergence, up to ±3° (§3).

A 15° unhandled declination means a robot commanded "north" drives 26 cm sideways per meter traveled. This is the most common "my robot tracks paths diagonally" bug.

```python
from pygeomag import GeoMag
gm = GeoMag()
res = gm.calculate(glat=47.6, glon=-122.3, alt=0.05, time=2026.44)  # decimal year
declination_deg = res.d   # add to magnetic heading to get true heading
true_heading = (mag_heading + declination_deg) % 360
```

ROS convention trap: `sensor_msgs/Imu` orientation is ENU, yaw=0 facing **East**, counterclockwise-positive. Compass heading is yaw=0 facing **North**, clockwise-positive. Conversion: `enu_yaw_rad = radians(90 - compass_deg)`. Get this wrong and everything is rotated 90° and mirrored.

### Why compasses fail on robots (and what to do)

A magnetometer measures Earth's field (~25–65 µT). Problems on a robot chassis:

- **Hard iron**: permanent magnetization of nearby steel/magnets → constant offset vector in body frame. Calibratable.
- **Soft iron**: ferrous material distorting the field directionally → ellipsoidal distortion. Calibratable.
- **Motor currents**: a brushed/BLDC motor drawing 20 A creates fields of tens of µT at 10–20 cm — *same magnitude as Earth's field*, and **current-dependent, so no static calibration fixes it.**

Mitigation hierarchy (do them in order):
1. **Mount the mag far from motors and power wiring.** Field falls off ~1/r³ from a dipole: doubling distance cuts interference 8×. Top of a mast is the standard answer. Twist motor power pairs (cancels their field).
2. **Calibrate in place, on the robot, motors in realistic state**: rotate the robot through full 360° (figure-8 for 3D). Fit hard-iron offset (sphere/ellipsoid fit):

```python
# Minimal hard-iron cal: collect mag samples over a full rotation
import numpy as np
def hard_iron_offset(samples):           # samples: Nx3 raw mag
    s = np.asarray(samples)
    return (s.max(axis=0) + s.min(axis=0)) / 2.0   # subtract from every reading
# Full ellipsoid (soft-iron) fit: use a least-squares ellipsoid fit; offset+3x3 matrix.
```

   Validate: after cal, the magnitude `|m_corrected|` should be constant (±5%) at every heading. If magnitude swings with throttle, you have motor interference — see step 3/4.
3. **Current-keyed rejection**: monitor motor current; when it exceeds a threshold, inflate mag covariance or drop mag updates entirely, hold heading on gyro. Gyro drift (decent MEMS, e.g., BMI088/ICM-42688) is ~1–10°/h after bias estimation — minutes of mag-free heading is fine.
4. **Best answer for RTK robots: dual-antenna GNSS heading (moving baseline).** Two antennas ≥ 0.5 m apart give true heading to ~0.2°/baseline-meter, immune to magnetics entirely. ZED-F9P pairs ("moving base" + "rover") or single-board solutions (Septentrio Mosaic-H, u-blox F9H). If you have RTK anyway, this costs one extra receiver and eliminates the entire compass problem. **Limitation: needs GNSS — under canopy you're back on gyro.**
5. **GPS-course fallback**: course-over-ground from GPS velocity is valid heading **only when moving** (> ~0.5 m/s) and only if the robot doesn't crab. Never use COG heading at standstill — it's noise.

Heading fusion recipe: gyro yaw rate always; absolute heading from dual-antenna GNSS (preferred) or calibrated mag (with current gating) or COG-when-moving; declination/convergence applied before fusion so everything is true/grid-north consistent with your map frame.

---

## 7. Debugging Methodology

Symptom-driven, in order of likelihood:

| Symptom | First check |
|---|---|
| Position offset constant ~meters | Wrong datum, or base station coords wrong (RTK), or antenna lever arm not configured (GPS antenna isn't at base_link — set the static transform!) |
| Path tracked diagonally | Declination not applied, or grid convergence, or ENU/compass yaw convention flip |
| Robot in the ocean / Null Island | lat/lon argument order, or float32 truncation, or zone mismatch |
| RTK never fixes | No GGA sent to VRS caster; missing RTCM 1005; baseline > 35 km; antenna under canopy; USB3 interference |
| Position jumps when driving under tree | Float↔fixed transitions — check covariance switching and innovation gating |
| Heading good at standstill, wrong under throttle | Motor current corrupting mag — log `|m|` vs current, then gate or go dual-antenna |
| Fence chatter at boundary | No hysteresis, or margins not inflated by pose sigma |
| Fusion diverges slowly | Wheel odom fused as pose instead of velocity; or IMU yaw fused as absolute with a bad mag |

Always log: raw NMEA/UBX, fix type, satellites, HDOP, correction age, motor current, and the fused pose covariance. A dropout postmortem without fix-type history is unsolvable.

Tools: `RTKLIB`/`rtkrcv` (open-source RTK + analysis), u-center (u-blox config/monitor), `gpsd`, `mapviz` or Foxglove with map tiles for plotting tracks, `pyubx2`/`pynmeagps` for parsing.

---

## 8. Pre-Deployment Checklist

- [ ] Receiver fix type drives covariance; no-fix means no publish
- [ ] Innovation gating on GPS measurements (3σ Mahalanobis)
- [ ] Datum persisted; waypoints/fence stable across reboot
- [ ] UTM zone locked at startup OR local ENU used; landmark unit test passes
- [ ] All lat/lon stored as float64 end-to-end
- [ ] Antenna lever-arm transform (base_link → antenna) published and used
- [ ] Declination from WMM by location/date; ENU vs compass convention test
- [ ] Mag calibrated on-robot; `|m|` constant over 360°; motor-current gating active (or dual-antenna heading)
- [ ] Dual-EKF: controllers consume odom frame only; map frame jumps verified harmless
- [ ] Dropout drill: cover the antenna while driving — robot slows, then stops within the error budget, resumes cleanly on reacquisition
- [ ] Geofence: margins ≥ stopping distance + 3σ; hysteresis verified by joystick walk-up; fail-safe on stale pose
- [ ] NTRIP reconnect tested by pulling the network; correction-age timeout verified
