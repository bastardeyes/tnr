# tnr

[p1]
tkinterによる文字入力結果を、電光掲示板のようにスクロール出力する。
(モニタまたはVNCでGUIから文字入力)

[p2]
加速度センサによりキャラクタ操作+α。
左で減速、右で加速、上下でピッチ変更。


[実行環境]
Raspberry Pi3 B
Raspbian (2018-06-27-raspbian-stretch)
Python3

[メモ]
・テノリオン本体はFW2.1を入れて、リモートモードにしておく。

・MIDIの出力先設定が都度必要。
aconnectで出力可能なMIDIポートを確認して、下記のコマンド実行
例) aconnect 14:0 20:0

・tkinterはpython3-tkを利用。
=>GUI起動が必要なため、sshから起動するとエラー。VNCなら可能。

・加速度センサは秋月のADXL345。
下記のコマンドでデーモン起動が必要。
sudo pigpiod



