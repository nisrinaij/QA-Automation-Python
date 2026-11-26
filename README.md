# QA-Automation-Python
Quality Assurance automation framework using Playwright Python. Made to meet the requirements of Internship Reporting in FILKOM UB.


```text
QA-Automation-Python/
│
├── pages/
│   ├── base_page.py
│   ├── login.py
│   ├── master_data/
│   │   ├── sub_staff.py
│   │   ├── sub_plant.py
│   │   ├── sub_labour.py
│   │   ├── sub_support.py
│   │   ├── sub_cycle.py
│   │   └── sub_shift.py
│   │
│   ├── resource_chart/
│   │   └── resource_chart_page.py
│   │
│   └── reports/
│       └── report_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_master_data/
│   │   ├── test_staff.py
│   │   ├── test_plant.py
│   │   ├── test_labour.py
│   │   ├── test_support.py
│   │   ├── test_cycle.py
│   │   └── test_shift.py
│   │
│   ├── resource_chart/
│   │   └── test_resource_chart.py
│   │
│   └── reports/
│       └── test_report.py
│
├── reports/
│   ├── test_master_data/
│   │   └── screenshots/
│   │
│   ├── test_resource_chart/
│   │   └── screenshots/
│   │
│   ├── test_reports/
│   │   └── screenshots/
│   │
│   └── full_suite_test.html
│
├── .venv/
├── auth_state.py
├── config.py
├── conftest.py
├── requirements.txt
├── README.md
└── storageState.json
```