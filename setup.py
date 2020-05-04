from setuptools import setup


APP = ["tetro.py"]
NAME = "Tetro"

DATA_FILES = [
    "pieces/piece_purple.png",
    "pieces/piece_blue.png",
    "pieces/piece_orange.png",
    "pieces/piece_red.png",
    "pieces/piece_green.png",
    "pieces/piece_lightblue.png",
    "pieces/piece_yellow.png",
    "images/background.png",
    "images/main_menu.png",
    "images/start_button.png",
    "images/start_button_hover.png"
]

OPTIONS = {
    "packages": ["pygame"],
    "iconfile": "images/tetro_icon.icns"
}

setup(
    app = APP,
    name = NAME,
    data_files = DATA_FILES,
    options = {"py2app": OPTIONS},
    setup_requires = ["py2app"]
)
