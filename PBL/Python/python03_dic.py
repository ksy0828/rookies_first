import os, time
import re 
from datetime import datetime

DIR_PATH = "uploads"

#기존 파일 목록 가져오기
pre_file = set(os.listdir(DIR_PATH)) #그냥하면 오류..set으로 타입 변환
print(','.join(pre_file))

#파일이  새로 들어오는지 모니터링
while True:
    #시간 정보
    now = datetime.now() 
    day = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H:%M:%S")

    current_file = set(os.listdir(DIR_PATH))
    result_diff = current_file - pre_file
    
    for file_name in result_diff:
        file_path = os.path.join(DIR_PATH, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            file_detected = False  # 새 파일 감지 여부

            for index, line in enumerate(lines):
                if not file_detected:
                    print(f"\n 새 파일 감지 : {file_name}, 시간 : {hour}")
                    file_detected = True  # 감지 메시지 출력 후 플래그 세팅
                
                if line.startswith("#") or line.startswith("//"):
                    print(f"\n주석 {file_path} (line: {index + 1}) {line}")
            
                if re.search(r'\d{6}\s*[-]\s*\d{7}', line): # \s*은 공백이 포함되어 있을 경우까지 찾기
                    print(f"\n주민번호 {file_path} (line: {index + 1}) {line}")

                if re.search(r'[\w\.-]+@[\w\.-]+', line):
                    print(f"\n이메일 {file_path} (line: {index + 1}) {line}") 

    print("모니터링 중..")
    pre_file = current_file #차이점을 기존파일로 업데이트
    time.sleep(2)