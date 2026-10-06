---
name: resume-assignment
description: Resume a paused or interrupted dev-manager assignment from its STATE.md
agent: dev-manager
argument-hint: "path to the assignment folder"
---

Resume the assignment in ${input:dir:assignment folder}.

1. If a `DONE` file exists there, report that and stop.
2. Read `BRIEF.md` and `STATE.md` completely.
3. Verify reality against the file: remote branch tips, open PRs, CI runs, deploy state, release console, gate files, and any agents still running. Reality wins; correct the file.
4. Reconcile: record anything the last run finished but did not write down; redo only what is provably missing.
5. Run the usage guard if one is configured. On stop, write `PAUSED` and end cleanly.
6. Continue from the "Next run does exactly this" block, under the same rules as `roles/dev-manager.md`.
