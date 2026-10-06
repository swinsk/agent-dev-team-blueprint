# Pattern: the occupancy lock

## Problem

More than one session (two top-level assistants, an email-triggered responder, a scheduled run) can decide to work the same repo or the same single-tenant resource at once. They silently overwrite each other.

## Solution

A lock file per shared resource, written before work starts and removed when it ends.

```json
{"owner": "manager-run-18", "since": "2026-01-15T14:58:00", "resource": "exampleapp-repo", "purpose": "epic #12"}
```

## Illustrative pseudo-code

```python
def acquire(resource, owner, purpose):
    path = lock_path(resource)
    if exists(path):
        lock = read(path)
        if lock["owner"] != owner and holder_alive(lock):   # exact PID or heartbeat, never a name match
            return False                                     # wait, queue, or message the owner
    # An absent lock does not prove the work is unclaimed. Also check the
    # assignment STATE.md and the list of live agents for a recent claim.
    if claimed_elsewhere(resource):
        return False
    write_atomically(path, {"owner": owner, "since": now(), "resource": resource, "purpose": purpose})
    return True

def release(resource, owner):
    if read(lock_path(resource))["owner"] == owner:
        remove(lock_path(resource))
```

## Rules

- Write atomically (write a temp file, then rename).
- Subagents inherit the parent's lock; never dispatch two agents that both need the same single-tenant resource.
- Stale locks are cleared only after proving the holder is dead, and the clearing is logged.
- If you discover you claimed something another session owns, stop your agent, remove your claim, and tell the owner.
- Use one lock per resource: the repo, a device, a GPU, a deploy target.
