import RiotApi
import RiotAzure
import RiotVisualize
import RiotMatchProcessor
import pandas as pd
import time


puuid = RiotApi.get_puuid(gameName='Pyanioux', tagLine='Data')
user_puuids = {'Pyanioux#Data': puuid}
matches = RiotApi.get_matchhistory(puuid, count=10)
RiotAzure.fetch_and_store_match_history(puuid)
for match_id in matches:
    RiotAzure.fetch_and_store_match(match_id)

df = RiotMatchProcessor.create_match_dataframe(matches, user_puuids)

RiotAzure.upload_dataframe_to_sql(df, table_name='match_data')


RiotVisualize.plot_roles(df)
RiotVisualize.plot_winrate(df)
RiotVisualize.plot_top_champs(df)
RiotVisualize.heatmap_champions(df)