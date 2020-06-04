from setuptools import setup

NAME = "Tetro"

APP = ["tetro.py"]

DATA_FILES = [
    "images",
    "pieces",
    "music"
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
