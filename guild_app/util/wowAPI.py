key = '2ghddk8z67szyz95bbtwcyqcec9bcpvx'
base_uri = 'https://eu.api.battle.net/wow/'
guild_news_uri = 'https://eu.api.battle.net/wow/guild/Arathor/Crimson%20Star?fields=news&locale=en_GB&apikey='
guild_info_uri = 'https://eu.api.battle.net/wow/guild/Arathor/Crimson%20Star?locale=en_GB&apikey='
guild_members_uri = 'https://eu.api.battle.net/wow/guild/Arathor/Crimson%20Star?fields=members&locale=en_GB&apikey='

class_map = {1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue', 5: 'Priest', 6: 'Death Knight', 7: 'Shaman',
             8: 'Mage', 9: 'Warlock', 10: 'Monk', 11: 'Druid', 12: 'Demon Hunter'}

class_colors = {'Warrior': '#c69b6d', 'Paladin': '#f48cba', 'Hunter': '#aad372', 'Rogue': '#fff468',
                'Priest': '#f5f5f5', 'Death Knight': '#c41e3b', 'Shaman': '#2359ff', 'Mage': '#68ccef',
                'Warlock': '#9382c9', 'Monk': '#008467', 'Druid': '#ff7c0a', 'Demon Hunter': '#a330c9'}

class_alternate_colors = {'Warrior': '#c69b6d', 'Paladin': '#f48cba', 'Hunter': '#aad372', 'Rogue': '#fff468',
                          'Priest': '#000000', 'Death Knight': '#c41e3b', 'Shaman': '#2359ff', 'Mage': '#68ccef',
                          'Warlock': '#9382c9', 'Monk': '#008467', 'Druid': '#ff7c0a', 'Demon Hunter': '#a330c9'}

race_map = {1: 'Human', 3: 'Dwarf', 4: 'Night Elf', 7: 'Gnome', 11: 'Draenei', 22: 'Worgen', 24: 'Pandaren',
            25: 'Pandaren', 29: 'Void Elf', 30: 'Lightforged Draenei'}

blizzard_tabard_logic = {
    "backgrounds": {0 : "ff2088", 1 : "bd005b", 2 : "9e0036", 3 : "ff891b", 4 : "e14500", 5 : "b1002e",
                    6 : "ffb317", 7 : "f68700", 8 : "ae4b00", 9 : "fffc14", 10 : "f3ca00", 11 : "c49b00",
                    12 : "ffff14", 13 : "d8dd00", 14 : "a6ac00", 15 : "e3f618", 17 : "8e9700", 16 : "b7c003",
                    19 : "88ba03", 18 : "bcf61b", 21 : "1eff68", 20 : "588000", 23 : "00820f", 22 : "04c347",
                    25 : "04b78f", 24 : "1ef7c1", 27 : "21dcff", 26 : "009061", 29 : "006391", 28 : "009dc5",
                    31 : "2c6aae", 30 : "4d8eda", 34 : "ad29ac", 35 : "860f9a", 32 : "003582", 33 : "d34ac8",
                    38 : "9b00a6", 39 : "ff1fbf", 36 : "ff38fa", 37 : "c900c3", 42 : "c58132", 43 : "875513",
                    40 : "d30087", 41 : "a30068", 46 : "646464", 47 : "b4bba8", 44 : "4f2300", 45 : "232323",
                    50 : "fc6891", 49 : "ffffff", 48 : "d7ddcb"},
    "icons": {  0: "670021", 1: "672300", 2: "674500", 3: "675600", 4: "636700", 5: "516700", 6: "376700",
                7: "00671f", 8: "006757", 9: "004867", 10: "092a5d", 11: "56095d", 12: "5d094f", 13: "54370a",
                14: "b1b8b1", 15: "101517", 16: "dfa55a"},
    "borders": { 0 : "670021", 1 : "672300", 2 : "674500",  3 : "675600", 4 : "639400",  5 : "63a300",  6 : "63b300",
                 7 : "00671f", 8 : "008e90",  9 : "006793", 10 : "00317c",  11 : "6d0077", 12 : "7b0067",  13 : "54370a",
                 14 : "ffffff",  15 : "0f1415", 16 : "f9cc30"}}

tabard = {'emblem': 62, 'border': 3, 'icon color': 0, 'bg color': 49, 'border color': 15,
          'faction': 'Alliance'}
