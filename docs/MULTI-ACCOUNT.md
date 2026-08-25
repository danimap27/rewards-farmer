# Multi-Account Edition

Fork/variant of `rewards-farmer` that runs **one isolated browser profile per Microsoft Rewards account**, so you can farm several accounts from a single machine.

> ⚠️ **Read this first.** Automated farming violates Microsoft Rewards Terms of Service. Microsoft can ban any account at any time, and multi-accounting from one machine/IP is precisely what their fraud detection looks for. Only use throwaway accounts you are prepared to lose. Use one **sticky residential proxy per account** if you want any realistic chance of longevity. The author of this variant does not guarantee anything works.

## What changed vs upstream

| File | Change |
|---|---|
| `src/browser.py` | **New.** Central browser factory. Reads all multi-account settings from environment variables. |
| `src/constants.py` | `USER_DATA_DIR` / `PROFILE_NAME` now come from env (`REWARDS_DATA_DIR`, `REWARDS_PROFILE`). |
| `src/main.py` | Uses `browser.build_driver()` (+ `.quit()` on exit). |
| `src/login_standby.py` | **New.** Opens `rewards.bing.com` + `bing.com` and idles — use it for the one-time manual sign-in per account. |
| `src/llm_utils.py` | Model switched from `gemma4:cloud` (Ollama cloud account) to a **local** model (`gemma3:4b`). No Ollama account needed. |
| `scripts/run.sh` | Launches the bot for one account (`./data-<acct>`, optional proxy). |
| `scripts/login.sh` | Launches sign-in standby for one account. |
| `scripts/farm_all.sh` | Launches every account in `accounts.conf`, staggered. |
| `accounts.conf.example` | Account list format: `<name> [proxy_url]` per line. |

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `REWARDS_DATA_DIR` | `./data-dir` | Per-account browser profile directory. **Isolates sessions/cookies.** |
| `REWARDS_PROFILE` | `Default` | Profile inside the data dir. |
| `REWARDS_PROXY` | *(none)* | HTTP proxy: `http://host:port` or `http://user:pass@host:port`. Credentialed proxies get a generated Chrome extension (auth handled automatically). |
| `REWARDS_USER_AGENT` | *(none)* | Custom User-Agent per account — helps differentiate fingerprints. |
| `REWARDS_CHROMEDRIVER` | `/snap/bin/chromium.chromedriver` | Path to chromedriver. |

## Setup (Linux host)

```sh
git clone https://github.com/<you>/rewards-farmer
cd rewards-farmer

# Python 3.14+ and deps
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python "selenium>=4.46,<5" "matplotlib>=3.11,<4" "pygetwindow>=0.0.9,<0.0.10" "keyboard>=0.13.5,<0.14" "pygame-ce>=2.5.8,<3" "ollama>=0.6.2,<0.7" numpy

# Local LLM for search queries (no cloud account)
ollama pull gemma3:4b       # or edit llm_utils.py model=

# Headless display (server without screen)
Xvfb :99 -screen 0 1280x900x24 -nolisten tcp &
```

If you run Chromium from the Ubuntu snap, its bundled chromedriver works out of the box:
`/snap/bin/chromium.chromedriver` (Chromium snap 151+). For other browsers install the matching chromedriver and point `REWARDS_CHROMEDRIVER` at it.

## One-time manual sign-in per account

The bot needs an authenticated Microsoft session in each account profile **once**:

```sh
scripts/login.sh cuenta01
# ...sign in via VNC/screen on rewards.bing.com AND bing.com, accept EU consent banner...
# Ctrl-C when done
scripts/login.sh cuenta02 http://user:pass@residential-proxy:8080
```

Headless server? Run `scripts/login.sh` inside the Xvfb display and connect with any VNC viewer
(`x11vnc -display :99 -rfbport 5901 -nopw -forever`).

## Running every account

```sh
cp accounts.conf.example accounts.conf
# edit: one account per line, optionally with a per-account proxy
scripts/farm_all.sh
```

`farm_all.sh`:
- starts Xvfb `:99` if missing
- launches **one bot process per account**, each with its own `./data-<name>`
- staggers startups (20–45s random) so accounts never act simultaneously
- writes logs to `logs/<name>.log`

Manual single run:

```sh
scripts/run.sh cuenta01 http://user:pass@proxy.example:8080
```

## Daily cron (optional)

Example — one pass a day at staggered times, taking it slow:

```
30 7 * * *  cd ~/proyectos/active/rewards-farmer && ./scripts/farm_all.sh
```

Keep in mind: bots that complete 100% of every task every single day at the same minute are the easiest pattern to fingerprint. Vary your schedule, skip days, don't max out every account.

## Anti-detection reality check

What this variant does for you:
- ✅ isolated profile + cookies per account (`REWARDS_DATA_DIR`)
- ✅ per-account proxy support, including auth via extension
- ✅ per-account User-Agent
- ✅ human-like mouse Bézier trajectories & typing pauses (upstream)
- ✅ LLM-generated, unique, semantically coherent search queries (upstream)

What it does **not** do (do not be fooled):
- ❌ Different browser fingerprint per account. All accounts use the *same* Chromium build — canvas/WebGL/font fingerprint stays identical. IP rotation alone will not hide that. For real fingerprint diversity you need different browser engines per account (or canvas-noise tooling).
- ❌ Residential-only IPs. Datacenter/VPN IPs are flagged instantly.
- ❌ Accounts created from correlated patterns: same machine, same email domain, same hour, same recovery phone → instant correlation.

## Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `Read timed out` / `DevToolsActivePort file doesn't exist` | Stale Chromium processes from earlier runs. Kill them: `pkill -f '[s]nap/chromium'` (adjust pattern to your browser), then retry. |
| Driver connects but page never loads | Proxy dead or requires auth without credentials. Check `REWARDS_PROXY` format. |
| Profile locks | Two bots with the same `REWARDS_DATA_DIR`/profile. Every account needs its own data dir. |
| `modal dialog` / banner on EU accounts | Accept consent once during manual login; choice is saved in the profile. |

## License

MIT (same as upstream). Use at your own risk; neither upstream nor this variant is affiliated with Microsoft.