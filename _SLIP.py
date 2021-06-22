# Shared Library of Internal Parameters

# Cuz I love cool names
# They don't have to make sense anyways

import json

global _vars, _permavars, _updatepv
_vars = {} #Global variables
_permavars = {} #Permanent variables
_updatepv = {} #Recently changed permanent variables

# SharedVariables are basically dicts with less functions
class SharedVariableHandler(object):
    def __init__(self, link):
        global _vars
        if not link or len(link) == 0:
            self.__dict = _vars
            self.__link = ""
        else:
            if not link in _vars:
                _vars[link] = {}
            self.__dict = _vars[link]
            self.__link = link

    def get_dict(self): #To get actual dict
        return self.__dict

    def __getitem__(self, key): #print(svh[0])
        if key in self.__dict:
            return self.__dict[key]
        assert False, "No %s in shared %s variables."%(key, self.__link) #In case this launched in debug mode
        return None
    
    def __setitem__(self, key, value): #svh[0] = "cookies"
        self.__dict[key] = value
    
    def __delitem__(self, key): #del svh[0]
        del self.__dict[key]
    
    def __contains__(self, item): #print("cookies" in svh)
        return item in self.__dict
    
    def __repr__(self): #print(svh)
        return "SVH(%s)"%self.__dict.__repr__()[1:-1] #Just return the same thing you use in dict object, but cooler
    
    def len(self):
        return len(self.__dict)
    
    def keys(self):
        return self.__dict.keys()

# Permanent variables however act more like a database with specific ids you can't really access from other places.
# Kinda hard to understand, but yeah
async def updateAllPermanentVariables(*args): #Function to save everything
    global _updatepv
    for k in list(_updatepv.keys()): 
        if _updatepv[k]:
            try:
                with open(k + ".json", "w", encoding = "utf-8") as f:
                    f.write(json.dumps(_permavars[k]))
            except:
                raise #Maybe do something later with it
    _updatepv = {}


class PermanentVariableHandler(object): #I can't inherit it???
    def __init__(self, link):
        global _permavars
        if link in _permavars:
            self.__dict = _permavars[link]
        else:
            try:
                with open(link + ".json", "r", encoding = "utf-8") as f:
                    self.__dict = json.loads(f.read())
            
            except FileNotFoundError:
                self.__dict = {}
                _updatepv[link] = True
            
            except json.JSONDecodeError:
                print("Something went wrong while decoding %s.json"%(link))
                self.__dict = {}
            
            except:
                raise #FIXME
            
            _permavars[link] = self.__dict
        
        self.__link = link

    def get_dict(self): #To get actual dict
        return self.__dict

    def __getitem__(self, key): #print(svh[0])
        if key in self.__dict:
            return self.__dict[key]
        assert False, "No %s in permanent %s variables."%(key, self.__link) #In case this launched in debug mode
        return None

    def __setitem__(self, key, value): #svh[0] = "cookies"
        self.__dict[key] = value
        _updatepv[self.__link] = True
    
    def __delitem__(self, key): #del svh[0]
        del self.__dict[key]
        _updatepv[self.__link] = True
    
    def __contains__(self, item): #print("cookies" in svh)
        return item in self.__dict
    
    def __repr__(self): #print(svh)
        return "PVH(%s)"%self.__dict.__repr__()[1:-1] #Just return the same thing you use in dict object, but cooler