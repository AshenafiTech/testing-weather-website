import pytest
from playwright.sync_api import sync_playwright
from tests.api_mocks import mock_weather_api_response
from tests.pagination_and_dynamic_content import pagination_and_dynamic_content

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch Chromium browser
        yield browser
        browser.close()

def test_weather_search(browser):
    context1 = browser.new_context()
    context2 = browser.new_context()

    # Mock the API response for "New York" in context1
    mock_weather_api_response(context1, "New York")

    # Mock the API response for "Addis Ababa" in context2
    mock_weather_api_response(context2, "Addis Ababa")

    # Use the first context to perform actions with city name "New York"
    page1 = context1.new_page()
    page1.goto('https://www.weather.com/', timeout=100000)
    page1.get_by_test_id("searchModalInputBox").fill("New York")
    page1.wait_for_selector('#LocationSearch_listbox')
    page1.click('#LocationSearch_listbox button:first-of-type')
    page1.wait_for_selector('.CurrentConditions--header--kbXKR h1')
    header_text = page1.locator('.CurrentConditions--header--kbXKR h1').inner_text()
    assert "New York".lower() in header_text.lower(), "City name not found in header text."
    page1.screenshot(path='screenshots/weather_results_context1.png', timeout=60000)
    page1.pdf(path='pdf_reports/weather_report_context1.pdf')

    # Handle pagination and dynamic content
    pagination_and_dynamic_content(page1)

    # Use the second context to perform actions with city name "Addis Ababa"
    page2 = context2.new_page()
    page2.goto('https://www.weather.com/', timeout=100000)
    page2.get_by_test_id("searchModalInputBox").fill("Addis Ababa")
    page2.wait_for_selector('#LocationSearch_listbox')
    page2.click('#LocationSearch_listbox button:first-of-type')
    page2.wait_for_selector('.CurrentConditions--header--kbXKR h1')
    header_text = page2.locator('.CurrentConditions--header--kbXKR h1').inner_text()
    assert "Addis Ababa".lower() in header_text.lower(), "City name not found in header text."
    page2.screenshot(path='screenshots/weather_results_context2.png', timeout=60000)
    page2.pdf(path='pdf_reports/weather_report_context2.pdf')

    # Close the contexts
    context1.close()
    context2.close()