import argparse
import sqlite3
from tabulate import tabulate




def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("create table if not exists Buchverwaltung(Buch text, Autor text, Erscheinungsjahr integer, PRIMARY KEY(Buch, Autor, Erscheinungsjahr))")
    con.commit()
    return cursorObj



def interface():
    parser = argparse.ArgumentParser(
    prog='Buchverwaltung',
    description='Geben sie an welche Bücher sie hinzufügen, löschen oder listen wollen.',
    epilog='-t Titel, -a Autor, -y Jahr')

    parser.add_argument("command")
    parser.add_argument('-t', '--titel')
    parser.add_argument('-a', '--author')
    parser.add_argument('-y', '--year')
    args = parser.parse_args()
    return args


def addbook(cursorObj, con, titel, author, year): 
    data = [(titel), (author), (year)]
    data1 = titel
    data2 = author
    data3 = year
    cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Buch=? AND Autor=? AND Erscheinungsjahr=?', [data1, data2, data3])
    fetching = cursorObj.fetchall()
    if fetching:
        print("Dieses Buch existiert bereits")
    else:    
        cursorObj.execute('INSERT INTO Buchverwaltung(Buch, Autor, Erscheinungsjahr) VALUES(?, ?, ?)', data)   
        con.commit()
        print("Sie haben das Buch " +titel+ " von " +author+ " mit dem Erscheinungsjahr " +year+ " erfolgreich hinzugefügt.")



def delete(cursorObj, con, titel, author, year):
    data = titel
    data1 = author
    data2  = year
    cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Buch=? AND Autor=? AND Erscheinungsjahr=?', [data, data1, data2])
    test = cursorObj.fetchall()

    if test:
        cursorObj.execute('DELETE FROM Buchverwaltung WHERE Buch=? AND Autor=? AND Erscheinungsjahr=?', [data, data1, data2])
        print("Sie haben erfolgreich das Buch: "+titel+" von "+author+ " mit dem Erscheinungsjahr: "+data2+" aus der Liste entfernt") 
        con.commit()

    else:
        print("Dieses Buch existiert nicht")



def listen(cursorObj, con):
    cursorObj = con.cursor()
    data = cursorObj.execute('SELECT * FROM Buchverwaltung')
    print(tabulate(data, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
    con.commit()


def search(cursorObj, con, titel, author, year):        #Revised code
    cursorObj = con.cursor()
    qery = "SELECT * from Buchverwaltung WHERE "
    requeres_and = False

    params = []

    if titel:
        qery += " Buch=? "
        print("1")
        requeres_and = True
        params += [titel]

    if author:
        if requeres_and:
            qery += "AND "
        qery +=  "Autor=? "
        print("2")
        requeres_and = True
        params += [author]

    if year:
        if requeres_and:
            qery += "AND "
        qery += 'Erscheinungsjahr=?'
        print("3")
        params += [year]
    print(qery)
    cursorObj.execute(qery, params)
    test = cursorObj.fetchall()
    print(tabulate(test, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))



"""def search(cursorObj, con, titel, author, year):
    cursorObj = con.cursor()
    data1 = titel
    data2 = author
    data3 = year


    if data1:
        x = 2
    if data2:
        x=3
    if data3: 
        x=4
    if data1 and data2:
        x=5
    if data2 and data3:
        x=6
    if data1 and data3:
        x=7
    if data1 and data2 and data3:
        x=8


    if x==2:
        cursorObj.execute('SELECT Buch FROM Buchverwaltung WHERE Buch=?', [data1])
        prüfen = cursorObj.fetchall()

        if len(prüfen) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Buch=?', [data1])
            print(tabulate(test, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Titel: "+data1+" wurde gefunden!")


    elif x==5:
        cursorObj.execute('SELECT Buch, Autor FROM Buchverwaltung WHERE Buch=? AND Autor=?', [data1, data2])
        prüfen2 = cursorObj.fetchall()
        
        if len(prüfen2) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test2 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Buch=? AND Autor=?', [data1, data2])
            print(tabulate(test2, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Titel: "+data1+" und dem Autor: "+data2+" wurde gefunden!")


    elif x==2:
        cursorObj.execute('SELECT Autor FROM Buchverwaltung WHERE Autor=?', [data2])
        prüfen3 = cursorObj.fetchall()

        if len(prüfen3) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test3 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Autor=?', [data2])
            print(tabulate(test3, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Autor: "+data2+" wurde gefunden!")


    elif x==6:
        cursorObj.execute('SELECT Autor, Erscheinungsjahr FROM Buchverwaltung WHERE Autor=? AND Erscheinungsjahr=?', [data2, data3])
        prüfen4 = cursorObj.fetchall()
        
        if len(prüfen4) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test4 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Autor=? AND Erscheinungsjahr=?', [data2, data3])
            print(tabulate(test4, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Autor: "+data2+" und dem Erscheinungsjahr: "+data3+" wurde gefunden!")


    elif x==4:
        cursorObj.execute('SELECT Erscheinungsjahr FROM Buchverwaltung WHERE Erscheinungsjahr=?', [data3])
        prüfen5 = cursorObj.fetchall()
        
        if len(prüfen5) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test5 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Erscheinungsjahr=?', [data3])
            print(tabulate(test5, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Erscheinungsjahr: "+data3+" wurde gefunden!")


    elif x==7:
        cursorObj.execute('SELECT Buch, Erscheinungsjahr FROM Buchverwaltung WHERE Buch=? AND Erscheinungsjahr=?', [data1, data3])
        prüfen6 = cursorObj.fetchall()
        
        if len(prüfen6) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test6 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE BUCH=? AND Erscheinungsjahr=?', [data1, data3])
            print(tabulate(test6, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Titel: "+data1+" und dem Erscheinungsjahr: "+data3+" wurde gefunden!")


    elif x==8:
        cursorObj.execute('SELECT * FROM Buchverwaltung WHERE Buch=? AND Autor=? AND Erscheinungsjahr=?', [data1,data2, data3])
        prüfen7 = cursorObj.fetchall()
        
        if len(prüfen7) == 0:
            print("Dieses Buch existiert nicht!"+" Bitte geben sie ein anderen Suchbegriff ein.")
        else:
            test7 = cursorObj.execute('SELECT * FROM Buchverwaltung WHERE BUCH=? AND Autor=? AND Erscheinungsjahr=?', [data1,data2, data3])
            print(tabulate(test7, headers="keys", tablefmt="double_outline", stralign='center', numalign='center'))
            print("Das Buch mit dem Titel: "+data1+" dem Autor: "+data2+" und dem Erscheinungsjahr: "+data3+" wurde gefunden!")


    else:
        print("Geben sie bitte ihren Suchbegriff ein")"""


def ueberpruefung(con, cursorObj, command, args):
    if command == "add":
        addbook(cursorObj, con, args.titel, args.author, args.year)
    elif command == "del":
        delete(cursorObj, con, args.titel, args.author, args.year)
    elif command == "list":
        listen(cursorObj, con)
    elif command == "search":
        search(cursorObj, con, args.titel, args.author, args.year)
    else:
        print("Kein gültiger Befehl!")



def main():
    con = sqlite3.connect('buchverwaltung.db')
    args = interface()
    cursorObj = sql_table(con)
    ueberpruefung(con, cursorObj, args.command, args)
    return True

if __name__ == '__main__':
    main()

