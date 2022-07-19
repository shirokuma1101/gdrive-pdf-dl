# gdrive-pdf-dl

GoogleDriveで保護されている(ReadOnly)PDFをダウンロードするツールです。

__⚠️ 生データを取得しているわけではありません。詳しくは[詳細](#詳細)__

## 使い方

Edgeのプロファイルを使用するので、先にEdgeで指定するGoogleDriveURLにアクセスできるアカウントでログインしておいてください。またフォルダの中身も取得したい場合は改めてフォルダのURLを指定してください。

プロキシサーバーを起動するためにJavaが必要になります。
> java version "1.8.0_331"  
> Java(TM) SE Runtime Environment (build 1.8.0_331-b09)  
> Java HotSpot(TM) 64-Bit Server VM (build 25.331-b09, mixed mode)

で動作確認済みです。

取得中はウィンドウが起動しますが仕様です。(headlessだと取得されないため)

| key | info | e.g. |
| - | - | - |
| proxy_bat_path | プロキシサーバーを実行するbatファイル | bin\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat |
| edge_driver_path | Edgeドライバー | bin\edgedriver_win64\msedgedriver.exe |
| edge_profile_path | GoogleDriveURLにアクセスできるEdge用プロファイル | C:\Users\{userdata}\AppData\Local\Microsoft\Edge\User Data\Default |
| gdrive_url | 取得したいGoogleDriveURL | url |
| mime_type | 拡張子 png jpeg webm | png |
| mode | モード q or s sの場合は800px webm固定(おそらく) | q |
| width | 横幅のピクセル | 800 |
| rendering_waiting_sec | レンダリング待ち時間 横幅が大きいと値を増やす必要がある | 2 |
| access_waiting_sec | アクセス待ち時間 アクセスに時間が掛かる場合は増やす | 5 |
| output_dir | 出力ディレクトリ | .\output |

## 詳細

Proxyを介してharを取得することで、プレビュー表示時のbase64化されたデータをでコードして画像化しています。

なのでテキストやオリジナル画像データなどは取得できません。あくまでプレビュー表示時の解像度の画像をPDF化しています。
