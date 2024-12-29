from instagrapi import Client
from datetime import datetime
import json
import random
import time
import os
import pytz
from dotenv import load_dotenv

def initialize_client():
    load_dotenv('/home/sudhucodes/instaBot/.env')
    
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    cl = Client()
    session_path = "/home/sudhucodes/instaBot/session.json"

    try:
        cl.load_settings(session_path)
        cl.login(username, password)
        print("Session loaded and login successful!")
    except Exception as e:
        print(f"Session load failed: {e}. Attempting fresh login...")
        time.sleep(random.randint(60, 180))
        try:
            cl.login(username, password)
            cl.dump_settings(session_path)
            print("Fresh login successful, session saved!")
        except Exception as e:
            print(f"Login failed: {e}")
            exit()
    return cl

def load_files():
    paths = {
        "wishes": "/home/sudhucodes/instaBot/wishes.json",
        "users": "/home/sudhucodes/instaBot/users_data.json",
        "used_birthday": "/home/sudhucodes/instaBot/used_birthday_messages.json",
        "used_countdown": "/home/sudhucodes/instaBot/used_countdown_messages.json"
    }

    for key in ["used_birthday", "used_countdown"]:
        if not os.path.exists(paths[key]):
            with open(paths[key], "w") as f:
                json.dump({}, f)

    with open(paths["wishes"], "r", encoding='utf-8') as file:
        wishes_data = json.load(file)

    with open(paths["users"], "r", encoding='utf-8') as file:
        users_data = json.load(file)

    with open(paths["used_birthday"], "r") as file:
        used_birthday_messages = json.load(file)

    with open(paths["used_countdown"], "r") as file:
        used_countdown_messages = json.load(file)

    return paths, wishes_data, users_data, used_birthday_messages, used_countdown_messages

def get_unique_message(used_dict, message_list, user, key):
    if user not in used_dict:
        used_dict[user] = []

    if len(used_dict[user]) >= len(message_list):
        used_dict[user] = []

    while True:
        index = random.randint(0, len(message_list) - 1)
        if index not in used_dict[user]:
            used_dict[user].append(index)
            with open(key, "w") as file:
                json.dump(used_dict, file)

            return message_list[index]

def get_india_time():
    utc_now = datetime.now(pytz.utc)
    india_tz = pytz.timezone('Asia/Kolkata')
    return utc_now.astimezone(india_tz)


def calculate_next_birthday(birthday_str, now):
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d %H:%M").date() 
    next_birthday = birthday.replace(year=now.year)

    if next_birthday < now.date():
        next_birthday = next_birthday.replace(year=now.year + 1)

    return next_birthday

def process_users(cl, wishes_data, users_data, used_birthday_messages, used_countdown_messages, paths):
    now = get_india_time()
    today_date = now.date() 

    for user in users_data:
        next_birthday = calculate_next_birthday(user["birthday"], now)

        days_left = (next_birthday - today_date).days
        user["days_left"] = days_left

    sorted_users_data = sorted(users_data, key=lambda x: x["days_left"])

    for user in sorted_users_data:
        username = user["username"]
        days_left = user["days_left"]
        message_type = user.get("message_type", "daily")
        next_birthday = calculate_next_birthday(user["birthday"], now)

        
        if message_type == "daily":
            if days_left == 0: 
                message = get_unique_message(
                    used_birthday_messages,
                    wishes_data["birthday_messages"],
                    username,
                    paths["used_birthday"]
                ).format(name=user["name"])
            else:
                message = get_unique_message(
                    used_countdown_messages,
                    wishes_data["countdown_messages"],
                    username,
                    paths["used_countdown"]
                ).format(
                    name=user["name"],
                    days_left=days_left,
                    date=next_birthday.strftime('%d-%B %Y')
                )
        elif message_type == "birthday" and days_left == 0: 
            message = get_unique_message(
                used_birthday_messages,
                wishes_data["birthday_messages"],
                username,
                paths["used_birthday"]
            ).format(name=user["name"])
        else:
            continue

        send_message(cl, username, message)

def send_message(cl, username, message):
    message = message.encode('utf-8').decode('utf-8')

    try:
        user_id = cl.user_id_from_username(username)
        cl.direct_send(message, [user_id])
        print(f"Message sent to {username}!")

        delay = random.randint(40, 60)
        print(f"Waiting {delay} seconds before sending the next message...")
        time.sleep(delay)
    except Exception as e:
        print(f"Failed to send message to {username}: {e}")

def main():
    cl = initialize_client()
    paths, wishes_data, users_data, used_birthday_messages, used_countdown_messages = load_files()
    process_users(cl, wishes_data, users_data, used_birthday_messages, used_countdown_messages, paths)

if __name__ == "__main__":
    main()