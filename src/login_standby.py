import time

import browser

driver = browser.build_driver()
driver.get("https://rewards.bing.com/")
driver.execute_script("window.open('https://www.bing.com/', '_blank');")
print("READY: navegador abierto en rewards.bing.com + bing.com. Login manual pendiente.")
while True:
    time.sleep(60)
    print("still alive, title:", driver.title[:60])