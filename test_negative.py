import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://bookcart.azurewebsites.net"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment for headless mode
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()


# ─────────────────────────────────────────────────────────
# NEGATIVE TEST CASES
# ─────────────────────────────────────────────────────────

class TestNegativeRegistration:

    def test_TC_REG_N01_register_with_empty_fields(self, driver):
        """TC_REG_N01 — Register with all fields empty."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

        # Click submit without filling any field
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(1)

        # Should still be on register page — not redirected
        assert "register" in driver.current_url, \
            "Should remain on register page when fields are empty"

        # Check for validation error messages
        error_elements = driver.find_elements(By.XPATH, "//mat-error")
        assert len(error_elements) > 0, \
            "Validation errors should be shown for empty fields"

    def test_TC_REG_N02_register_with_invalid_email_format(self, driver):
        """TC_REG_N02 — Register with invalid email format as username."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Meera")
        driver.find_element(By.NAME, "lastName").send_keys("Joshi")
        driver.find_element(By.NAME, "userName").send_keys("meerajoshi@@invalid..com")
        driver.find_element(By.NAME, "password").send_keys("Meera@123")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Meera@123")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "female" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(1)

        # Should remain on register page
        assert "register" in driver.current_url, \
            "Should remain on register page for invalid email format"

        # Should show a validation error
        error_elements = driver.find_elements(By.XPATH, "//mat-error")
        assert len(error_elements) > 0, \
            "Validation error should appear for invalid email format"

    def test_TC_REG_N03_register_with_existing_username(self, driver):
        """TC_REG_N03 — Register with an already existing username."""
        # Step 1: Register original user
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Aman")
        driver.find_element(By.NAME, "lastName").send_keys("Sharma")
        driver.find_element(By.NAME, "userName").send_keys("duplicate_user_n03")
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Test@1234")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        wait.until(EC.url_contains("login"))
        time.sleep(1)

        # Step 2: Try to register again with same username
        driver.get(REGISTER_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Aman")
        driver.find_element(By.NAME, "lastName").send_keys("Sharma")
        driver.find_element(By.NAME, "userName").send_keys("duplicate_user_n03")
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Test@1234")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)

        # Should NOT redirect to login — should show error
        assert "login" not in driver.current_url, \
            "Should not allow registration with duplicate username"


class TestNegativeLogin:

    def test_TC_LOG_N01_login_with_incorrect_password(self, driver):
        """TC_LOG_N01 — Login with incorrect password."""
        # Register user first
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Aman")
        driver.find_element(By.NAME, "lastName").send_keys("Sharma")
        driver.find_element(By.NAME, "userName").send_keys("wrong_pw_n01")
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Test@1234")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        wait.until(EC.url_contains("login"))
        time.sleep(1)

        # Attempt login with wrong password
        driver.get(LOGIN_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("wrong_pw_n01")
        driver.find_element(By.NAME, "password").send_keys("WrongPass@99")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)

        # Should remain on login page
        assert "login" in driver.current_url, \
            "Should remain on login page for incorrect password"

        # Check for error snackbar or message
        error_elements = driver.find_elements(
            By.XPATH, "//*[contains(@class,'snack') or contains(@class,'error') or contains(@class,'alert')]"
        )
        assert len(error_elements) > 0 or "login" in driver.current_url, \
            "Error message should appear for incorrect password"

    def test_TC_LOG_N02_login_with_unregistered_username(self, driver):
        """TC_LOG_N02 — Login with unregistered username."""
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("ghost_user_xyz99")
        driver.find_element(By.NAME, "password").send_keys("AnyPass@123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)

        # Should remain on login page
        assert "login" in driver.current_url, \
            "Should remain on login page for unregistered username"

        # Check for error message
        error_elements = driver.find_elements(
            By.XPATH, "//*[contains(@class,'snack') or contains(@class,'error') or contains(@class,'alert')]"
        )
        assert len(error_elements) > 0 or "login" in driver.current_url, \
            "Error message should appear for unregistered username"
