from .database import get_shipment, search_shipments


def lookup_shipment(tracking_id: str) -> dict:
    shipment = get_shipment(tracking_id)
    if not shipment:
        return {"found": False, "tracking_id": tracking_id}
    return {"found": True, **shipment}


def delay_risk(tracking_id: str) -> dict:
    shipment = get_shipment(tracking_id)
    if not shipment:
        return {"found": False, "tracking_id": tracking_id}
    hours = shipment["delay_hours"]
    risk = "high" if hours >= 4 else "medium" if hours >= 2 else "low"
    return {"tracking_id": tracking_id, "risk": risk, "delay_hours": hours, "status": shipment["status"]}


def search_routes(query: str) -> dict:
    return {"query": query, "results": search_shipments(query)}

TOOLS = {
    "lookup_shipment": lookup_shipment,
    "delay_risk": delay_risk,
    "search_routes": search_routes,
}
