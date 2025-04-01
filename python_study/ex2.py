import requests
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("일단 실행이 되는지 확인")

# 로그인 URL
LOGIN_URL = "https://nid.naver.com/nidlogin.login"
CART_URL = "https://shopping.naver.com/cart"

# 세션 시작
session = requests.Session()
header_info = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36'}

# 로그인 데이터
login_data = {
    'id_error_msg': 'kim42348',  # 아이디 필드
    'pw_error_msg': 'young0828!'  # 비밀번호 필드
}

# 로그인 시도
response = session.post(CART_URL, data=login_data, headers=header_info)

# 로그인 성공 여부 확인
if response.ok:
    print("로그인 성공!")
    
# 장바구니 페이지 요청
    cart_response = session.get(CART_URL, headers=header_info, verify=False)
    
    if cart_response.ok:

        print("장바구니 페이지 요청 성공!")
        # HTML 출력으로 확인
        print(cart_response.text) 
        # BeautifulSoup을 사용하여 장바구니 데이터 파싱
        soup = BeautifulSoup(cart_response.text, 'html.parser')
        
        # 장바구니 아이템 추출 (예시로 전체 HTML 출력)
        cart_items = soup.select('#app > div > div.contents--2E6XJtdAJn > div > div > div.store_content--1atEHLZlpd > div:nth-child(1) > div > div > div.info--2I2hfPeviI > div > div > div > div:nth-child(1) > div > div.inner--1emXN2Ic_f > a')
        for item in cart_items:
            product_name = item.select_one('#app > div > div.contents--2E6XJtdAJn > div > div > div.store_content--1atEHLZlpd > div:nth-child(1) > div > div > div.info--2I2hfPeviI > div > div > div > div:nth-child(2) > div > div')
            if product_name:
                print(product_name.get_text(strip=True))
    else:
        print("장바구니 요청 실패.")
else:
    print("로그인 실패.")
