# coding: utf-8

import json
import os
import sqlite3
import werkzeug

from contextlib import closing
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    dict(DATABASE=os.path.join(app.root_path, 'test.db'),
         SECRET_KEY='development key',
         USERNAME='John',
         PASSWORD='TheyLive1988Obey',
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


@app.route("/api/upload", methods=['POST'])
def UploadAnything():
    if request.method == 'POST':
        fileBuff = request.files.get('facefile')

        if fileBuff is None:
            return jsonify({'message': 'Image file required.'}), 400
        elif 'image/gif' != fileBuff.mimetype and 'image/png' != fileBuff.mimetype and 'image/jpeg' != fileBuff.mimetype:
            return jsonify({
                'message':
                'Request file type is image and extend for gif or png or jpeg.'
            }), 415
        filename = fileBuff.filename
        if '' == filename:
            return jsonify({'message': 'enter a filename.'}), 415

        saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") + \
            werkzeug.utils.secure_filename(filename)
        fileBuff.save(os.path.join(app.config['UPLOAD_FOLDER'], saveFileName))

        return 'Upload OK.', 200
        # return redirect(url_for('hello'))
