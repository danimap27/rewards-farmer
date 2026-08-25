#!/usr/bin/env bash
# Lanza el bot completo para una cuenta.
# Uso: scripts/run.sh <cuenta> [proxy_url]
#   proxy_url: http://user:pass@host:port  o  http://host:port  (opcional)
set -euo pipefail

ACCOUNT="${1:?Uso: scripts/run.sh <cuenta> [proxy_url]}"
cd "$(dirname "$0")/.."

export REWARDS_DATA_DIR="./data-${ACCOUNT}"
[ $# -ge 2 ] && export REWARDS_PROXY="$2"

echo "[run] cuenta=${ACCOUNT} data=${REWARDS_DATA_DIR}${REWARDS_PROXY:+ proxy=${REWARDS_PROXY}}"
exec .venv/bin/python src/main.py