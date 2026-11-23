---
name: sol-loop
description: Review a code change with GPT Sol in a loop until both agents agree. Use before calling any code change done or filing/updating a PR, and when the user says "sol loop".
---

# sol-loop

Have OpenAI's GPT Sol review your change in a loop before a PR is filed or
updated. Make the smallest changes that answer its findings, watch for scope
creep, and push back when it is wrong.

## Budget

- 3 rounds. Round 1 is full; later rounds cover only changed code and open
  findings.
- Extend to 5 only for security, permissions, auth, data loss or
  state/concurrency while a blocker or should is still open with evidence,
  or when the user asks.
- Stop early when a round returns only nits. Declined nits and comment, doc
  or format-only fixes need no new round.
- One reviewer. Sol starts no subagents.
- Keep a ledger: id, severity, outcome.

## 1. Scope

The change is the diff from its base to the working tree, untracked files
included. The base is the merge base with the PR's base branch, or with the
default branch when there is no PR. Use the same diff command every round.

Do not stash, discard or include unrelated changes. Limit the review to this
change's paths; if they don't separate cleanly, stop and ask. State the
intent and what is out of scope in a sentence or two. Run the covering checks
first, and do not send code this change breaks.

## 2. Start Sol

Use the latest Sol on the `codex` provider, at high reasoning effort, unless
the user named a version. Start a fresh review delegate every round. If
nothing can run Sol, report the blocker; do not substitute a model.

Do not edit the scoped files while a review runs. A timeout, an error or no
reply is not approval: cancel it and restart with the ledger.

Round 1 brief (the delegate gets no history):

```
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results>
See: git diff <base> [-- <paths>]; git status --short (read untracked).
Read surrounding code. Find bugs, broken callers, mismatch with intent.
Skip style unless it hides a bug. Hold to the smallest change. Flag code,
tests, or guards the intent does not need. Other paths, rare cases, small
perf, extra compat: nits.
blocker = intended case wrong. should = real bug callers will hit, in intent. nit = rest.
Reply:
VERDICT: APPROVE or CHANGES
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion> (stable ids)
```

## 3. Answer findings

Check each finding and its severity yourself. Another path, a rare case or a
small cost is a nit, whatever label it came with.

- Agree: make the smallest fix. Prefer deleting or narrowing over a new
  lock, cache, helper or option. Add no tests unless the user asked.
- Disagree: say why, with evidence (file:line, test, output).
- Out of scope or nit: decline in one line.

Update the ledger and re-run the checks. If the review grew the diff, cut
first. Do not agree just to end the loop.

## 4. Next round

Start one only while budget remains and a blocker or should is open, or
behaviour code changed since the last approval. Send the round 1 brief, the
ledger (`fixed:` / `disagree:` / `declined:` with evidence) and the change
since last round. Tell Sol: open ids and changed code only, and mark each old
id `resolved` or `still open: <reason>`.

## 5. Stop

Agreed: APPROVE on the current behaviour diff, no blocker or should open,
and no concern of your own. Stuck: an item is still disputed after two
replies, or the budget ends. Show both sides in two or three lines each and
let the user decide. Running out of budget is not approval.

Do not push during the loop. Never mention the review, Sol or any model in
commits, PR descriptions or comments.

Report: rounds, model, what changed because of Sol, fixed and declined
findings with reasons, and whether you pushed.
