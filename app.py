# coding: utf-8

import os
import sqlite3
# import werkzeug
import json

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from contextlib import closing
# from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    dict(DATABASE=os.path.join(app.root_path, 'test.db'),
         SECRET_KEY='development key',
         USERNAME='hoge',
         PASSWORD='******',
         MAX_CONTENT_LENGTH=5 * 1024 * 1024,
         UPLOAD_FOLDER='./upload',
         ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif', 'csv'])))
app.config.from_envvar('FLASKR_SETTINGS ', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.text_factory = str
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """
    schema.sql ファイルを変更することでテストテーブルとデータをカスタマイズ可能
    """
    with closing(connect_db()) as db:
        # with app.open_resource('schema.sql', 'r') as sqlFile:  日本語が使えない
        with open('schema.sql', 'r', encoding='utf8') as sqlFile:
            db.cursor().executescript(sqlFile.read())
        db.commit()


@app.route("/initdb")
def InitializationDb():
    """
    sqliteファイルにDDLとテストデータを登録する
    """
    init_db()
    return render_template('index.html')


@app.route("/api/GetUserInfo", methods=['POST'])
def GetUserInformation():
    """
    作業者情報取得サービス
    """
    if request.method == 'POST':
        rqjson = request.get_json()
        userID = rqjson['UserId']
        dbconn = connect_db()

        retval = {"Result": 1, "ErrMess": "error occurred.",
                  "UserName": '', "Tateya": '', "KouteiNo": '', "KouteiName": ''}

        if (userID == "9999"):
            return json.dumps(retval), 500
        else:
            for row in dbconn.execute('SELECT * FROM users WHERE UserId=?', userID):
                retval["Result"] = 0
                retval["ErrMess"] = ''
                retval["UserName"] = row[1]
                retval["Tateya"] = row[2]
                retval["KouteiNo"] = row[3]
                retval["KouteiName"] = row[4]
            return json.dumps(retval, ensure_ascii=False), 200
    else:
        return 'Method Not Allowed.', 405


@app.route("/api/MakeCheckList", methods=['POST'])
def MakeCheckList():
    """
    チェックリスト作成サービス
    """
    retval = {"Result": 1, "ErrMess": "error occured.",
              "TotalCheckNum": None, "TotalRemainNum": None, "KouteiCheckNum": None, "KouteiRemainNum": None, "MismatchNum": None}

    if request.method == 'POST':
        rqjson = request.get_json()
        osno = rqjson['Osno']
        koutei_no = rqjson['KouteiNo']
        list_remake_flag = int(rqjson['ListRemakeFlag'])
        dbconn = connect_db()

        # ecoh_back = {'Osno': None, 'KouteiNo': None, 'ListRenakeFlag': None}
        # ecoh_back['Osno'] = osno
        # ecoh_back['KouteiNo'] = koutei_no
        # ecoh_back['ListRenakeFlag'] = list_remake_flag
        # return json.dumps(ecoh_back, ensure_ascii=False), 200

        rescode: int = 0
        for row in dbconn.execute('SELECT * FROM checklist WHERE Osno=? AND KouteiNo=? AND ListRemakeFlag=?', (osno, koutei_no, list_remake_flag)):
            retval['Result'] = row[3]
            rescode = int(row[3])
            retval['ErrMess'] = row[4]
            retval['TotalCheckNum'] = row[5]
            retval['TotalRemainNum'] = row[6]
            retval['KouteiCheckNum'] = row[7]
            retval['KouteiRemainNum'] = row[8]
            retval['MismatchNum'] = row[9]

        if (rescode == 0):
            return json.dumps(retval, ensure_ascii=False), 200
        else:
            return json.dumps(retval, ensure_ascii=False), 500
    else:
        return 'Method Not Allowed.', 405