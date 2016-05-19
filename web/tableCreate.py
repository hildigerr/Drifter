#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('tweet.db')

# with con:
    
#     cur = con.cursor()    
#     cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
#     cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
#     cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
#     cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
#     cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
#     cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
#     cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
#     cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
#     cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")

with con:
    
    cur = con.cursor()

    cur.executescript("""
        DRO  P TABLE IF EXISTS Player;
        CREATE TABLE Player(Id INT, Name TEXT, Message TEXT, Success INT, Total INT);

        Insert Into Player VALUES(1, '@MrBot', 'goto A', 2, 10);
        Insert Into Player VALUES(2, '@Driller', 'goto A', 2, 4);
        Insert Into Player VALUES(3, '@Destroyer', 'goto B', 1, 5);
        Insert Into Player VALUES(4, '@Player4', 'goto C', 3, 10);
        Insert Into Player VALUES(5, '@Player5', 'goto A', 5, 20);
        Insert Into Player VALUES(6, '@Player6', 'goto K', 2, 3);
        """)
    con.commit()
con.close()