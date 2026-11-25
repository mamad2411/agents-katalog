---
name: script
description: >-
  Use when an Omniverse or Isaac Sim task needs Python run inside the Kit app with execute_script: something no tool
  does, a batch of tool calls in one go, a tool that failed and needs the same thing done by hand, or Kit and USD APIs
  to look up before writing that code. Also for long work run as a job with run_script_job, get_job and cancel_job:
  many physics steps, settling or baking objects one after another, anything that may outlast 120 s.
allowed-tools: >-
  mcp__plugin_omniverse-mcp_omniverse__get_sim_state mcp__plugin_omniverse-mcp_omniverse__get_logs
  mcp__plugin_omniverse-mcp_omniverse__get_prim_properties mcp__plugin_omniverse-mcp_omniverse__get_job
---

# Script inside Kit

`execute_script` runs any Python inside the Kit app, with the user's rights on their machine, so it always asks
first; so does `run_script_job`, which runs a long script as a job. Kit's and Isaac Sim's APIs change between releases
and models are not trained on them: look an API up before using it, never guess.

## Steps

1. **Prefer a tool.** A tool that does the job is checked, bounded and safer; script only what no tool covers.
2. **Look the API up** with Context7: library `isaac-sim/isaacsim`, and `/websites/omniverse_nvidia_kit_omni_physics`
   for PhysX (stepping by hand, Fabric, `/physics/*` settings), which the first doesn't hold. Look for the app's
   version: ask the user, or in Isaac Sim run `from isaacsim.core.version import get_version; result = get_version()`.
   Without Context7, NVIDIA's documentation for that version.
3. **Choose how it runs.** A short script, done in seconds: `execute_script`, whose call gives up after 120 s while
   the script runs on. Work that may take longer, such as many physics steps or objects settled one after another:
   a job, `run_script_job` (step 6). Up to 1000 physics steps with nothing done between them need no script:
   `sim_control("step", steps=...)`.
4. **Write the script.** Already imported: `omni`, `carb`, `Usd`, `UsdGeom`, `UsdLux`, `UsdPhysics`, `Sdf`, `Gf` and
   `mcp`. Set `result = <value>` to return data. `await mcp.<handler>(...)` calls the tools' handlers from the
   script, so one script can capture, measure and move:

   ```python
   bounds = await mcp.prim_bounds("/World/Robot")
   await mcp.set_camera([bounds["result"]["center"][0] + 3, 3, 3])
   result = bounds["result"]
   ```

5. **Run it** with `execute_script`, then check the result, and `get_logs(min_level="warn")` when it fails: the
   error result carries the traceback's last lines, the log what Kit reported around it.
6. **A job:** the script awaits once a step, so Kit renders and other tools answer between its steps, and prints a
   line a step, its progress:

   ```python
   import omni.timeline

   app = omni.kit.app.get_app()
   omni.timeline.get_timeline_interface().play()
   for i, path in enumerate(PATHS):
       for _ in range(180):  # 3 s of simulation at 60 updates a second
           await app.next_update_async()
       print(f"{i + 1} of {len(PATHS)} done")
   result = "done"
   ```

   `run_script_job(code=...)`, or `file=` for a `.py` on Kit's machine, answers the job's id at once. Then
   `get_job(id, wait=60)` until its state is `completed`, `failed` or `cancelled`: each read gives the lines since the
   last, and at the end the result, or the error and the traceback's last lines. `cancel_job(id)` stops it at its
   next await. With no id, `get_job()` reads the running or last job, after a compacted conversation too. Before a
   job that plays the timeline for long, `get_sim_state`'s `timeline` line says whether it reaches the end first.
7. **Let a job run alone.** One job runs at a time, and a tool that changes the stage meanwhile changes it under the
   job; `get_sim_state` names the job running.

## Traps

| Trap | What to do |
|---|---|
| Backslashes in a Windows path | raw strings (`r"D:\3d\a.usda"`) or forward slashes |
| Moving Kit's viewport camera with `UsdGeom.Xformable` in the stage's edit layer | nothing moves: Kit keeps its own cameras' ops in the session layer, which outranks the edit layer, and the edit stays in the user's file. `await mcp.set_camera()` or `await mcp.look_at()`, or `ViewportCameraState` |
| Switching a variant in a script | the viewport keeps the old geometry: `set_variant_selection` |
| USD called from a thread | crashes Kit: stay on the script's own task |
| `stage.Flush()` | does not exist in OpenUSD; `stage.Reload()` reloads layers from disk |
| A job that never awaits at its top level | refused before it starts: its loops would hold Kit from its start to its end. Await once a step; a coroutine it only defines or schedules doesn't count, so `await main()` at the top level |
| A job that awaits once and then loops, or calls Isaac Sim's `world.step()` | holds Kit like a blocking script: no tool, `get_job` included, answers until it ends. Await `next_update_async()` in the loop instead, with the timeline playing |
| A bare `except:` in a job's loop | catches the cancel, and the job runs on, reading `cancelling`: catch `Exception`, or call `cancel_job` again |
| `sim_control("stop")` after a job | puts every body back where play found it: pause to keep where they landed |
| `sys.exit()` in a script or a job | Isaac Sim quits, since its fast shutdown ends the app on a call to it: never call it; return, or raise an error |
