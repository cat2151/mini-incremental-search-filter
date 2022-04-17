#!/usr/bin/env python3
# インクリメンタルサーチ絞り込み
#   入力ファイルと入力欄を元にインクリメンタルサーチして絞り込みリストを表示し、ENTERで決定した1行をファイルに出力する
import tkinter as tk
import re
import argparse
import cmigemo
import sys
import winreg

# インクリメンタルサーチで絞り込む
def inputArea_onChange(event):
    pattern = event.widget.get()
    if pattern == '':
        listBox_ini2(listBox) # Delete等で入力欄が空になった場合用
        return

    # patternで絞り込む
    global matchedIndexList
    if args.andsearch:
        (filtered, matchedIndexList) = createMultiFilteredLines(pattern.split(" "), lines) # space区切りでAND検索する
    else:
        (filtered, matchedIndexList) = createMultiFilteredLines([pattern], lines) # spaceを含む一つの文字列として検索する

    # listBoxに出力する
    listBox.delete(0, 'end')
    for line in filtered:
        listBox.insert('end', line)
    if len(filtered) >= g_lineNumber:
        listBox.select_set(g_lineNumber)
    else:
        # 最後尾等を選んでいて、絞り込み結果で最後尾が空行になった場合等に、最終行を選択しなおす（選択が消えると見た目がわかりづらいので）
        listBox.select_set(len(filtered) - 1)

# patternsの個数ぶん絞り込む
def createMultiFilteredLines(patterns, lines):
    filtered = lines
    global matchedIndexList
    for i in range(0, len(patterns)):
        if not patterns[i] == "":
            (filtered, matchedIndexList) = createSearchedLines(patterns[i], filtered)
    return (filtered, matchedIndexList)

# linesをpatternで絞り込みし、結果listを得る
def createSearchedLines(pattern, lines):
    if args.migemo:
        pattern = migemo.query(pattern)
    outList = []
    matchedIndexList = []
    i = 0
    for line in lines:
        if args.regex or args.migemo:
            result = re.search(pattern, line, flags=re.IGNORECASE)
            if result:
                outList.append(line)
                matchedIndexList.append(i)
        else:
            if pattern.lower() in line.lower():
                outList.append(line)
                matchedIndexList.append(i)
        i += 1
    return (outList, matchedIndexList)

def clamp(v, min, max):
    if v < min:
        return min
    elif v > max:
        return max
    else:
        return v

def printAtDebug(v):
    if args.debug:
        print(v)

def readFileToLines(filename):
    with open(filename, encoding=args.encode) as f:
        return f.read().splitlines()

def writeFileFromLine(filename, line):
    with open(filename, mode = "w", newline="\n", encoding=args.encode) as f:
        f.write(line)
        f.write("\r")
        f.write("\n")

# inputArea用
class ModifiedEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.sv = tk.StringVar()
        self.sv.trace('w',self.var_changed)
        self.configure(textvariable = self.sv)
    def var_changed(self, *args):
        if args[0] == self.sv._name:
            s = self.sv.get()
            self.event_generate("<<TextModified>>")

def inputArea_init(uiRoot, args):
    inputArea = ModifiedEntry(uiRoot, width=args.width)
    if isWindowsDarkMode():
        inputArea.configure(fg = '#F8F8F2', bg = '#272822')
    inputArea.grid()
    inputArea.bind("<<TextModified>>", inputArea_onChange)
    inputArea.bind('<Key-Up>', listbox_selection_up)
    inputArea.bind('<Key-Down>', listbox_selection_down)
    inputArea.bind('<Key-Escape>', ui_exitByEsc)
    inputArea.bind('<Key-Return>', ui_exitByEnterKey) # Enter
    inputArea.bind('<Key-Prior>', listbox_selection_top) # Page Up
    inputArea.bind('<Key-Next>', listbox_selection_bottom) # Page Down
    inputArea.focus_set()
    return inputArea

def listbox_selection_up(event):
    listbox_select_line_updown(-1)

def listbox_selection_down(event):
    listbox_select_line_updown(1)

def listbox_selection_top(event):
    listbox_select_line_updown(-args.height)

def listbox_selection_bottom(event):
    listbox_select_line_updown(args.height)

def listbox_select_line_updown(updown):
    global g_lineNumber
    if not listBox.size(): # 空のlist用
        return
    g_lineNumber += updown
    g_lineNumber = clamp(g_lineNumber, 0, listBox.size() - 1)
    listBox.select_clear(0, 'end')
    listBox.select_set(g_lineNumber)
    listBox.see(g_lineNumber) # 選択した行が画面内に入る用

def listbox_focusIn(event):
    inputArea.focus_set()

def listBox_init(uiRoot, args):
    listBox = tk.Listbox(uiRoot, width=args.width, height=args.height)
    if isWindowsDarkMode():
        listBox.configure(fg = '#F8F8F2', bg = '#272822')
    listBox.grid()
    listBox.bind('<FocusIn>', listbox_focusIn)
    listBox_ini2(listBox)
    return listBox

def listBox_ini2(listBox):
    # lines先頭が表示され、先頭行を選択した状態、に初期化する
    listBox.delete(0, 'end')
    for i in range(0, len(lines)):
        listBox.insert('end', lines[i])
        matchedIndexList.append(i)
    listBox.select_clear(0, 'end')
    listBox.select_set(0)

def ui_exitByEsc(event):
    uiRoot.title("Escape!")
    sys.exit()

def ui_exitByEnterKey(event):
    if len(matchedIndexList):
        uiRoot.title("OK!")
        lineNumber = matchedIndexList[listBox.curselection()[0]]
        line = listBox.selection_get()
        printAtDebug(lineNumber)
        printAtDebug(line)
        writeFileFromLine(args.output, line)
    else:
        uiRoot.title("Did not hit!")
    sys.exit()

def isWindowsDarkMode():
    key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    data, regtype = winreg.QueryValueEx(key, "AppsUseLightTheme")
    winreg.CloseKey(key)
    if data == 0:
        return True
    else:
        return False

def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--encode', help='[utf_8] / cp932', default='utf_8')
    parser.add_argument('--andsearch', action='store_true')
    parser.add_argument('--regex', action='store_true')
    parser.add_argument('--migemo')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--width', default=80, type=int)
    parser.add_argument('--height', default=10, type=int)
    parser.add_argument('--alpha', default=1, type=float)
    args = parser.parse_args()
    return args


###
args = parseArg()
lines = readFileToLines(args.input)
printAtDebug(lines)
g_lineNumber = 0
matchedIndexList = []

uiRoot = tk.Tk()
if args.alpha:
    uiRoot.attributes("-alpha", args.alpha)
inputArea = inputArea_init(uiRoot, args)
listBox = listBox_init(uiRoot, args)

if args.migemo:
    migemo = cmigemo.Migemo(args.migemo)
    if migemo.query('hoge') == 'hoge': # roma2hira.dat が読めない、シンボリックリンク実体が日本語名ディレクトリにある等、いろいろな原因がありうる。思ったように動かない原因が何かわからない状態より、問題があればすぐ動作を停止して問題があることを明確にするほうを優先する。
        writeFileFromLine("miniIncrementalSearchFilter_error.log", "migemo init error") # 用途の都合で、標準出力等を得られないことが多いため、苦肉の策
        sys.exit(1)

uiRoot.mainloop()
