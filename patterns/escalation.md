# Pattern: escalation

## When

Only for what the team cannot decide: spend, compliance or legal judgment, real-user data or new-user exposure, irreversible actions, credentials only the human holds, and product direction. Everything else the manager resolves.

## How

- The manager writes the escalation with `patterns/templates/ESCALATION.md` and sends it to the orchestrator. Team members never contact the human directly.
- Every escalation carries options and a **recommendation**, so the human can answer in one word.
- The orchestrator relays one question at a time and stops until the human answers.
- While waiting, the team keeps working on everything not blocked by the question. A gated story ships dark if it can.
- The escalation is also recorded in `STATE.md` and, if your setup has one, a dated entry in the human's priorities list, so it survives the run ending.
- When the answer arrives, it is recorded verbatim (state file and decision log) and the work resumes from the gate.

## Anti-patterns

- A bare question ("what should we do about sign-in?") with no options or recommendation.
- Escalating a technical choice the manager owns. Write an ADR instead.
- Stopping the whole team because one story is gated.
- Escalating through several agents at once, producing duplicate questions.
