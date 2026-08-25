import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--user-data-dir=/home/quantum-nas/proyectos/active/rewards-farmer/data-remote-test")
opts.add_argument("--window-size=1280,900")
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Remote(command_executor="http://localhost:9515", options=opts)
driver.get("https://rewards.bing.com/")
time.sleep(10)
print("TITLE:", driver.title)
driver.quit()