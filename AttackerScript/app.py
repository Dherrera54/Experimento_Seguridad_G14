import requests
import logging
from random import randint, random
import json
from datetime import datetime

def random_character():
    return random_character.choices[randint(0, random_character.size)]

random_character.choices = "qwertyuipoasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-_+*!/#$?&"
random_character.size = len(random_character.choices) - 1


def generate_keys(lenght):
    key = ''
    while len(key) < lenght:
        key = key + random_character()
    return key


def build_token():
    return generate_keys(37) + '.' + generate_keys(72) + '.' + generate_keys(42)

def build_altered_token(token):
    size = len(token)-1
    index = randint(0, size)
    current_character = token[index]
    new_character = random_character()
    while new_character == current_character:
        new_character = random_character()
    
    altered_token = token[:index] + new_character
    if index != size:
        altered_token = altered_token + token[index + 1:]
    return altered_token
    

def attack(token):
    choice = randint(0,2)
    
    if choice == 0: # attack without a token
        status_code=requests.get('http://localhost:5000/paciente/1').status_code
        attack_type="Not Token Attack"
        return {"Type": attack_type, "Token used": "-", "Status code": status_code}
    
    if choice == 1: # attack with a random token
        random_token = build_token()
        headers = {"Authorization": "Bearer " + build_token()}
        attack_type="Random Token Attack"
        status_code=requests.get('http://localhost:5000/paciente/1', headers=headers).status_code
        return {"Type":attack_type, "Token used": random_token, "Status code": status_code}
    
    if choice == 2: # attack using an altered token
        altered_token = build_altered_token(token)
        headers = {"Authorization": "Bearer " + altered_token}
        attack_type="Altered Token Attack"
        status_code=requests.get('http://localhost:5000/paciente/1', headers=headers).status_code
        return {"Type": attack_type, "Token used" : altered_token, "Status code":status_code }
        

def correct_request(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get('http://localhost:5000/paciente/1', headers = headers)

if __name__ == '__main__':

    # login with correct credentilas to optain a valid token
    credentials = {"nombre": "testDHG", "contrasena": "TEST1234"}
    data = json.loads(requests.post('http://localhost:5000/login', json = credentials).content)
    correct_token = data["token"]

    attack_count = 0
    total_attends = 100
    attack_probability = 0.5
    successful_attack_count = 0
    iter = 1
    print("Correct token:", correct_token)
    with open('log_attacker.txt', 'w', encoding='utf-8') as log_file:
        while attack_count < 100:
            possible_attack = random() < attack_probability
            if possible_attack:
                attack_count = attack_count + 1
                attack_info =  attack(correct_token)
                log_file.writelines('TimeStamp: {} - {} - Status code: {} - Token: {}\n'.format(datetime.now(),
                                                                                                attack_info["Type"],
                                                                                                attack_info["Status code"], 
                                                                                                attack_info["Token used"]))  
                success = attack_info["Status code"] == 200
                if success:
                    successful_attack_count = successful_attack_count + 1
                print(str(iter) + ")", f"Attack({attack_count}) -> Attack Info: {attack_info} -> {'Passed' if success else 'Not passed'}")
            else:
                print(str(iter)+ ")", "Correct Request -> Responce:",correct_request(correct_token))
            iter = iter + 1 

    print("Execution ended.")
    print("Successfull attacks: ", successful_attack_count)