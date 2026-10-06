# BRIEF: <assignment name>

> Written by the orchestrator when handing an approved priority to the dev manager. The manager copies the approvals and decisions into STATE.md verbatim.

- **Approved by** <human> on <date time>.
- **Scope:** <epics and stories, in order>.
- **Window:** <until when; start nothing new after <time>; nothing half-done at the cutoff> or <none>.
- **Decisions already made:** <list, verbatim>.
- **Not approved (do not build):** <list>.
- **Hard gates:** compliance, real-user data and new-user exposure, spend, irreversible actions, plus: <anything specific>.
- **Budget:** run the usage guard before every dispatch and every new story; on stop, pause cleanly, write PAUSED, update STATE.md, end the run. Do not switch model providers.
- **State:** `<assignment dir>/STATE.md`. Read it first on every run. Write DONE when finished.
- **Repo rules:** occupancy lock, worktrees for parallel devs, never two devs in one checkout, at most two dev streams.
- **Reporting:** one consolidated report to the orchestrator; escalations with a recommendation; never return while a subagent is in flight.
