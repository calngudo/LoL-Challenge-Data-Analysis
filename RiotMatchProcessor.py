from time import time
from dotenv import load_dotenv
import os, requests, pandas as pd, RiotApi
from dotenv import load_dotenv
load_dotenv()



def has_valid_team(participants, user_puuids):
    team1 = 0
    team2 = 0
    for participant in participants:
        puuid = participant['puuid']
        if puuid in user_puuids.values():
            if participant['teamId'] == 100:
                team1 += 1
            else:
                team2 += 1
        if team1 == 5 or team2 == 5:
            return True
        
    return False

def create_match_dataframe(all_valid_match_ids, user_puuids):
    records = []

    for match_data in all_valid_match_ids:
        match = RiotApi.get_match_details(match_data)
        match_id = match['metadata']['matchId']
        info = match['info']
        participants = info['participants']
        teams = info['teams']
        game_duration  = info['gameDuration']
        for participant in participants:
            if participant['puuid'] in user_puuids.values():
                challenges = participant.get('challenges', {})
                team_id = participant['teamId']
                record = {
                'match_id': match_id,
                'summoner_name': participant.get('riotIdGameName', ''),
                'puuid': participant.get('puuid', ''),
                'champion_name': participant.get('championName', ''),
                'team_position': participant.get('teamPosition', ''),

                'win': participant.get('win', False),
                'kills': participant.get('kills', 0),
                'deaths': participant.get('deaths', 0),
                'assists': participant.get('assists', 0),
                'total_cs': participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0),

                'baron_kills': participant.get('baronKills', 0),
                'dragon_kills': participant.get('dragonKills', 0),
                'double_kills': participant.get('doubleKills', 0),
                'triple_kills': participant.get('tripleKills', 0),
                'quadra_kills': participant.get('quadraKills', 0),
                'penta_kills': participant.get('pentaKills', 0),
                'largest_multi_kill': participant.get('largestMultiKill', 0),
                'killing_sprees': participant.get('killingSprees', 0),


                'total_damage_dealt_to_champions': participant.get('totalDamageDealtToChampions', 0),
                'damage_dealt_to_buildings': participant.get('damageDealtToBuildings', 0),
                'first_blood_kill': participant.get('firstBloodKill', False),
                'first_tower_kill': participant.get('firstTowerKill', False),
                'turret_takedowns': participant.get('turretTakedowns', 0),
                'game_duration': game_duration,


                'total_heal_on_teammates': challenges.get('totalHealOnTeammates', 0),
                'total_damage_shielded': challenges.get('totalDamageShieldedOnTeammates', 0),
                'vision_score': participant.get('visionScore', 0),
                
                'gold_per_minute': challenges.get('goldPerMinute', 0),
                'kill_participation': challenges.get('killParticipation', 0),
                'kills_under_own_turret': challenges.get('killsUnderOwnTurret', 0),
                'solo_kills': challenges.get('soloKills', 0),
                'epic_monster_steals': challenges.get('epicMonsterSteals', 0),
                'epic_monster_stolen_without_smite': challenges.get('epicMonsterStolenWithoutSmite', 0),
                'dodge_skillshots_small_window': challenges.get('dodgeSkillshotsSmallWindow', 0),
                'kill_on_laners_early_jungle_as_jungler': challenges.get('killOnLanersEarlyJungleAsJungler', 0),

                }
                records.append(record)
        time.sleep(15)

    df = pd.DataFrame(records)
    return df





    