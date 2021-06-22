#########################################
# This is what hope feels like.         #
# Sorry for being an asshole. Hope that #
#  you'll forgive me eventually. After  #
#  all, that's why I'm here, right?..   #
#########################################

#Imports
#Basic stuff, ya know
import sys, os, asyncio
import importlib.util

#To make importing easier for me
from functools import partial

#Shared variables and config
import _SLIP, config

#Thing for an actual wrapper
import discord

### IMPORTER ###
modules = {}
found_files = os.listdir("modules/")

#Here path must be overriden
prevpath = sys.path
sys.path = [prevpath[0] + "\\modules"] #Lock for only one directory

for f in found_files:
    if len(f) > 3 and f[-3:] == ".py":
        module_name = f[:-3]
        #We will execute those modules later
        spec = importlib.util.find_spec(module_name)
        modules[module_name] = (spec, importlib.util.module_from_spec(spec))
        
sys.path = prevpath #And get everything to normal so each library can use it's own dependencies

#Each module has to be executed so it will work correctly
for m in modules:
    modules[m][0].loader.exec_module(modules[m][1]) 

### Here we go ###

um = _SLIP.SharedVariableHandler("_usedmodules")
um[um.len()] = (_SLIP.updateAllPermanentVariables, 30, False) #Autoupdate permanent variables

class Client(discord.Client): #Main client
    _firstlaunch = True
    _implementedfunctions = {}
    _queuedfunctions = []
    async def on_ready(self): #Everything initializes in there
        if self._firstlaunch:
            um = _SLIP.SharedVariableHandler("_usedmodules")
            self._implementedfunctions["on_ready"] = [] #To avoid crashing
            #(func, time, replace)
            for m in um.get_dict():
                fname = um[m][0].__name__
                
                if um[m][2]: #If should add to the clients function
                    isimplemented = fname in self._implementedfunctions

                    if not isimplemented:
                        def a(funcname, slf): #slf is self, just kinda truncated. I have no idea why this stuff is broken
                            async def b(*args, **kwargs):
                                for func in slf._implementedfunctions[funcname]:
                                    await func[0](slf, *args, **kwargs)
                            return b
                        setattr(self, fname, partial(a, fname, self)())
                        self._implementedfunctions[fname] = []
                    
                    self._implementedfunctions[fname].append(um[m])
                else:
                    #It has to be stated like that by some unknown reason
                    efunc = um[m][0]
                    enum = um[m][1]
                    if enum and isinstance(enum, int): #If should add to the queue
                        def a(self, efu, efunction, queuelen):
                            async def b(self):
                                self.loop.call_later(efu, asyncio.create_task, self._queuedfunctions[queuelen](self))
                                await efunction(self)
                            self._queuedfunctions.append(b)
                            return b
                        r = partial(a, self, enum, efunc, len(self._queuedfunctions))() #Omg why
                        await r(self)
                    else:
                        await efunc(self)
        
        for func in self._implementedfunctions["on_ready"]: #Just in case
            await func[0](self)
        
        self._firstlaunch = False #This thing belongs to the end so anyone can edit that

runclient = Client(intents=config.intents, status=config.status, activity=config.activity)
runclient.run(config.token)
