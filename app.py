import argparse
from typing import Any

from date_utils import generate_nearby_dates
from flight_service import search_flights


def print_flight(flight: dict[str, Any]) -> None:
    """
    Print one flight in readable format.
    """

    print(f"Date: {flight['date']}")
    print(f"Price: {flight['currency']} {flight['price']}")
    print(f"Airline: {flight['airline']}")
    print(f"Route: {flight['route']}")
    print(f"Stops: {flight['stops']}")
    print(f"Duration: {flight['duration']}")
    print(f"Booking link: {flight['booking_link']}")
    print(f"Source: {flight['source']}")


def show_results(all_flights: list[dict[str, Any]], selected_date: str) -> None:
    """
    Display cheapest exact-date flight, cheapest nearby-date flight,
    and top cheapest options.
    """

    if not all_flights:
        print("\nNo flights found.")
        print("Try a smaller date range first, for example --range 1.")
        print("Also test LetsFG directly: letsfg search BER MAA 2026-07-30 --mode fast")
        return

    all_flights = sorted(all_flights, key=lambda flight: flight["price"])

    exact_date_flights = [
        flight for flight in all_flights
        if flight["date"] == selected_date
    ]

    print("\n==============================")
    print("CHEAPEST EXACT DATE FLIGHT")
    print("==============================")

    if exact_date_flights:
        exact_cheapest = sorted(exact_date_flights, key=lambda flight: flight["price"])[0]
        print_flight(exact_cheapest)
    else:
        print("No flight found for the exact selected date.")

    print("\n==============================")
    print("CHEAPEST NEARBY DATE FLIGHT")
    print("==============================")

    cheapest_overall = all_flights[0]
    print_flight(cheapest_overall)

    print("\n==============================")
    print("TOP 10 CHEAPEST OPTIONS")
    print("==============================")

    for index, flight in enumerate(all_flights[:10], start=1):
        print(f"\n{index}.")
        print_flight(flight)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backend-only free flight finder using LetsFG local search."
    )

    parser.add_argument(
        "--from",
        dest="origin",
        required=True,
        help="Origin airport IATA code, for example: BER"
    )

    parser.add_argument(
        "--to",
        dest="destination",
        required=True,
        help="Destination airport IATA code, for example: MAA"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Departure date in YYYY-MM-DD format, for example: 2026-07-30"
    )

    parser.add_argument(
        "--range",
        dest="date_range",
        type=int,
        default=1,
        help="Nearby date range. Example: 3 means search 3 days before and 3 days after."
    )

    parser.add_argument(
        "--mode",
        default="fast",
        choices=["fast", "full"],
        help="LetsFG search mode. Use fast first. Full can take much longer."
    )

    parser.add_argument(
        "--max",
        dest="max_results",
        type=int,
        default=20,
        help="Maximum flight results per date."
    )

    args = parser.parse_args()

    dates = generate_nearby_dates(args.date, args.date_range)

    print("\nSearching flights using LetsFG local search...")
    print(f"From: {args.origin.upper()}")
    print(f"To: {args.destination.upper()}")
    print(f"Main date: {args.date}")
    print(f"Nearby range: ±{args.date_range} days")
    print(f"Mode: {args.mode}\n")

    all_flights = []

    for date in dates:
        print(f"Checking {date}...")

        flights = search_flights(
            origin=args.origin,
            destination=args.destination,
            departure_date=date,
            mode=args.mode,
            max_results=args.max_results
        )

        all_flights.extend(flights)

    show_results(all_flights, args.date)


if __name__ == "__main__":
    main()
