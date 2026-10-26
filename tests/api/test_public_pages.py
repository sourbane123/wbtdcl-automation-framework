import pytest
import requests
from config import BASE_URL, HOME_URL, PACKAGES_URL

pytestmark = pytest.mark.api
HEADERS = {"User-Agent": "WBTDCL-QA-Learning-Project/1.0 (non-invasive smoke tests)"}

@pytest.mark.parametrize("url", [BASE_URL + "/", HOME_URL, PACKAGES_URL])
def test_public_page_http_response(url):
    """Smoke check only: public page responds and is not a server-error response."""
    response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
    assert response.status_code < 500, f"Server error {response.status_code} for {url}"
    assert response.url.startswith("https://"), "Unexpected non-HTTPS final URL"
    assert len(response.text) > 100, "Response body unexpectedly empty"

def test_home_page_contains_tourism_branding():
    response = requests.get(HOME_URL, headers=HEADERS, timeout=30)
    assert response.status_code == 200
    body = response.text.lower()
    assert "tourism" in body or "wbtdcl" in body

def test_invalid_path_is_handled_without_server_error():
    response = requests.get(BASE_URL + "/qa-automation-invalid-path-404-check", headers=HEADERS, timeout=30)
    assert response.status_code < 500, f"Unexpected server error for invalid path: {response.status_code}"
    # Do not require 404 because legacy PHP apps sometimes redirect or render a custom page.
