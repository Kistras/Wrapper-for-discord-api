# ANY function imported must be async
from _module import mod_decorator as decorator #Important

import time
import _example_library

# Note that every function has "self" field

@decorator(60, False)
async def repeatingfunction1(self): #This function will be repeated every 60 seconds
    print("I print therefore I am")

@decorator(15, False)
async def repeatingfunction2(self): #This function will be repeated every 15 seconds
    print("I compute therefore I am")

@decorator(30, False)
async def repeatingfunction2(self): #This function will be repeated every 30 seconds
    print("I am therefore I am")

@decorator(None, False)
async def execute(self): #This function will be called once on boot
    print("Executed only once!")
    for i in range(_example_library.b): #Just to know that those thing are callable
        _example_library.a()

@decorator(None, True)
async def on_message(self, message): #This function is going to replace (or add additional functionality) to on_message event
                                     #Check https://discordpy.readthedocs.io/en/stable/api.html#event-reference for additional info
    if message.author == self.user:
        return

    if message.content.startswith("ping"):
        await message.channel.send("pong!")

@decorator(None, True)
async def on_ready(self): #Just notify everyone that our bot had started
    print("%s is going to become sentient!"%(self.user))


