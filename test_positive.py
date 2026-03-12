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

VALID_USER = {
    "firstName": "Aman",
    "lastName": "Sharma",
    "username": "aman_sharma_test",
    "password": "Test@1234",
    "gender": "Male",
}


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment for headless mode
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()


def register_user(driver, user):
    """Helper to fill and submit the registration form."""
    driver.get(REGISTER_URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
    driver.find_element(By.NAME, "firstName").send_keys(user["firstName"])
    driver.find_element(By.NAME, "lastName").send_keys(user["lastName"])
    driver.find_element(By.NAME, "userName").send_keys(user["username"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    driver.find_element(By.NAME, "confirmPassword").send_keys(user["password"])

    # Select gender radio button
    gender_xpath = f"//input[@type='radio' and following-sibling::*[contains(text(),'{user['gender']}')]]"
    gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
    for radio in gender_radios:
        if user["gender"].lower() in radio.text.lower():
            radio.click()
            break

    driver.find_element(By.XPATH, "//button[@type='submit']").click()


# ─────────────────────────────────────────────────────────
# POSITIVE TEST CASES
# ─────────────────────────────────────────────────────────

class TestPositiveRegistration:

    def test_TC_REG_P01_register_with_valid_user_details(self, driver):
        """TC_REG_P01 — Register with valid user details."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Aman")
        driver.find_element(By.NAME, "lastName").send_keys("Sharma")
        driver.find_element(By.NAME, "userName").send_keys("aman_sharma_p01")
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Test@1234")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # After successful registration, should redirect to login
        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url, "Expected redirect to login page after registration"

    def test_TC_REG_P02_register_with_valid_email_format(self, driver):
        """TC_REG_P02 — Register with valid email as username."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Priya")
        driver.find_element(By.NAME, "lastName").send_keys("Patel")
        driver.find_element(By.NAME, "userName").send_keys("priya.patel.test@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("Priya@5678")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Priya@5678")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "female" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url, "Valid email format should be accepted as username"

    def test_TC_REG_P03_register_with_strong_password(self, driver):
        """TC_REG_P03 — Register with a strong password."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Raj")
        driver.find_element(By.NAME, "lastName").send_keys("Kumar")
        driver.find_element(By.NAME, "userName").send_keys("raj_kumar_p03")
        driver.find_element(By.NAME, "password").send_keys("Str0ng@Pass#21")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Str0ng@Pass#21")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url, "Strong password should be accepted"

    def test_TC_REG_P04_register_with_unique_username(self, driver):
        """TC_REG_P04 — Register with a unique username."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Sneha")
        driver.find_element(By.NAME, "lastName").send_keys("Reddy")
        driver.find_element(By.NAME, "userName").send_keys("sneha_reddy_unique99")
        driver.find_element(By.NAME, "password").send_keys("Sneha@9999")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Sneha@9999")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "female" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url, "Unique username should be accepted"

    def test_TC_REG_P05_register_all_required_fields(self, driver):
        """TC_REG_P05 — Register with all required fields filled."""
        driver.get(REGISTER_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Vikram")
        driver.find_element(By.NAME, "lastName").send_keys("Singh")
        driver.find_element(By.NAME, "userName").send_keys("vikram_singh_p05")
        driver.find_element(By.NAME, "password").send_keys("Vikram@123")
        driver.find_element(By.NAME, "confirmPassword").send_keys("Vikram@123")

        gender_radios = driver.find_elements(By.XPATH, "//mat-radio-button")
        for radio in gender_radios:
            if "male" in radio.text.lower():
                radio.click()
                break

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url, "Registration with all fields should succeed"


class TestPositiveLogin:

    def test_TC_LOG_P01_login_with_valid_credentials(self, driver):
        """TC_LOG_P01 — Login with valid email and password."""
        # First register the user
        register_user(driver, {**VALID_USER, "username": "aman_login_p01"})
        time.sleep(1)

        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("aman_login_p01")
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains(BASE_URL))
        assert "login" not in driver.current_url, "Should be redirected away from login after success"

    def test_TC_LOG_P02_login_after_registration(self, driver):
        """TC_LOG_P02 — Login immediately after successful registration."""
        uname = "post_reg_login_p02"
        register_user(driver, {**VALID_USER, "username": uname})

        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("login"))

        driver.find_element(By.NAME, "username").send_keys(uname)
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains(BASE_URL))
        assert "login" not in driver.current_url, "Login after registration should succeed"

    def test_TC_LOG_P03_login_with_correct_registered_account(self, driver):
        """TC_LOG_P03 — Login with correct registered account."""
        uname = "vikram_login_p03"
        register_user(driver, {**VALID_USER, "username": uname})
        time.sleep(1)

        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(uname)
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains(BASE_URL))
        assert "login" not in driver.current_url, "Login with correct account should succeed"

    def test_TC_LOG_P04_login_and_navigate_home(self, driver):
        """TC_LOG_P04 — Login and navigate to home page successfully."""
        uname = "nav_home_p04"
        register_user(driver, {**VALID_USER, "username": uname})
        time.sleep(1)

        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(uname)
        driver.find_element(By.NAME, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_contains(BASE_URL))

        # Navigate to home and check page loads
        driver.get(BASE_URL)
        assert driver.title != "", "Home page should load after login"
        assert "login" not in driver.current_url, "Session should persist after navigation"

    def test_TC_LOG_P05_login_multiple_times_valid_credentials(self, driver):
        """TC_LOG_P05 — Login multiple times with valid credentials."""
        uname = "multi_login_p05"
        register_user(driver, {**VALID_USER, "username": uname})
        time.sleep(1)

        wait = WebDriverWait(driver, 10)

        for attempt in range(1, 4):
            driver.get(LOGIN_URL)
            wait.until(EC.presence_of_element_located((By.NAME, "username")))
            driver.find_element(By.NAME, "username").send_keys(uname)
            driver.find_element(By.NAME, "password").send_keys("Test@1234")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            wait.until(EC.url_contains(BASE_URL))
            assert "login" not in driver.current_url, \
                f"Login attempt {attempt} should succeed without lockout"
            time.sleep(0.5)
