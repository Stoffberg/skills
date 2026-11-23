---
name: catchup
description: Trigger this if the user says 'catchup' or 'catch up' as a command. GPT Sol gathers the workspace evidence with the Codex $catchup skill; Claude organises it into a ranked briefing.
---

# Catch up

Read-only. This skill authorizes reading the current workspace's records,
including live and production records, through the Sol delegate. It does not
authorize sending messages, changing tickets, editing code, merging,
deploying, running migrations, or changing records.

Sol does all source reading, including mail, calendar, chat, and anything that
needs computer use. Do not repeat its source reads yourself. You reconcile,
rank, and write the briefing.

The dump names sources by service only (`Teams`, `Mail`). Do not ask Sol, or
look yourself, for accounts, profiles, tenants, or other workspaces.

## 1. Start Sol

1. Run `date '+%Y-%m-%dT%H:%M:%S%z %Z'` and `pwd`. Record both.
2. Call `orchestrator_capabilities`. Pick the latest GPT Sol on the `codex`
   provider unless the user named a version. Do not hardcode an ID. If no Sol
   model can run a child task, report the blocker. Do not substitute a model.
3. Pick a dump path in your scratchpad: `<scratchpad>/catchup-<timestamp>.md`.
4. Call `delegate_task` once: `role: "research"`, `mode: "async"`,
   `target: {providerInstanceId: "codex", model: <sol>, options: {reasoningEffort: "high"}}`.
   Save the `taskId`. Brief:

```
Use $catchup in handoff mode.
Workspace directory: <pwd>
Requested at: <date output>
Dump path: <dump path>
Window: <user's stated window, else "since last meaningful activity; no cutoff for open obligations">
Focus: <anything the user asked to focus on, else "none">
Do not ask the user questions; record them in the dump. Do not start subagents.
```

Do not poll. Wait for the completion notice. Tell the user Sol is gathering
and roughly what it covers. A timeout, error, or empty dump is not a result:
report it and offer to retry.

## 2. Check the dump

Read the dump file. Check, before writing anything:

- Every source in the workspace's inventory appears under Coverage as
  searched, failed, or skipped with a reason.
- Every item has a source link or record reference and an absolute
  last-evidence time.
- Times are consistent with the generation time. Recompute ages against
  your own `date`, not Sol's relative wording.

If a gap matters to ranking, send one follow-up `delegate_task` with the
original brief plus the specific gap. One follow-up at most; then report the
gap instead of chasing it.

You may run cheap read-only `ws` queries (ticket or PR state) to confirm an
item that decides the top recommendation. Never use computer use, mail, or
calendar yourself.

## 3. Brief the user

Rank on Sol's evidence, not its ranking:
explicit deadlines first, then where the user is blocking someone or owes a
reply, then current sprint and release handoffs, then follow-ups waiting on
others. A handed-off external blocker is a scheduled follow-up, not an urgent
fix. Noise and recency are not importance.

- Lead with the recommendation: what takes priority and why, and what the
  user was busy with.
- One sentence of coverage: sources checked, records reviewed, as of
  `<generated at>` (say how old the evidence is if over an hour).
- Ranked points, no tables. Bold short name, then origin and current state
  with a primary source link, then the next move. Name the expected step
  and your recommended step when they differ. Include owner, deadline, and
  follow-up date when the dump supports them.
- Keep distinct: merged vs deployed vs accepted, findings vs fix,
  workaround vs permanent fix, reported vs verified.
- A short list of other things to clear from the user's head. Label
  uncertain items as uncertain.
- Close with material coverage gaps and their effect on confidence, and
  Sol's open questions for the user.
- State that no actions were taken. Wait for direction.

Link the dump file by its absolute path at the end.
