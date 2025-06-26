# from typing import Any
# import httpx
# from mcp.server.fastmcp import FastMCP

# # Initialize FastMCP server
# mcp = FastMCP("weather")

# # Constants
# NWS_API_BASE = "https://api.weather.gov"
# USER_AGENT = "weather-app/1.0"

# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None

# def format_alert(feature: dict) -> str:
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """

# @mcp.tool()
# async def get_alerts(state: str) -> str:
#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_nws_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return "No active alerts for this state."

#     alerts = [format_alert(feature) for feature in data["features"]]
#     return "\n---\n".join(alerts)

# @mcp.tool()
# async def get_forecast(latitude: float, longitude: float) -> str:

#     # First get the forecast grid endpoint
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)

#     if not points_data:
#         return "Unable to fetch forecast data for this location."

#     # Get the forecast URL from the points response
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_nws_request(forecast_url)

#     if not forecast_data:
#         return "Unable to fetch detailed forecast."

#     # Format the periods into a readable forecast
#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecast = f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """
#         forecasts.append(forecast)

#     return "\n---\n".join(forecasts)

# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='sse')






# from typing import Any
# import httpx
# from mcp.server.fastmcp import FastMCP

# # Initialize FastMCP server
# mcp = FastMCP("weather")

# # Constants
# NWS_API_BASE = "https://api.weather.gov"
# UK_API_BASE = "https://www.metoffice.gov.uk"
# INDIA_API_BASE = "https://api.openweathermap.org"
# USER_AGENT = "weather-app/1.0"

# async def make_request(url: str, headers: dict = None, params: dict = None) -> dict[str, Any] | None:
#     default_headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/json"
#     }
#     if headers:
#         default_headers.update(headers)
    
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=default_headers, params=params, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             print(f"Error making request: {e}")
#             return None

# # US Region Tools (using NWS API)
# @mcp.tool()
# async def get_us_alerts(state: str) -> str:
#     """Get active weather alerts for a US state. Input should be a valid 2-letter state code like 'NY' or 'CA'."""
#     print(" US Region Tool")
#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return f"No active alerts for {state}."

#     alerts = [format_alert(feature) for feature in data["features"]]
#     return "\n---\n".join(alerts)

# @mcp.tool()
# async def get_us_forecast(latitude: float, longitude: float) -> str:
#     """Get weather forecast for a location in the US. Input should be latitude and longitude coordinates."""
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_request(points_url)

#     if not points_data:
#         return "Unable to fetch forecast data for this location."

#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_request(forecast_url)

#     if not forecast_data:
#         return "Unable to fetch detailed forecast."

#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecasts.append(format_us_forecast(period))

#     return "\n---\n".join(forecasts)

# # UK Region Tools (using Met Office API - you'll need an API key)
# @mcp.tool()
# async def get_uk_forecast(location: str) -> str:
#     """Get weather forecast for a location in the UK. Input should be a UK town or city name."""
#     # Note: You'll need to register for Met Office API and add your key to environment variables
#     print(" UK Region Tool")
#     params = {
#         "q": location,
#         "appid": "your_met_office_api_key"  # Should be from environment variables
#     }
#     url = f"{NWS_API_BASE}/public/data/val/wxfcs/all/json/{location}"
#     data = await make_request(url, params=params)

#     if not data:
#         return "Unable to fetch UK weather data."

#     # Process UK specific data format
#     return format_uk_forecast(data)

# # India Region Tools (using OpenWeatherMap API - you'll need an API key)
# @mcp.tool()
# async def get_india_forecast(city: str) -> str:
#     """Get weather forecast for a city in India. Input should be an Indian city name like 'Mumbai' or 'Kolkata'."""
#     params = {
#         "q": f"{city},IN",
#         "appid": "your_openweather_api_key",  # Should be from environment variables
#         "units": "metric"
#     }
#     print(" Indian Region Tool")
#     url = f"{INDIA_API_BASE}/data/2.5/weather"
#     data = await make_request(url, params=params)

#     if not data:
#         return "Unable to fetch India weather data."

#     return format_india_forecast(data)

# # Helper functions for formatting responses
# def format_alert(feature: dict) -> str:
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """

# def format_us_forecast(period: dict) -> str:
#     return f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """

# def format_uk_forecast(data: dict) -> str:
#     # Example formatting - adjust based on actual API response
#     return f"""
# UK Weather Forecast:
# Location: {data.get('name', 'Unknown')}
# Temperature: {data['main']['temp']}°C
# Conditions: {data['weather'][0]['description']}
# Humidity: {data['main']['humidity']}%
# Wind: {data['wind']['speed']} m/s
# """

# def format_india_forecast(data: dict) -> str:
#     # Example formatting for India
#     return f"""
# India Weather Forecast:
# City: {data.get('name', 'Unknown')}
# Temperature: {data['main']['temp']}°C
# Feels Like: {data['main']['feels_like']}°C
# Conditions: {data['weather'][0]['description']}
# Humidity: {data['main']['humidity']}%
# Wind: {data['wind']['speed']} m/s
# """

# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='sse')










from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"  # No-key US weather API
WTTR_API_BASE = "https://wttr.in"        # No-key global weather
USER_AGENT = "weather-app/1.0"

async def make_request(url: str, headers: dict = None) -> dict[str, Any] | None:
    default_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    if headers:
        default_headers.update(headers)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=default_headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request to {url}: {e}")
            return None

# ================= US WEATHER TOOLS =================
# @mcp.tool( description="Get weather forecast for US by passing state as a string parameter (e.g., 'CA', 'TX', 'NY' ). ")
# async def get_NA_alerts(state: str) -> str:

#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return f"No active alerts for {state}."

#     alerts = []
#     for feature in data["features"][:3]:  # Limit to 3 most recent alerts
#         props = feature["properties"]
#         alerts.append(
#             f"""🚨 {props.get('event','Unknown')} ({props.get('severity','Unknown')})
# 📍 {props.get('areaDesc','Unknown')}
# 📝 {props.get('headline','No details')}
# """
#         )
#     return "\n".join(alerts) if alerts else "No active alerts"

@mcp.tool()
async def get_NA_forecast(city: str) -> str:
    """Get weather forecast for US by passing state as a string parameter (e.g., 'CA', 'TX', 'NY' )."""
    print(" #################### US Region Tool ####################")
    url = f"{WTTR_API_BASE}/{city},US?format=j1"
    data = await make_request(url)
    
    if not data:
        return f"Unable to get weather for {city}, US"
    
    current = data['current_condition'][0]
    return f"""
🌍 {city}, US
🌡 Temperature: {current['temp_C']}°C (Feels {current['FeelsLikeC']}°C)
☁ Conditions: {current['weatherDesc'][0]['value']}
💧 Humidity: {current['humidity']}%
🌬 Wind: {current['windspeedKmph']} km/h ({current['winddir16Point']})
"""

# @mcp.tool( description="Get weather forecast for US by passing state as a string parameter (e.g., 'CA', 'TX', 'NY' ). ")
# async def get_NA_forecast(latitude: float, longitude: float) -> str:
#     # Step 1: Get grid points
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_request(points_url)
#     if not points_data:
#         return "Unable to get location data."

#     # Step 2: Get forecast
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_request(forecast_url)
#     if not forecast_data:
#         return "Unable to get forecast data."

#     # Format response
#     periods = forecast_data["properties"]["periods"][:4]  # Next 2 days (day/night)
#     forecast = []
#     for period in periods:
#         forecast.append(
#             f"""📅 {period['name']}
# 🌡 {period['temperature']}°{period['temperatureUnit']} 
# 🌬 {period['windSpeed']} {period['windDirection']}
# 📋 {period['shortForecast']}
# """
#         )
#     return "\n".join(forecast)


# ================= UK WEATHER TOOLS =================
@mcp.tool()
async def get_uk_forecast(city: str) -> str:
    """Get current weather for UK cities (e.g., 'London' or 'Edinburgh')."""
    url = f"{WTTR_API_BASE}/{city},UK?format=j1"
    data = await make_request(url)
    
    if not data:
        return f"Unable to get weather for {city}, UK"
    
    current = data['current_condition'][0]
    return f"""
🌍 {city}, UK
🌡 Temperature: {current['temp_C']}°C (Feels {current['FeelsLikeC']}°C)
☁ Conditions: {current['weatherDesc'][0]['value']}
💧 Humidity: {current['humidity']}%
🌬 Wind: {current['windspeedKmph']} km/h ({current['winddir16Point']})
"""

# ================= INDIA WEATHER TOOLS =================
@mcp.tool()
async def get_india_forecast(city: str) -> str:
    """Get current weather for Indian cities (e.g., 'Mumbai' or 'Delhi')."""
    print(" #################### Indian Region Tool ####################")
    url = f"{WTTR_API_BASE}/{city},India?format=j1"
    data = await make_request(url)
    
    if not data:
        return f"Unable to get weather for {city}, India"
    
    current = data['current_condition'][0]
    return f"""
🌍 {city}, India
🌡 Temperature: {current['temp_C']}°C (Feels {current['FeelsLikeC']}°C)
☁ Conditions: {current['weatherDesc'][0]['value']}
💧 Humidity: {current['humidity']}%
🌬 Wind: {current['windspeedKmph']} km/h ({current['winddir16Point']})
"""

if __name__ == "__main__":
    print("Starting weather server...")
    mcp.run(transport='sse')