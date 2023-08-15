from yubico_client import Yubico
from yubico_client.yubico_exceptions import YubicoError
import json

with open("creds.json") as json_file:
    env_vars = json.load(json_file)

CLIENT_ID = env_vars.get('CLIENT_ID')
API_KEY = env_vars.get('API_KEY')

def load_users(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def authenticate_user(yubikey_otp, users_dict):
    yubikey_prefix = yubikey_otp[:12]
    return yubikey_prefix in users_dict

if __name__ == "__main__":
    users = load_users('users.json')
    
    yubikey_otp = input("Enter your YubiKey OTP: ")
    
    if authenticate_user(yubikey_otp, users):
        try:
            yubico = Yubico(CLIENT_ID, API_KEY)
            yubikey_otp_verified = yubico.verify(yubikey_otp)
            
            if yubikey_otp_verified:
                print("Authentication successful.")
                username = users[yubikey_otp[:12]]['username']
                print("Username:", username)
            else:
                print("YubiKey OTP verification failed.")
                print("Authentication failed.")
        except YubicoError as e:
            print("Yubico Error:", e)
            print("Authentication failed.")
    else:
        print("Authentication failed.")