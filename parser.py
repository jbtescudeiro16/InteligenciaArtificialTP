class parser:

    def create_table(l, c, lines):
        for linha in lines:
            for pos in linha:
                if pos == 'X':
                    print('?')
                else:
                    if pos == '-':
                        print('??')
                    else:
                        print('???')



    #main func do parser
    def mParser():
        f = open('circuitos.txt','r')
        lines = f.readlines() # matriz com o ficheiro lido

        l = len(lines)
        c = len(lines[0])

        f.close()



