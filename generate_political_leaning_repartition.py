from load_files import generate_df_votes_by_allignement, ordered_alignement
import matplotlib.pyplot as plt

df_votes_by_allignement = generate_df_votes_by_allignement()

df_votes_by_allignement = \
    df_votes_by_allignement.iloc[:, :] / df_votes_by_allignement.values.sum(axis=1, keepdims=True)
df_votes_by_allignement['allignment_score'] = (df_votes_by_allignement * [-2, -1, -0.5, 0 , 0.5, 1, 2]).sum(axis=1)
df_votes_by_allignement = df_votes_by_allignement.sort_values('allignment_score')
df_votes_by_allignement=df_votes_by_allignement[ordered_alignement]

plt.figure()
ax = df_votes_by_allignement.plot.barh(
    stacked=True, figsize=(30,200),
    color=[
        'red', 'lightcoral', 'orange',
        'grey',
        'lime', 'turquoise', 'darkblue',
    ]
)
ax.axvline(x=0.25, color='black', linestyle=':')
ax.axvline(x=0.5, color='black', linestyle='--')
ax.axvline(x=0.75, color='black', linestyle=':')

plt.savefig('data/political_leaning_repartition.png')