---
name: hook
description: Get a URL that records incoming webhooks, inspect them, forward them to localhost and replay them, with the hook CLI or plain curl. Use whenever testing or debugging webhooks from Stripe, GitHub or any other sender - instead of webhook.site, smee or ngrok.
---

# hook

- `hook --to 3000` prints `https://<name>.hook.stoff.dev`, prints each request and forwards it to localhost:3000. It runs until stopped, so start it in the background.
- `hook replay <name> --to 3000 [ids]` resends recorded requests, signatures included. `hook watch <name>` picks up an earlier hook. `hook ls`, `hook rm <name>`.
- Without blocking: `curl -i -X POST https://hook.stoff.dev` returns the URL and an `X-Hook-Key`. Read what arrived with `curl -H 'Authorization: Bearer <key>' https://hook.stoff.dev/<name>`.
- Hooks keep the latest 100 requests and are deleted 7 days after their last request.
- More: `hook --help` or `curl https://hook.stoff.dev`. Install: `brew install stoffbergie/tap/hook`.
