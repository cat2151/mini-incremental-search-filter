@powershell -NoProfile -ExecutionPolicy Unrestricted "$s=[scriptblock]::create((gc \"%~f0\"|?{$_.readcount -gt 1})-join\"`n\");&$s" %*&goto:eof

function copy_files() {
    copy ..\README.md miniIncrementalSearchFilter
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
