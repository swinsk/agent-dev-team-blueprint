# Pattern: the usage guard

## Problem

Model plans meter usage in windows (for example, a rolling few-hour window and a weekly cap). A team that hits the limit mid-deploy leaves things half-done.

## Solution

A tiny command the manager runs before every dispatch and every new story. It reads current usage from whatever source your setup exposes and returns an exit code:

- `0`: continue
- `3`: stop starting new work; pause cleanly

## Illustrative pseudo-code

```python
# usage_guard (illustrative): adapt read_usage() to your harness
import sys, json

PAUSE_AT = {"window": 0.80, "weekly": 0.97}   # thresholds the human chose

def read_usage():
    """Return {"window": float|None, "weekly": float|None, "resets_at": str|None}.
    Source is harness specific: a status command, a usage API, a local meter file."""
    ...

def main():
    try:
        u = read_usage()
    except Exception as e:
        print(f"WARN guard could not read usage: {e}", file=sys.stderr)
        return 3                      # fail safe: unknown means stop
    for key, limit in PAUSE_AT.items():
        value = u.get(key)
        if value is None:
            # Some sources omit a field right after a reset. Handle that case
            # explicitly and loudly; never crash on it.
            print(f"WARN {key} missing, treating as 0", file=sys.stderr)
            continue
        if value >= limit:
            print(json.dumps({"stop": key, "value": value, "resets_at": u.get("resets_at")}))
            return 3
    return 0

sys.exit(main())
```

## Manager behavior on exit 3

1. Start nothing new.
2. Let a near-finished step finish only if that leaves a clean state; otherwise stop it at a clean point (pushed branch, no deploy or upload mid-flight).
3. Write `PAUSED` containing `resets_at`.
4. Update `STATE.md`, including the "next run does exactly this" block.
5. End the run. The resume watcher takes it from here.

## Notes

- Test the guard with empty, partial, and malformed input before trusting it with an unattended night.
- Keep thresholds in one place and record them in the brief.
- A usage-limit error from the model is equivalent to exit 3.
