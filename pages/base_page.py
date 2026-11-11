from playwright.sync_api import Page, Locator
import re

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def get_row_by_text(self, unique_text: str, row_selector: str = ".oxd-table-card, .oxd-table-row, .oxd-grid-item") -> Locator:
        """
        Locates a row or card based on a dynamic text value (e.g., an ID).
        
        :param unique_text: The dynamic text/ID to search for in the row.
        :param row_selector: The CSS selector for the row/card wrapper. Defaults cover standard OrangeHRM tables/grids.
        """
        # Using a regex word boundary (\b) ensures we match the exact string.
        # This prevents searching for "222" and accidentally grabbing "1222".
        exact_match_pattern = re.compile(rf"\b{unique_text}\b")
        
        return self.page.locator(row_selector).filter(has_text=exact_match_pattern)