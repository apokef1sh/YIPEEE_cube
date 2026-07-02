import json

class Card:
    def __init__(self):
        self.name = ""
        self.manacost = ""
        self.maintype = ""
        self.type = ""
        self.oracle_text = ""
        self.pt = ""
        self.side = "front"
        self.colors = ""
        self.image = ""
        self.transform = ""

    def __str__(self):
        return f"name: {card.name}, manacost: {card.manacost}, type: {card.type}, subtypes: {card.subtypes}, oracle text: {card.oracle_text}"

def get_card_from_json(jsontext: dict):
    card = Card()
    card.name = jsontext["name"].replace("&", "&amp;")
    card.manacost = jsontext["mana_cost"].replace("{", "").replace("}", "")
    cardtypes = jsontext["type"].split(" ")
    card.maintype = cardtypes[-1]
    subtypes = ""
    if "subtypes" in jsontext.keys():
        subtypes = " ".join(jsontext["subtypes"])
        card.type = " ".join(cardtypes) + " - " + subtypes
    else:
        card.type = " ".join(cardtypes)
    if "power" in jsontext.keys():
        card.pt = jsontext["power"]+"/"+jsontext["toughness"]
    else:
        card.pt = ""
    if "colors" in jsontext.keys():
        card.colors = "".join(jsontext["colors"])
    card.image = jsontext["image"]
    card.oracle_text = jsontext["oracle_text"].replace("&", "&amp;")
    if "back" in jsontext.keys():
        card.transform = jsontext["back"]["name"]
        print(card.transform)
    return card

while True:
    #print("Input location of draftmancer file.")
    #filepath = input(">").replace("\"", "")
    filepath = "C:/Users/apoke/Documents/YIPEEE_cube/YIPEEE_Draftmancer.txt"
    file = open(filepath, errors="ignore")
    filetext = file.read()
    prompt = filetext.split("[CustomCards]")[1].split("[MainSlot]")[0]
    #prompt = prompt.replace("\n", "").replace("  ", "")
    #print(prompt)
    jsonprompt = json.loads(prompt)
    #jsonprompt = json.load(file)
    cards = []
    for jsoncard in jsonprompt:
        card = get_card_from_json(jsoncard)
        cards.append(card)
        if card.transform != "":
            cardback = get_card_from_json(jsoncard["back"])
            cardback.side = "back"
            cardback.transform = card.name
            cards.append(cardback)
    fulltext = """<?xml version="1.0" encoding="UTF-8"?>
<cockatrice_carddatabase version="4">
  <sets>
    <set>
      <name>YPE</name>
      <longname>Yipeee Cube 1: The Beginning</longname>
      <settype>Custom</settype>
    </set>
  </sets>
  <cards>"""
    for card in cards:
        cmc = 0
        if card.manacost != "":
            if card.manacost[0].isdigit():
                cmc += int(card.manacost[0])
                cmc -= 1
            cmc += len(card.manacost)
        if card.transform != "":
            transform = "\n          <related attach=\"transform\">"+card.transform+"</related>"
        else:
            transform = ""
        if "Token" not in card.type:
            setrarity = " rarity=\"common\""
            tokentext = ""
            layout = "normal"
        else:
            setrarity = ""
            tokentext = """
          <token>1</token>"""
            layout = "token"
        if "Room" in card.type or "Hunt" in card.type:
            orientation = """
          <landscapeOrientation>1</landscapeOrientation>"""
        else:
            orientation = ""


        cardtext = f"""
        <card>
          <name>{card.name}</name>
          <prop>
            <layout>{layout}</layout>
            <colors>{card.colors}</colors>
            <manacost>{card.manacost}</manacost>
            <cmc>{cmc}</cmc>
            <type>{card.type}</type>
            <maintype>{card.maintype}</maintype>
            <pt>{card.pt}</pt>
            <side>{card.side}</side>
            <coloridentity>{card.colors}</coloridentity>
          </prop>
          <set{setrarity} picURL="{card.image}">YPE</set>{transform}{orientation}{tokentext}
          <tablerow>2</tablerow>
          <text>{card.oracle_text}</text>
        </card>"""
        fulltext = fulltext + cardtext
    fulltext = fulltext + """
  </cards>
</cockatrice_carddatabase>"""
    print(fulltext)
    with open("YipeeeXMLoutput.xml", "w", encoding="utf-8") as xmlfile:
        xmlfile.write(fulltext)
        pass
    input("check em out")

