# F1 25 Time Trial Telemetry Dashboard

## Purpose
A real-time telemetry dashboard for F1 25 Time Trial mode on PS5. Receives live UDP data and compares your current lap against a saved best lap telemetry package.

Display live car telemetry against a reference lap (personal best or rival ghost) to identify where you're gaining or losing time, metre by metre.

## Key Interactions
- Live lap telemetry displayed as you drive
- Reference lap loaded for comparison (best lap or rival ghost)
- Continuous delta time — are you ahead or behind at every point on track

## Tech Stack
- **UDP Parser**: `f1-packets` Python library (pip install f1-packets) — parses F1 25 binary UDP packets
- **GUI**: Dear PyGui — GPU-accelerated desktop dashboard, no browser
- **Storage**: SQLite — saves raw UDP sessions and best lap telemetry locally

## Architecture

### Data Source Abstraction
The app must be agnostic to where telemetry data comes from. All data flows through a common `TelemetrySource` interface:
```python
class TelemetrySource:
    def get_latest_frame(self) -> TelemetryFrame: ...
```

Two implementations:
- `LiveUDPSource` — listens on UDP port 20777, parses real F1 25 packets from PS5
- `MockSource` — replays a recorded session file or streams FastF1 real-world data

During development, use `MockSource`. For real use, swap to `LiveUDPSource`. The dashboard never knows the difference.

### Mock Data Strategy
Use **FastF1** to pull real qualifying lap telemetry (speed, throttle, brake, gear, distance) from actual F1 sessions. This data has the same shape as F1 25 game data and is ideal for building and testing the UI without needing the PS5.
```python
import fastf1
session = fastf1.get_session(2025, "Monaco", "Q")
session.load(telemetry=True, laps=True)
lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_car_data().add_distance()
```

### Session Recording & Replay
- On first real PS5 session: record raw UDP packets to SQLite
- Replay saved sessions as a mock stream during development
- Best lap stored as a telemetry snapshot indexed by lap distance (metres)

## Telemetry Data
All comparisons are done by **lap distance (metres)**, not time. This allows accurate overlay of two laps regardless of their overall lap time difference.

Key data fields used:
- `m_lapDistance` — metres into current lap (from Lap Data packet)
- `m_speed` — km/h (from Car Telemetry packet)
- `m_throttle` — 0.0 to 1.0 (from Car Telemetry packet)
- `m_brake` — 0.0 to 1.0 (from Car Telemetry packet)
- `m_gear` — current gear (from Car Telemetry packet)
- `m_engineRPM` — RPM (from Car Telemetry packet)
- `m_currentLapTimeInMS` — live lap time in milliseconds (from Lap Data packet)
- `m_lastLapTimeInMS` — completed lap time in milliseconds (from Lap Data packet)

## Packet Source
F1 25 UDP spec format `2025`, default port `20777`, recommended send rate `20Hz`.
Official spec: https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-udp-specification/12187347