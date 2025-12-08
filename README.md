anaconda 설치

## 32 bit env install, 관리자모드에서 anaconda prompt를 시작한다.
(base) C:\Windows\System32>conda create -n kiwoom_32

(base) C:\Windows\System32>conda activate kiwoom_32

(kiwoom_32) C:\Windows\System32>conda config --env --set subdir win-32

(kiwoom_32) C:\Windows\System32>conda install python=3.10

## vscode 설치 및 설정
vscode 설치 : python plugin, pthon Extension pack, python indent 설치

Anaconda Prompt 로 이동

conda activate kiwoom_32

(kiwoom_32) C:\Windows\System32>pip install pandas --only-binary :all:

(kiwoom_32) C:\Windows\System32>pip install pykiwoom

(kiwoom_32) C:\Windows\System32>pip install "numpy<2.0" --force-reinstall

(kiwoom_32) C:\Users\jack>pip install PyQt5Designer

(kiwoom_32) C:\Users\jack>designer
