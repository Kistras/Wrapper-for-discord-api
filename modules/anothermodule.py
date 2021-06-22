# Another example module
# Check examplemodule.py for commentary
from _module import mod_decorator as decorator #Important

import time
import _example_library, _SLIP

@decorator(None, True)
async def on_message(self, message): 
    if message.author == self.user:
        return

    if message.content.startswith("bruh"): #An example of permanent variables
        await message.channel.send("bruhn't")
