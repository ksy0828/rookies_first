import requests
from bs4 import BeautifulSoup

LOGIN_URL = '<https://login.coupang.com/login/login.pang>'
UserNAME = '45cc@naver.com'
Password = 'young0828!!'

session = requests.Session()

login_data = {
    'kim42348@naver.com' : UserNAME,
    'young0828!!' : Password
}

response = session.post(LOGIN_URL, data=login_data)

if response.status_code == 200:
    print("로그인 성공")
else:
    print("실패")

C_url = 'https://cart.coupang.com/cartView.pang'
response = session.get(C_url)

print(response.content)