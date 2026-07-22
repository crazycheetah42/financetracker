

def read_file():
    with open("expenses.txt", "r", encoding="utf-8") as file:
        return file.read()

def write_file(data):
    with open("expenses.txt", "w", encoding="utf-8") as file:
        file.write(data)