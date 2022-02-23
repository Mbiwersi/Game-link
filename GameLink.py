# May have to install this package before using
import requests


def connect():
    # Need this header to tie into my account info. If you want to test with your account, replace the
    # key from the OpenXBL Site
    headers = {"X-Authorization": "wcckckkwgg4k0g4s8g4cgc0ggw08skskwwg"}

    # This is what we will be using to gather info from the api, what comes after the v2/ is where you put the
    # command that you want to get (friends, account, group, etc.) from this site: https://xbl.io/console
    response = requests.get('https://xbl.io/api/v2/friends', headers=headers)
    print(response.status_code)
    print(response.json())

    # Use this to print header info if needed
    # print(response.headers)


if __name__ == '__main__':
    connect()