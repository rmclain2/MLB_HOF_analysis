import streamlit as st
import pandas as pd
import altair as alt
import zipfile
from vega_datasets import data

st.title("Hall of Famers by Wins Above Replacement")

zf = zipfile.ZipFile('baseball_HOF.csv.zip') 
data = pd.read_csv(zf.open('baseball_HOF.csv'))
df=pd.DataFrame(data)
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data minus the header row
df.columns = new_header #set the header row as the df header
df.dropna( #Remove the extra N/A rows from the df
    axis=0,
    how='all',
    thresh=None,
    subset=None,
    inplace=True
)
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.write("Wins above replacement (WAR) is an all encompassing statistic that is used to evaluate players. It factors in hitting, defense, baserunning, and pitching value to try and predict how many wins above a replacement level player that a player provides for their team. There are two different calculations, bWAR (Baseball Reference) and fWAR (Fangraphs). This data uses bWAR. ")

df=df[(df.hof == "Yes")]
df = df.drop(df.columns[[0,2,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]], axis = 1)
df.drop_duplicates(subset='name', keep="last", inplace=True)
df.sort_values(['year_voted_into_hof','committee'], inplace=True)
counts = df.committee.value_counts()
counts = counts.rename_axis('count').reset_index()
counts.rename(columns = {'committee':'count','count':'committee'}, inplace = True)

hof_war = alt.Chart(df).mark_bar().encode(
    alt.X('name',sort='-y', title = 'Hall of Famer'),
    alt.Y('war:Q',axis=alt.Axis(values=list(range(0, 170, 10))), title = 'Wins Above Replacement (bWAR)'), 
    tooltip = [alt.Tooltip('name', title = "Name"), alt.Tooltip('war', title="WAR")]
).properties(
    title='Number of Players Elected by Committee'
).interactive()

line = alt.Chart().mark_rule(color='firebrick').encode(
    y=('mean(war):Q'),
    size=alt.SizeValue(3)
)
bar = alt.layer(hof_war, line, data=df)

bar