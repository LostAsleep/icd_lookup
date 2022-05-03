#-------------------------------------------------------------------------------
# Name:        dump_dict
# Purpose:
#
# Author:      phammersen
#
# Created:     03.05.2022
# Copyright:   (c) phammersen 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
ICD_CODE_FILE = "./kodes/icd10gm2022syst_kodes.txt"


def read_file_as_dict(fname):
    global icd_dict
    icd_dict = dict()
    with open(fname, encoding='utf-8') as f:
        for line in f:
            line = line.split(";")
            icd_dict[line[6]] = line[8]

def main():
    read_file_as_dict(ICD_CODE_FILE)
    with open('myfile.txt', 'w') as f:
        print(icd_dict, file=f)

if __name__ == '__main__':
    main()
