# WBTDCL UI + API Automation (Python, pytest, Selenium, POM, Excel)

A starter automation framework for the official West Bengal Tourism Development Corporation website:
https://wbtdcl.wbtourismgov.in/

## Important test-safety notes
- The website is a live public site. The suite does **not** submit a real booking, payment, OTP, or customer PII.
- UI booking flows are tested up to the booking form / validation stage. Any final submit is deliberately not performed.
- The site has no public API contract documented in this project. `tests/api/` therefore performs HTTP smoke and response checks on publicly accessible pages; it does not pretend to test private booking APIs.
- Website markup/locators can change. Inspect current DOM in browser DevTools and update page objects if needed. Tests use resilient locator fallbacks but should be validated locally before relying on CI.

## Stack
Python 3.11+, pytest, Selenium 4, webdriver-manager, openpyxl, requests, pytest-html, allure-pytest.

## Project tree
```
wbtdcl_automation_project/
├── config.py
├── requirements.txt
├── pytest.ini
├── conftest.py
├── data/test_data.xlsx
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── property_page.py
│   └── package_page.py
├── tests/
│   ├── ui/test_search_and_booking.py
│   └── api/test_public_pages.py
├── utils/excel_reader.py
├── .github/workflows/pytest.yml
├── Jenkinsfile
└── .gitignore
```

## 1. Setup locally
```bash
# Windows PowerShell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Install Chrome or Edge. Selenium Manager normally handles the driver automatically; `webdriver-manager` is included as a fallback dependency.

Run all tests:
```bash
pytest -v
```
Run UI tests:
```bash
pytest -v tests/ui
```
Run API smoke tests:
```bash
pytest -v tests/api
```
HTML report:
```bash
pytest -v --html=reports/pytest-report.html --self-contained-html
```
Allure results:
```bash
pytest -v --alluredir=allure-results
```

## 2. Data-driven test design
`data/test_data.xlsx` contains 20 rows. `TestCases` columns include `case_id`, `flow`, `scenario`, `destination`, `price_range`, `min_price`, `max_price`, `package_keyword`, `customer_name`, `mobile`, `email`, `expected`, `enabled`.
The Excel values are loaded during pytest collection and each row becomes a separately named test. Some negative cases validate input-data rules locally or assert that the site remains usable; they do not intentionally send malformed personal data to a live booking endpoint.

## 3. Current website navigation
The public home page currently exposes destination and price-range filters, property cards and a Packages section. Search values shown by the site include destinations such as Digha, Darjeeling, Sunderban and price bands such as `Upto Rs. 2000`, `Rs. 2001 - Rs. 3000`, etc. Package detail pages may require choosing a departure date and account/login steps. Use the UI in a normal browser to confirm current flows before enabling more intrusive tests.

## 4. GitHub: create and push
1. Sign in at https://github.com/ and select **New repository**.
2. Name it `wbtdcl-automation-project`; choose Public or Private; do not initialize with README (this folder already has one).
3. Extract this ZIP and open a terminal in the extracted folder.
4. Configure identity if needed:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
5. Initialize and push (replace `YOUR_USERNAME`):
```bash
git init
git add .
git commit -m "Initial WBTDCL pytest POM framework"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wbtdcl-automation-project.git
git push -u origin main
```
Never commit passwords, access tokens, real customer information, or `.env` files. If GitHub asks for authentication, use browser sign-in / a GitHub token or SSH; do not put a token in the remote URL.

## 5. GitHub Actions
The workflow is `.github/workflows/pytest.yml`. After pushing to `main`:
1. Open the repository on GitHub.
2. Select **Actions**.
3. Open **Pytest UI + API Tests** and inspect the run.
4. Download `pytest-report` and `allure-results` artifacts from a completed run.
The runner installs Chrome and dependencies. Live-site UI tests can fail if the site is down, rate-limits automation, or changes markup; this is not necessarily a framework defect.

## 6. Jenkins
1. Install Jenkins (LTS) and a supported Java version per the official Jenkins installation guide.
2. Ensure the Jenkins agent has Python 3.11+ and Google Chrome installed.
3. Install plugins: **Git**, **Pipeline**, and optionally **HTML Publisher** and **Allure Jenkins**.
4. Create a **New Item → Pipeline** job.
5. Select **Pipeline script from SCM**, SCM **Git**, enter your repository URL, branch `*/main`, Script Path `Jenkinsfile`.
6. Save and click **Build Now**.
The Jenkinsfile creates a venv, installs requirements, runs pytest, and archives reports. For a Windows agent, adapt shell commands (`sh`) to `bat`.

## 7. Allure report setup
Allure has two parts: `allure-pytest` writes result files, and the Allure command-line tool generates/opens the report.
1. Install Java (a supported JDK) and verify `java -version`.
2. Install Allure CLI using the official Allure documentation for your OS. Verify `allure --version`.
3. Generate results:
```bash
pytest --alluredir=allure-results
```
4. Build and open report:
```bash
allure serve allure-results
```
or generate a static report:
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```
Do not commit generated `allure-report/` unless you have a specific reason. The CI workflow uploads raw results; you can download them and run `allure serve` locally. Jenkins Allure plugin can publish results when configured to read `allure-results`.

## Suggested safe next steps
- First run `pytest tests/api -v` to check basic connectivity.
- Run one UI test and inspect screenshots/page source if a locator fails.
- Update selectors in `pages/` against the current DOM.
- Use a staging environment and approved test account before adding final booking submission or payment tests.
