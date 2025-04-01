# 숫자 맞추기 게임
# 게임 시작 시 컴퓨터는 1부터 100 사이의 임의의 숫자 선택
# 사용자가 숫자를 추측하여 입력
# 컴퓨터는 사용자의 입력이 정답보다 높은지 낮은지를 알려줌
# 사용자가 맞출때까지 반복 / 몇 번 만에 맞혔는지 결과 도출

import random
secretNum = random.randint(1,100)
print("1부터 100까지 제가 생각하는 숫자를 맞추세요.")
count = 0

while True:
    guess = int(input("숫자를 입력하세요."))
    count = count +1

    if guess > secretNum:
        print("더 낮습니다.")
    elif guess < secretNum:
        print("더 높습니다.")
    else:
        print(f"정답입니다! {count}번 만에 맞추셨습니다.")
        break

