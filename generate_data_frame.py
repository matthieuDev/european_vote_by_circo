from load_files import generate_df_votes_by_allignement, ordered_alignement

def generate_normed_df_votes_by_allignement() :
    df_votes_by_allignement = generate_df_votes_by_allignement()

    df_votes_by_allignement = \
        df_votes_by_allignement.iloc[:, :] / df_votes_by_allignement.values.sum(axis=1, keepdims=True)
    df_votes_by_allignement['allignment_score'] = (df_votes_by_allignement * [-2, -1, -0.5, 0 , 0.5, 1, 2]).sum(axis=1)
    df_votes_by_allignement = df_votes_by_allignement.sort_values('allignment_score')
    df_votes_by_allignement=df_votes_by_allignement[ordered_alignement]

    return df_votes_by_allignement