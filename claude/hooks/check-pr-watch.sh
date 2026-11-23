#!/bin/bash
input=$(cat)
url=$(jq -r '.tool_input.url // empty' <<<"$input")
host=$(jq -r '.tool_input.host // empty' <<<"$input")
repository=$(jq -r '.tool_input.repository // empty' <<<"$input")

if [[ "$url" =~ ^https://([^/]+)/ ]]; then
  host="${BASH_REMATCH[1]}"
fi
if [[ "$url" =~ ^https://github\.com/([^/]+/[^/]+)/pull/ ]]; then
  repository="${BASH_REMATCH[1]}"
fi
host="${host:-github.com}"

refuse() {
  echo "T3's watcher cannot read $1. Run \`pr-wait <url>\` in the background instead, as the global instructions describe." >&2
  exit 2
}

if [ "$host" = "dev.azure.com" ]; then
  refuse "Azure DevOps pull requests"
fi
if [ "$host" != "github.com" ] || [ -z "$repository" ]; then
  exit 0
fi

response=$(env -u GH_CONFIG_DIR -u GH_TOKEN -u GITHUB_TOKEN gh api --hostname github.com "repos/$repository" --silent 2>&1)
if grep -qE 'HTTP 40[34]' <<<"$response"; then
  refuse "$repository with the GitHub account T3 uses"
fi
exit 0
