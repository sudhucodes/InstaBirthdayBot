from instagrapi import Client
from datetime import datetime
import json
import random

# Login to Instagram
username = "apexbdaybot"
password = "sudhu@123"

cl = Client()
try:
    cl.login(username, password)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit()

with open("wishes.json", "r", encoding='utf-8') as file:
    wishes_data = json.load(file)

with open("users_data.json", "r", encoding='utf-8') as file:
    users_data = json.load(file)
with open("users_data.json", "r") as file:
    users_data = json.load(file)
now = datetime.now()

for user in users_data:
    birthday = datetime.strptime(user["birthday"], "%Y-%m-%d %H:%M")

    next_birthday = birthday.replace(year=now.year)
    if next_birthday < now:
        next_birthday = next_birthday.replace(year=now.year + 1)

    days_left = (next_birthday - now).days

    if days_left == 0:
        if user["birthday_message"] == "random":
            message = random.choice(wishes_data["birthday_messages"]).format(name=user['name'])
        elif isinstance(user["birthday_message"], int) and 0 <= user["birthday_message"] < len(wishes_data["birthday_messages"]):
            index = user["birthday_message"]
            message = wishes_data["birthday_messages"][index].format(name=user['name'])
        else:
            message = wishes_data["birthday_messages"][0].format(name=user['name'])
    else:
        if user["countdown_message"] == "random":
            message = random.choice(wishes_data["countdown_messages"]).format(
                name=user['name'],
                days_left=days_left,
                date=next_birthday.strftime('%d-%B %Y at %I:%M %p')
            )
        elif isinstance(user["countdown_message"], int) and 0 <= user["countdown_message"] < len(wishes_data["countdown_messages"]):
            index = user["countdown_message"]
            message = wishes_data["countdown_messages"][index].format(
                name=user['name'],
                days_left=days_left,
                date=next_birthday.strftime('%d-%B %Y at %I:%M %p')
            )
        else:
            message = wishes_data["countdown_messages"][0].format(
                name=user['name'],
                days_left=days_left,
                date=next_birthday.strftime('%d-%B %Y at %I:%M %p')
            )

    message = message.encode('utf-8').decode('utf-8')

    try:
        user_id = cl.user_id_from_username(user["username"])
        cl.direct_send(message, [user_id])
        print(f"Message sent to {user['username']}!")
    except Exception as e:
        print(f"Failed to send message to {user['username']}: {e}")