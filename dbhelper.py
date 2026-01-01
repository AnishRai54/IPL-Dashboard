import  mysql
import mysql.connector
import os
import pandas as pd

# mycursor.execute("""
# Create Database IPL""")
# conn.commit()


# df=pd.read_csv("IPL.csv")

import pandas as pd
# from sqlalchemy import create_engine
# #
# engine = create_engine(
#    "mysql+pymysql://root:{}@localhost:3306/IPL".format(password)
# )
#
# df.to_sql(
#     name="IPL_data",
#     con=engine,
#     if_exists="replace",   # or "append"
#     index=False
#  )
#
# print("✅ Table imported")


class DB:

    def __init__(self):
        password = os.getenv("DB_Password")

        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password,
                port=3306,
                database="IPL"
            )

            self.mycursor = self.conn.cursor()
            print("Connection Establised")

        except mysql.connector.Error as e:
            print(" Connection Error", e)

    def fetch_Season(self):
        self.mycursor.execute(""" select distinct(year) from ipl_data;""")
        data=self.mycursor.fetchall()
        season=[i[0] for i in data]
        return season


    def fetch_team(self):
        self.mycursor.execute(""" 
        select distinct(batting_team) from ipl_data;""")
        data=self.mycursor.fetchall()
        team=[i[0] for i in data]
        return team
