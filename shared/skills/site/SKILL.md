---
name: site
description: Put a folder, an HTML page or any static files on a live URL with the site CLI or plain curl. Use whenever built output, a report, a prototype or a preview needs a link that renders in a browser - instead of Vercel, Netlify, GitHub Pages or surge.
---

# site

- `site --no-copy <folder>` deploys the folder and prints `https://<id>.site.stoff.dev`. Loose files work too (`site --no-copy index.html app.js`), and `cmd | site --no-copy -` deploys piped HTML as the page.
- Read what you deploy before uploading: the URL is public to anyone who has it and stays until removed.
- A stable address: `site --no-copy <folder> -n todo` points `https://todo.site.stoff.dev` at the deploy, and deploying again with `-n todo` moves it at once. `site point todo <id>` rolls back. Add `--spa` for client-side routes.
- `site ls` lists names and deploys. `site rm <id>` deletes a deploy and `site rm <name>` releases a name; remove deploys made for a one-off task.
- The key in `site key` owns your deploys and names. Never print or share it.
- Without the CLI: `curl -T page.html https://site.stoff.dev` returns the URL.
- More: `site --help` or `curl https://site.stoff.dev`. Install: `brew install stoffbergie/tap/site`.
