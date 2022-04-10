@powershell -NoProfile -ExecutionPolicy Unrestricted "$s=[scriptblock]::create((gc \"%~f0\"|?{$_.readcount -gt 1})-join\"`n\");&$s" %*&goto:eof

function build() {
    copy ..\src\miniIncrementalSearchFilter.py .
    python setup.py py2exe
#    xcopy /E /I /Y miniIncrementalSearchFilter\*.* ..
#    Remove-Item miniIncrementalSearchFilter -Recurse
    del miniIncrementalSearchFilter.py
}

function install_migemo() {
    pushd miniIncrementalSearchFilter
    curl.exe -L https://raw.githubusercontent.com/cat2151/migemo-auto-install-for-windows/main/install_cmigemo.bat --output install_cmigemo.bat
    cmd /c install_cmigemo.bat
    popd
}

function test() {
    pushd miniIncrementalSearchFilter
    cmd /c miniIncrementalSearchFilter.exe ..\..\src\miniIncrementalSearchFilter.py output.txt
    popd
}

function remove() {
    pushd miniIncrementalSearchFilter
    Remove-Item dict -Recurse
    del migemo.dll
    del cmigemo-default-win64-20110227.zip
    del output.txt
    popd
}

function main() {
    build
    install_migemo
    test
    remove
}


###
main
