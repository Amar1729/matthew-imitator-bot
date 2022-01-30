import pytz


TZ = pytz.timezone("America/New_York")


with open("token", "r") as f:
    TOKEN = f.read().strip()


with open("group_chat_id", "r") as f:
    GROUP_CHAT_ID = int(f.read().strip())
