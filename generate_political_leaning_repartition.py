from generate_data_frame import generate_normed_df_votes_by_allignement
import matplotlib.pyplot as plt

df_votes_by_allignement = generate_normed_df_votes_by_allignement()

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