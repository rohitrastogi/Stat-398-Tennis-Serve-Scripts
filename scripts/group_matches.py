import pandas as pd

points = pd.read_csv('../data/2017-ausopen-points.csv')
matches = pd.read_csv('../data/2017-ausopen-matches.csv')
matches['player1'] = matches['player1'].astype('str') 
matches['player2'] = matches['player2'].astype('str') 
cols = points.columns
points[cols] = points[cols].apply(pd.to_numeric, errors = "ignore")
points[["PointNumber"]] = points[["PointNumber"]].apply(pd.to_numeric, errors = "raise")

def create_empty_dict(match_id):
    return {
        "match_id" : match_id,
        "1_points_won" : 0,
        "2_points_won" : 0,
        "1_1servevelocity" : 0,
        "2_1servevelocity" : 0,
        "1_2servevelocity" : 0,
        "2_2servevelocity" : 0,
        "1_1stservesin" : 0,
        "2_1stservesin" : 0,
        "1_2ndservesin" : 0,
        "2_2ndservesin" : 0,
        "1_1stserveaces" : 0,
        "2_1stserveaces" : 0,
        "1_1stservepointswon" : 0,
        "2_1stservepointswon" : 0,
        "1_servedeucepointswon" : 0,
        "2_servedeucepointswon" : 0,
        "1_serveadpointswon" : 0,
        "2_serveadpointswon" : 0,
        "1_pointsserved" : 0,
        "2_pointsserved" : 0,
        "1_double_faults" : 0,
        "2_double_faults" : 0,
        "1_servepointswon" : 0,
        "2_servepointswon" : 0, 
    }

def update_dict(row, dict):
    if row["PointWinner"] == 1:
        dict["1_points_won"] += 1

    elif row["PointWinner"] == 2:
        dict["2_points_won"] += 1

    if row['PointServer'] == 1:
        dict["1_pointsserved"] += 1

        if row["PointWinner"] == 1:
            if row["PointNumber"] % 2 == 0:
                dict["1_serveadpointswon"] += 1
            else:
                dict["1_servedeucepointswon"] += 1
            dict["1_servepointswon"] += 1

        if row["ServeNumber"] == 1:
            dict["1_1servevelocity"] += row["Speed_MPH"]
            dict["1_1stservesin"] += 1
            if row["PointWinner"] == 1:
                dict["1_1stservepointswon"] += 1
            if row["P1Ace"] == 1:
                dict['1_1stserveaces'] += 1

        elif row["ServeNumber"] == 2:
            dict["1_2servevelocity"] += row["Speed_MPH"]
            dict["1_2ndservesin"] += 1

        elif row["ServeNumber"] == 0:
            dict["1_double_faults"] += 1

    elif row["PointServer"] == 2:
        dict["2_pointsserved"] += 1

        if row["PointWinner"] == 2:
            if row["PointNumber"] % 2 == 0:
                dict["2_serveadpointswon"] += 1
            else:
                dict["2_servedeucepointswon"] += 1
            dict["2_servepointswon"] += 1

        if row["ServeNumber"] == 1:
            dict["2_1servevelocity"] += row["Speed_MPH"]
            dict["2_1stservesin"] += 1
            if row["PointWinner"] == 2:
                dict["2_1stservepointswon"] += 1
            if row["P2Ace"] == 1:
                dict["2_1stserveaces"] += 1

        elif row["ServeNumber"] == 2:
            dict["2_2servevelocity"] += row["Speed_MPH"]
            dict["2_2ndservesin"] += 1
            
        elif row["ServeNumber"] == 0:
            dict["2_double_faults"] += 1

def split_dict(dict):
    matching_row = matches.loc[matches["match_id"] == dict["match_id"]]
    player1 = matching_row["player1"]
    player2 = matching_row["player2"]
    gender = "M" if (int(dict["match_id"].split('-')[-1]) < 2101) else "F"

    player1_dict = {
        "player" : player1,
        "opponent" : player2,
        "gender" : gender,
        "tournament" : "aus", 
        "surface" : "hard", 
        "points_won" : dict["1_points_won"], 
        "1st_velocity" : dict["1_1servevelocity"]/dict["1_1stservesin"], 
        "2nd_velocity" : dict["1_2servevelocity"]/dict["1_2ndservesin"], 
        "1st_ace_percentage" : dict["1_1stserveaces"]/dict["1_1stservesin"], 
        "1st_serve_percentage" : dict["1_1stservesin"]/dict["1_pointsserved"],
        "double_fault_percentage" : dict["1_double_faults"]/dict["1_pointsserved"],
        "deuce_percentage" : dict["1_servedeucepointswon"]/dict["1_servepointswon"],
        "ad_percentage" : dict["1_serveadpointswon"]/dict["1_servepointswon"],
        "serve_win_percentage" : dict["1_servepointswon"]/dict["1_pointsserved"]
    }

    player2_dict = {
        "player" : player2,
        "opponent" : player1,
        "gender" : gender,
        "tournament": "aus", 
        "surface" : "hard", 
        "points_won" : dict["2_points_won"], 
        "1st_velocity" : dict["2_1servevelocity"]/dict["2_1stservesin"], 
        "2nd_velocity" : dict["2_2servevelocity"]/dict["2_2ndservesin"], 
        "1st_ace_percentage" : dict["2_1stserveaces"]/dict["2_1stservesin"], 
        "1st_serve_percentage" : dict["2_1stservesin"]/dict["2_pointsserved"],
        "double_fault_percentage" : dict["2_double_faults"]/dict["2_pointsserved"],
        "deuce_percentage" : dict["2_servedeucepointswon"]/dict["2_servepointswon"],
        "ad_percentage" : dict["2_serveadpointswon"]/dict["2_servepointswon"],
        "serve_win_percentage" : dict["2_servepointswon"]/dict["2_pointsserved"]
    }
    return (player1_dict, player2_dict)


match_id = points.iloc[0,0]
match_dict = create_empty_dict(match_id)
data = pd.DataFrame(columns = ["player", "opponent", "gender", "tournament", "surface", "points_won", "1st_velocity", "2nd_velocity", "1st_ace_percentage", "double_fault_percentage", "deuce_percentage", "ad_percentage"])
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
data.to_csv("aus_open.csv")