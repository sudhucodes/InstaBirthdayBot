from instagrapi import Client
from datetime import datetime
import json
import random
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/home/sudhucodes/instaBot/.env')

# Instagram credentials from the environment variables
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

# Initialize the Instagram Client
cl = Client()

# Define paths for session and JSON files
session_path = "/home/sudhucodes/instaBot/session.json"
wishes_path = "/home/sudhucodes/instaBot/wishes.json"
users_data_path = "/home/sudhucodes/instaBot/users_data.json"
used_birthday_path = "/home/sudhucodes/instaBot/used_birthday_messages.json"
used_countdown_path = "/home/sudhucodes/instaBot/used_countdown_messages.json"

# Try to load the session or login fresh
try:
    cl.load_settings(session_path)
    cl.login(username, password)
    print("Session loaded and login successful!")
except Exception as e:
    print(f"Session load failed: {e}. Attempting fresh login...")
    time.sleep(random.randint(60, 180))  # Random wait to mimic human behavior
    try:
        cl.login(username, password)
        cl.dump_settings(session_path)
        print("Fresh login successful, session saved!")
    except Exception as e:
        print(f"Login failed: {e}")
        exit()

# Ensure JSON files exist
for path in [used_birthday_path, used_countdown_path]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)  # Use empty dictionary instead of list

# Load wishes and user data
with open(wishes_path, "r", encoding='utf-8') as file:
    wishes_data = json.load(file)

with open(users_data_path, "r", encoding='utf-8') as file:
    users_data = json.load(file)

# Load used message indices
with open(used_birthday_path, "r") as file:
    used_birthday_messages = json.load(file)

with open(used_countdown_path, "r") as file:
    used_countdown_messages = json.load(file)

now = datetime.now()

# Helper function to get a unique message for each user
def get_unique_message(used_dict, message_list, user, key):
    # Initialize the user-specific message list if not present
    if user not in used_dict:
        used_dict[user] = []

    # Reset the user's list if all messages have been used
    if len(used_dict[user]) >= len(message_list):
        used_dict[user] = []

    # Find a unique message that hasn't been used for the user
    while True:
        index = random.randint(0, len(message_list) - 1)
        if index not in used_dict[user]:
            used_dict[user].append(index)  # Track the used message index

            # Save the updated dictionary back to the JSON file
            with open(key, "w") as file:
                json.dump(used_dict, file)

            return message_list[index]


# Calculate days until next birthday and sort users
for user in users_data:
    birthday = datetime.strptime(user["birthday"], "%Y-%m-%d %H:%M")
    next_birthday = birthday.replace(year=now.year)

    if next_birthday < now:
        next_birthday = next_birthday.replace(year=now.year + 1)

    days_left = (next_birthday - now).days
    user["days_left"] = days_left  # Add days_left to user data for sorting

# Sort users by days_left, prioritizing those with the nearest birthdays
sorted_users_data = sorted(users_data, key=lambda x: x["days_left"])

# Helper function to calculate the next birthday
def calculate_next_birthday(birthday_str):
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d %H:%M")
    next_birthday = birthday.replace(year=now.year)
    
    if next_birthday < now:
        next_birthday = next_birthday.replace(year=now.year + 1)
    
    return next_birthday

for user in sorted_users_data:
    username = user["username"]
    days_left = user["days_left"]
    
    # Calculate the next birthday only once
    next_birthday = calculate_next_birthday(user["birthday"])

    message_type = user.get("message_type", "daily")

    if message_type == "daily":
        if days_left == 0:
            message = get_unique_message(
                used_birthday_messages,
                wishes_data["birthday_messages"],
                username,
                used_birthday_path
            ).format(name=user["name"])
        else:
            message = get_unique_message(
                used_countdown_messages,
                wishes_data["countdown_messages"],
                username,
                used_countdown_path
            ).format(
                name=user["name"],
                days_left=days_left,
                date=next_birthday.strftime('%d-%B %Y at %I:%M %p')  # Unique date
            )
    elif message_type == "birthday" and days_left == 0:
        message = get_unique_message(
            used_birthday_messages,
            wishes_data["birthday_messages"],
            username,
            used_birthday_path
        ).format(name=user["name"])
    else:
        continue

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

print("All messages processed successfully!")
