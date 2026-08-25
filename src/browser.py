"""Centro de construcción del navegador para multi-cuenta.

Variables de entorno soportadas:
  REWARDS_DATA_DIR      Directorio de perfil por cuenta (default: ./data-dir)
  REWARDS_PROFILE       Perfil dentro del data-dir (default: Default)
  REWARDS_PROXY         Proxy HTTP:  http://host:port  o  http://user:pass@host:port
  REWARDS_USER_AGENT    User-Agent propio (variar por cuenta)
  REWARDS_CHROMEDRIVER  Ruta al chromedriver (default: /snap/bin/chromium.chromedriver)
"""
import json
import os
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from constants import USER_DATA_DIR, PROFILE_NAME


def make_proxy_auth_extension(proxy_url: str) -> str:
    """Genera una extensión Chrome descomprimida que fija el proxy y responde
    a autenticación básica (necesario para proxies con user:pass)."""
    parsed = urlparse(proxy_url)
    user = parsed.username or ""
    password = parsed.password or ""
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    scheme = parsed.scheme or "http"

    manifest = {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth",
        "permissions": [
            "proxy", "tabs", "unlimitedStorage", "storage",
            "<all_urls>", "webRequest", "webRequestBlocking",
        ],
        "background": {"scripts": ["background.js"]},
    }
    background_js = f"""
var config = {{
    mode: "fixed_servers",
    rules: {{
        singleProxy: {{
            scheme: "{scheme}",
            host: "{host}",
            port: {port}
        }},
        bypassList: []
    }}
}};
chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{user}",
            password: "{password}"
        }}
    }};
}}
chrome.webRequest.onAuthRequired.addListener(callbackFn, {{urls: ["<all_urls>"]}}, ["blocking"]);
"""

    ext_dir = os.path.join(USER_DATA_DIR, "proxy_ext")
    os.makedirs(ext_dir, exist_ok=True)
    with open(os.path.join(ext_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f)
    with open(os.path.join(ext_dir, "background.js"), "w") as f:
        f.write(background_js)
    return ext_dir


def build_options() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    options.add_argument(f"--profile-directory={PROFILE_NAME}")
    options.add_argument("--window-size=1280,900")

    ua = os.environ.get("REWARDS_USER_AGENT")
    if ua:
        options.add_argument(f"--user-agent={ua}")

    proxy = os.environ.get("REWARDS_PROXY")
    if proxy:
        if "@" in proxy:
            ext_dir = make_proxy_auth_extension(proxy)
            options.add_argument(f"--load-extension={ext_dir}")
            options.add_argument(f"--disable-extensions-except={ext_dir}")
        else:
            options.add_argument(f"--proxy-server={proxy}")

    return options


def build_driver() -> webdriver.Chrome:
    chromedriver = os.environ.get(
        "REWARDS_CHROMEDRIVER", "/snap/bin/chromium.chromedriver"
    )
    return webdriver.Chrome(
        service=Service(executable_path=chromedriver),
        options=build_options(),
    )