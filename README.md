# このリポジトリについて
自分でデータセットを構築することは良いことですが、<br>
実際自分で集めて、アノテーションすることは非常に大変です。<br>
せっかくオープンデータセットがあるなら再利用したい。<br>
再利用するためにこのリポジトリを作成しました。<br>

### ◆このリポジトリができること
欲しいクラスの画像とxmlファイルを抽出し、COCO形式からVOC形式に変換することができます。<br>
現状としては、下記の9クラスが映る画像とxmlファイルを抽出します。<br>
"person", "bicycle", "car", "motorbike", "bus", "truck", "traffic light", "bird", "cat", "dog"<br>
※xmlファイルには、上記の9クラスの情報以外は記載されませんので注意してください。<br><br>
変換する他に、必要に応じて作成した機能を使用してください。<br>
### ◆他の機能
・VOC形式に変更した際にバウンディングボックスが正しく物体を囲めているか確認するDebug機能。<br>
・欲しい各クラスの出現数を可視化する機能。(用意するデータの数など検討する際に使用。)<br>
・train.txtとval.txtに分ける機能。<br>
　などがあります。<br>
### ◆使い方
後で追加します（まだ説明が不十分です）。<br>
・coco datasetだけで学習させる場合(欲しいデータだけ！)<br>
　python main.py<br><br>
・coco dataset以外も混ぜてやりたい場合<br>
　1.最初にAnnotationsフォルダとJPEGImagesフォルダを作成<br>
　2.自分が作成したアノテーションデータと画像をAnnotationsフォルダとJPEGImagesフォルダに格納する。<br>
　3.pyhon main.py<br>

・equalize_data_number.pyは学習データの数を均等化するためにしようする。<br>
後で、equalize_data_number.pyのコードの整理をする。<br>
