---
name: beam
description: Give a local server a public HTTPS URL with the beam CLI. Use whenever localhost needs to be reached from outside - a phone, a teammate, an OAuth callback or a third-party service - instead of ngrok, cloudflared or localtunnel.
---

# beam

- `beam 3000` prints `https://<random>.beam.stoff.dev` and forwards to localhost:3000. `beam 3000 -- npm run dev` starts the app first.
- `--name app` gives `app.beam.stoff.dev`, if nobody else is using it.
- It runs until stopped, so start it in the background and stop it when done. The URL is public while it runs.
- Catching webhooks rather than serving pages? Use `hook`.
- More: `beam --help`. Install: `brew install stoffbergie/tap/beam`.
