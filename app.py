from flask import Flask, render_template, request
import requests
import random
import string

app = Flask(__name__)

def check_email_compromised(email):
    url = "https://webapi.namescan.io/v1/freechecks/email/breaches"
    headers = {
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Version": "2.8.1",
    "Sec-Ch-Ua-Mobile": "?0",
    "Authorization": "Bearer null",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Origin": "https://namescan.io",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://namescan.io/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Sec-Gpc": "1",
    "Priority": "u=1, i"
    }
    data = {
        "email": email,
        "g-recaptcha-response": None
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        breaches = result.get("breaches", [])
        return len(breaches) > 0, breaches
    else:
        return False, []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        is_compromised, compromised_breaches = check_email_compromised(email)
        return render_template('index.html', email=email, is_compromised=is_compromised, compromised_breaches=compromised_breaches)
    return render_template('index.html')

def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(random.choice(characters) for _ in range(length))
    return secure_password

# Test the function
print(generate_secure_password())

@app.route('/generate_password', methods=['POST'])
def generate_password():
    email = request.form['email']
    password = generate_secure_password()  # Generate a secure password
    return render_template('index.html', email=email, is_compromised=True, compromised_breaches=[], password=password)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9856)
