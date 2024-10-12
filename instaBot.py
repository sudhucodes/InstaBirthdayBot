from instagrapi import Client
from datetime import datetime
import json
import schedule  # For scheduling
import time      # To keep the script running
import os        # To read environment variables

# Instagram login credentials (store them as environment variables)
username = os.environ.get('INSTA_USERNAME')
password = os.environ.get('INSTA_PASSWORD')

# Function to send birthday wishes
def send_wishes():
    cl = Client()
    try:
        cl.login(username, password)
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")
        return  # Stop execution if login fails

    with open("users_data.json", "r") as file:
        users_data = json.load(file)

    now = datetime.now()

    # Loop through users to send personalized wishes
    for user in users_data:
        birthday = datetime.strptime(user["birthday"], "%Y-%m-%d %H:%M")
        next_birthday = birthday.replace(year=now.year)
        if next_birthday < now:
            next_birthday = next_birthday.replace(year=now.year + 1)

        days_left = (next_birthday - now).days

        if days_left == 0:
            message = (
                f"🎉 Happy Birthday, {user['name']}! 🎉\n\n"
                f"Today is your special day! I hope it's filled with fun and joy! 🎂✨\n\n"
                f"Make wonderful memories today! 🎈"
            )
        else:
            message = (
                f"🌟 Hi {user['name']}! 🎂\n\n"
                f"Just {days_left} days left until your birthday on "
                f"{next_birthday.strftime('%d-%B %Y, %I:%M %p')}! 🎉\n\n"
                f"Get ready to celebrate soon! ✨"
            )

        try:
            user_id = cl.user_id_from_username(user["username"])
            cl.direct_send(message, [user_id])
            print(f"Message sent to {user['username']}!")
        except Exception as e:
            print(f"Failed to send message to {user['username']}: {e}")

# Schedule the job to run daily at midnight
schedule.every().day.at("00:00").do(send_wishes)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
