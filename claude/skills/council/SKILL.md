---
name: council
description: Trigger this if the user says 'council'.
---

# Council

Bring in three delegates at high reasoning effort to help with the user's
request, usually a review. By default the council is one GPT 6.2 Sol, one
Claude Opus 5.5 and one Claude Fable 5.2. On the personal profile
(`CLAUDE_CONFIG_DIR` ends in `.claude_personal`), the third is Claude Mythos
5.2 instead of Fable. Never Gemini. If the user names the members, use those
instead.

Before a review, fix known issues, address open PR comments and run the
checks, so the council sees the current implementation. Skip that for code
the user wants replaced.

Start one delegate per member in parallel with the request and the context
it needs. Reviews are read-only. While the others run, check each result
against the code as it arrives and decide what to fix, but do not edit files
a delegate is still reviewing. If the user marks a delegate as non-blocking,
do not wait for it or record its score.

For a code review, ask each delegate for a score out of 10. Each full review
pass is one round. If you agree with their findings, make the changes and
start a fresh round, until every delegate is satisfied. Do not let repeated
rounds grow the scope.

Report the result in your final reply only, in this format:

```markdown
## Council review

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| GPT Sol | 8/10 | 10/10 |
| Claude Opus | 7/10 | 9/10 |
| Claude Fable | 7/10 | 9/10 |
```

Write `no score` when a delegate gives none. Never put the council, its
delegates or its scores in a PR, commit, ticket or any other shared place.
