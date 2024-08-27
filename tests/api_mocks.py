# api_mocks.py

def mock_weather_api_response(context, city):
    """Mock the API response based on the city name."""
    if city.lower() == "new york":
        context.route('**/v3/wx/forecast/*', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"weather": "sunny", "temperature": "75°F", "city": "New York"}'
        ))
    elif city.lower() == "addis ababa":
        context.route('**/v3/wx/forecast/*', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"weather": "rainy", "temperature": "60°F", "city": "Addis Ababa"}'
        ))
