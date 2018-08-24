import pandas as pd

points = pd.read_csv('../data/2017-wimbledon-points.csv')
matches = pd.read_csv('../data/2017-wimbledon-matches.csv')
matches['player1'] = matches['player1'].astype('str') 
matches['player2'] = matches['player2'].astype('str') 
cols = points.columns
points[cols] = points[cols].apply(pd.to_numeric, errors = "ignore")
points[["PointNumber"]] = points[["PointNumber"]].apply(pd.to_numeric, errors = "raise")

def create_empty_dict(match_id):
    return {
        "match_id" : match_id,
        "1_1stservesin" : 0,
        "2_1stservesin" : 0,
        "1_deuce1stserveaces" : 0,
        "2_deuce1stserveaces" : 0,
        "1_ad1stserveaces" : 0,
        "2_ad1stserveaces" : 0,
        "1_deuce1stservesin" : 0,
        "2_deuce1stservesin" : 0,
        "1_ad1stservesin" : 0,
        "2_ad1stservesin" : 0,
        "1_1stserveaces" : 0,
        "2_1stserveaces" : 0
    }

def update_dict(row, dict):

    if row['PointServer'] == 1:
        if row["ServeNumber"] == 1:
            dict["1_1stservesin"] += 1
            if row["PointNumber"] % 2 == 0:
                dict["1_ad1stservesin"] += 1
            else:
                dict["1_deuce1stservesin"] += 1
            if row["P1Ace"] == 1:
                dict["1_1stserveaces"] += 1
                if row["PointNumber"] % 2 == 0:
                    dict["1_ad1stserveaces"] += 1
                else:
                    dict["1_deuce1stserveaces"] += 1

    elif row["PointServer"] == 2:
        if row["ServeNumber"] == 1:
            dict["2_1stservesin"] += 1
            if row["PointNumber"] % 2 == 0:
                dict["2_ad1stservesin"] += 1
            else:
                dict["2_deuce1stservesin"] += 1
            if row["P2Ace"] == 1:
                dict["2_1stserveaces"] += 1
                if row["PointNumber"] % 2 == 0:
                    dict["2_ad1stserveaces"] += 1
                else:
                    dict["2_deuce1stserveaces"] += 1

def split_dict(dict):
    matching_row = matches.loc[matches["match_id"] == dict["match_id"]]
    player1 = matching_row["player1"]
    player2 = matching_row["player2"]
    gender = "M" if (int(dict["match_id"].split('-')[-1]) < 2101) else "F"

    player1_dict = {
        "player" : player1,
        "opponent" : player2,
        "gender" : gender,
        "tournament" : "wimbledon", 
        "surface" : "grass", 
        "deuce_firstservepercentage" : dict["1_deuce1stservesin"]/dict["1_1stservesin"], 
        "ad_firstservepercentage" : dict["1_ad1stservesin"]/dict["1_1stservesin"], 
        "deuce_acepercentage" : dict["1_deuce1stserveaces"]/dict["1_1stserveaces"] if(dict["1_1stserveaces"] != 0) else 0, 
        "ad_acepercentage" : dict["1_ad1stserveaces"]/dict["1_1stserveaces"] if(dict["1_1stserveaces"] != 0) else 0
    }

    player2_dict = {
        "player" : player2,
        "opponent" : player1,
        "gender" : gender,
        "tournament" : "wimbledon", 
        "surface" : "grass", 
        "deuce_firstservepercentage" : dict["2_deuce1stservesin"]/dict["2_1stservesin"], 
        "ad_firstservepercentage" : dict["2_ad1stservesin"]/dict["2_1stservesin"], 
        "deuce_acepercentage" : dict["2_deuce1stserveaces"]/dict["2_1stserveaces"] if (dict["2_1stserveaces"] != 0) else 0,
        "ad_acepercentage" : dict["2_ad1stserveaces"]/dict["2_1stserveaces"] if(dict["2_1stserveaces"] != 0) else 0
    }
    return (player1_dict, player2_dict)


match_id = points.iloc[0,0]
match_dict = create_empty_dict(match_id)
data = pd.DataFrame(columns = ["player", "opponent", "gender", "tournament", "surface", "deuce_firstservepercentage", "ad_firstservepercentage", "deuce_acepercentage", "ad_acepercentage"])
for index, row in points.iterrows():
    if row["ElapsedTime"] == 0:
        continue
    curr_match_id = row["match_id"]
    if curr_match_id == match_id:
        update_dict(row, match_dict)
    else:
        dicts = split_dict(match_dict)
        match_id = curr_match_id
        match_dict = create_empty_dict(match_id)
        data = data.append(pd.DataFrame.from_dict(dicts[0], orient = "columns"))
        data = data.append(pd.DataFrame.from_dict(dicts[1], orient = "columns"))
data = data.reset_index(drop = True)
data.to_csv("comp_wimbledon.csv")