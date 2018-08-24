import pandas as pd
import numpy as np
import csv


def create_empty_dict(match_id, pid):
    return {
        "match_id" : match_id,
        "id" : pid, 
        "ad_seq" : [],
        "deuce_seq" : [],
        "seq" : []
    }

deuce_directions = {
    "BW" : 1,
    "B" : .5,
    "BC" : 0,
    "C" : 0,
    "W" : 1
}

ad_directions = {
    "BW" : 0, 
    "B" : .5,
    "BC" : 1,
    "C" : 1,
    "W" : 0
}

tot_directions = {
    "BW" : 1,
    "B" : .5,
    "BC" : 0,
    "C" : 0,
    "W" : 1
}

def update_dict(row, dict):
    if row['PointServer'] == dict['id']: # you are the server
        if row["PointNumber"] % 2 == 0:
            dict["ad_seq"].append(ad_directions[row['ServeWidth']])
            dict['seq'].append(tot_directions[row['ServeWidth']])
        else:
            dict["deuce_seq"].append(deuce_directions[row['ServeWidth']])
            dict["seq"].append(tot_directions[row['ServeWidth']])

def merge_data(dict):
    matching_row = matches.loc[matches["match_id"] == dict["match_id"]]
    if dict['id'] == 1:
        player1 = matching_row["player1"]
        player2 = matching_row["player2"]
    else:
        player1 = matching_row["player2"]
        player2 = matching_row["player1"]
    gender = "M" if (int(dict["match_id"].split('-')[-1]) < 2101) else "F"
    dict['player'] =  player1
    dict['opponent'] = player2 
    del dict['match_id']
    del dict['id']

def extract_string(s):
    split = str(s).split()
    name = ' '.join(split[1:3])
    return(name)

def concatenate_dicts(dicts):
    res = {
        "ad_seq" : [],
        "deuce_seq" : [],
        "seq" : []
    }
    for d in dicts:
        res['ad_seq'].extend(d['ad_seq'])
        res['deuce_seq'].extend(d['deuce_seq'])
        res['seq'].extend(d['seq'])

    return res

tournaments = ['../data/2017-ausopen-points.csv', '../data/2017-usopen-points.csv', '../data/2017-wimbledon-points.csv',  '../data/2017-frenchopen-points.csv']
matches_links = ['../data/2017-ausopen-matches.csv', '../data/2017-usopen-matches.csv', '../data/2017-wimbledon-matches.csv',  '../data/2017-frenchopen-matches.csv']
roger = []
isner = []
diego = []
for i, tournament in enumerate(tournaments):
    points = pd.read_csv(tournament)
    matches = pd.read_csv(matches_links[i])
    cols = points.columns
    points[cols] = points[cols].apply(pd.to_numeric, errors = "ignore")
    points[["PointNumber"]] = points[["PointNumber"]].apply(pd.to_numeric, errors = "raise")
    #matches = matches.drop(matches[(matches['ServeWidth'] == "") & (matches['ServeNumber'] != 0)].index)
    points = points[pd.notnull(points['ServeWidth'])]
    matches['player1'] = matches['player1'].astype('str') 
    matches['player2'] = matches['player2'].astype('str') 
    cols = points.columns
    match_id = points.iloc[0,0]
    dict_1 = create_empty_dict(match_id, 1)
    dict_2 = create_empty_dict(match_id, 2)
    for index, row in points.iterrows():
        if row["ElapsedTime"] == 0:
            continue
        curr_match_id = row["match_id"]
        if curr_match_id == match_id:
            update_dict(row, dict_1)
            update_dict(row, dict_2)
        else:
            merge_data(dict_1)
            merge_data(dict_2)
            match_id = curr_match_id
            if (extract_string(dict_1['player'])) == "Roger Federer":
                roger.append(dict_1)
            if (extract_string(dict_2['player'])) == "Roger Federer":
                roger.append(dict_2)
            if (extract_string(dict_1['player'])) == "John Isner":
                isner.append(dict_1)
            if (extract_string(dict_2['player'])) == "John Isner":
                isner.append(dict_2)
            if (extract_string(dict_1['player'])) == "Diego Schwartzman":
                diego.append(dict_1)
            if (extract_string(dict_2['player'])) == "Diego Schwartzman":
                diego.append(dict_2)
            dict_1 = create_empty_dict(match_id, 1)
            dict_2 = create_empty_dict(match_id, 2)
rog = concatenate_dicts(roger)
isn = concatenate_dicts(isner)
di = concatenate_dicts(diego)

with open('diego3.csv', 'w') as f:
    vals = di['seq']
    writer = csv.writer(f)
    for val in vals:
        writer.writerow([val])
