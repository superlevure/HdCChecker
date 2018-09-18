from pprint import pprint
import trio
import asks
from bs4 import BeautifulSoup

from lib import print_c, conf


async def check_hotel(trip):
    hotel_url = f"https://fr.hotels.com/{trip['hotel_id']}/?q-check-out={trip['check-out']}&q-check-in={trip['check-in']}&q-room-0-children={trip['children']}&q-room-0-adults={trip['adults']}"
    print_c(f'Fetching price for "{trip["hotel"]}" ({hotel_url})', "run")
    html = await asks.get(hotel_url)
    soup = BeautifulSoup(html.content, "html.parser")
    room = soup.find(
        "h3", string=trip["room"], attrs={"class": "room-name additional-room-info-cta"}
    )

    try:
        room_price = (
            room.parent.parent.find_all("li", attrs={"class": "rateplan"})[
                trip["option"] - 1
            ]
            .find("strong", attrs={"class": "current-price"})
            .string
        )
    except IndexError:
        print("Error:")
        print(room.parent.parent)
        print()
    else:
        print_c(
            f'Hotel "{trip["hotel"]}": room "{trip["room"]}" (option {trip["option"]}) price is {room_price} ',
            "good",
        )
    # 1. Find data-index of room (<li>) from h3
    # 2. in <div class="rateplans"> [option - 1] : <strong class="current-price">250 €</strong>


async def main():
    print(
        """
                 _       _         _       _     ___                  ___ _               _             
      /\  /\___ | |_ ___| |___  __| | ___ | |_  / __\___  _ __ ___   / __\ |__   ___  ___| | _____ _ __ 
     / /_/ / _ \| __/ _ \ / __|/ _` |/ _ \| __|/ /  / _ \| '_ ` _ \ / /  | '_ \ / _ \/ __| |/ / _ \ '__|
    / __  / (_) | ||  __/ \__ \ (_| | (_) | |_/ /__| (_) | | | | | / /___| | | |  __/ (__|   <  __/ |   
    \033[31m\/ /_/ \___/ \__\___|_|___/\__,_|\___/ \__\____/\___/|_| |_| |_\____/|_| |_|\___|\___|_|\_\___|_|\033[0m   


    """
    )

    hotel_count = len(conf["trips"])
    print_c(f"{hotel_count} hotel(s) found in configuration file.")

    async with trio.open_nursery() as nursery:
        for trip in conf["trips"]:
            nursery.start_soon(check_hotel, trip)


if __name__ == "__main__":
    try:
        asks.init("trio")
        trio.run(main)
    except KeyboardInterrupt:
        print("\nBye bye.\n")

