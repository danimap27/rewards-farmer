#!/usr/bin/env bash
# Lanza el bot para TODAS las cuentas de accounts.conf.
# Formato de accounts.conf (una por linea, "nombre [proxy]"): ver accounts.conf.example
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f accounts.conf ]; then
    echo "Falta accounts.conf. Copia desde accounts.conf.example y edita." >&2
    exit 1
fi

mkdir -p logs

# Display virtual compartido (si no hay Xvfb :99, lo levantamos)
if ! pgrep -f "Xvfb :99" >/dev/null; then
    echo "[farm] levantando Xvfb :99"
    Xvfb :99 -screen 0 1280x900x24 -nolisten tcp &
    disown
    sleep 2
fi

PIDS=()
while read -r name proxy; do
    [ -z "$name" ] && continue
    [[ "$name" == \#* ]] && continue

    logfile="logs/${name}.log"
    if [ -n "$proxy" ]; then
        DISPLAY=:99 REWARDS_DATA_DIR="./data-${name}" REWARDS_PROXY="$proxy" \
            .venv/bin/python src/main.py >>"$logfile" 2>&1 &
    else
        DISPLAY=:99 REWARDS_DATA_DIR="./data-${name}" \
            .venv/bin/python src/main.py >>"$logfile" 2>&1 &
    fi
    pid=$!
    PIDS+=("$pid:$name")
    echo "[farm] lanzada ${name} (pid ${pid}) log=${logfile}"

    # Escalonar arranques: evita el patron "todas a la misma hora"
    sleep "$((RANDOM % 25 + 20))"
done < accounts.conf

echo "[farm] ${#PIDS[@]} cuentas lanzadas. PIDs: ${PIDS[*]}"
echo "[farm] Para ver logs: tail -f logs/<cuenta>.log"