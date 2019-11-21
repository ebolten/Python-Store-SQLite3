#creating a python SQL application

import sqlite3
from sqlite3 import Error


#select everything from table
def select_items(conn):
    cur = conn.cursor()

    print('Tables: ')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    question = input('\nWould you like to see data? ')

    if question.lower() == 'yes':
        name = input('Select a table name: ')
        try:
            cur.execute("SELECT * FROM {}".format(name))
            rows = list(cur.fetchall())

            for i in range(len(rows)):
                row = str(rows[i]).split(',')
                print('Name: ' + row[1] + ", " + 'Price: ' + row[2] + ", " + 'Stock: ' + row[3])
        except Error as e:
            print(e)
            return select_items(conn)
    elif question.lower() == 'no':
        print('Ok!')
    else:
        print('Invalid response (looking for yes or no)')
        return select_items(conn)
        

#create a new table if it doesn't exist
def create_table(conn):
    cur = conn.cursor()
    table = input('Enter a table name: ')
    # columns = ""
    # while True:
    #     i = 0
    #     columns += " " + input('Enter a column name and data type: ') + ","
    #     if input('Would you like to enter another column?: ') == 'yes':
    #         continue
    #     else:
    #         break
    # columns = columns[:-1]
    try:
        cur.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY,name TEXT,price REAL,stock INTEGER);".format(table))
    except Error as e:
        print(e)
        return create_table(conn)
    conn.commit()
    

#insert a row into table
def insert_row(conn):
    cur = conn.cursor()
    print('\nTables: ')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    insert = True
    while insert == True:
        question = input('\nWould you like to add an item to a table?: ')

        if question.lower() == 'yes':
            table = input('Enter a table: ')
            
            name = input('Enter a name: ')
            price = input('Enter a price: ')
            stock = input('Enter the stock: ')
            try:
                cur.execute('INSERT INTO {}(name,price,stock) VALUES ("{}",{},{})'.format(table,name,price,stock))
            except Error as e:
                print(e)
                return insert_row(conn)
        elif question.lower() == 'no':
            print('Ok!')
            insert = False
        else:
            print('Invalid response (looking for yes or no)')
            return insert_row(conn)
    conn.commit()
    

#drop a table from the database
def drop_table(conn):
    cur = conn.cursor()
    print('\nTables: ')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    question = input('Would You Like to Drop a Table?: ')

    if question.lower() == 'yes':
        name = input('\nChoose a Table to Drop: ')
        try:
            cur.execute('DROP TABLE {}'.format(name))
            conn.commit()
        except Error as e:
            print(e)
            return drop_table(conn)
    elif question.lower() == 'no':
        print('Ok!')
    else:
        print('Invalid response (looking for yes or no)')
        return drop_table(conn)


#buy an item from the store
def buy_item(conn):
    cur = conn.cursor()
    print('\nTables: ')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    question = input('Would You Like to Buy an Item?: ')

    if question.lower() == 'yes':
        table = input('Choose a Table to Buy From: ')
        item = input('Choose an Item to Buy: ')

        try:
            cur.execute('SELECT * FROM {} WHERE name = "{}"'.format(table,item))
            rows = list(cur.fetchall())

            if (len(rows)) == 0:
                print('Invalid Item.')
                return buy_item(conn)

            rows = str(rows).split(',')
            stock = rows[3]
            stock = int(stock[1])

            if stock == 0:
                print('There are no more {}(s) in stock.'.format(item))
            else:
                cur.execute("UPDATE {} SET stock = {} WHERE stock = {}".format(table,(stock - 1),stock))
                print('\nThere are {} {}(s) left in stock.'.format((stock - 1),item))
                conn.commit()
        except Error as e:
            print(e)
            return buy_item(conn)

    elif question.lower() == 'no':
        print('Ok!')
    else:
        print('Invalid response (looking for yes or no)')
        return buy_item(conn)


#show the menu
def show_menu(conn):
    print('\nThe Menu:')
    print('1. Create New Table')
    print('2. Get Data')
    print('3. Insert Values into Table')
    print('4. Drop Table')
    print('5. Buy Item')
    print('6. Quit Program')

    num = input('\nEnter a Number: ')

    try:
        num = int(num)
    except:
        print('Invalid Menu Item.')
        return show_menu(conn)

    if num == 1:
        create_table(conn)
        return 1
    elif num == 2:
        select_items(conn)
        return 1
    elif num == 3:
        insert_row(conn)
        return 1
    elif num == 4:
        drop_table(conn)
        return 1
    elif num == 5:
        buy_item(conn)
        return 1
    elif num == 6:
        print('Have a nice day!')
        return 0
    else:
        print('Invalid Menu Item.')
        return show_menu(conn)


#establish the connection to the database
def create_connection(db_file):
    #create a database connection
    conn = None
    #try to create the connection
    try:
        conn = sqlite3.connect(db_file)
        running = True
        while running:
            ret = show_menu(conn)
            if ret == 0:
                break
            else:
                continue
        
        #print(sqlite3.version)
            
    #if cannot be done, print the error
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


#if in main, establish a connection to the database
if __name__ == '__main__':
    create_connection(r"data.db")

