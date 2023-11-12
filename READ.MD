#老師的 github
https://github.com/17app001/linebot
https://render.com/
gunicorn trainapp.wsgi

#安裝 django 套件
pip install django

#建立專案
django-admin startproject 專案 app-name

#開啟目錄
open floder

#啟動 Server
python manage.py runserver

#修改語系
LANGUAGE_CODE=''zh-Hant'
TIME_ZONE="Asia/Taipei"

#新增功能
python manage.py startapp main

from django.http import HttpResponse
'DIRS': [os.path.join(BASE_DIR, 'templates')]

python manage.py startapp login

python manage.py startapp test_html

#git 指令 1.安裝 git 2.專案目錄底下 #初始化本地倉庫
-git init

#產生忽略檔案

- .gitignore

#檔案屬性
-U->UnTack
-A->Added
-M->Modified

#加入控管
-git add<filename>
-git add .

- 加入所有版本控管/變動確認

#確認儲存

- git commit -m "異動訊息“
- git config --global user.email "peiyi523@gmail.com"
- git config --global user.name "peiyi"

#檢視狀態

- git status

#檢視 commit log
-git log
-git log --oneline

#綁定遠端倉庫
-git remote add origin https://github.com/peiyi523/linebot2.git
-git remote -v

#推送資料到雲端
git push -u origin master

#複製專案
要從 github 下載自己的 code，在專案資料夾中按右鍵選 Open Git Bash here 打開 git 的終端機
輸入 git clone + 專案的遠端倉庫網址，這樣做才會有.git（開發歷程）

- git clone https://github.com/peiyi523/linebot2

#Channel secret
d36eb1d5f583fdad1ebce24c3f9ace05

#Channel access token
Y9OJcBnITGsZTxe2gMsoQpg4L8r9kqH9G26QgYaQS7bevmm1AXEBUicTyZaMtauBvD8WWX1VYsexjvgVGZKUokil3M+7VfadWYvwUoeekpxecCEiawIuTtm8oYeY7h2qQdmdeDi88gwY0oIOkuS40AdB04t89/1O/w1cDnyilFU=

#同步資料庫
python manage.py migrate

#同步雲端倉庫
-python manage.py migrate

- git push
