#!/usr/bin/env bash
# Abre el navegador en modo standby para hacer el login manual de una cuenta.
# Uso: scripts/login.sh <cuenta> [proxy_url]
set -euo pipefail

ACCOUNT="${1:?Uso: scripts/login.sh <cuenta> [proxy_url]}"
cd "$(dirname "$0")/.."

export REWARDS_DATA_DIR="./data-${ACCOUNT}"
[ $# -ge 2 ] && export REWARDS_PROXY="$2"

echo "[login] cuenta=${ACCOUNT} data=${REWARDS_DATA_DIR}${REWARDS_PROXY:+ proxy=${REWARDS_PROXY}}"
echo "[login] Conectate por VNC si el homelab no tiene pantalla."
exec .venv/bin/python src/login_standby.py