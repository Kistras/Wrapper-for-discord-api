# Thing that all modules are going to use
import _SLIP

_allmods = _SLIP.SharedVariableHandler("_usedmodules")

# Wut is that
# This is module's function we're going to broadcast to wrapper
# function - function that will be called
# timespan - if this is not repeatable function then input None/False/0
#            otherwise input intervals (in seconds) in which this function will be called
# embedable - if this function is going to replace original discord's library functions
def mod_decorator(timespan, embedable):
    a = None #Temp
    def another_one(function):        
        _allmods[_allmods.len()] = (function, timespan, embedable)
        a = function
        return a
    return another_one
