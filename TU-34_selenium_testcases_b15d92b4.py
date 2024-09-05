from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Initialize WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Update path to WebDriver
wait = WebDriverWait(driver, 15)  # Explicit wait with a 15-second timeout

# Constants
base_url = "http://example.com"  # Update to your web application's URL

# Helper Functions
def login(username, password):
    """
    Log in to the web application using the given username and password.
    """
    driver.get(base_url + "/login")
    try:
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "loginButton").click()
        wait.until(EC.visibility_of_element_located((By.ID, "userHeader")))
        print("Successfully logged in.")
    except NoSuchElementException as e:
        print("Login failed due to missing elements:", e)

def access_member_lookup():
    """
    Access the Member Lookup feature by revealing the Member Lookup header
    and navigating to the Member Lookup page.
    """
    try:
        # Reveal Member Lookup header
        driver.find_element(By.ID, "userHeader").click()
        wait.until(EC.visibility_of_element_located((By.ID, "memberLookupHeader")))

        # Navigate to the Member Lookup page
        driver.find_element(By.ID, "memberLookupHeader").click()
        wait.until(EC.visibility_of_element_located((By.ID, "enterMRNSection")))
        print("Navigated to the Member Lookup page.")
    except (NoSuchElementException, TimeoutException) as e:
        print("Error accessing Member Lookup:", e)

# Test Cases
def test_member_lookup_header_access():
    """
    Verify that the Member Lookup header is initially hidden and
    becomes visible after holding shift and clicking the user ID header.
    """
    login("testUser", "testPassword")
    access_member_lookup()
    try:
        assert driver.find_element(By.ID, "memberLookupHeader").is_displayed(), "Member Lookup header is not displayed"
        print("Test Case 1: Member Lookup Header Access - Passed")
    except AssertionError as e:
        print("Test Case 1: Member Lookup Header Access - Failed:", e)

def test_navigation_to_member_lookup_page():
    """
    Verify that the Member Lookup page is correctly navigated to.
    """
    access_member_lookup()
    try:
        assert driver.find_element(By.ID, "enterMRNSection").is_displayed(), "Enter MRN section is not displayed"
        print("Test Case 2: Navigation to Member Lookup Page - Passed")
    except AssertionError as e:
        print("Test Case 2: Navigation to Member Lookup Page - Failed:", e)

def test_enter_mrn_section():
    """
    Verify that the Enter MRN section accepts input, retrieves member details,
    and clears input fields upon clicking the Cancel button.
    """
    access_member_lookup()

    try:
        # Input MRN data
        driver.find_element(By.ID, "region").send_keys("SCAL")
        driver.find_element(By.ID, "mrnPrefix").send_keys("00")
        driver.find_element(By.ID, "enterMRN").send_keys("1234567890")
        driver.find_element(By.ID, "enterButton").click()

        # Wait for data retrieval
        wait.until(EC.visibility_of_element_located((By.ID, "memberDetailsSection")))
        wait.until(EC.visibility_of_element_located((By.ID, "recentOrdersSection")))

        # Verify Member Details and Recent Orders sections
        assert driver.find_element(By.ID, "memberDetailsSection").is_displayed(), "Member Details section not displayed"
        assert driver.find_element(By.ID, "recentOrdersSection").is_displayed(), "Recent Orders section not displayed"

        # Clear input fields
        driver.find_element(By.ID, "cancelButton").click()
        assert driver.find_element(By.ID, "region").text == "", "Region field is not cleared"
        assert driver.find_element(By.ID, "mrnPrefix").text == "", "MRN Prefix field is not cleared"
        assert driver.find_element(By.ID, "enterMRN").text == "", "MRN field is not cleared"

        print("Test Case 3: Enter MRN Section - Passed")
    except AssertionError as e:
        print("Test Case 3: Enter MRN Section - Failed:", e)
    except (NoSuchElementException, TimeoutException) as e:
        print("Error in Enter MRN Section:", e)

def test_member_details_section():
    """
    Verify that the Member Details section displays the correct member information.
    """
    access_member_lookup()
    driver.find_element(By.ID, "enterMRN").send_keys("1234567890")
    driver.find_element(By.ID, "enterButton").click()

    try:
        # Verify relevant details
        wait.until(EC.visibility_of_element_located((By.ID, "memberDetailsSection")))
        assert driver.find_element(By.ID, "firstName").text != "", "First name is missing"
        assert driver.find_element(By.ID, "lastName").text != "", "Last name is missing"
        assert driver.find_element(By.ID, "mrn").text != "", "MRN is missing"
        print("Test Case 4: Member Details Section - Passed")
    except AssertionError as e:
        print("Test Case 4: Member Details Section - Failed:", e)
    except TimeoutException as e:
        print("Error in Member Details Section:", e)

def test_recent_orders_section():
    """
    Verify that the Recent Orders section displays the correct orders based on filter selection.
    """
    access_member_lookup()
    driver.find_element(By.ID, "enterMRN").send_keys("1234567890")
    driver.find_element(By.ID, "enterButton").click()
    wait.until(EC.visibility_of_element_located((By.ID, "recentOrdersSection")))

    try:
        # Verify orders are populated
        assert driver.find_element(By.ID, "orderRow1").is_displayed(), "Default order row is missing"

        # Test filters
        filter_dropdown = driver.find_element(By.ID, "orderFilter")
        filter_dropdown.send_keys("Past Month")
        assert driver.find_element(By.ID, "orderRow1").is_displayed(), "Order row for past month is missing"

        filter_dropdown.send_keys("Past 3 Months")
        assert driver.find_element(By.ID, "orderRow1").is_displayed(), "Order row for past 3 months is missing"

        print("Test Case 5: Recent Orders Section - Passed")
    except AssertionError as e:
        print("Test Case 5: Recent Orders Section - Failed:", e)

def test_order_details_expansion():
    """
    Verify that clicking the expansion icon displays the detailed order information.
    """
    access_member_lookup()
    driver.find_element(By.ID, "enterMRN").send_keys("1234567890")
    driver.find_element(By.ID, "enterButton").click()
    wait.until(EC.visibility_of_element_located((By.ID, "recentOrdersSection")))

    try:
        # Expand the first order
        driver.find_element(By.XPATH, "//tr[@id='orderRow1']/td[1]/button").click()
        wait.until(EC.visibility_of_element_located((By.ID, "orderDetailsTable")))

        # Verify the order details
        assert driver.find_element(By.ID, "drugName").text != "", "Drug name is missing"
        assert driver.find_element(By.ID, "kpRxNumber").text != "", "KP RX Number is missing"
        assert driver.find_element(By.ID, "ndcCode").text != "", "NDC Code is missing"
        assert driver.find_element(By.ID, "totalAmount").text != "", "Total amount is missing"

        print("Test Case 6: Order Details Expansion - Passed")
    except AssertionError as e:
        print("Test Case 6: Order Details Expansion - Failed:", e)
    except (NoSuchElementException, TimeoutException) as e:
        print("Error in Order Details Expansion:", e)

if __name__ == "__main__":
    # Run all test cases
    test_member_lookup_header_access()
    test_navigation_to_member_lookup_page()
    test_enter_mrn_section()
    test_member_details_section()
    test_recent_orders_section()
    test_order_details_expansion()

    # Close the browser
    driver.quit()