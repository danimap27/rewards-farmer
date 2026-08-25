import browser
import mouse_trajectory
import mimic_typing
import rewards_tasks

driver = browser.build_driver()

mouse = mouse_trajectory.MouseUtils(driver)
keyboard = mimic_typing.KeyboardUtils(driver)

rewards = rewards_tasks.RewardsTaskUtils(driver)

rewards.complete_all_tasks()

input("Press Enter to exit...")

driver.quit()