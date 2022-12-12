import streamlit as st
import pandas as pd
import altair as alt
import zipfile

st.title("HOF Offensive Production")

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

st.write("For position players, the most important part of their game when it comes to hall of fame voting is their offense. Historically, teams have liked counting stats such home runs, runs batted in, and hits to judge this. In recent years, analytics have allowed for comparisons of players across different eras. OPS+ takes a players OPS (on base percentage + slugging percentage) and normalizes it across the league while accounting for ballpark factors. This allows for comparisons against different eras where the average offensive player may be better or worse than a given year. An OPS+ of 100 is average. ")
df['ab']=df['ab'].astype(float)
df['home_runs']=df['home_runs'].astype(float)
df=df[(df.hof == "Yes") & (df.ab >= 3000)]
df.drop_duplicates(subset='name', keep="last", inplace=True)
df.sort_values(['year_voted_into_hof','committee'], inplace=True)
counts = df.committee.value_counts()
counts = counts.rename_axis('count').reset_index()
counts.rename(columns = {'committee':'count','count':'committee'}, inplace = True)

offense = alt.Chart(df).mark_circle().encode(
    alt.X('home_runs:Q', title = 'Home Runs'),
    alt.Y('ab:Q',axis=alt.Axis(values=list(range(3000,13000, 1000))), title = 'At Bats'),
    color=alt.Color('ops_plus:Q',
        scale=alt.Scale(
        range=['pink', 'purple'])),
    tooltip = [alt.Tooltip('name', title = "Name"), alt.Tooltip('ab', title="At Bats"), alt.Tooltip('home_runs', title="Home Runs"), alt.Tooltip('ops_plus', title="OPS+")]
)

offense + offense.transform_regression('home_runs','ab').mark_line().interactive() 
