#Basic Requeriments
import pandas as pd
from sqlalchemy import create_engine
import os
import re

############################################################################################
#This block of code allows making the connection with the database and generating a pkl file
#that stores the data from the first query and thus avoid making the connection at all times.
#We import 2 files, v_consolidada_v3 which has basic information on the students and 
#information on the model and v_consolidada_v2 which has information on the students of each
#of the periods studied.
#############################################################################################

path_file = "./data/v_consolidada_v3.pkl"
path_file_all_periods = "./data/v_consolidada_v2.pkl"

if os.path.isfile(path_file) and os.path.isfile(path_file_all_periods):
    df = pd.read_pickle(path_file)
    df_all_periods = pd.read_pickle(path_file_all_periods)
    print("files loaded")
else:
    #Connecion con la BD
    engine=create_engine(f'postgresql://team37:te@m37@db-unire.cta1quddbuts.us-east-2.rds.amazonaws.com/uniremington', max_overflow=20)
    df = pd.read_sql('SELECT * FROM v_consolidada_v3', engine.connect())
    df.to_pickle(path_file)

    df_all_periods = pd.read_sql('SELECT * FROM v_consolidada_v2', engine.connect())
    df_all_periods.to_pickle(path_file_all_periods)