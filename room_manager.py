import random
from string import ascii_uppercase

SCECRET_KEY = "youwontguessthiskey"
ROOM_CODE_LENGTH = 11
rooms = {}


def generate_room_code(ROOM_CODE_LENGTH):
    while True:
        code = ""
        for _ in range(ROOM_CODE_LENGTH):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
        
    print(code)    
    return code