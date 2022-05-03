import PyInstaller.__main__


PyInstaller.__main__.run([
    'offline.py',
    '--clean',
    '--onefile',
    ##'--add-data=kodes;kodes',
])
