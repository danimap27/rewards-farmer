import browser

driver = browser.build_driver()
driver.get("about:blank")
import time
time.sleep(3)
print("TITLE:", driver.title)
print("EXT_LOADED:", __import__("os").path.exists(__import__("os").path.join(browser.USER_DATA_DIR, "proxy_ext")))
driver.quit()