import os
import time

from mozio_client import MozioClient

MOZIO_BASE_URL = os.getenv("MOZIO_BASE_URL")
MOZIO_API_KEY = os.getenv("MOZIO_API_KEY")


def main():
    search_parameters = {
        "start_address": "44 Tehama Street, San Francisco, CA, USA",
        "end_address": "SFO",
        "mode": "one_way",
        "pickup_datetime": "2024-12-01 15:30",
        "num_passengers": 2,
        "currency": "USD",
        "campaign": "Lucas Bastos de Assis",
    }

    client = MozioClient(MOZIO_BASE_URL, MOZIO_API_KEY)

    response = client.create_search(search_parameters)

    response.raise_for_status()

    search_id = response.json()["search_id"]

    results = []

    more_coming = True

    while more_coming:
        time.sleep(5)
        response = client.poll_search(search_id)
        results = results + response.json()["results"]
        more_coming = response.json()["more_coming"]

    quotes = []

    for quote in results:
        for step in quote["steps"]:
            if step["details"]["provider_name"] == "Dummy External Provider":
                quotes.append(quote)

    cheapest_quote = quotes[0]
    for quote in quotes[1:]:
        if float(quote["total_price"]["total_price"]["value"]) < float(
            cheapest_quote["total_price"]["total_price"]["value"]
        ):
            cheapest_quote = quote

    result_id = cheapest_quote["result_id"]

    response = client.create_reservation(
        {
            "search_id": search_id,
            "result_id": result_id,
            "email": "happytraveler@mozio.com",
            "country_code_name": "US",
            "phone_number": "8776665544",
            "first_name": "Happy",
            "last_name": "Traveler",
            "airline": "AA",
            "flight_number": "123",
            "customer_special_instructions": "My doorbell is broken, please yell",
        }
    )

    response.raise_for_status()

    status = response.json()["status"]

    while status == "pending":
        time.sleep(5)
        response = client.poll_reservation(search_id)
        response.raise_for_status()
        status = response.json()["reservations"]

    reservation = response.json()["reservations"][0]

    reservation_id = reservation["id"]

    print("Reservation ID: " + reservation_id)

    response = client.cancel_reservation(reservation_id)

    response.raise_for_status()


if __name__ == "__main__":
    main()
