# Selenium Assignments - Magnus Application (JALA Academy)

Selenium WebDriver automation for https://magnus.jalatechnologies.com, written in **Python** with **pytest** (the Python equivalent of TestNG). Prepared by Sahithi Dasari.

## Folders
| Folder | What it contains |
|---|---|
| `docs/Magnus_Test_Cases.xlsx` | Test scenarios (12), test cases (50), defects (7) and a summary sheet |
| `exercises/` | One script per assignment PDF: locators, web elements, WebDriver methods, popups/windows, miscellaneous scenarios |
| `framework/` | Page Object Model framework: config file, locators file, page classes, BaseTest (conftest.py), Excel data, logging, HTML report, 40+ tests |
| `explore_magnus.py` | Script used to explore the application pages |

## Setup
```
pip install -r requirements.txt
```
Chrome must be installed. Selenium downloads the matching driver automatically.

## Run the exercise scripts
```
cd exercises
python ex1_locators.py
python ex2_web_elements.py
python ex3_webdriver_methods.py
python ex4_popups_windows.py
python ex5_misc_scenarios.py
```

## Run the framework
```
cd framework
pytest                                   # all tests, HTML report in reports/report.html
pytest tests/test_login.py               # one module (like one TestNG suite)
pytest -m smoke                          # one group
pytest --browser firefox                 # another browser
pytest -n 3                              # run in parallel
pytest tests/test_testng_features.py -s  # TestNG features shown in pytest (no browser)
```

## Framework features (from "Selenium Framework Steps")
- Web elements kept in `config/locators.ini`, constants in `config/config.ini`
- Page classes in `pages/` (PageObjects + PageActions), `conftest.py` acts as the BaseTest
- Groups (`-m smoke`), priority (`@pytest.mark.order`), dependency (`@pytest.mark.depends_on`), skip, repeat
- Data-driven tests from Excel (`data/test_data.xlsx`) and `@pytest.mark.parametrize` (DataProvider)
- Logging to `logs/test_run.log`, screenshot on failure, HTML report (like Extent Reports)
- Chrome, Firefox and Edge support

## Note
The Change Password tests only check validation messages. They never submit a real password change, because the training account is shared.
