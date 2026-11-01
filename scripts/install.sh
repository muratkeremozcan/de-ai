#!/usr/bin/env bash
# Link this repository's de-ai skill into every host discovery folder under $HOME.
# Checks all destinations first and writes nothing when any is a real file or directory.
set -euo pipefail

skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/skills/de-ai"
roots=("$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills" "$HOME/.gemini/config/skills")

for root in "${roots[@]}"; do
  if [ -e "$root/de-ai" ] && [ ! -L "$root/de-ai" ]; then
    echo "refusing: $root/de-ai is a real file or directory" >&2
    exit 1
  fi
done

for root in "${roots[@]}"; do
  mkdir -p "$root"
  ln -sfn "$skill" "$root/de-ai"
  echo "$root/de-ai -> $skill"
done
