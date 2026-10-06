# Walkthrough: one epic from approval to shipped

ExampleApp is a small expense-tracking product: a backend API, a web app, and a mobile client that reads receipts with an AI model. This is how one epic moves through the team, including the parts that go wrong. Issue numbers, times, and SHAs are illustrative.

## 1. The request

The human: "People keep losing a draft expense when the receipt upload fails. Fix that, and flag amounts the AI is unsure about."

## 2. Orchestrator: think it through, batch the questions

The orchestrator reads the product's ADRs and the backlog and comes back with one batch:

> Four questions before the team starts, each with my recommendation:
> 1. Scope: the failed-upload fix and the low-confidence flag as one epic? **Recommend yes.**
> 2. Mobile only, or the web client too? **Recommend mobile now, web as a follow-up story.**
> 3. Should a low-confidence item block saving? **Recommend no: flag it, let the user confirm or edit.**
> 4. Window: may the team ship today? **Recommend yes, until 17:00.**

The human answers "yes to all". That is the approval: the team may build, merge, deploy, and ship this epic without asking again.

## 3. Orchestrator hands off, then steps back

It writes `BRIEF.md` (scope, window, decisions, gates) and dispatches **only** the dev manager. From here the orchestrator does nothing until the manager reports or escalates.

## 4. Dev manager: intake and plan

- Reads `BRIEF.md`, creates `STATE.md`, copies the decisions verbatim.
- Verifies reality: main at `a1b2c3d`, no open PRs, CI green.
- Dispatches the product manager (foreground): epic #40 with stories #41 (failed upload never destroys the draft) and #42 (per-item confidence flag), acceptance criteria included.
- Writes ADR 004: a structured, retryable failure contract on the receipt-extraction endpoint, bounded under the gateway timeout; additive confidence fields.
- Runs the usage guard: 12%. Continue.

## 5. Two streams, two worktrees

```
backend-dev   wt/backend-41   branch backend/41-estimate-failure-contract
frontend-dev  wt/mobile-41    branch frontend/41-retry-draft
```

Both are dispatched in the foreground as two blocking chains. The manager stays resident.

## 6. Handbacks are claims, so the manager verifies

- Backend: PR #50, CI green, tip on the remote matches. Review against ADR 004: approved.
- Mobile: PR #51, "build succeeded". The manager reads the diff and finds a sheet that is swapped mid-dismissal and could drop the manual-entry screen. **Changes requested** on the same PR. Compile success was not proof.
- Frontend-dev fixes it and continues to #42 stacked on #51.

## 7. Backend ships first

The release manager merges #50, builds the deploy artifact, **creates a change preview**, sees only the expected function updates, deploys, and verifies the live endpoint returns the new error contract. Backend is live; the clients are unaffected because the change is additive.

## 8. QA gate, and the wrong-build trap

QA builds the mobile app at `b7c8d9e`, installs it, and checks identity: the installed binary contains a string only that commit adds, checksum recorded. Cases 1 to 4 pass. Case 6 fails: a corrected merchant name is saved on the draft but the line items keep the old label. QA files bug #53 and writes `QA_MOBILE_GATE = FAIL b7c8d9e`.

On the re-check, QA is about to reuse the installed app "because the build number matches". The identity check fails: the installed app is from an older commit. The manager voids those results, reinstalls the right build, and re-dispatches QA with only the affected cases. Without the identity rule this would have shipped a phantom fix.

## 9. A pause in the middle

The usage guard returns stop at 80%. The manager lets the release manager's in-progress merge finish (clean point), does not start the next QA pass, writes `PAUSED` with the reset time, updates `STATE.md` with a "next run does exactly this" block, and ends the run with nothing in flight.

After the reset, the resume watcher sees `PAUSED` has expired, no manager running, guard below threshold, and before the cutoff. It relaunches the manager, which reads `STATE.md`, verifies the remote, and continues exactly where it stopped.

## 10. A gated story does not idle the team

A stretch story, #43 "sync to an accounting service", needs a vendor developer account only the human can create. The manager builds it to the boundary with a mock vendor, ships it dark behind a flag, and escalates with `ESCALATION.md`: options, recommendation ("create the vendor app; here are the exact callback URLs to enter"), and what happens if the answer is no. The other stream keeps working.

## 11. Ship on PASS for the exact commit

QA's narrow re-check passes: `QA_MOBILE_GATE = PASS e1f2a3b`. A squash-merge leaves the stacked PR conflicting; the manager resolves it back to the QA'd content and proves `git diff e1f2a3b -- mobile/` is empty, so no re-QA is needed. The release manager reads the gate, bumps the version by one, updates the changelog, uploads, assigns the build to the test group, and **reads the result back** from the store console: processed, assigned, available.

## 12. Close the loop

The manager amends ADR 004 with a ship record, closes the issues, writes `RESULT:` lines and `DONE` in the state folder, and sends one report:

```
RESULT: shipped
Shipped: backend contract (PR #50, deployed, live check passed); mobile retry + confidence flags (PRs #51, #54, build 12, in the test group, verified in the console). ADR 004.
In flight: none
Blocked: accounting sync shipped dark, awaiting the vendor account (escalation sent)
Decisions made: re-run extraction with the user's correction instead of patching labels in place (ADR 004 amendment)
Decisions needed: create the vendor app? Recommendation: yes, steps in the escalation
Incidents: none
```

The orchestrator spot-checks the build in the console and the merged PRs, then tells the human the result and the one open question.
