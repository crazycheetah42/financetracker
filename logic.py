

def read_file():
    with open("expenses.txt", "r", encoding="utf-8") as file:
        data = file.read()
        return data

def write_file(purpose, amount):
    with open("expenses.txt", "a", encoding="utf-8") as file:
        data = f"{purpose}, {amount}\n"
        file.write(data)