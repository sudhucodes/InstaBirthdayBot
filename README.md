# **Instagram Birthday Bot 🎉**

A Python-based Instagram bot that logs into an Instagram account and sends personalized birthday wishes to users listed in a JSON file. This bot calculates the number of days remaining until the user's birthday and sends timely wishes via Instagram Direct Message (DM). It also manages sessions and avoids message duplication.

---

## **Features 📋**

- **Automated login** using the `instagrapi` library with session management.
- **Reads user data** from a JSON file containing usernames, names, and birthdays.
- **Calculates the next occurrence** of the user's birthday.
- **Sends personalized birthday wishes** on the user's birthday or countdown messages in advance.
- **Graceful error handling** during login and message sending.
- **Prevents duplicate messages** by tracking used messages in JSON files.

---

## **Project Structure 🗂**

```bash
instaBot/
│
├── main.py                    # Main script for sending birthday wishes
├── .env                       # Environment file to store Instagram credentials
├── session.json               # Session data to reuse login (auto-generated)
├── users_data.json            # JSON file with user data (username, name, birthday)
├── wishes.json                # JSON file with birthday and countdown messages
├── used_birthday_messages.json  # Tracks used birthday messages
├── used_countdown_messages.json # Tracks used countdown messages
└── README.md                  # Project documentation (you are here!)
```

---

## **Prerequisites 🛠**

1. **Python 3.x** installed on your system.  
2. An **Instagram account** (Ensure it's verified to avoid login issues).  
3. Install the required Python packages:

    ```bash
    pip install instagrapi python-dotenv
    ```

---

## **Setup Guide 🔧**

### 1. **Clone the Repository**

```bash
git clone https://github.com/sudhucodes/instaBot.git
cd instaBot
```

---

### 2. **Prepare the User Data**

Create a file named `users_data.json` in the project folder with the following structure:

```json
[
  {
    "username": "user1_insta",
    "name": "User One",
    "birthday": "1995-10-18 00:00"
  },
  {
    "username": "user2_insta",
    "name": "User Two",
    "birthday": "2000-12-25 15:30"
  }
]
```

- **`username`**: Instagram username of the user.
- **`name`**: The user's real name for personalized messages.
- **`birthday`**: Date and time in the format `YYYY-MM-DD HH:MM`.

---

### 3. **Configure Instagram Credentials**

1. Create a **`.env` file** in the `instaBot/` folder with your Instagram credentials:

   ```env
   INSTAGRAM_USERNAME=your_insta_username
   INSTAGRAM_PASSWORD=your_insta_password
   ```

2. Ensure the credentials are correct to avoid login issues.

---

### 4. **Customize Messages**

Create a file named `wishes.json` with your birthday and countdown messages:

```json
{
  "birthday_messages": [
    "Happy Birthday, {name}! 🎉 Hope you have an amazing day!",
    "Wishing you all the best on your special day, {name}! 🎂"
  ],
  "countdown_messages": [
    "Only {days_left} days to go until your birthday, {name}! 🎊",
    "Get ready, {name}! Your birthday is coming up on {date}. 🎈"
  ]
}
```

- **`{name}`**: Placeholder for the user's name.
- **`{days_left}`**: Days left until the birthday.
- **`{date}`**: The exact date of the birthday.

---

### 5. **Run the Bot**

Execute the following command in your terminal:

```bash
python main.py
```

---

## **How It Works 🛠️**

1. **Session Management**:
   - If a session exists in `session.json`, the bot tries to use it for login.
   - If the session fails, it performs a **fresh login** and saves a new session.

2. **Sending Messages**:
   - For each user in `users_data.json`, the bot calculates the **next birthday**.
   - If **today is the user’s birthday**, a birthday message is sent.
   - If **the birthday is upcoming**, a countdown message is sent with the number of days left.

3. **Unique Message Handling**:
   - The bot **tracks used messages** in `used_birthday_messages.json` and `used_countdown_messages.json` to prevent duplicates.
   - If all messages have been used, it resets the list.

4. **Error Handling**:
   - If login or message sending fails, the bot **logs the error** and moves on to the next user.
   - A **random delay** (30-60 seconds) is added between messages to avoid spam detection.

---

## **Error Handling & Session Recovery 🔄**

- If the **`session.json`** file is missing, the bot performs a fresh login.
- If the **Instagram credentials** are incorrect, the login will fail, and the program will exit.
- The bot ensures that **JSON files for tracking used messages** exist; if not, they are created automatically.

---

## **Example Run 🖥️**

```
Session loaded and login successful!
Message sent to user1_insta!
Waiting 45 seconds before sending the next message...
Message sent to user2_insta!
All messages processed successfully!
```

---

## **Contact 📧**

If you have any questions or need further help, feel free to reach out:

- **GitHub**: [sudhucodes](https://github.com/sudhucodes)  
- **Instagram**: [@sudhucodes](https://instagram.com/sudhucodes)  
- **Email**: sudhuteam@gmail.com  
- **Twitter**: [@sudhucodes](https://twitter.com/sudhucodes)

---

## **License 📝**

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## **Contributing 🤝**

Feel free to submit **pull requests** or **issues** to contribute to this project. All contributions are welcome!
```

### Key Changes Made:
- Merged the sections to create a clear flow and cohesive structure.
- Ensured that all features and functionalities are well articulated.
- Maintained formatting for easy reading and navigation.

Feel free to modify any sections or details as necessary!