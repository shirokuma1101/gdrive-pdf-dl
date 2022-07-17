# gdrive-pdf-dl

## 初めに

- GoogleDriveで保護されている(ReadOnly)PDFをダウンロードするツールです。
注意 データをそのまま取得しているわけではなく、プレビューから画像を取得してPDF化するという方法で取得しています。

- Edgeのプロファイルを使用するので、先にEdgeでGoogle Driveにアクセスできるアカウントでログインしておいてください。
- 指定されたGoogleDriveURLの中にフォルダがある場合は取得されないので、フォルダの中身も欲しい場合は改めてURLを指定してください。

> プロキシサーバーを起動するためにJavaが必要になります。
> java version "1.8.0_331"
> Java(TM) SE Runtime Environment (build 1.8.0_331-b09)
> Java HotSpot(TM) 64-Bit Server VM (build 25.331-b09, mixed mode)
> で動作確認済みです。

取得中はウィンドウが起動しますが仕様です。(headlessだと取得されないため)

mode=0 # プレビュー表示した際に取得されるwebmを保存

mode=1 # PDFに割り当てられた一意のURLにクエリを追加してアクセスした際に取得されるimageを保存 ('webp', 'png', 'jpeg')
