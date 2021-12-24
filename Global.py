from os import replace
from sqlite3.dbapi2 import Cursor
import sqlite3
from datetime import datetime
import pandas as pd
from pandas.core.tools.datetimes import to_datetime


# DB connection---------------------------------------------------------------------------

NAS_dir = "//fsa.kenki-intra.com/HCM/(開発)AHS開発プロジェクト/2-public/他部署授受（一時保存）/岩城/Production Analisys/"
conn = sqlite3.connect(
    'C:\Islam\AHS Productivity Team\Python-Dash-Data-visualization-tool\ProductionAnalisys.db')
df_TrendData = pd.read_sql_query(
    "SELECT * FROM TrendData GROUP BY ShiftDate, Category, SubCategory1, SubCategory2, SubCategory3, SubCategory4 HAVING UpdateDate=MAX(UpdateDate)", conn)

# ---------------------------------------------------------------------------

# print(df_TrendData['ShiftDate'].dtype)
# color pallete

# daytime conversion
df_TrendData.assign(
    # new_col=lambda x: some_operation(x)
    # ShiftDate=lambda ShiftDate: datetime.strptime('ShiftDate', '%Y-%m-%d'),
    # UpdateDate=lambda UpdateDate: datetime.strptime(
    #     UpdateDate, '%Y-%m-%d %H:%M:%S')
    ShiftDate=pd.to_datetime(df_TrendData['ShiftDate']),
    UpdateDate=pd.to_datetime(df_TrendData['UpdateDate'])
).assign(
    select_label='SubCategory1' + 'SubCategory2' + 'SubCategory3' + 'SubCategory4'
)
