import httpx
from mcp.server.fastmcp import FastMCP

# Initializing FastMCP app
mcp = FastMCP("trip-app")

# Our API requests secret info and configuration
TRIP_API_TOKEN = "60A0A98ABE494CF58008BD1197447C25"
USER_AGENT = "trip-app/1.0"

# Base URL for TripAdvisor searches
BASE_URL = "https://api.content.tripadvisor.com/api/v1/location"


async def make_url_request(url: str) -> list[str] | None:
    """
        Helper function to perform API requests to TripAdvisor
    """
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def nearby_search(lat_long: str, category: str, radius: str, radius_unit: str) -> str:
    """
        The Nearby Location Search request returns up to 10 locations found near the given latitude/longtitude.
        You can use category ("hotels", "attractions", "restaurants", "geos"), phone number, address to search with more accuracy.
    Args:
        latLong: Latitude/Longitude pair to scope down the search around a specifc point - eg. "42.3455,-71.10767".
        category: Filters result set based on property type. Valid options are "hotels", "attractions", "restaurants", and "geos".
        radius: Length of the radius from the provided latitude/longitude pair to filter results.
        radiusUnit: Unit for length of the radius. Valid options are "km", "mi", "m" (km=kilometers, mi=miles, m=meters)
    """

    search_url = f"{BASE_URL}/nearby_search/?key={TRIP_API_TOKEN}&latLong={lat_long}&category={category}&radius={radius}&radiusUnit={radius_unit}&language=en"
    search_result = await make_url_request(search_url)
    return search_result

@mcp.tool()
async def locations_search(lat_long: str, search_query: str, category: str, radius: str, radius_unit: str) -> str:
    """
        The Location Search request returns up to 10 locations found by the given search query.
        You can use category ("hotels", "attractions", "restaurants", "geos"), phone number, address, and latitude/longtitude to search with more accuracy.
    Args:
        search_query: Text to use for searching based on the name of the location.
        lat_long: Latitude/Longitude pair to scope down the search around a specifc point - eg. "42.3455,-71.10767".
        category: Filters result set based on property type. Valid options are "hotels", "attractions", "restaurants", and "geos".
        radius: Length of the radius from the provided latitude/longitude pair to filter results.
        radius_unit: Unit for length of the radius. Valid options are "km", "mi", "m" (km=kilometers, mi=miles, m=meters)
    """

    search_url = f"{BASE_URL}/search/?key={TRIP_API_TOKEN}&searchQuery={search_query}&latLong={lat_long}&category={category}&radius={radius}&radiusUnit={radius_unit}&language=en"
    search_result = await make_url_request(search_url)
    return search_result

@mcp.tool()
async def location_details(location_id: str) -> str:
    """
        A Location Details request returns comprehensive information about a location (hotel, restaurant, or an attraction) such as name, address, rating, and URLs for the listing on Tripadvisor.
    Args:
        location_id: A unique identifier for a location on Tripadvisor. The location ID can be obtained using the Location Search or from previous search result (Path Param).
    """

    search_url = f"{BASE_URL}/{location_id}/details/?key={TRIP_API_TOKEN}"
    search_result = await make_url_request(search_url)
    return search_result

@mcp.tool()
async def location_reviews(location_id: str) -> str:
    """
        The Location Reviews request returns up to 5 of the most recent reviews for a specific location.
    Args:
        location_id: A unique identifier for a location on Tripadvisor. The location ID can be obtained using the Location Search or from previous search result (Path Param).
    """

    search_url = f"{BASE_URL}/{location_id}/reviews/?key={TRIP_API_TOKEN}"
    search_result = await make_url_request(search_url)
    return search_result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')