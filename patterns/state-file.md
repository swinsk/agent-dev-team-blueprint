# Pattern: the durable state file

## Problem

Long assignments outlive any single run. Runs pause on budget, die at runner caps, or crash. Conversation memory does not survive any of that.

## Solution

One `STATE.md` per assignment, owned by the dev manager, kept outside the product repo's working trees (so it never gets swept into a commit) and outside anything a sync tool might auto-commit. Template: `patterns/templates/STATE.md`.

## Rules

1. **Read it first** on every run, before any dispatch.
2. **Verify it** against reality before acting on it. Reality wins; correct the file.
3. **Append after every meaningful step**: dispatch, handback, review verdict, merge, deploy, QA verdict, ship, escalation, decision. Use the real clock.
4. **Keep the brief's decisions verbatim** in an "Approvals and decisions" section that survives rewrites.
5. **Maintain a "Next run does exactly this" block** at the end. Make it executable by a cold reader: exact branches, PR numbers, gate files, and the order of steps.
6. **Record results** as one `RESULT:` line per shipped item so the final report can be built from the file.
7. **Never put secret values in it.** Name the vault item instead.

## Companion files

```
assignment/
  BRIEF.md          what was approved, by whom, until when, hard gates (written by the orchestrator)
  STATE.md          the manager's memory
  PAUSED            present while paused: reset time
  DONE              present when finished
  QA_<scope>_GATE   QA verdict per scope, one line
  progress/         per-agent progress files for long tasks
```

## Sample entry style

```
## 14:58 run 18 (window ends 15:40; guard 4%)
- Verified at start: main a1b2c3d, no open PRs, no live agents, emulator up.
- Dispatched: backend-dev #42 in wt/backend-42 (branch backend/42-export-fix), hard stop 15:25.
- 15:12 handback VERIFIED: PR #57 tip e4f5a6b on remote, CI green (812 passed). Review APPROVED.
- NEXT RUN DOES EXACTLY THIS: (1) guard; (2) release-manager merge #57 + deploy with preview; (3) QA gate on the merge SHA -> QA_BE_GATE; (4) on PASS, close #42 and write RESULT.
```
