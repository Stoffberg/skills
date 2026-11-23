---
name: writing
description: Use before writing or rewording any text the user will send or post as themselves - a Slack, Teams, WhatsApp or email message, a reply, a ticket or PR comment, a PR description, a ticket update or a handoff. Triggers include "draft a message to", "reply to", "text", "tell", "let them know", "write a comment", "reword", "make it shorter", "make it friendlier" and "format it nicely"; load it again for every revision of a draft. Load it once the facts the text depends on are gathered, immediately before presenting the wording. Not for coding, investigation or your own replies in chat.
metadata:
  source: https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md
---

# Writing

Load this skill last. Finish the investigation, collect the evidence needed for every claim, and establish the current status before drafting. If a factual gap changes the message, resolve it first. For a blocker handoff, verify the blocker and the specific ask; the blocked work need not be complete.

## Voice

- Write direct, natural English with a little irreverence when the audience suits it. Keep workplace criticism calm and about the work.
- Start with the outcome or decision. Give enough context for a reader who has not followed the conversation.
- Use plain words, active verbs and complete sentences. Split dense sentences rather than dropping words the reader needs.
- Keep facts, uncertainty, ownership, estimates and commitments intact. Preserve the user's stated facts in a rewrite without implying independent verification.
- Name the specific behaviour, effect or next action. Remove vague claims, sales language, jargon, canned openings and generic conclusions.
- Avoid em dashes, contrastive "not X, but Y" framing, forced groups of three and decorative formatting.
- Use the same term consistently. Keep technical names only when the recipient needs them to act.
- Use headings and lists when they help. Do not repeat a bold label in the sentence after it.

## Format

- PR descriptions: explain what broke and what now works. Describe tested user actions and outcomes in 1-2 bullets. Follow required repository fields and the current evidence rules. Omit commands, hashes, test counts, benchmark dumps and implementation detail unless explicitly requested. Mention only limitations that affect users or approval. Upload evidence via `--attach` only, embed native GitHub user-attachment URLs and respect repository visibility.
- Ticket updates: give the outcome, current status and next action briefly. Keep acceptance criteria to a few observable outcomes. Separate completed work from pending verification.
- Handoffs: explain how the issue surfaced, its impact, the supporting evidence and the specific ask. Preserve the owner's role and frame help as support.
- Messages and comments to people: follow the section below.

## Messages and comments to people

This covers Teams, Slack, WhatsApp, email, and ticket or PR comments the user will post. These are hard rules. The user has corrected each of them many times, so the first draft must already follow all of them.

- **Short.** Three short sentences or four bullets at most; a comment is shorter still. Lead with what the reader needs. Question the opening line and cut it if it isn't needed. Cut greetings, background they already have and reassurances nobody asked for, like "no engineering needed".
- **Never in a code block.** Return the draft as rendered Markdown in chat so it copies formatted.
- **Formatted, never a blob.** Short lines, bullets for separate points, bold for the key status or ask. Friendly, and it sounds like the user typing, not a summary or report.
- **Links, always and inline.** Find every link the reader might open (PR, ticket, doc, dashboard, page) before drafting, and embed each on the words it belongs to. Never paste bare URLs into the text, and never make the user ask for a link.
- **For the reader, not the engineer.** Assume a non-technical reader unless told otherwise. No backticks, code names, file paths, PR or ticket numbers, or jargon. Say what is broken or what they need to do, not how it works or what happened behind the scenes.
- **Follow the workspace's language rules**, such as writing to Afrikaans colleagues in mengels.
- **"Shorter" means at least half the length.** Rewrite rather than trimming a few words. "Formatted" means structure, not more words.

Bad:

```
Hi Sam, hope you're well! Just a quick update: I fixed the issue in `sync-worker` (PR #351) where the `retry.enabled` flag caused retries. No engineering work is needed on your side. The PR is here: https://github.com/org/repo/pull/351
```

Good (quoted here only to set it apart; return it unquoted):

> Hey Sam, the **order sync is fixed** and live in dev.
> - Try it on the [orders page](https://example.com/orders)
> - The [change is here](https://github.com/org/repo/pull/351) if you want a look

Draft, then remove stock phrasing and unnecessary detail. Compare the final claims against the evidence. Return the ready-to-use text without a writing analysis unless asked. Drafting never grants permission to publish.
