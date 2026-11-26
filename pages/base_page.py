import re
import openpyxl
from playwright.sync_api import Page, Locator
from openpyxl import load_workbook


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

    def read_ui_table(table: Locator) -> list[dict]:
        """
        Extract data from an HTML table using Playwright.

        Args:
            table: Playwright Locator pointing to the table element.

        Returns:
            List of dictionaries containing table data.
        """

        # Get all table rows
        rows = table.locator("tr").all()

        if not rows:
            return []

        # Find headers
        header_locator = table.locator("thead th")
        headers = header_locator.all_inner_texts()

        # Fallback: use the first row as headers
        if not headers:
            headers = rows[0].locator("th, td").all_inner_texts()
            data_rows = rows[1:]
        else:
            data_rows = table.locator("tbody tr").all()

        # Clean header values
        headers = [header.strip() for header in headers]

        # Handle duplicate or empty headers
        seen = {}
        unique_headers = []

        for index, header in enumerate(headers):
            header = header or f"column_{index + 1}"

            if header in seen:
                seen[header] += 1
                header = f"{header}_{seen[header]}"
            else:
                seen[header] = 1

            unique_headers.append(header)

        # Extract row data
        table_data = []

        for row in data_rows:
            cells = row.locator("th, td").all_inner_texts()

            values = [cell.strip() for cell in cells]

            row_data = {
                header: values[index] if index < len(values) else ""
                for index, header in enumerate(unique_headers)
            }

            table_data.append(row_data)

        return table_data


    def read_excel(file_path: str, sheet_name=0) -> list[dict]:
        """
        Read Excel data and convert it into a list of dictionaries.

        Args:
            file_path: Path to the Excel file.
            sheet_name: Worksheet name or index (default: 0).

        Returns:
            List of dictionaries containing Excel data.
        """

        workbook = load_workbook(
            filename=file_path,
            data_only=True,
            read_only=True
        )

        try:
            # Select worksheet
            if isinstance(sheet_name, int):
                worksheet = workbook.worksheets[sheet_name]
            else:
                worksheet = workbook[sheet_name]

            rows = list(worksheet.iter_rows(values_only=True))

            # Find first non-empty row as headers
            header_index = next(
                (
                    index for index, row in enumerate(rows)
                    if any(value is not None for value in row)
                ),
                None
            )

            if header_index is None:
                return []

            headers = list(rows[header_index])

            # Clean and normalize headers
            seen = {}
            unique_headers = []

            for index, header in enumerate(headers):
                header = str(header).strip() if header is not None else ""
                header = header or f"column_{index + 1}"

                if header in seen:
                    seen[header] += 1
                    header = f"{header}_{seen[header]}"
                else:
                    seen[header] = 1

                unique_headers.append(header)

            # Extract data
            excel_data = []

            for row in rows[header_index + 1:]:
                if not any(value is not None for value in row):
                    continue

                row_data = {
                    header: row[index] if index < len(row) else None
                    for index, header in enumerate(unique_headers)
                }

                excel_data.append(row_data)

            return excel_data

        finally:
            workbook.close()
