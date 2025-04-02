# 지정된 디렉 [static]의 모든 파일을 순회하며 zip압축
# 압축 파일 이름은 "디렉이름_현재날짜"
# 압축 후 zip을 FTP서버로 전송
# 네트워크지연이나 파일 크기에 따른 전송시간 고려 
# - 적절한 타이밍에 자동 실행

from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import ftplib
import shutil
import time

from datetime import datetime

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

#로그인
@app.route('/')
def login():
    return render_template('login.html')

# ftp파일목록 리스트화
def get_ftp_files(ftp):
    files_info = []
    ftp.retrlines('LIST', files_info.append)
    
    files = []
    for file_info in files_info:
        parts = file_info.split()
        file_name = parts[-1]
        file_size = parts[4]
        file_date = ' '.join(parts[5:8])
        file_path = f"{ftp.host}/{file_name}" 
        files.append({
            'name': file_name,
            'size': file_size,
            'date': file_date,
            'path': file_path
        })
    
    return files

#ftp파일목록 가져오기
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['HostIP']
        username = request.form['UserID']
        password = request.form['UserPW']

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)

            files = get_ftp_files(ftp)
            ftp.quit() 

            return render_template('index.html', files=files, hostname=hostname, user_id=username, user_pw=password)
        except Exception as e:
            return f"로그인 실패: {str(e)}"

#압축하고 FTP로 업로드
def zip_and_upload(ftp, user_id, user_pw):
    current_date = datetime.now().strftime('%Y%m%d')
    zip_filename = f'static_{current_date}.zip'
    
    shutil.make_archive(zip_filename[:-4], 'zip', 'static')
    
    with open(zip_filename, 'rb') as file:
        ftp.storbinary(f'STOR {zip_filename}', file)

#업로드
@app.route('/upload', methods=['POST'])
def upload():
    hostname = request.form['HostIP']
    username = request.form['UserID']
    password = request.form['UserPW']

    try:
        ftp = ftplib.FTP(hostname)
        ftp.login(username, password)

        time.sleep(5)

        zip_and_upload(ftp, username, password)
        ftp.quit()

        return '''
            <script>
                alert("파일 업로드 성공");
                window.history.back();
            </script>
        '''
    except Exception as e:
        return f'''
            <script>
                alert("파일 업로드 실패: {str(e)}");
                window.history.back();
            </script>
        '''

#특정시간에 자동전송 
def scheduled_upload():
    return upload() 

scheduler.add_job(scheduled_upload, 'cron', hour=9, minute=0)

if __name__ == '__main__':
    app.run(debug=True)
