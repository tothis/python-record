打包
```shell
# add-data 分隔符 Windows使用`;` Linux使用`:`
pyinstaller -w \
--add-data=lib:lib \
-i favicon.ico \
main.py
```