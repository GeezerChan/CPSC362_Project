"""Assests for the scenes."""

import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

asset_dict = {
    'soundtrack': '8bp051-06-random-happy_ending_after_all.mp3',
    'music-grid': 'music-grid.wav',
    'music-grid.BJ': 'music-grid.BJ.wav',
    'goofy_ahh': 'goofy_ahh.mp3',
    'soundfx': 'meow.mp3',
    'sun1': 'sun1.bmp',
    'cat': 'cat.png',
    'dragon': 'Dragon.png',
    'fire': 'Fueguito_magia_copia.png'
}


def get(key):
    """Gets needed sound from asset_dict"""
    value = asset_dict.get(key, None)
    assert value
    if value:
        value = os.path.join(data_dir, value)
    return value