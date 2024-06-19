import pandas as pd

def read_xls_file(path: str) -> list:
    """Функция, которая считывает финансовые операции с XLSX-файла"""
    xls_file = pd.read_excel(path)
    xls_dict = xls_file.to_dict(orient="records")
    return xls_dict

print(read_xls_file("C:\\Users\\Sonya\\lecture\\coursework\\data\\operations.xls"))