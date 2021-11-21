import os
print(os.getcwd())
path = input(":")


if os.path.exists(path) == True:
    print("Папка DataBase уже существует")
elif os.path.exists(path) == False:
    os.mkdir(path)
    print("bot dir")


