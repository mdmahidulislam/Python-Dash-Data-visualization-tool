from sqlite3.dbapi2 import Cursor
import sqlite3

# DB connection---------------------------------------------------------------------------
conn = sqlite3.connect(
    'C:\Islam\AHS Productivity Team\Python-Dash-Data-visualization-tool\ProductionAnalisys.db')
cursor = conn.cursor()
df = cursor.execute(
    "SELECT * FROM TrendData GROUP BY ShiftDate, Category, SubCategory1, SubCategory2, SubCategory3, SubCategory4 HAVING UpdateDate=MAX(UpdateDate)")
# ---------------------------------------------------------------------------

# replace yen symble to "/"" symble
NAS_dir = "//fsa.kenki-intra.com/HCM/(開発)AHS開発プロジェクト/2-public/他部署授受（一時保存）/岩城/Production Analisys/"

# color pallete
