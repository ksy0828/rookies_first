import requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_latest_exchange_rates():
    url = f'https://openexchangerates.org/api/latest.json?app_id={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['rates']
    else:
        print("API 호출 실패:", response.status_code)
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == "USD":
        base_amount = amount
    else:
        base_amount = amount / rates[from_currency]

    converted_amount = base_amount * rates[to_currency]
    return converted_amount

def main():
    rates = get_latest_exchange_rates()
    if rates is None:
        return
    
    print("사용 가능한 통화 코드:", ', '.join(rates.keys()))
    
    from_currency = input("변환할 통화 (예: USD, KRW) : ").upper()
    to_currency = input("목표 통화 (예: USD, KRW) : ").upper()
    amount = float(input(f"{from_currency} 금액을 입력하세요 : "))

    if from_currency in rates and to_currency in rates:
        converted_amount = convert_currency(amount, from_currency, to_currency, rates)
        print(f"{amount} {from_currency}는 {converted_amount:.2f} {to_currency}입니다.")
    else:
        print("유효하지 않은 통화 코드입니다.")

if __name__ == "__main__":
    main()