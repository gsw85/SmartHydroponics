from datetime import datetime
import time

def get_timestamp():
    now = datetime.now()

    timestamp = datetime.timestamp(now)

    return timestamp


# x = get_timestamp()
# print(x)
# time.sleep(5)
# y = get_timestamp()
# print(y)
# diff = y - x
# print(diff)