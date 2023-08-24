import time


def time_now():
    current_time = time.localtime()
    
    hour = current_time.tm_hour 
    minute = current_time.tm_min

    formatted_time = f"{hour:02d}:{minute:02d}"
    
    return formatted_time
    