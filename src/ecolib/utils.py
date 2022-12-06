from typing import List, Iterable
import os


class Utils:

    @staticmethod
    def mountQuerysStringifiedArrays(arr, QUERY_SIZE) -> List[str]:
        arr_s = len(arr)
        str_arr = []

        if arr_s >= QUERY_SIZE:  # BLOCO 1
            temp_str = ""
            for i in range(0, QUERY_SIZE):
                temp_str += arr[0] + ","
                arr.pop(0)
            if temp_str[-1] == ",": temp_str = temp_str[0:len(temp_str) - 1]
            str_arr.append(temp_str)

        if arr_s < QUERY_SIZE:  # BLOCO 2
            temp_str = ""
            for i in range(0, arr_s):
                temp_str += arr[0] + ","
                arr.pop(0)
            if temp_str[-1] == ",": temp_str = temp_str[0:len(temp_str)-1]
            str_arr.append(temp_str)

        # Podia juntar os dois blocos [1 e 2]? Sim, podia, mas ia ter de fazer algo como:
        # limite = None; if arr_s >= QUERY_SIZE: limite = QUERY_SIZE else: limite = arr_s
        # E depois fica menos intuitivo

        if len(arr) > 0:
            return str_arr + Utils.mountQuerysStringifiedArrays(arr, QUERY_SIZE)
        else:
            return str_arr

    @staticmethod
    def getParentPathOfFile(file):
        path = os.path.abspath(file)
        i = path.split("\\")
        newPath = ""
        for j in range(0, len(i) - 1):
            newPath += i[j] + "\\"
        return newPath

    @staticmethod
    def getParentPathOfPath(path):
        dirs = path.split("\\")
        newpath = ""
        for j in range(0, len(dirs) - 2):
            newpath += dirs[j] + "\\"
        return newpath

    @staticmethod
    def dismountStringifiedArray(sarr: str) -> List[str]:
        return sarr.split(",")

    @staticmethod
    def genMissingParamsErrorMessage(param_keys_required: list, param_keys_gotten: list):
        missing_params = []
        for pr in param_keys_required:
            if not (pr in param_keys_gotten):
                missing_params.append(pr)

        return f"Missing fields: {missing_params}"

    @staticmethod
    def isAllAinB(a: list, b: list):
        return all(elem in b for elem in a)

    @staticmethod
    def a_minus_b (a: Iterable, b: Iterable):
        return [ia for ia in a if ia not in b]  # O(n)

