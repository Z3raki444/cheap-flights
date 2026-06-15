import json
import subprocess
from typing import Any


def _extract_price(value: Any) -> float | None:
    """
    Try to convert different possible price formats into float.
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        cleaned = (
            value.replace("€", "")
            .replace("$", "")
            .replace("₹", "")
            .replace(",", "")
            .strip()
        )

        try:
            return float(cleaned)
        except ValueError:
            return None

    return None


def _normalize_offer(offer: dict[str, Any], departure_date: str) -> dict[str, Any] | None:
    """
    LetsFG output may change depending on version.
    This function tries to normalize common JSON fields.
    """

    price = (
        _extract_price(offer.get("price"))
        or _extract_price(offer.get("amount"))
        or _extract_price(offer.get("total"))
        or _extract_price(offer.get("fare"))
    )

    if price is None:
        return None

    currency = (
        offer.get("currency")
        or offer.get("currency_code")
        or offer.get("price_currency")
        or "EUR"
    )

    airlines = offer.get("airlines") or offer.get("airline") or offer.get("carrier") or "N/A"

    if isinstance(airlines, list):
        airline_text = ", ".join(str(a) for a in airlines)
    else:
        airline_text = str(airlines)

    route = offer.get("route") or offer.get("itinerary") or "N/A"

    if isinstance(route, list):
        route_text = " → ".join(str(r) for r in route)
    else:
        route_text = str(route)

    stops = offer.get("stops", offer.get("stopovers", "N/A"))
    duration = offer.get("duration", "N/A")

    booking_link = (
        offer.get("booking_link")
        or offer.get("bookingLink")
        or offer.get("url")
        or offer.get("deep_link")
        or "N/A"
    )

    return {
        "date": departure_date,
        "price": price,
        "currency": currency,
        "airline": airline_text,
        "route": route_text,
        "stops": stops,
        "duration": duration,
        "booking_link": booking_link,
        "source": "LetsFG local"
    }


def _extract_offers_from_json(data: Any) -> list[dict[str, Any]]:
    """
    LetsFG JSON can be either:
    - a list of offers
    - a dictionary with offers/results/flights
    This keeps the program flexible.
    """

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ["offers", "results", "flights", "data"]:
            value = data.get(key)
            if isinstance(value, list):
                return value

    return []


def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    mode: str = "fast",
    max_results: int = 20
) -> list[dict[str, Any]]:
    """
    Search flights using LetsFG local CLI.

    This does not use Amadeus.
    This does not require an API key.

    Example command used internally:
        letsfg search BER MAA 2026-07-30 --mode fast --sort price --json
    """

    command = [
        "letsfg",
        "search",
        origin.upper(),
        destination.upper(),
        departure_date,
        "--mode",
        mode,
        "--sort",
        "price",
        "--json"
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=180
        )

        if completed.returncode != 0:
            print(f"LetsFG error for {departure_date}:")
            print(completed.stderr.strip() or completed.stdout.strip())
            return []

        output = completed.stdout.strip()

        if not output:
            print(f"No output returned for {departure_date}")
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            print(f"Could not parse JSON for {departure_date}. Raw output:")
            print(output[:1000])
            return []

        raw_offers = _extract_offers_from_json(data)

        flights = []

        for offer in raw_offers[:max_results]:
            if isinstance(offer, dict):
                normalized = _normalize_offer(offer, departure_date)
                if normalized:
                    flights.append(normalized)

        return flights

    except FileNotFoundError:
        print("LetsFG is not installed or not available in PATH.")
        print("Run: pip install letsfg")
        return []

    except subprocess.TimeoutExpired:
        print(f"Search timed out for {departure_date}. Try --mode fast or smaller --range.")
        return []
