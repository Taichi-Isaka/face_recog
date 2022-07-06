# face_recognition app

### インストール
pip install cmake  
pip install dlib  
pip install face-recognition  
pip install numpy  
pip install opencv-python  
pip install streamlit  

windowsでdlibを使うには, visual studioが必要
https://visualstudio.microsoft.com/ja/downloads/

のインストーラーからC++によるデスクトップ開発を選択して, Winsows用C++CMakeツールにチェックしてインストール
![vs](https://user-images.githubusercontent.com/102122652/177480176-a6390780-28c4-4571-9043-48202d367528.png)

### 実行
face_recog.pyがあるフォルダに移動して, 
streamlit run fare_recog.pyを実行

### 使い方
名前を入力して, 登録する.
登録した顔があると名前が表示される. 
log.csvにログが記録
