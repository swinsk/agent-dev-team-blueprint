# Autonomy and hard gates

## The model

The human approves work at the **feature, epic, or story** level. That approval is the authority for the team to build, review, merge, deploy, and ship it end to end, with no per-step re-confirmation.

Why: the agents are specialized to do exactly this. Asking the human to confirm every merge and deploy is micromanagement they did not ask for, and it turns the human into the bottleneck.

## What stays gated

Approval never covers these. The team stops at the gate, and the dev manager escalates with a recommendation:

| Gate | Examples |
|---|---|
| **Compliance and legal judgment** | health, finance, or legal claims in the product; regulated data handling; changing what the product promises users |
| **Real-user data and new-user exposure** | onboarding users beyond the approved test group; migrating real users' data; making something public |
| **Spend** | any charge to a payment method; a new paid cloud resource; a plan upgrade; buying credits. Metered use of an already funded, already approved service is usage, not a purchase, if the human has said so |
| **Irreversible actions** | destructive migrations, deleting data or backups, rewriting history, revoking access, anything that could break the live product for everyone |
| **Credentials only the human holds** | creating vendor developer accounts, accepting legal agreements, signing keys tied to the human's identity |

QA before ship is not a gate the human can be asked to waive mid-run. It is a precondition of shipping. Approval authorizes the ship; QA PASS is what allows executing it.

## How a gate is handled

1. Build everything up to the gate. A credential-gated feature is built, tested with mocks, and shipped **dark** behind a flag.
2. Stop at the gate. Do not "just do it" because the rest is ready.
3. Escalate with `patterns/templates/ESCALATION.md`: what, why it is gated, options, recommendation, and what happens if the answer is no.
4. Keep the team busy on other approved work while waiting. A gated story never idles both dev streams.
5. When the human answers, the answer goes into the state file and the decision log, and the work resumes from the gate.

## Scope of an approval

- An approval covers the items it names and their natural children (the stories of an approved epic). It does not cover a new epic the team discovered along the way: that is a recommendation for the human, not a license.
- An approval may have a time window ("until 17:00 Monday"). Start nothing that cannot be built, QA'd, and shipped inside the window. Nothing is left half-done at the cutoff.
- An approval may carry decisions ("keep the legacy sign-in for now", "do not build the encryption proposal"). Record them in the state file verbatim and treat them as locked for the run.

## Who decides what

| Decision | Owner |
|---|---|
| Product direction, priorities between epics, anything gated | the human |
| Technical architecture inside an approved item | the dev manager (recorded as an ADR) |
| Story shape and acceptance criteria | the product manager, reviewed by the dev manager |
| Implementation details | the developer, reviewed by the dev manager |
| Whether a build is good enough to ship | QA's gate result; nobody overrides a FAIL |
