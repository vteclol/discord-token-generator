import requests
import json
import time
import random
import string

letters = string.ascii_lowercase

while True:

    proxy = set()

    with open("proxies.txt", "r") as f:
        file_lines1 = f.readlines()
        for line1 in file_lines1:
            proxy.add(line1.strip())

    proxiesRandom = {
        'https': 'http://'+random.choice(list(proxy))
    }

    payload = {
        "clientKey": "211bd40ffc904ede05409e2f81d73f29",
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": "https://discord.com",
            "websiteKey": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34"
        }
    }

    sendTask = requests.post('http://api.anti-captcha.com/createTask', proxies=proxiesRandom, data=json.dumps(payload))

    taskId = json.loads(sendTask.content)

    taskIdResult = taskId["taskId"]

    print("[!] Created Task |", taskIdResult)

#####################################################################################

    time.sleep(50)


########## GET RESULT ###########################################################

    try:

        payload = {
            "clientKey": "YOUR_ANTICAPTCHA_API_KEY_HERE",
            "taskId": taskIdResult
        }

        getTask = requests.post('http://api.anti-captcha.com/getTaskResult', data=json.dumps(payload))

        response = json.loads(getTask.content)

        gToken = response['solution']['gRecaptchaResponse']

    except KeyError:

        print("[!] Couldn't get solution from Anti-Captcha Task ID within 50 seconds skipping...")

        continue


################# SEND REQUEST TO DISCORD ########################

    try:
        proxiesRandomDC = {
            'https': 'http://'+random.choice(list(proxy))
        }  

        headers2 = {
            'Content-Type': "application/json",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        }

        payloadDC = {
            'captcha_key': gToken,
            'username': "".join(random.choice(letters) for i in range(10))
        }

        register = requests.post('https://discord.com/api/v9/auth/register', proxies=proxiesRandomDC, headers=headers2, data=json.dumps(payloadDC))

        getToken = json.loads(register.content)

        getToken2 = getToken['token']

        print("[!] Account created |", getToken2)

        with open('./output.txt', 'a') as f1:
            f1.write(getToken2 + "\n")

    except requests.exceptions.ProxyError:
        print("[!] Dead/Proxy Error")
        continue
    except KeyError:
        print('[!] Error skipping...')
        continue
    except register.status_code == 429:
        ratelimit = getToken['retry_after']
        print(f"[!] Discord IP Ratelimit for {ratelimit} seconds")
        continue

