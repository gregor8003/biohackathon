import os


for folder, subfolders, files in os.walk(os.getcwd()):
    for file in files:
        filepath = os.path.join(os.path.abspath(folder), file)
        print(filepath)
