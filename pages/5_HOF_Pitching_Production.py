import streamlit as st
import pandas as pd
import altair as alt

st.title("HOF Pitching Production")

data = pd.read_csv('baseball_HOF.csv')
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

st.write("For pitchers, injury and volatility can easily eliminate what may look like early career hall of fame cases. Becoming a hall of fame pitcher requires either a career of durability with at least all star level production on average or a shorter career with a completely dominant peak. Historically, teams have liked stats such as strikeouts, ERA, and wins to judge hall of fame cases. In recent years, analytics have allowed for comparisons of players across different eras. ERA+ takes a players ERA (earned runs allowed per 9 innings) and normalizes it across the league while accounting for ballpark factors. This allows for comparisons against different eras where the average pitcher may be better or worse than a given year. An ERA+ of 100 is average. ")

df['innings_pitched']=df['innings_pitched'].astype(float)
df['strikeouts']=df['strikeouts'].astype(float)
df=df[(df.hof == "Yes") & (df.innings_pitched >= 1000)]
df.drop_duplicates(subset='name', keep="last", inplace=True)
df.sort_values(['year_voted_into_hof','committee'], inplace=True)
counts = df.committee.value_counts()
counts = counts.rename_axis('count').reset_index()
counts.rename(columns = {'committee':'count','count':'committee'}, inplace = True)
pitching = alt.Chart(df).mark_circle().encode(
    alt.X('strikeouts:Q', title = 'Strikeouts'),
    alt.Y('innings_pitched:Q', title = 'Innings Pitched'),
    color=alt.Color('era_plus:Q',
        scale=alt.Scale(
        range=['pink', 'purple'])),
    tooltip = [alt.Tooltip('name', title = "Name"), alt.Tooltip('innings_pitched', title="Innings Pitched"), alt.Tooltip('strikeouts', title="Strikeouts"), alt.Tooltip('era_plus', title="ERA+")]
)

pitching + pitching.transform_regression('strikeouts','innings_pitched').mark_line().interactive() 
