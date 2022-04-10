# mini incremental search filter

入力をインクリメンタルサーチして絞り込みリストを表示し、選んだ1行を出力します。

# Features
- AND検索モード --andsearch
- 正規表現モード --regex
- migemoモード --migemo
- 文字コード指定 --encode （utf_8 や cp932 を選べます）
- 行数や桁数を指定 --width, --height

# Requirement
- Windows 64bit
- 入力ファイルを作るscript（例えばテキストエディタのマクロの一覧や機能の一覧を作る）
- 出力ファイルを元に動くscript（例えば選んだマクロや機能を実行する）
- 実行からウィンドウ表示まで待つこと（ウィンドウが出る前にタイプするとウィンドウがアクティブ化しません）
- 遊び心

# Usage
- 例えば :
  - 後述のmigemoをインストールします（1行でインストールできます）
  - 以下のコマンドを実行します :
    ```
    miniIncrementalSearchFilter.exe README.md out.txt --andsearch --migemo dict\migemo-dict --width 100 --height 50
    ```
  - 任意の文字をタイプし、インクリメンタルサーチで絞り込んで、任意の行を選びます
  - ENTERを押します
  - `out.txt` を開き、選んだ行が出力されていることを確認します
- 任意のアプリの拡張scriptに（例えばテキストエディタのマクロに）組み込んでコマンドパレットのように使えるか遊びましょう
- 正規表現モードは、目的を果たせる正規表現パターンは何か？を探すときに使えるかもしれませんし、その用途ならほかにもっと向くものがあるかもしれません

# migemo
- migemoをインストールするときは以下をコマンドプロンプトに貼り付けてENTERが楽です。
```
curl.exe -L https://raw.githubusercontent.com/cat2151/migemo-auto-install-for-windows/main/install_cmigemo.bat --output install_cmigemo.bat && install_cmigemo.bat
```

# 起動を速くするには
- VC++で作れば高速そうです。参考は [afxfazzy](https://github.com/yuratomo/afxtools)
- テキストエディタのプラグインとしてDLLで作れば高速そうです。

# 名前が長すぎて扱いづらい
- もしVC++版やテキストエディタのプラグイン版を作れたらそのときはより短い名称を考えるかもしれません。
