import re
from playwright.sync_api import Page, expect
from config import TEST_FIRST_NAME, TEST_LAST_NAME, TEST_EMP_ID
from pages.pim_page import PIMPage 

# TC-emp-01: Successfully open the add employee page
def test_open_add_emp(page: Page):
    # TODO: Perform login here or pass a logged-in page via a pytest fixture
    
    pim = PIMPage(page)
    pim.goto_pim()
    pim.add_emp_tab()
    
    # Assert the URL changes to the add employee endpoint
    expect(page).to_have_url(re.compile(r".*/pim/addEmployee"))
    # Assert the page heading is visible
    expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()

# TC-emp-02: Fail to add employee due to missing required fields
def test_fail_add_emp(page: Page):
    """TC2: Only adding the first name and failing to save."""
    # TODO: Perform login here
    
    pim = PIMPage(page)
    pim.goto_pim()
    pim.add_emp_tab()
    
    pim.fill_first_name("Nisrina")
    pim.fill_employee_id("0508")
    # Intentionally leaving Last Name blank
    pim.save()
    
    # Assert that the "Required" error message appears under the Last Name field
    # OrangeHRM displays "Required" texts when mandatory fields are missed
    expect(page.get_by_text("Required", exact=True)).to_be_visible()
    expect(page.get_by_text("Employee Id already exists")).to_be_visible()

# TC-emp-03: Successfully add a new employee and assert by searching
def test_add_new_emp(page: Page):
    """TC3: Successfully adding the new employee data and asserting by searching."""
    # TODO: Perform login here
    
    pim = PIMPage(page)
    
    # 1. Add the employee
    pim.goto_pim()
    pim.add_emp_tab()
    pim.fill_first_name(TEST_FIRST_NAME)
    pim.fill_last_name(TEST_LAST_NAME)
    pim.fill_employee_id(TEST_EMP_ID)
    pim.save()
    
    # Wait for the success toast to appear and disappear before navigating away
    expect(page.locator(".oxd-toast--success")).to_be_visible()
    expect(page.locator(".oxd-toast--success")).to_be_hidden()
    
    # 2. Search for the employee
    pim.emp_list_tab()
    pim.click_reset() # Good practice to reset filters first
    pim.search_by_id(TEST_EMP_ID)
    pim.click_search()
    
    # 3. Assert the employee shows up in the table
    employee_card = pim.get_employee_card_by_id(TEST_EMP_ID)
    expect(employee_card).to_be_visible()

# def test_edit_emp(page: Page):
#     """TC4: Successfully opening the edit page for that employee."""
#     # TODO: Perform login here
    
#     pim = PIMPage(page)
#     pim.goto_pim()
#     pim.emp_list_tab()
    
#     # Search for the specific employee created in TC3
#     pim.search_by_id(TEST_EMP_ID)
#     pim.click_search()
    
#     # Click the edit button using your POM method
#     pim.click_edit_employee(TEST_EMP_ID)
    
#     # Assert we navigated to the Personal Details (Edit) page
#     # OrangeHRM edit URL structure: /web/index.php/pim/viewPersonalDetails/empNumber/{id}
#     expect(page).to_have_url(re.compile(r".*/pim/viewPersonalDetails.*"))
#     expect(page.get_by_role("heading", name="Personal Details")).to_be_visible()