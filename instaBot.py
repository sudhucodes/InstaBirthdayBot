from instagrapi import Client
from datetime import datetime
import json

# Login to Instagram
username = "apexbday"
password = "sudhu.123"

cl = Client()
try:
    cl.login(username, password)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit()  # Stop the script if login fails

# Load user data from JSON file
with open("users_data.json", "r") as file:
    users_data = json.load(file)

# Get current date and time
now = datetime.now()

# Loop through users to send personalized wishes
for user in users_data:
    # Parse the exact birthdate and time
    birthday = datetime.strptime(user["birthday"], "%Y-%m-%d %H:%M")

    # Calculate the next occurrence of the birthday
    next_birthday = birthday.replace(year=now.year)
    if next_birthday < now:
        next_birthday = next_birthday.replace(year=now.year + 1)

    # Calculate days left for the next birthday
    days_left = (next_birthday - now).days

    # Create the message based on the time left for the birthday
    if days_left == 0:
        message = (
            f"🎉 Happy Birthday, {user['name']}! 🎉\n\n"
            f"Today is your special day! I hope it's filled with lots of fun, laughter, and everything you love. 🎂✨\n\n"
            f"Enjoy every moment and make some wonderful memories today! You deserve it! 🎈"
        )
    else:
        message = (
            f"🌟 Hi {user['name']}! 🎂\n\n"
            f"Your birthday is almost here—just {days_left} days to go until we celebrate you on "
            f"{next_birthday.strftime('%d-%B %Y, %I:%M %p')}! 🎉\n\n"
            f"I hope this next year brings you happiness and success. Get ready to enjoy your special day soon! ✨"
        )

    # Send the message
    try:
        user_id = cl.user_id_from_username(user["username"])
        cl.direct_send(message, [user_id])
        print(f"Message sent to {user['username']}!")
    except Exception as e:
        print(f"Failed to send message to {user['username']}: {e}")