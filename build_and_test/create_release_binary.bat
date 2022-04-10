@powershell -NoProfile -ExecutionPolicy Unrestricted "$s=[scriptblock]::create((gc \"%~f0\"|?{$_.readcount -gt 1})-join\"`n\");&$s" %*&goto:eof

function copy_files() {
    mkdir miniIncrementalSearchFilter
    xcopy /E /I /Y ..\lib\*.*               miniIncrementalSearchFilter\lib
    copy ..\libcrypto-1_1.dll               miniIncrementalSearchFilter
    copy ..\libffi-7.dll                    miniIncrementalSearchFilter
    copy ..\tcl86t.dll                      miniIncrementalSearchFilter
    copy ..\tk86t.dll                       miniIncrementalSearchFilter
    copy ..\miniIncrementalSearchFilter.exe miniIncrementalSearchFilter
    copy ..\README.md                       miniIncrementalSearchFilter
}

function compress() {
    Compress-Archive -Path miniIncrementalSearchFilter -DestinationPath miniIncrementalSearchFilter.zip
}

function main() {
    copy_files
    compress
    Remove-Item miniIncrementalSearchFilter -Recurse
}


###
main
