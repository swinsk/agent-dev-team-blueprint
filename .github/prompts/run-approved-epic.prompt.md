---
name: run-approved-epic
description: Hand an approved epic to the dev manager and drive it to shipped
agent: dev-manager
argument-hint: "epic number, approval window, decisions already made"
---

Run the approved work described below as the dev manager for this repository.

Approved work: ${input:scope:Epic #N and its stories}
Approval window: ${input:window:until when, or none}
Decisions already made: ${input:decisions:none}

Before dispatching anything:

1. Read `AGENTS.md`, `roles/dev-manager.md`, and `principles/manager-lessons.md`.
2. Create or read the assignment `STATE.md` (template `patterns/templates/STATE.md`) and copy the approval and decisions into it verbatim.
3. Verify the real repository state (main tip, open PRs, CI) and record it.

Then run the playbook: decompose with the product manager, at most two dev streams in separate worktrees, verify every handback, architecture review, QA gate on the exact commit, release only on PASS. Escalate only gated items, each with a recommendation. Do not stop until every item is shipped and verified or blocked on a human decision, then give one consolidated report.
