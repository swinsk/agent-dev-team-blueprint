# DISPATCH: <role> for #<issue>

- **Approved item:** Epic #<n> / Story #<m>, approved by <human> on <date>.
- **Scope (complete; anything not listed here is out of scope):**
  1. <...>
  2. <...>
- **Where:** repo <name>, worktree `<path>`, branch `<role>/<issue>-<slug>` off `<base sha>`.
- **Acceptance:** <criteria or QA cases A..F>. Gate file to write (QA only): `<path>/QA_<scope>_GATE`.
- **Constraints:** follow ADR <n>; do not touch <paths>; <gate reminders>.
- **Hard stop:** <time>. Commit and push before it.
- **Progress file:** `<path>` (long tasks only).
- **Handback:** use the format in `patterns/handoff-protocol.md`.
- **Rules:** team rules apply (`roles/_shared-rules.md`): evidence only, no secrets in output, plain punctuation, stop processes by exact PID.
