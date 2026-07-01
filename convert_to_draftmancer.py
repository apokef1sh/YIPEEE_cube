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
file = open(filepath, errors="ignore")
filetext = file.read()
cards = []
for new_card in filetext.split("<card>")[1:]:
    print("new card")
    card = Card()
    card.name = new_card.split("<name>")[1].split("</name>")[0].replace("&apos;", "")
    if "<manacost>" in new_card:
        card.manacost = new_card.split("<manacost>")[1].split("</manacost>")[0]
    card.type = new_card.split("<type>")[1].split("</type>")[0].replace(" //", "")
    card.oracle_text = new_card.split("<text>")[1].split("</text>")[0]
    if "<pt>" in new_card:
        card.pt = new_card.split("<pt>")[1].split("</pt>")[0]
    print(card)
    cards.append(card)
fulltext = """[Settings]
{
    "name": "room test",
    "colorBalance": false,
    "cardBack": "https://lh3.googleusercontent.com/d/1p6BQ9NAWpVMY8vPDJjhU2kvC98-P9joA"
}
[CustomCards]
[\n"""
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
    if "Room" in card.type:
        layout = f"""
        "layout": "split","""
    else:
        layout = ""
    oracletext = card.oracle_text.replace("\n", "\\n")
    fulltext = fulltext+f"""
    {{
        "id": "{uuid.uuid4()}",
        "name": "{card.name}",
        "mana_cost": "{card.manacost}",
        "type": "{card.type}",
        "image": "https://raw.githubusercontent.com/apokef1sh/YIPEEE_cube/main/Images/{card.name.replace(" ", "%20").replace(",", "")}.png",
        "colors": [
            "{colortext}"
        ],
        "set": "YPE",{layout}
        "oracle_text": \"{oracletext}\"{pt}
    }}"""
    if not cards[len(cards)-1] == card:
        fulltext = fulltext + ","
    print(fulltext)
fulltext = fulltext + """\n]
[MainSlot]\n"""
for card in cards:
    if "Token" not in card.type:
        fulltext = fulltext +f"4 {card.name}\n"
print(fulltext)
with open("draftmanceroutput.txt", "w", encoding="utf-8") as draftmancerfile:
    draftmancerfile.write(fulltext)
    pass
input("here you can copy it now")