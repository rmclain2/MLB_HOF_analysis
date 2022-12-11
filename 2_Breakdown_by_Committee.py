import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

st.title("Breakdown by Committee")

data = pd.read_csv("baseball_HOF.csv")
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


col1, col2 = st.columns(2)

with col1:
    df1=df[(df.hof == "Yes")]
    df1 = df1.drop(df.columns[[0,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]], axis = 1)
    #df = df.drop(df.iloc[:,0,2,5:42], inplace=True, axis=1)
    df1.drop_duplicates(subset='name', keep="last", inplace=True)
    df1.sort_values(['year_voted_into_hof','committee'], inplace=True)
    counts = df1.committee.value_counts()
    counts = counts.rename_axis('count').reset_index()
    counts.rename(columns = {'committee':'count','count':'committee'}, inplace = True)

    count_by_committee = alt.Chart(counts).mark_bar().encode(
        alt.X('committee', sort='-y', title = 'Committee'),
        alt.Y('count', axis=alt.Axis(values=list(range(0, 140, 10))), title = ('Number of Players Elected')), 
        tooltip = [alt.Tooltip('committee'), alt.Tooltip('count', title="Players Elected")]
    ).properties(
        title='Number of Players Elected by Committee'
    ).interactive()

    count_by_committee
    st.write("The BBWAA election is the primary method of election for players who are elected in the HOF. If a player is not inducted by the BBWAA, they can be included on future committee ballots. ")
    st.write("The Veteran's Committee was formed in 1953. Elections were held in odd-numbered years until 1962 when they changed to annual elections. Starting in 1977, the Veterean's Committee was limited to a maximum of two inductees per year because of the elections between 1970 to 1973. Between these years, hall of famer Frankie Frisch was the leading voice on the committee that elected 16 people, including 5 of his former teamates. Many saw these players as undeserving with their BBWAA vote totals nearing zero. In 1995, the committee election total was expanded again to allow for Negro League player voting. After Bill Mazeroski, a stellar defender albeit a light hitting second baseman, was elected in 2001, the Hall of Fame gave voting privileges to the Hall of Famers, which resulted in nobody being elected for several years. The committee returned to a small group in 2007 before it was split into several subcommittees after 2009.")
    st.write("The Old-Timers Committee was formed in 1939 to consider players from the 19th century. This comittee continued to meet until 1949.")
    st.write("The Golden Era Committee was a committee that replaced the Veteran's Committee in 2010. This committee considers players who played the majority of their career between 1947 and 1972. ")
    st.write("The Modern Baseball Era Comittee was a committee that was instated in 2016. This comittee considers players whose greatest contributions came between 1970 and 1987. ")
   
with col2:
    df2=df[(df.hof == "Yes")]
    df2 = df2.drop(df.columns[[0,2,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]], axis = 1)
    df2.drop_duplicates(subset='name', keep="last", inplace=True)
    df2['war']=df2['war'].astype(float)
    average_war = df2.groupby('committee', as_index=False)['war'].mean()

    war = alt.Chart(average_war).mark_bar().encode(
        alt.X('committee', sort='-y', title = 'Committee'),
        alt.Y('war', title = 'bWAR'), 
        tooltip = [alt.Tooltip('committee', title = "Committee"), alt.Tooltip('war', title="WAR")]
    ).properties(
        title='Average Wins Above Replacement by Committee'
    ).interactive()

    war

    st.write("The Centennial Comittee was a committee that was instated in 1937. This comittee only met once to consider MLB players, executives, and coaches whose greatest contributions were prior to 1900. ")
    st.write("The Today's Game Era Committee was a committee that was instated in 2016. This comittee considers players whose greatest contributions came between 1988-current.")
    st.write("The Special Election Committee was a committee that was put together in 1939 to elect Lou Gehrig after his diagnosis of ALS (Lou Gehrig's disease) forced him to retire. Lou Gehrig died in 1941 which was before he would have been eligible to appear on the BBWAA ballot. ")
    st.write("The Negro League Committee was a committee that was put together in 1972 following Ted William's Hall of Fame speech in 1966 pushing for the induction of Negro Leaguers.")
    st.write("The Golden Days Era Committee was a committee that replaced the Golden Era Committee in 2016. This committee considers players who played the majority of their career between 1950 and 1969. ")
    st.write("The Expansion Era Committee was a committee that replaced the Veteran's Committee in 2010. This committee considers players who played the majority of their career between 1973-current. ")

    
