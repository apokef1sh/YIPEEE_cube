import uuid
class Card:
    def __init__(self):
        self.name = ""
        self.manacost = ""
        self.type = ""
        self.subtypes = ""
        self.oracle_text = ""
        self.pt = ""

    def __str__(self):
        return f"name: {card.name}, manacost: {card.manacost}, type: {card.type}, subtypes: {card.subtypes}, oracle text: {card.oracle_text}"

print("Input location of XML file")
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
    types = new_card.split("<type>")[1].split("</type>")[0].replace(" //", "").split()
    if ("-" in types):
        card.type = " ".join(types[:(types.index("-"))])
        card.subtypes = " ".join(types[(types.index("-")+1):])
    else:
        card.type = " ".join(types)
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
    if "Room" in card.subtypes:
        layout = f"""
        "layout": "split","""
    else:
        layout = ""
    oracletext = card.oracle_text.replace("\n", "\\n")
    subtype_text = ""
    if card.subtypes != "":
        subtype_text = "\n        \"subtypes\": ["
        for subtype in card.subtypes.split():
            subtype_text = subtype_text + f"\n             \"{subtype}\""
            if subtype != card.subtypes.split()[len(card.subtypes.split())-1]:
                subtype_text = subtype_text + ","
        subtype_text = subtype_text + "\n        ],"
    fulltext = fulltext+f"""
    {{
        "id": "{uuid.uuid4()}",
        "name": "{card.name}",
        "mana_cost": "{card.manacost}",
        "type": "{card.type}",{subtype_text}
        "image": "https://raw.githubusercontent.com/apokef1sh/YIPEEE_cube/main/Images/{card.name.replace(" ", "%20").replace(",", "")}.png",
        "colors": [
            "{colortext}"
        ],
        "set": "YPE",{layout}
        "oracle_text": \"{oracletext}\"{pt}
    }}"""
    if not cards[len(cards)-1] == card:
        fulltext = fulltext + ","
fulltext = fulltext + """\n]
[MainSlot]\n"""
for card in cards:
    if "Token" not in card.type:
        fulltext = fulltext +f"4 {card.name}\n"
# print(fulltext)
with open("draftmanceroutput.txt", "w", encoding="utf-8") as draftmancerfile:
    draftmancerfile.write(fulltext)
    pass
input("here you can copy it now")