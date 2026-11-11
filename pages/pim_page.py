import re
from playwright.sync_api import Page, Locator

class PIMPage:
    def __init__(self, page: Page):
        self.page = page


    ## PAGE NAVIGATION
    # ================================

    def goto_pim(self):
        self.page.get_by_role("link", name="PIM").click()

    def emp_list_tab(self):
        self.page.get_by_role("link", name="Employee List").click()

    def add_emp_tab(self):
        self.page.get_by_role("link", name="Add Employee").click()

    def reports_tab(self):
        self.page.get_by_role("link", name="Reports").click()


    ## TABLE NAVIGATION
    # ================================

    def get_employee_card_by_id(self, emp_id: str) -> Locator:
        """
        Locates the specific employee card/row based on their exact ID.
        """
        # Using a regex word boundary (\b) ensures we match exactly "Id 457" 
        # and not accidentally grab "Id 4578"
        exact_match_pattern = re.compile(rf"\bId\s+{emp_id}\b")
        
        # Targets the generic container for each employee record (works for both list and grid views)
        return self.page.locator(".oxd-table-card, .oxd-grid-item").filter(has_text=exact_match_pattern)

    def click_edit_employee(self, emp_id: str):
        """Clicks the Edit (pencil) button for a specific employee ID."""
        card = self.get_employee_card_by_id(emp_id)
        # Locates the specific edit icon button scoped only inside that employee's card
        card.locator("button:has(i.bi-pencil-fill), button:has(i.oxd-icon.bi-pencil)").click()

    def click_delete_employee(self, emp_id: str):
        """Clicks the Delete (trash) button for a specific employee ID."""
        card = self.get_employee_card_by_id(emp_id)
        # Locates the specific delete icon button scoped only inside that employee's card
        card.locator("button:has(i.bi-trash-fill), button:has(i.oxd-icon.bi-trash)").click()


    ## EMPLOYEE ADDITION
    # ================================
    
    def click_add_employee(self):
        self.page.get_by_role("link", name="Add Employee").click()

    def fill_first_name(self, first_name: str):
        self.page.get_by_role("textbox", name="First Name").fill(first_name)

    def fill_middle_name(self, middle_name: str):
        self.page.get_by_role("textbox", name="Middle Name").fill(middle_name)

    def fill_last_name(self, last_name: str):
        self.page.get_by_role("textbox", name="Last Name").fill(last_name)

    def fill_employee_id(self, employee_id: str):
        self.page.get_by_role("textbox").nth(4).fill(employee_id)

    def save(self):
        self.page.get_by_role("button", name="Save").click()


    ## SEARCH EMPLOYEE
    # ================================

    def click_search(self):
        self.page.get_by_role("button", name="Search").click()

    def click_reset(self):
        self.page.get_by_role("button", name="Reset").click()

    def search_by_name(self, employee_name: str):
        self.page.get_by_placeholder("Type for hints...").fill(employee_name)

    def search_by_id(self, employee_id: str):
        self.page.get_by_role("textbox").nth(2).fill(employee_id)

    def search_by_job_title(self, job_title: str):
        self.page.get_by_text("-- Select --").nth(1).click()
        self.page.get_by_role("option", name= job_title).click() 
