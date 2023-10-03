@echo off
echo Преобразование Python скрипта в исполняемый файл...
pyinstaller --onefile --windowed --icon=qiyanka.ico .\qiyana.py
echo Готово! Исполняемый файл создан. Погладь Киану.
pause