# Pattern: the QA gate file

## Problem

"QA signed off" in a chat message is a claim that drifts: which build, which commit, which scope? Releases went out on stale or mismatched sign-offs, and QA tested binaries that were not the commit under review.

## Solution

QA writes a one-line gate file per scope. The release manager reads it before shipping and ships only on an exact match.

```
QA_WEB_GATE        PASS 3f9c2e1a
QA_MOBILE_GATE     FAIL 3f9c2e1a
QA_BACKEND_GATE    INCOMPLETE 7d0b44c2
```

Format: `<VERDICT> <commit sha>`, where VERDICT is `PASS`, `FAIL`, or `INCOMPLETE`.

## Rules

- QA writes PASS only after proving the installed or deployed artifact is that commit (see `roles/qa.md`), and only with no open p1 in scope.
- The release manager ships only if the gate says `PASS` for the commit being shipped, or for a commit whose shipped paths are byte-identical (proven by a diff that is empty over those paths).
- A new commit in shipped paths invalidates the gate. Re-gate narrowly: only the cases the change could affect, plus a smoke pass.
- The full QA report still goes on the PR. The gate file is the machine-readable summary, not a replacement.
- Gate files live with the assignment's `STATE.md`, not in the product repo.

## Release check (illustrative)

```sh
verdict_line=$(cat "$ASSIGNMENT_DIR/QA_MOBILE_GATE" 2>/dev/null)
case "$verdict_line" in
  "PASS $SHIP_SHA"*) echo "gate ok" ;;
  *) echo "blocked: awaiting QA PASS on $SHIP_SHA (gate says: ${verdict_line:-missing})"; exit 1 ;;
esac
```
