#-------------------------------------------------------------------------------
# Name:        ICD_Codes_offline
# Purpose:
#
# Author:      phammersen
#
# Created:     03.05.2022
# Copyright:   (c) phammersen 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pyperclip
import pymsgbox
import time
from global_hotkeys import *
from icd_dict import icd_dict


is_alive = True
##ICD_CODE_FILE = "./kodes/icd10gm2022syst_kodes.txt"


##def read_file_as_dict(fname):
##    global icd_dict
##    icd_dict = dict()
##    with open(fname, encoding='utf-8') as f:
##        for line in f:
##            line = line.split(";")
##            icd_dict[line[6]] = line[8]


def clean_up_code(icd_str):
    code = "".join(icd_str.split())
    code = code.upper()
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
    global icd_dict
    code_to_search = clean_up_code(icd_code)

    if icd_dict.get(code_to_search) is not None:
        pyperclip.copy(code_to_search)
        descr_string = f"{code_to_search}: {icd_dict[code_to_search]}"
        return descr_string
    else:
        return "Kein ICD Code gefunden."


def pop_up_message():
    description = search_icd_code(pyperclip.paste())
    print(description)
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
    ##read_file_as_dict(ICD_CODE_FILE)
    print("Drücke STRG + y um den ICD Code nachzuschlagen, der in der Zwischenablage gespeichert ist.")
    print("Dieses Programm verwendet die ICD-10-GM Version 2022.")
    print("Heruntergeladen am 03.05.2022.")
    print("------------------------------\n")
    main()
