# Pattern: the dashboard heartbeat

## Problem

With several agents running headless, nobody can see who is working, who is blocked, and who died. "No news" gets mistaken for "done".

## Solution

Every agent reports its state at start, at each phase change, and at finish to a small registry that a dashboard (or a plain status command) reads.

```
heartbeat <agent-id> --state working --task "backend #42: export fix"
heartbeat <agent-id> --state blocked --task "awaiting human: vendor account (recommend: create it)"
heartbeat <agent-id> --state idle    --task "PR #57 opened for #42"
```

The registry can be a JSON file, a small table, or a key-value store:

```json
{"agent": "backend-dev", "state": "working", "task": "backend #42: export fix", "updated": "2026-01-15T15:02:11"}
```

## Rules

- States: `working`, `blocked`, `idle`. Blocked always says what for.
- Heartbeat again when a long step changes phase, so the tile does not go stale.
- **Staleness is a prompt to check, not a verdict.** A long build or test pass can go quiet for many minutes. Before declaring an agent dead, check for a live process, recent file writes, or a new commit. Before declaring it alive, check the same things.
- Do not tell agents to "do nothing else" in a way that suppresses their start and finish beats.
- Never put secrets in task text.
