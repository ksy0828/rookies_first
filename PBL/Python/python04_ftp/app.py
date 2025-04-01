from flask import Flask, render_template, request
import ftplib

app = Flask(__name__)

#로그인
@app.route('/')
def login():
    return render_template('login.html')

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

            return render_template('index.html', files=files, hostname = hostname)
        except Exception as e:
            return f"로그인 실패: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
