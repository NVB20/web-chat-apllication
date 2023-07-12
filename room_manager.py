import random
from string import ascii_uppercase

SCECRET_KEY = "youwontguessthiskey"
ROOM_CODE_LENGTH = 11
rooms = {}

#python room
rooms["SBSOVMQFEJJ"] = {"members": 0, "messages": []}
#java room
rooms["JFVRWQHEDRG"] = {"members": 0, "messages": []}
#devops room
rooms["HVXNDLUNQFD"] = {"members": 0, "messages": []}


def generate_room_code(ROOM_CODE_LENGTH):
    while True:
        code = ""
        for _ in range(ROOM_CODE_LENGTH):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
        
    print(code)    
    return code