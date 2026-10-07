from httpx2._client import USER_AGENT
from typing import Any
import httpx2
from mcp.server.fastmcp import FastMCP

# initializing FastMCP Server
mcp = FastMCP("weather")

# constants 
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url : str) -> dict[str, Any]:
    """Make a GET request to NWS API with proper headers and error handling"""
    headers = {
        "User-Agent" : USER_AGENT,
        "Accept" : "application/geo+json"
    }
    # with is used to work with resources safely—especially files. It automatically handles cleanup when you're done.
    async with httpx2.AsyncClient() as client:
        try:
            response = await client.get(url , headers = headers , timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature : dict) -> str:
    """Format an alert feature into readable string."""
    props = feature['properties']
    return f"""
        Event : {props.get('event' , 'Unknown')}     
        Area : {props.get('area' , 'Unkknown')}
        Severity : {props.get('severity' , 'Unknown')}
        Description : {props.get('description' , 'No Description available')}
        Instruction : {props.get('instruction' , 'No instruction available')}
        """


@mcp.tool()
async def get_alerts(state : str) -> str:
    """Get weather alerts for a US State.

    Args : 
        state : Two-letter US state code (e.g. CA , NY , FL)        
     """
    
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data['features']:
        return "No active weather alerts for this state."

    alerts = [format_alert(feature) for feature in data['features']]
    return "\n---\n".join(alerts)

@mcp.resource("echo://{message}")
def echo_resource(message : str)->str:
    """Echo a message as a resource"""
    return f"Resource code :{message}"

@mcp.prompt()
def review_code(code: str) -> str:
    """Review a piece of code."""
    return f"Please review this code:\n\n{code}"