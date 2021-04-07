# Flask REST API

## 目的

* テスト用にインスタントに、REST API モックを起動したい欲求から。

## 依存関係

* Flask
* bootstrap css
* sqlite3
* html5
* JavaScript
* click==7.1.2
* itsdangerous==1.1.0
* Jinja2==2.11.3
* MarkupSafe==1.1.1
* Werkzeug==1.0.1

## 仮想環境

```cmd
git clone
python -m venv .
.\Script\activate
pip install -r requirements.txt
flask run -h 0.0.0.0
.\Script\deactivate.bat
```

## Flask 起動方法

```cmd
REM 環境変数はapp.pyを起動対象にしている場合は不要。
set FLASK_APP=C:\Users\z00h230862\vscode\workspace\python\virtual_env\robo_con_rest_api\app.py
.\Script\activate
flask run -h 0.0.0.0
.\Script\deactivate.bat
```

## bootstrap.sh の説明

Linuxプラットフォーム向けの実行スクリプト、Windowsでは不要です。

## schema.sql

Sqliteにテーブルとデータを作成して、リクエストパラメータによって返すデータを変更する。

## 配布パッケージ

* 仮想環境を作成
* 依存ライブラリの整理
* パッケージ実装

```cmd
REM -e 開発モードでパッケージをインストールする
REM '.'は、カレントディレクトリの setup.py を検索して実行する
REM パッケージ実装のカレントディレクトリへ移動して以下を実行
REM 仮想環境を activate したまま
pip install -e .
```

* setup.py の作成

* 配布物作成

```cmd
pip install --upgrade pip setuptools wheel
python setup.py bdist_wheel
```

* uninstall package

```cmd
REM 対象パッケージ名を探す
pip freeze

REM 詳細を表示
pip show <package_name>

pip uninstall <package_name>
```
