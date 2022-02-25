from riotwatcher import LolWatcher, ValWatcher, TftWatcher, ApiError
import os

# from apikey import *
# lol_watcher = LolWatcher(API_KEY)
# val_watcher = ValWatcher(R_KEY)
# tft_watcher = TftWatcher(R_KEY)

lol_watcher = LolWatcher(os.environ['API_KEY'])
val_watcher = ValWatcher(os.environ['R_KEY'])
tft_watcher = TftWatcher(os.environ['R_KEY'])
my_region = "na1"
data_version = lol_watcher.data_dragon.versions_for_region(my_region)
latest_champion_ver = data_version['n']['champion']
static_champ_list = lol_watcher.data_dragon.champions(latest_champion_ver, False, 'en_US')

spell_dict = lol_watcher.data_dragon.summoner_spells(data_version["v"], 'en_US')["data"]
spell_icon = {}
for key, value in spell_dict.items():
    spell_icon[str(value["key"])] = key


def getSummonerDetailsByName(name):
    me = lol_watcher.summoner.by_name(my_region, name)
    ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])

    ranked_dictionary = {
        "solo": {"rank": "Unranked"},
        "flex": {"rank": "Unranked"}
    }
    for rank in ranked_stats:
        if "SOLO" in rank["queueType"]:
            ranked_dictionary["solo"]["rank"] = rank['tier'] + " " + rank['rank']
            ranked_dictionary["solo"]["wins"] = rank["wins"]
            ranked_dictionary["solo"]["loss"] = rank["losses"]
            ranked_dictionary["solo"]["total_games"] = rank["wins"] + rank["losses"]
            ranked_dictionary["solo"]["points"] = rank["leaguePoints"]
            ranked_dictionary["solo"]["wr"] = str(
                round(ranked_dictionary["solo"]["wins"] / ranked_dictionary["solo"]["total_games"] * 100, 1)) + '%'
            if "miniSeries" in rank:
                promos = rank["miniSeries"]["progress"].replace("N", "X")
                ranked_dictionary["solo"]["promos"] = promos
        if "FLEX" in rank["queueType"]:
            ranked_dictionary["flex"]["rank"] = rank['tier'] + " " + rank['rank']
            ranked_dictionary["flex"]["wins"] = rank["wins"]
            ranked_dictionary["flex"]["loss"] = rank["losses"]
            ranked_dictionary["flex"]["total_games"] = rank["wins"] + rank["losses"]
            ranked_dictionary["flex"]["points"] = rank["leaguePoints"]
            ranked_dictionary["flex"]["wr"] = str(
                round(ranked_dictionary["flex"]["wins"] / ranked_dictionary["flex"]["total_games"] * 100, 1)) + '%'
            if "miniSeries" in rank:
                promos = rank["miniSeries"]["progress"].replace("N", "X")
                ranked_dictionary["flex"]["promos"] = promos

    return ranked_dictionary


def getSummonerTopChampionsByName(name):
    me = lol_watcher.summoner.by_name(my_region, name)

    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']

    mastery = lol_watcher.champion_mastery.by_summoner(my_region, me['id'])
    champion_mastery = []
    for champion in mastery:
        single_champ = {}
        single_champ['Champion'] = champ_dict[str(champion['championId'])]
        if single_champ['Champion'] == 'MonkeyKing':
            single_champ['Champion'] = 'Wukong'
        single_champ['Mastery Level'] = champion['championLevel']
        single_champ['Champion Points'] = champion['championPoints']
        champion_mastery.append(single_champ)

    return {"top_10": champion_mastery}
    # print(mastery)


def getMatchHistoryByNameLOL(name):
    me = lol_watcher.summoner.by_name(my_region, name)
    match_list = lol_watcher.match.matchlist_by_puuid('americas', me['puuid'], type="ranked", count=10)
    match_detail = lol_watcher.match.by_id('americas', match_list[-1])
    player_game_details = {}
    for player in match_detail["info"]["participants"]:
        if player["summonerName"] == name:
            player_game_details['Win'] = player['win']
            player_game_details["Summoner"] = player["summonerName"]
            player_game_details['Icon'] = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(data_version["n"]["champion"], player['championName'])
            player_game_details['champion'] = player['championName']
            if player_game_details['champion'] == 'MonkeyKing':
                player_game_details['champion'] = 'Wukong'
            player_game_details['Spell1'] = 'https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(data_version["n"]["champion"], spell_icon[str(player['summoner1Id'])])
            player_game_details['Spell2'] = 'https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(data_version["n"]["champion"], spell_icon[str(player['summoner2Id'])])
            player_game_details['LVL'] = player['champLevel']
            player_game_details['K/D/A'] = (str(player['kills']) + "/" + str(player['deaths']) + "/" + str(player['assists']))
            player_game_details['DMG'] = player['totalDamageDealt']
            player_game_details['Gold'] = player['goldEarned']

    return player_game_details


def getSummonerTFTDetailsByName(name):
    me = tft_watcher.summoner.by_name(my_region, name)
    ranked_stats = tft_watcher.league.by_summoner(my_region, me["id"])
    ranked_dict = {}
    ranked_dict["name"] = ranked_stats[0]["summonerName"]
    ranked_dict["tier"] = ranked_stats[0]["tier"]
    ranked_dict["rank"] = ranked_stats[0]["rank"]
    ranked_dict["LP"] = ranked_stats[0]["leaguePoints"]
    ranked_dict["wins"] = ranked_stats[0]["wins"]
    return ranked_dict


def getMatchHistoryByNameTFT(name):
    me = tft_watcher.summoner.by_name(my_region, name)
    match_list = tft_watcher.match.by_puuid('americas', me['puuid'], count=10)

    match_detail = tft_watcher.match.by_id('americas', match_list[0])
    player_game_details = {}
    for player in match_detail["info"]["participants"]:
        if player["puuid"] == me["puuid"]:
            player_game_details["placement"] = player["placement"]
            player_game_details["level"] = player["level"]
            traits_activated = []
            for trait in player["traits"]:
                if trait["tier_current"] > 0:
                    traits_activated.append({trait["name"]: trait["tier_current"]})
            player_game_details["active_traits"] = traits_activated

    return player_game_details


# print(getMatchHistoryByNameLOL("Linom"))
# getSummonerTopChampionsByName("Linom")
# getMatchHistoryByName("Linom")
# print(getMatchHistoryByNameTFT("Linom"))
# getSummonerTFTDetailsByName("Linom")
