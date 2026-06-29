import uuid
class Card:
    def __init__(self):
        self.name = ""
        self.manacost = ""
        self.type = ""
        self.oracle_text = ""
        self.pt = ""

    def __str__(self):
        return f"name: {card.name}, manacost: {card.manacost}, type: {card.type}, oracle text: {card.oracle_text}"


filepath = input(">").replace("\"", "")
file = open(filepath)
filetext = file.read()
cards = []
print(filetext.split("<card>"))
for new_card in filetext.split("<card>")[1:]:
    print("new card")
    card = Card()
    card.name = new_card.split("<name>")[1].split("</name>")[0]
    if "<manacost>" in new_card:
        card.manacost = new_card.split("<manacost>")[1].split("</manacost>")[0]
    card.type = new_card.split("<type>")[1].split("</type>")[0].replace(" //", "")
    card.oracle_text = new_card.split("<text>")[1].split("</text>")[0]
    if "<pt>" in new_card:
        card.pt = new_card.split("<pt>")[1].split("</pt>")[0]
    print(card)
    cards.append(card)
fulltext = ""
for card in cards:
    colors = []
    colors = list(dict.fromkeys([color for color in card.manacost if (not color.isdigit() and color not in ["/", " "])]))
    colortext = "\",\n            \"".join(colors)
    if card.pt != "":
        pt = f""",
        "power": "{card.pt.split("/")[0]}",
        "toughness": \"{card.pt.split("/")[1]}\""""
    else:
        pt = ""
    fulltext = fulltext+f"""
    {{
        "id": "{uuid.uuid4()}",
        "name": "{card.name.replace("&apos;", "'")}",
        "mana_cost": "{card.manacost}",
        "type": "{card.type}",
        "image": "https://raw.githubusercontent.com/apokef1sh/YIPEEE_cube/main/Images/{card.name.replace(" ", "%20").replace(",", "").replace("&apos;", "")}.png",
        "colors": [
            "{colortext}"
        ],
        "set": "YPE",
        "oracle_text": "{card.oracle_text.replace("\n", "\\n")}"{pt}
    }},"""
    print(fulltext)
with open("draftmanceroutput.txt", "w", encoding="utf-8") as draftmancerfile:
    draftmancerfile.write(fulltext)
    pass
for card in cards:
    print(f"2 {card.name}")