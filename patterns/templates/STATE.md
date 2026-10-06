# STATE: <assignment name>

> Owned by the dev manager. Read FIRST on every run, verify against reality, update after every meaningful step. Use the real clock. No secret values, ever: name the vault item instead.

## Approvals and decisions (keep this section on every rewrite)

- Approved by: <human>, <date time>, scope: <epics/stories>, window: <until when, or none>
- Hard gates for this assignment: <compliance | real-user data | spend | irreversible | other>
- Decisions given with the approval (verbatim):
  - <decision>
- Thresholds: usage guard pauses at <x>% of the window, <y>% weekly. Runner cap: <minutes> per run.

## Plan

| Order | Item | Stories | Status | Notes |
|---|---|---|---|---|
| 1 | Epic #<n> <title> | #<a>, #<b> | not started | |
| 2 | Epic #<n> <title> | #<c> | not started | credential-gated: build to boundary, ship dark |

## Worktrees and streams

- Stream A: <role> in <worktree path> on <branch> (base <sha>)
- Stream B: <role> in <worktree path> on <branch> (base <sha>)
- Main checkout: reserved for release-manager and manager unblocking edits

## Gates

- QA_<scope>_GATE: <PASS|FAIL|INCOMPLETE> <sha>, written <time>

## Log (append only)

### <date time> run <n> (window ends <time>; guard <x>%)
- Verified at start: main <sha>, open PRs <list>, live agents <none|list>, deploy state <ref>.
- Dispatched: <role> #<issue> in <worktree> (branch <branch>), hard stop <time>.
- <time> handback VERIFIED: PR #<n> tip <sha> on remote, CI <result>, review <APPROVED|CHANGES>.
- <time> merged <sha>; deployed <ref> (preview: <summary>); live check: <evidence>.
- <time> QA_<scope>_GATE = <verdict> <sha> (<cases summary>, bugs <list>).
- <time> shipped <version> (<verification>).
- RESULT: <item> shipped (<version>, PRs <list>, ADR <n>).

## Escalations open

- <date> <question> | recommendation: <answer> | blocking: <stories> | sent via orchestrator: <yes/time>

## Next run does exactly this

1. Run the usage guard.
2. <exact step with branch, PR, gate file>
3. <exact step>
4. If the window has less than <n> minutes left, do not start any upload, deploy, or migration.

## Incidents

- <date time> <what> | action taken: <rotation, revert> | recommendation: <...>
