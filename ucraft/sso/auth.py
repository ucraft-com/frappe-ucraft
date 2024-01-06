from pprint import pprint

import requests

from ucraft.constants import MAIN_URL_UCRAFT


class UcraftAuth:
    def login(
            self,
            email: str,
            password: str,
    ):
        login_url = f"{MAIN_URL_UCRAFT}/login"
        login_data = {
            "email": email,
            "password": password
        }
        response = requests.post(login_url, data=login_data)
        if response.status_code == 200:
            r = response.json()
            return (True, r['data'], response.status_code, r['accessToken'])
        else:
            return (False, response.text, response.status_code, None)
