import json
while True:
    prompt = input(">")
    prompt.replace("  ", "")
    jsonprompt = json.loads(prompt)
    cmctext = jsonprompt["mana_cost"].replace("{", "").replace("}", "")
    cmc = 0
    if cmctext[0].isdigit():
        cmc += int(cmctext[0])
        cmc -= 1
    cmc += len(cmctext)
    cardtypes = jsonprompt["type"].split(" ")
    if cardtypes[0] in ["Legendary", "Token"]:
        maintype = cardtypes[1]
    else:
        maintype = cardtypes[0]
    try:
        pt = f"{jsonprompt["power"]}/{jsonprompt["toughness"]}"
    except:
        pt = ""
        
    print(f"""<card>
      <name>{jsonprompt["name"]}</name>
      <set rarity="common"></set>
      <prop>
        <colors>{"".join(jsonprompt["colors"])}</colors>
        <manacost>{jsonprompt["mana_cost"].replace("{", "").replace("}", "")}</manacost>
        <cmc>{cmc}</cmc>
        <type>{jsonprompt["type"]}</type>
        <maintype>{maintype}</maintype>
        <pt>{pt}</pt>
        <side>front</side>
        <coloridentity>{"".join(jsonprompt["colors"])}</coloridentity>
      </prop>
      <set rarity="common" picURL="{jsonprompt["image"]}">YPE</set>
      <tablerow>2</tablerow>
      <text>{jsonprompt["oracle_text"]}</text>
    </card>""")
    

"""{
        "id": "56636278-d503-4cab-8c4b-066e711de73e",
        "name": "Donut Witch",
        "mana_cost": "{U}{U}{B}{B}{B}",
        "type": "Legendary Creature - Human Advisor ",
        "image": "https://raw.githubusercontent.com/apokef1sh/YIPEEE_cube/main/Images/Suspicious%20Schemer.png",
        "colors": [
            "U",
            "B"
        ],
        "set": "YPE",
        "oracle_text": "Whenever you commit a crime, Suspicious Schemer connives.\nWhenever another creature you control connives, each instant and sorcery in your hand has plot until end of turn. Its plot cost is equal to its mana cost reduced by {3}.",
        "power": "2",
        "toughness": "1"
    },"""