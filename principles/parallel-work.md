# Parallel work without collisions

## Limits

- **At most two dev streams** in flight at once. More streams multiply review and QA load faster than they multiply output, and the manager loses track.
- QA and release can run alongside the dev streams, but each still obeys single-writer rules.

## One writer per checkout

Never let two agents write the same checkout or branch. When two developers work the same repo in parallel, each gets its own **git worktree**:

```
git worktree add ../exampleapp-wt/backend-42 -b backend/42-export-fix origin/main
git worktree add ../exampleapp-wt/frontend-43 -b frontend/43-empty-state origin/main
```

- The main checkout is reserved for the release manager and for the manager's small unblocking edits, one at a time.
- QA builds from its own detached worktree at the exact commit under test.
- Remove worktrees when their branch merges.
- Some harnesses can create the worktree for you when dispatching a subagent (for example, an isolation option on the dispatch, or a frontmatter setting). Use it when available.

## Serialize the shared build phase

Some resources are shared even across worktrees. Treat each as single-tenant and serialize access:

- project generators and lockfile updates that touch the main checkout,
- signing keychains and release credentials,
- a specific simulator, emulator, or test device,
- a GPU or other scarce machine,
- infrastructure deploys (one change set at a time),
- the version number.

Use a lock file for anything that more than one session could grab. See `patterns/occupancy-lock.md`. An absent lock does not prove the work is unclaimed: there is a window between a session deciding to take a job and the lock file existing. Check the state file and the live agents before claiming.

## Stacked and conflicting PRs

- Prefer branches off main. Stack only when the second story truly depends on the first.
- When a squash-merge leaves a stacked PR conflicting, resolve back to the content QA tested and prove it with a diff against the QA'd commit (an empty diff over the shipped paths means no re-QA is needed).
- Batch QA-passed work into one build per platform where possible; fewer builds means fewer version collisions.
