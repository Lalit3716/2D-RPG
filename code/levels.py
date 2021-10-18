from helpers import import_level

levels = {
    1: {"data": import_level("../Maps/csv/level1"), "resources": {
        "floor_tileset": "../assets/Backgrounds/Tilesets/TilesetFloor.png",
        "house_tileset": "../assets/Backgrounds/Tilesets/TilesetHouse.png",
        "nature_tileset": "../assets/Backgrounds/Tilesets/TilesetNature.png",
        "player": "../assets/Actor/Characters/BlueNinja",
    }},
}
