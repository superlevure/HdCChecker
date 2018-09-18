from pprint import pprint
from bs4 import BeautifulSoup

with open("example.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# print(soup.find_all("ul", attrs={"class": "rooms"}))
room = soup.find("h3", string="Chambre Privilège")
# pprint(room.parent.parent.find_all("li"))
# print(room.parent.parent["data-index"])
# print(room.parent.parent.find_all("li", attrs={"class": "rateplan"}))
# print(room.parent.parent.find("li", attrs={"class": "room"}))


room_price = (
    room.parent.parent.find_all("li", attrs={"class": "rateplan"})[1 - 1]
    .find("strong", attrs={"class": "current-price"})
    .string
)

print(room_price)
# <li class="room" data-index="0">
