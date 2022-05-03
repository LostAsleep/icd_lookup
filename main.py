#-------------------------------------------------------------------------------
# Name:        icd_test
# Purpose:
#
# Author:      phammersen
#
# Created:     29.04.2022
# Copyright:   (c) phammersen 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
import pyperclip
import pymsgbox
import time
from global_hotkeys import *


TEST_CODE = "S 82.28"
is_alive = True


def clean_up_code(icd_str):
    code = "".join(icd_str.split())
    code = "-".join(code.split("."))
    if len(code) == 5:
        return code
    if len(code) > 6:
        code = code[:6]
    if len(code) == 6:
        if code[-1] in "0123456789":
            return code
        return code[0:5]
    return code


def search_icd_code(icd_code):
    code_to_search = clean_up_code(icd_code)
    r = requests.get(f"https://gesund.bund.de/icd-code-suche/{code_to_search}")
    icd_descr = ""

    for line in r.text.split("\n"):
        if 'aria-label="Service: ICD-Code' in line:
            icd_descr = line

    icd_descr = icd_descr.split()
    icd_descr = " ".join(icd_descr[2:])
    icd_descr = icd_descr[:-2]

    if len(icd_descr) <= 1:
        icd_descr = "Kein ICD Code gefunden."
        print(icd_descr)
        return icd_descr

    # If valid, copy back a usable ICD Code to the clipboard
    pyperclip.copy(icd_descr.split(":")[0])

    print(icd_descr)
    return icd_descr


def pop_up_message():
    description = search_icd_code(pyperclip.paste())
    pymsgbox.alert(text=f"{description}", title="ICD CODE", button='OK')


def exit_application():
    global is_alive
    stop_checking_hotkeys()
    is_alive = False


def main():
    global is_alive

    bindings = [
    [["control", "y"], None, pop_up_message],
    [["control", "shift", "9"], None, exit_application],
    ]

    register_hotkeys(bindings)

    # start listening for keypresses
    start_checking_hotkeys()

    # Keep waiting until the user presses the exit_application keybinding.
    # Note that the hotkey listener will exit when the main thread does.
    while is_alive:
        time.sleep(0.1)


if __name__ == '__main__':
    print("Drücke STRG + y um den ICD Code nachzuschlagen,")
    print("der in der Zwischenablage gespeichert ist.")
    print("(Voraussetzung ist eine bestehende Internetverbindung.)")
    main()
