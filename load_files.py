import json, numpy as np, pandas as pd

data_folder = 'imported_data/'
res_by_circo_file = data_folder + 'resultats-eu2024-circonscriptions.csv'
details_circo_file = data_folder + 'bureaux-de-vote-circonscriptions.csv'
categories_political_party_file = data_folder + 'categories_political_party.json'

alignement_score = {
    'Extrême gauche': -2,
    'Gauche radicale': -1.5,
    'Gauche': -1,
    'Centre gauche': -0.5,
    'Centre': 0,
    'Centre droit': 0.5,
    'Droite': 1,
    'Extrême droite': 2,
}

ordered_alignement = ['Extrême gauche', 'Gauche', 'Centre Gauche', 'Centre', 'Centre droit', 'Droite', 'Extrême droite']

def load_raw_votes() :
    lines = []
    with open(res_by_circo_file, encoding='utf8') as f :
        next(f)
        for line in f:
            code, registered, total_votes, abstentions, abstention_rates, name, nb_vote, percentage = line.strip().split(';')
            lines.append(
                #(code, registered, int(total_votes), int(abstentions), float(abstention_rates), name, float(nb_vote), float(percentage))
                (code, registered, int(total_votes), int(abstentions), float(abstention_rates), name, float(nb_vote), float(percentage))
            )
    return lines

def load_categories_political_party() :
    with open(categories_political_party_file, encoding='utf8') as f :
        categories_political_party = json.load(f)
    return categories_political_party

def load_code_commune2circo():
    code_commune2circo = {}
    with open(details_circo_file, encoding='utf8') as f :
        next(f)
        for line in f:
            _,nomDepartement,_,nomCirconscription,codeCommune,_,_,_ = line.strip().split(',')
            code_commune2circo[codeCommune] = f'{nomDepartement} {nomCirconscription}'
    return code_commune2circo

def load_code_circo2name():
    code_circo2name = {}
    with open(details_circo_file, encoding='utf8') as f :
        next(f)
        for line in f:
            _,nomDepartement,code_circo,nomCirconscription,_,_,_,_ = line.strip().split(',')
            code_circo2name[code_circo] = f'{nomDepartement} {nomCirconscription}'
    return code_circo2name

def load_political_party_alignement_score() : 
    categories_political_party = load_categories_political_party()
    categories_political_party = {
        party: [alignement for alignement in alignements if alignement != 'Attrape-tout']
        for party, alignements in categories_political_party.items()
        if alignements != ['Attrape-tout']
    }
    political_party_alignement_score = {
        party: np.mean([alignement_score[alignement] for alignement in alignements])
        for party, alignements in categories_political_party.items()
    }
    return political_party_alignement_score

def get_ordered_parties() :
    political_party_alignement_score = load_political_party_alignement_score()
    return list(sorted(
        political_party_alignement_score,
        key = lambda x : (political_party_alignement_score[x], x)
    ))

def load_party_alignement():
    political_party_alignement_score = load_political_party_alignement_score()
    def get_alignement(score):
        if score < -1.5 :
            return 'Extrême gauche'
        elif -1.5 <= score < -0.5 :
            return 'Gauche'
        elif -0.5 <= score < 0 :
            return 'Centre Gauche'
        elif score == 0 :
            return 'Centre'
        elif 0 < score <= 0.5 :
            return 'Centre droit'
        elif 0.5 < score <= 1.5 :
            return 'Droite'
        elif 1.5 < score :
            return 'Extrême droite'
        else :
            print(score)
            raise Exception("should not happen")
    party_alignement = {
        party : get_alignement(score)
        for party , score in political_party_alignement_score.items()
    }
    return party_alignement


def generate_df_votes_by_allignement() :
    lines = load_raw_votes()
    code_circo2name = load_code_circo2name()
    party_alignement = load_party_alignement()

    agg_votes = {}
    for code_circo, _, _, _, _, name_party, nb_vote, _ in lines:
        if not name_party in party_alignement :
            continue
        circo_name = code_circo2name[code_circo[:2] + code_circo[-2:]]
        alignement = party_alignement[name_party]
        if not circo_name in agg_votes :
            agg_votes[circo_name] = {}
        if not alignement in agg_votes[circo_name] :
            agg_votes[circo_name][alignement] = 0
        agg_votes[circo_name][alignement] += nb_vote
        
    df_votes_by_allignement = pd.DataFrame(agg_votes).T
    df_votes_by_allignement = df_votes_by_allignement[ordered_alignement]

    return df_votes_by_allignement
