def mParser(path):
    f = open(path,'r')
    lines = f.readlines() # matriz com o ficheiro lido

    res = []

    for sub in lines:
        res.append(sub.replace("\n", ""))

    l = len(lines)
    c = len(lines[0])

    f.close()

    return res