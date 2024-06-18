import zipfile
import json

# Use zlib if we have it
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED

pack_format = 48

def addToLootTable(lootfilename, weight = 1, pool = 0, indent = None):
    with open('base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())
    lootjson['pools'][pool]['entries'].append({
        'type': 'minecraft:loot_table',
        'weight': weight,
        "value": "babel:books"
    })
    return json.dumps(lootjson, indent=indent, ensure_ascii=False)

def getBooksJsonString(loottable, indent = None):
    return json.dumps(loottable, indent=indent, ensure_ascii=False)
    
def getFileJson(filename, indent = None):
    with open(filename) as jsonFile:
        return json.dumps(json.load(jsonFile), indent=indent)

def buildDatapack(config, loottable):
    if config['indent-output']:
        indent = 2
    else:
        indent = None

    zf = zipfile.ZipFile(config['output-filename'], mode='w', compression=compression)
    zf.writestr('pack.mcmeta', json.dumps({
        "pack": {
            "pack_format": pack_format,
            "description": "Add pre-written books to your vanilla world. https://github.com/JiFish/babel"
        }
    }, indent=indent, ensure_ascii=False))
    zf.writestr('data/babel/loot_table/books.json', getBooksJsonString(loottable, indent=indent))
    if config['add-stronghold-loot']:
        print ("Adding to Stronghold Library loot table.")
        zf.writestr('data/minecraft/loot_table/chests/stronghold_library.json', addToLootTable('stronghold_library.json',15, indent=indent))
    if config['add-mansion-loot']:
        print ("Adding to Woodland Mansion loot table.")
        zf.writestr('data/minecraft/loot_table/chests/woodland_mansion.json', addToLootTable('woodland_mansion.json',5, indent=indent))
    if config['add-village-loot']:
        print ("Adding to Village loot table.")
        zf.writestr('data/minecraft/loot_table/chests/village/village_desert_house.json', addToLootTable('village_desert_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_plains_house.json', addToLootTable('village_plains_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_savanna_house.json', addToLootTable('village_savanna_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_snowy_house.json', addToLootTable('village_snowy_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_taiga_house.json', addToLootTable('village_taiga_house.json',3, indent=indent))
    if config['add-fishing-loot']:
        print ("Adding to Fishing Treasure loot table.")
        zf.writestr('data/minecraft/loot_table/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1, indent=indent))
    if config['add-zombie-drop']:
        print ("Adding to Zombie drop loot table.")
        zf.writestr('data/minecraft/loot_table/entities/zombie.json', addToLootTable('zombie.json',1,1, indent=indent))
    if config['replace-hero-of-the-village-gift']:
        print ("Replacing Librarian's Hero of the village gift.")
        #zf.write('extras/librarian_gift.json', 'data/minecraft/loot_table/gameplay/hero_of_the_village/librarian_gift.json')
        zf.writestr('data/minecraft/loot_table/gameplay/hero_of_the_village/librarian_gift.json', getFileJson('extras/librarian_gift.json', indent=indent))
    if config['add-crafting-recipe']:
        print ("Adding crafting recipe.")
        #zf.write('extras/babel_book_recipe.json', 'data/babel/recipe/babel_book_recipe.json')
        zf.writestr('data/babel/recipe/babel_book_recipe.json', getFileJson('extras/babel_book_recipe.json', indent=indent))
    zf.close()
