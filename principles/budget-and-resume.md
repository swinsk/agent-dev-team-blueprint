# Budget, pauses, and resuming

Unattended runs stop for three reasons: the model plan's usage window fills up, the runner's wall-clock cap is reached, or something crashes. The team must survive all three without losing work or leaving anything half-done.

## The pieces

| Piece | Job | Pattern |
|---|---|---|
| **STATE.md** | durable memory of the assignment | `patterns/state-file.md` |
| **Usage guard** | says "continue" or "stop" before each dispatch | `patterns/usage-guard.md` |
| **PAUSED / DONE markers** | tell the watcher whether to relaunch | below |
| **Resume watcher** | relaunches the manager after a pause or crash | `patterns/resume-watcher.md` |
| **Run queue** | launches headless runs one at a time | `patterns/run-queue.md` |
| **Occupancy lock** | one session per repo at a time | `patterns/occupancy-lock.md` |
| **Heartbeat** | makes liveness visible | `patterns/heartbeat.md` |

## Markers

Plain files next to `STATE.md`:

- `PAUSED`: one line, the time the usage window resets. Written by the manager when the guard says stop. The watcher will not relaunch before that time.
- `DONE`: written when the approved scope is shipped (or everything left is blocked on the human). The watcher stops relaunching.
- Gate files (`QA_<scope>_GATE`): written by QA. See `patterns/qa-gate.md`.

## Rules for the manager

1. Run the guard before every dispatch and before starting each story.
2. On "stop": do not start anything new. Let a step finish only if it is close and finishing leaves a clean state. Otherwise stop it at a clean point: committed and pushed branch, no deploy mid-flight, no upload started.
3. Write `PAUSED`, update `STATE.md` with exactly where things stand and what the next run does first, and end the run.
4. Treat an actual usage-limit error the same as "stop".
5. Keep briefs tight, use the cheaper model the role file sets, and keep QA re-checks narrow. Budget is a resource the manager manages.
6. Do not switch model providers to keep working unless the human explicitly allowed it. A different brain mid-run loses context and may break rules the team relies on.

## Rules for every agent

- Commit early and push work-in-progress, so any stop loses minutes, not hours.
- Keep a progress file for long tasks (QA passes, migrations) so a successor sees how far you got.

## Wall-clock windows

If runs are killed at a fixed time, every run is a window:

- Write the window's hard end into `STATE.md` at the start of the run.
- Give subagents hard stop times inside the window.
- Never start an upload, deploy, or migration after a set point in the window (we used: not after minute 25 of a 45 minute window).
- End voluntarily and cleanly when there is not enough window left for the next step; the watcher starts a fresh window.

## Resuming

The relaunched manager:

1. Reads `STATE.md`.
2. Verifies reality: remote branch tips, open PRs, CI, deploy state, release console, gate files, live processes. Reality wins.
3. Reconciles: anything the last run did but did not record gets recorded; anything recorded but not real gets redone.
4. Continues from the contingency block.
