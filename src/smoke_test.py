import time

import browser

driver = browser.build_driver()
driver.get("https://rewards.bing.com/")
time.sleep(8)
driver.save_screenshot("smoke_test.png")
print("TITLE:", driver.title)
print("URL:", driver.current_url)
driver.quit()