# Pattern: dispatch and handback

Every unit of work moves as a **dispatch** down and a **handback** up. Both are written to be read cold by an agent that has seen nothing else.

## Dispatch (manager to team member)

Use `patterns/templates/DISPATCH.md`. A dispatch always contains:

1. **The approved item** it belongs to (epic and story numbers) and who approved it.
2. **Complete scope.** Everything the agent is allowed to do in this dispatch. Agents should refuse scope added later by side messages.
3. **Where to work**: repo, worktree path, branch name, base commit.
4. **Acceptance**: the criteria, the cases to run, the gate file to write.
5. **Constraints** specific to this item (an ADR to follow, a file not to touch, a gate to respect).
6. **Hard stop time** if the run has a window.
7. **Progress file path** for long tasks.
8. **The handback format** you expect.

## Handback (team member to manager)

```
ITEM: <issue>  ROLE: <role>
DONE: <what changed>
EVIDENCE: <branch tip SHA on remote, PR number, test summary, CI link or run id, screenshots path>
UNVERIFIED: <what could not be checked and why>
REFUSED: <anything out of scope or gated that was not done>
WATCH-FORS: <what review or QA should look at>
INCIDENTS: <none | description>
```

## Manager's verification checklist (before advancing)

- [ ] Commit exists on the remote branch tip
- [ ] Right repo, right branch, right base
- [ ] Tests pass where I can see them (CI or a run I observed)
- [ ] Runtime bugs: runtime repro run and clean
- [ ] Diff matches scope and ADRs (no drift, no surprise files)
- [ ] No secrets, no dashes rule violations, no debug leftovers
- [ ] Next step dispatched in the same turn

## Pipeline per story

```
product-manager: story + acceptance criteria
  -> developer: branch, tests, PR
  -> manager: verify + architecture review (request changes or approve)
  -> release-manager: merge (and deploy backend with change preview)
  -> qa: gate on the exact merge or release-candidate SHA -> gate file
  -> release-manager: ship only on PASS <sha>, verify ship
  -> manager: ADR ship record, close issues, RESULT line in STATE.md
```

Backend changes that clients depend on usually deploy before the client QA gate, so QA tests the client against the real backend. Client builds ship only after QA PASS.
