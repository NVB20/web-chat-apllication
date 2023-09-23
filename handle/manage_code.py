import re

def room_code_regex(code):
    output_code = re.sub(r'custom-room-(\w+)-secret-code-room-\d+', r'Room \1', code)
    return output_code

