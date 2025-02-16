import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

serv_obj = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service = serv_obj)

url = "https://inc42.com/"
email = "inc@yopmail.com"
password = "Vishal@inc42"

# wait function
def wait_for_elem(loc_type, loc, time_out=20):
    return WebDriverWait(driver, time_out).until(EC.presence_of_element_located((loc_type, loc)))

# screenshot function
def screenshot(filename):
    driver.save_screenshot(filename)
    print(f"screenshot captured: {filename}")

try:
    driver.get(url)
    driver.maximize_window()

    # verify "Datalabs" button
    datalabs_link = wait_for_elem(By.LINK_TEXT, "DATALABS")
    if datalabs_link.is_displayed() and datalabs_link.is_enabled():
        datalabs_link.click()
        print("Datalabs button is clickable")
    else:
        print("Datalabs link is not clickable")
        screenshot("datalabs_link_not_found.png")
        driver.quit()
        exit()

    # login
    login_btn = wait_for_elem(By.LINK_TEXT, "Login")
    if login_btn.is_displayed() and login_btn.is_enabled():
        login_btn.click()
        print("Login Button is clickable")

        # error (login popup is slow, so we have to wait a little)
        time.sleep(5)

        # login form
        email_box = wait_for_elem(By.ID, "2-email")
        pass_box = wait_for_elem(By.NAME, "password")
        submit_btn = wait_for_elem(By.XPATH, "//span[@class='auth0-label-submit']")

        if email_box.is_displayed() and email_box.is_enabled():
            email_box.send_keys(email)
            pass_box.send_keys(password)
            submit_btn.click()
            print("clicked on LOG IN")

            # login takes a little bit of time
            time.sleep(5)
        else:
            print("Email Box not found")
            screenshot("login_popup_error.png")
            driver.quit()
            exit()


        # verify successful login
        try:
            dashboard_elem = wait_for_elem(By.LINK_TEXT, "My Lists")
            print("Login Successfull")
            dashboard_elem.click()
            screenshot("login_successful.png")
            time.sleep(5)
        except:  # noqa: E722
            print("Login failed")
            screenshot("login_failed.png")
            driver.quit()
            exit()

        # perform a search
        finally:
            search_box = wait_for_elem(By.ID, "global_search")
            search_box.send_keys("Fintech")
            search_box.send_keys(Keys.RETURN)
            print("Search for 'Fintech' performed")

        # verify "Fintech" search results
        try:
            time.sleep(5) # wait for search result
            search_res = wait_for_elem(By.XPATH, "//input[@placeholder='Search For...']")
            print("Search result displayed properly")
            screenshot("search_result.png")
        except:
            print("Search result not displayed")
            screenshot("search_failed.png")


    else:
        print("Login button is not clickable")
        driver.quit()
        exit()

except Exception as e:
    print(f"Error encounterd: {e}")
    screenshot("error.png")

finally:
    driver.quit()
    print("Test completed and browser closed")




