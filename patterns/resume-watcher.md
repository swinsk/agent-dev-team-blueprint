# Pattern: the resume watcher

## Problem

A manager that pauses for budget, hits a runner cap, or crashes cannot relaunch itself. Without something external, "the team will resume after the reset" is a promise with no mechanism.

## Solution

A small scheduled job (cron, a system scheduler, a CI schedule, a cloud scheduler) that runs every few minutes and decides whether to relaunch the manager.

## Illustrative pseudo-code

```sh
#!/bin/sh
# resume-watcher (illustrative). Run every 10 minutes by your scheduler.
A="$ASSIGNMENT_DIR"                       # holds BRIEF.md, STATE.md, markers

[ -f "$A/DONE" ] && exit 0                # finished: never relaunch
[ -f "$A/STOP" ] && exit 0                # human kill switch

if [ -f "$A/PAUSED" ]; then
  now=$(date +%s); resume_at=$(to_epoch "$(cat "$A/PAUSED")")
  [ "$now" -lt "$resume_at" ] && exit 0   # still inside the paused window
fi

manager_is_running && exit 0              # one manager at a time (exact PID check)
launched_recently 30m && exit 0           # backoff so a crash loop cannot burn budget
past_cutoff "$A/BRIEF.md" && exit 0       # approval window over: do not start new runs

usage_guard || exit 0                     # still over the threshold

rm -f "$A/PAUSED"
record_launch_time
enqueue_manager_run "Resume the assignment in $A. Read BRIEF.md and STATE.md first."
```

## Rules

- **DONE wins.** The manager checks for DONE before anything else, and the watcher never relaunches a finished assignment. Do not leave a stale `PAUSED` next to `DONE`.
- **One manager at a time.** Check liveness by exact process ID or a lock file, never by a name pattern.
- **Backoff.** A minimum gap between launches keeps a crash loop from draining the budget.
- **Respect the approval window.** Past the cutoff, the watcher does nothing new; the human decides what happens next.
- **Kill switch.** A `STOP` file (or equivalent) the human can create to halt everything.
- **Log every decision** (launched, skipped and why) to a small log file, without secrets.
