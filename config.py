#Your config goes here
from discord import Intents, Game, Status
token = "Your token goes here" 
intents = Intents.default()
activity = Game("The Game Of Leaf")
status = Status.dnd