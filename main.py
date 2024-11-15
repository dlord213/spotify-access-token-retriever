import requests, datetime

"""
Implementation of Token class for gaining, storing and verifying Spotify developer
tokens. Using text file to store; explore databases for production code.
"""

# Enter client ID and secret from developer console; store in .env or similar
CLIENT_ID = ""
CLIENT_SECRET = ""


class Token:
    def __init__(self):
        self.__token = None
        self.__time = None
        self.load_token()
        try:
            if self.__time + datetime.timedelta(hours=1) < datetime.datetime.now():
                print("Token out of time")
                self.get_token()
            else:
                print("Token up to date")

        except TypeError:
            print("Token time format incorrect")
            self.get_token()
        self.save_token()

    def get_token(self):
        endpoint = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(endpoint, headers=headers, data=body)
        self.__token = response.json()["access_token"]
        self.__time = datetime.datetime.now()
        self.save_token()

    def save_token(self):
        details = self.__token + "," + self.__time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        with open("token.txt", "w") as file:
            file.write(details)

    def load_token(self):
        try:
            with open("token.txt", "r") as file:
                result = file.read()
                result = result.strip().split(",")
                self.__token = result[0]
                self.__time = datetime.datetime.strptime(
                    result[1], "%d-%b-%Y (%H:%M:%S.%f)"
                )
        except FileNotFoundError:
            print("No tokens stored found.")
            self.get_token()
        except ValueError:
            print("File for tokens is corrupted.")
            self.get_token()

    def token(self):
        return self.__token

    def time(self):
        return self.__time


token = Token()

print(token.token())
