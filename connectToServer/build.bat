echo off
IF NOT EXIST build mkdir build
cd build
python -m PyInstaller -w -F ../connectToServer.py
cd ..
copy /y build\dist\connectToServer.exe
rmdir /s /q build
