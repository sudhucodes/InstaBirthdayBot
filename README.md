# Instagram Automation Bot

This is an open-source Instagram automation bot designed for sending personalized **birthday messages** and **countdown messages** to users. The project uses the `instagrapi` library to interact with Instagram's API and is structured for scalability, reusability, and maintainability.

## Features

- **Session Management**: Automatically saves and reloads the login session to avoid frequent logins.
- **Personalized Messages**: Sends unique birthday and countdown messages to users based on their data.
- **Data Handling**: Reads user data, message templates, and usage history from JSON files.
- **Error Handling**: Includes structured error handling for login and message-sending operations.
- **Modular Design**: Functions are divided logically for better readability and reusability.

## Installation

### Prerequisites

- Python 3.8+
- An Instagram account
- Environment file (`.env`) with the following variables:
  ```env
  INSTAGRAM_USERNAME=<your_instagram_username>
  INSTAGRAM_PASSWORD=<your_instagram_password>
  ```

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/sudhucodes/InstaBirthdayBot
   cd InstaBirthdayBot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the `.env` file:

   ```bash
   touch .env
   ```

   Add your Instagram credentials to the `.env` file.

4. Create required JSON files if they don't exist:

   ```bash
   touch wishes.json users_data.json used_birthday_messages.json used_countdown_messages.json
   ```

5. Add data to `wishes.json` and `users_data.json`:

   - `wishes.json` (message templates):
     ```json
     {
       "birthday_messages": [
         "Happy Birthday, {name}! 🎉",
         "Wishing you a fantastic birthday, {name}! 🥳"
       ],
       "countdown_messages": [
         "Hey {name}, only {days_left} days left until your big day on {date}!",
         "Countdown alert! {name}'s birthday is just {days_left} days away ({date})."
       ]
     }
     ```
   - `users_data.json` (user information):
     ```json
     [
       {
         "username": "example_user",
         "name": "John Doe",
         "birthday": "2000-12-25 00:00",
         "message_type": "daily"
       }
     ]
     ```

## Usage

Run the bot using the following command:

```bash
python main.py
```

The bot will:

1. Log in to your Instagram account.
2. Load user and message data from JSON files.
3. Calculate days left until users' birthdays.
4. Send personalized messages to each user.

## File Structure

- `main.py`: The main script.
- `wishes.json`: Contains message templates for birthdays and countdowns.
- `users_data.json`: Contains user information (username, birthday, etc.).
- `used_birthday_messages.json`: Tracks used birthday messages to avoid repetition.
- `used_countdown_messages.json`: Tracks used countdown messages to avoid repetition.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact Information:  
Developed and maintained by **SudhuCodes**.  

- **GitHub:** [@sudhucodes](https://github.com/sudhucodes)  
- **Instagram:** [@sudhucodes](https://instagram.com/sudhucodes)  
- **YouTube:** [SudhuCodes YT Channel](https://www.youtube.com/@sudhucodes)  
- **Telegram**: [SudhuCodes TG Channel](https://t.me/sudhucodes)
- **Email:** [sudhuteam@gmail.com](mailto:sudhuteam@gmail.com)

---

Feel free to reach out for support or questions!