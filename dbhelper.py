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
                database="ipl",
                auth_plugin="mysql_native_password"
            )

            self.mycursor = self.conn.cursor()
            print("✅ Connection Established")

        except mysql.connector.Error as e:
            print("❌ Connection Error:", e)
            raise e

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


    def fetch_NoOfTrophy(self):
        self.mycursor.execute("""select match_won_by,count(*) as "no of Trophy" from(

             select match_won_by,match_id from ipl.ipl_data
             where stage ="final"
             group by match_won_by,match_id) t
             group by t.match_won_by""")
        data=self.mycursor.fetchall()
        team=[i[0] for i in data]
        no_of_trophy=[i[1] for i in data]

        return team,no_of_trophy


    def fetch_Season_Total_Matches(self,season):
        self.mycursor.execute(
            "SELECT COUNT(DISTINCT match_id) AS Total_Matches "
            "FROM ipl_data WHERE year = {}".format(int(season))
        )

        return   self.mycursor.fetchone()[0]

    def Season_winner_loser(self,year):
        self.mycursor.execute(""" SELECT 
         match_won_by AS winner,
       CASE
       WHEN match_won_by = batting_team THEN bowling_team
       ELSE batting_team
         END AS loser
     FROM ipl_data
     WHERE year = {} AND stage = 'final' limit 1;""".format(int(year)))


        data=self.mycursor.fetchone()
        winner=data[0]
        losser=data[1]

        return  winner,losser


    def fetch_Cap(self,year):
        self.mycursor.execute(""" SELECT * FROM ipl.cap
        where year={};""".format(int(year)))
        data=self.mycursor.fetchone()
        oragne_cap=data[1]
        run=data[2]
        purple_cap=data[3]
        wicket=data[4]

        return oragne_cap,run,purple_cap,wicket


    def fetch_totalSix(self,year):
        query=""" SELECT count(*) as "Total Sixes"  FROM ipl.ipl_data
          where year =%s and runs_batter=6;"""
        self.mycursor.execute(query,(year,))
        data=self.mycursor.fetchone()

        # total_six=data[1]
        return data[0]

    def total_wickets(self, year):
        query = """
        SELECT COUNT(*) AS TotalWicket
        FROM ipl.ipl_data
        WHERE year = %s AND wicket_kind IS NOT NULL;
        """
        self.mycursor.execute(query, (year,))
        return self.mycursor.fetchone()[0]


    def fetch_Point_table(self,year):
        query="""  select match_won_by as "Team" ,count(*) as "Points"from(
                 SELECT match_id,match_won_by  FROM ipl.ipl_data
                 where year =%s group by  match_id,match_won_by)t
                 GROUP BY match_won_by
                 ORDER BY points DESC;"""

        self.mycursor.execute(query,(year,))
        data=self.mycursor.fetchall()

        return data
    
    def fetch_team_run(self,team):
        query="""SELECT batting_team AS team, SUM(runs_total) AS total_runs
                  FROM ipl_data
                  GROUP BY batting_team 
                  having team =%s ;"""
        self.mycursor.execute(query,(team,))
        data= self.mycursor.fetchall()
        return data[0][1]
    
    
    def fetch_total_matches(self,team):
        query=""" SELECT team, COUNT(DISTINCT match_id) AS total_matches
              FROM
              (
                  SELECT match_id, batting_team AS team FROM ipl_data
                  UNION ALL
                  SELECT match_id, bowling_team AS team FROM ipl_data
              ) t
              where team =%s
              GROUP BY team
              """
        self.mycursor.execute(query,(team,))
        data=self.mycursor.fetchone()[1]
        return data
    
    def fetch_total_wicket(self,team):
        query=""" select bowling_team,count(*) as Total_wicket from ipl_data 
                    where wicket_kind is not null 
                    and bowling_team=%s
                    group by bowling_team  """
        self.mycursor.execute(query,(team,))
        data= self.mycursor.fetchone()[1]
        return data
    
    def fetch_Season_runs(self,team,year):
        query=""" select batting_team,sum(runs_total) as Total_Runs from ipl_data
          where year=%s and batting_team=%s
         group by batting_team"""
         
        self.mycursor.execute(query,(year,team))
        data=self.mycursor.fetchone()[1]
        
        return data
    
    def fetch_season_wickets(self, team, year):

        query = """
        SELECT COUNT(*)
        FROM ipl_data
        WHERE wicket_kind IS NOT NULL
        AND year=%s
        AND bowling_team=%s
        """

        self.mycursor.execute(query,(year,team))
        result = self.mycursor.fetchone()

        return result[0]
        

    
    
db=DB()
team="Chennai Super Kings"
d=db.fetch_Season_runs(team,2009)
print(d)






