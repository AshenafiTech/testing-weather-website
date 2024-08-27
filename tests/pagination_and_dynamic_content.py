def pagination_and_dynamic_content(page):
    tabs = ['Hourly', '10 Day', 'Weekend', 'Monthly']
    for tab in tabs:
        # Reload the home page before clicking on the tab
        page.goto('https://www.weather.com/', timeout=100000)

        # Click the tab
        tab_selector = f'a:has-text("{tab}")'
        page.click(tab_selector)

        # Wait for the content to load
        try:
            header_selector = 'h1.LocationPageTitle--PageHeader--JBu5- strong'
            page.wait_for_selector(header_selector, timeout=60000)
            print(f"Tab '{tab}' loaded successfully.")
        except TimeoutError:
            print(f"Tab '{tab}' failed to load.")
            page.screenshot(path=f'screenshots/error_{tab.lower().replace(" ", "_")}.png')
            continue

        # Verify the header content
        header_text = page.locator(header_selector).inner_text()
        assert tab.lower() in header_text.lower() and "weather" in header_text.lower(), f"Tab '{tab}' content not found."

        # Take a screenshot for each tab
        page.screenshot(path=f'screenshots/weather_{tab.lower().replace(" ", "_")}.png')