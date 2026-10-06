# Pattern: the run queue

## Problem

Headless manager runs get launched from several places (the orchestrator, the resume watcher, a schedule). Launching them directly causes overlapping runs, lost results, and runs started while the plan is out of budget.

## Solution

One queue and one runner. Producers enqueue; the runner launches one item at a time and records the result where the requester will find it.

## Illustrative pseudo-code

```python
# producer
item = {"id": new_id(), "agent": "dev-manager", "cwd": repo_dir,
        "prompt": "Resume the assignment in <dir>. Read BRIEF.md and STATE.md first.",
        "created": now()}
enqueue(item)
print({"id": item["id"], "position": queue_position(item), "results": results_path(item)})

# runner, every minute
item = next_queued()
if item and not over_budget() and not running(item["agent"]):
    mark_running(item)
    rc, output = launch_headless(item, timeout=RUN_CAP)   # the wall-clock cap your runs must plan for
    write_result(results_path(item), rc, output)
    append_pointer_to_priorities(item)                    # so a human or the next session sees it
    mark_done(item, rc)
```

## Rules

- **Know and publish the cap.** Every run gets the same `RUN_CAP`; the manager plans its window inside it. Overseer roles may need a longer cap than workers.
- **Defer, do not burn.** If the plan is out of budget, the runner waits for the reset instead of launching a run that will fail.
- **Results always land somewhere durable** with a pointer the requester will read. A queued run whose result lands silently is a broken promise.
- **Tell the requester the truth.** A queued or deferred run is reported as queued or deferred, never as if it ran.
- **One run per agent** at a time, enforced by the runner.
