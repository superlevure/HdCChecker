"""
HoteldotComChecker 
"""
from socket import gaierror
import sys

import trio
import asks
from bs4 import BeautifulSoup

from lib import print_c, conf


async def check_hotel(trip):
    hotel_url = (
        f"https://fr.hotels.com/{trip['hotel_id']}/?"
        + f"q-check-out={trip['check-out']}"
        + f"&q-check-in={trip['check-in']}"
        + f"&q-room-0-children={trip['children']}"
        + f"&q-room-0-adults={trip['adults']}"
    )
    print_c(f'Fetching price for "{trip["hotel"]}" ({hotel_url})', "run")
    try:
        html = await asks.get(hotel_url)
    except gaierror:
        print_c("Please check internet connection.", "bad")
    else:

        soup = BeautifulSoup(html.content, "html.parser")
        room = soup.find("h3", string=trip["room"])

        for parent in room.parents:
            if parent.name == "li":

                try:
                    room_price = (
                        parent.find_all("", attrs={"class": "rateplan"})[
                            trip["option"] - 1
                        ]
                        .find("", attrs={"class": "current-price"})
                        .string
                    )
                except IndexError:
                    print_c("Room not found.", "bad")
                break

        room_price, room_price_currency = room_price.split(" ")
        room_price = int(room_price)
        print_c(
            f'Hotel "{trip["hotel"]}": room "{trip["room"]}" (option {trip["option"]}) price is {room_price} {room_price_currency}',
            "info",
        )

        if room_price == trip["price"]:
            print_c("Room price hasn't changed", "good")
        elif room_price > trip["price"]:
            print_c("Room price is higher now", "good")
        else:
            print_c("Room price is cheaper, time to get some money back !", "bad")
            try:
                await asks.post(
                    "https://maker.ifttt.com/trigger/HdCChecker_price_down/with/key/"
                    + conf["ifttt_key"],
                    json={
                        "value1": trip["hotel"],
                        "value2": trip["price"] - room_price,
                        "value3": room_price_currency,
                    },
                )
            except gaierror:
                print_c("Please check internet connection.", "bad")


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
    print_c(
        f"{hotel_count} hotel{'s' if hotel_count > 1 else ''} found in configuration file."
    )

    async with trio.open_nursery() as nursery:
        for trip in conf["trips"]:
            nursery.start_soon(check_hotel, trip)


if __name__ == "__main__":
    try:
        asks.init("trio")
        trio.run(main)
    except KeyboardInterrupt:
        print("\nBye bye.\n")

