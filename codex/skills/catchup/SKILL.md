---
name: catchup
description: "Build a current, evidence-backed priority briefing for the workspace where the user invokes $catchup."
---

# Catch up

Run only when the user explicitly invokes `$catchup`, or when a parent agent's brief says `Use $catchup in handoff mode`. Do not invoke this skill from a general request for status or priorities. Do not delegate this workflow to subagents.

In handoff mode, do the same discovery and reconciliation, then write the dump described under Handoff mode instead of the briefing. The parent agent writes the briefing.

Produce a read-only briefing. The invocation authorizes reading relevant current-workspace records, including live and production records. It does not authorize sending messages, changing tickets, editing code, merging PRs, deploying, running migrations, or changing records. The user can ask for those actions later in the thread.

## Scope

1. Run `ws context --pretty` from the current directory. Work only within the returned workspace. Read its `AGENTS.md`, relevant project instructions, and configured source inventory. Never use another workspace's credentials, account, repositories, or data to fill a gap.
2. Load identities, communication accounts, source mappings, and access details only from the current workspace's `AGENTS.md` and configuration. Keep workspace-specific facts out of this shared skill and do not read sibling workspaces' instructions. If the relevant identity is missing, discover it within this workspace or ask. Verify the selected mail, calendar, Teams, or Slack account before reading it.
3. Use `ws` for scoped Git, GitHub, Jira, Asana, Azure, AWS, Datadog, and other supported workspace operations. If `ws` rejects a scope, stop that source and report the error; never retry through an unscoped command, another account, or a direct API. Use a configured app connector for communications when available.

## Discover live work

Start with recent activity, then trace active items backward until their origin and current handoff are clear. An unresolved obligation has no age cutoff. Do not treat a merged PR or completed ticket as irrelevant until the linked release, deployment, acceptance, communication, and status handoffs are reconciled.

- Start with `ws catchup --json`. Inspect its source failures and coverage gaps before drawing conclusions. Treat it as a starting inventory, not complete coverage. Expand to current sprint and assigned To Do tickets, active Asana or Azure Boards work, relevant unassigned work promised in messages, review requests, open PR comments, and recent merged PRs linked to live work. Inspect exact ticket and PR state when it affects the next step.
- Check for handoff mismatches: code merged but ticket still open; work in `develop` without a release PR; release PR merged without confirmed deployment; deployment without target-environment acceptance; completed investigation without a promised reply; a PR waiting on the user's review, response, or fix. Keep implementation, merge, deployment, and acceptance distinct.
- Prefer direct, read-only queries of the local Apple Mail and Calendar databases over computer use. Verify the workspace email identity before searching. Examine recent incoming mail, unanswered or flagged threads, sent commitments, and relevant past or upcoming meetings. If macOS denies database access or the account cannot be verified, ask the user how to proceed. Do not silently omit mail or calendar.
- Search the current workspace's Teams or Slack account for direct requests, mentions, commitments, and linked threads. Follow relevant older threads. Ignore routine notifications unless they reveal a live handoff. Correlate messages with tickets, PRs, mail, and meetings rather than creating duplicate items.
- Read past Codex and Claude chat records only while running as Codex, and only for this workspace. Use them to recover background and prior promises; verify present state in current systems. In handoff mode, pass on the facts and promises you recovered as `past chat, <date>`. Do not copy transcripts or give the parent agent access to chat records.
- Inspect runtime, production, cloud, or monitoring records when needed to establish the state of a live item. Read only. Follow workspace instructions and account boundaries.

## Reconcile and rank

For each candidate, establish its origin, current verified state, owner, next expected step, and next recommended step. The expected step is what the existing workflow or commitment calls for; the recommended step is your judgment about what should happen first. If a report-back is expected but investigation is incomplete, recommend the investigation before the reply. Include a source link or precise record reference and the time of the last meaningful evidence.

Rank explicit deadlines first, then work where the user is blocking someone or owes a reply, then current sprint and release handoffs, then follow-ups on work waiting for others. An external blocker that the user has already handed off is usually a scheduled follow-up, not an urgent fix. Adjust for impact and approaching deadlines. Do not confuse a noisy or recently updated item with an important one.

Before finishing, check whether each source was actually searched and whether the candidate set has an unexplained gap. Try another authorized read path within the same workspace if useful. If a source remains unavailable or the result looks incomplete, ask the user a specific question and continue independent investigation. In handoff mode, record the question in the dump instead of asking. Never imply complete coverage when a relevant source was not checked.

## Briefing

Give a concise, scannable catch-up for someone returning after a context switch:

- Lead with a clear recommendation about what should take priority and why. Briefly explain what the user was busy with and what remains to finish it.
- State the coverage in one sentence: sources checked and counts of records actually reviewed, when known. Distinguish search totals from inspected records.
- Use ranked point form, not a table. Start each item with a short bold priority name, followed by brief context and concrete next steps. Group related tickets, PRs, and conversations by the outcome they serve.
- Preserve each item's origin, current state, next expected step, and recommended step without forcing four repeated labels. Weave the origin and a primary source link into the current-state explanation. When the expected commitment differs from the immediate recommendation, make both explicit in the next move. Add enough background to understand an unfamiliar item.
- Use plain language and concrete next moves, naming the owner, deadline, or follow-up date when supported. Make meaningful gaps clear: merged code versus customer acceptance, investigation findings versus implemented fixes, and a workaround versus a permanent fix. Use bold sparingly for priorities, deadlines, and decisive caveats.
- Follow with a short list of other things worth clearing from the user's head: smaller commitments, due follow-ups, routine reviews waiting on them, and confirmed closures that retire a likely concern. Label uncertain completion or supersession as uncertain. Omit routine completed work and the full inventory.
- Let the ranking and next moves establish the action order. Add a specific first action only if it helps; avoid repeating the priorities in another list.
- Close with any material coverage gap and its consequence for confidence, distinguishing reported counts or claims from independently verified evidence. Ask about unresolved access gaps as described above.
- State that no actions were taken. Wait for the user's direction before acting on the briefing.

## Handoff mode

Write one Markdown file to the dump path in the brief. This file is the only thing you write. Reply with the path and a two-line summary.

Make every time absolute (`YYYY-MM-DD HH:MM` with the user's timezone) and add the age relative to the generation time, such as `2026-11-14 16:05 SAST (19h ago)`. Use the system clock, not the brief's request time.

The dump crosses the workspace boundary, so it carries content but not account details. Name sources by service only: `Teams`, `Slack`, `Mail`, `Calendar`, `Jira`, `GitHub`. Leave out account names, email addresses, profile or tenant names and IDs, the number of accounts or profiles you have, and anything about other workspaces. People's names in the content stay. Keep a link only if it reveals none of the above; otherwise give a neutral reference such as `Teams, chat with <person>, 2026-11-14 16:05`. Run `ws` and other scoped commands yourself; never put credentials, tokens, or profile flags in the dump.

```
# Catch-up dump
Generated: <absolute time> | Directory: <dir> | Identity verified: <yes | no, which source>
Window: <what was searched>

## Coverage
- <source>: searched | failed | skipped. <query or scope>. <N found, N inspected>. <error or reason>

## Upcoming
- <absolute time> (<in Nh/Nd>): <meeting, deadline, or release>. <link>

## Items
### <short outcome name>
- Origin: <what started it, when, who>. <link>
- State: <verified current state>. Verified: <yes, via source | reported only>
- Owner: <who> | Waiting on: <who or nothing>
- Expected next: <what the workflow or commitment calls for>
- Recommended next: <your judgment>
- Deadline: <absolute time or none stated>
- Last evidence: <absolute time (age)>. <link or record ref>
- Sources: <every link and record ref used, one per line>
- Evidence: <short quotes or facts that decide the state, each with time and source>
- Your ranking: <1..N> because <reason>

## Other things
- <smaller commitment, routine review, or retired concern>. <time>. <link>. <uncertain if so>

## Gaps and questions
- <gap and its effect on confidence>
- Question for the user: <specific question>
```

Include every candidate you reviewed that still needs anything, not only the top items. Leave out routine completed work. Do not paste mail bodies or chat transcripts; quote only the lines that decide state or a commitment.
