import streamlit as st
import pandas as pd
import altair as alt

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


st.title("Player Elections by Year")
st.header("Notable Ballots")
st.write("There have been nine years where no BBWAA election was held: 1940, 1941, 1943, 1944, 1957, 1959, 1961, 1963, 1965 ")
st.write("There have been nine years where the BBWAA election resulted in no players being elected: 1945, 1950, 1958, 1960, 1965, 1971, 1996, 2013, 2021")
st.write("Because of the backlog of player voting that resulted from World War 2 where only one player was elected between 1940-1944, 1945 and 1946 represented two of the highest election totals in HOF voting history with the 10 elected in 1946 representing the highest total in an individual year.  ")

df=df[(df.hof == "Yes")]
df = df.drop(df.columns[[0,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]], axis = 1)
df.drop_duplicates(subset='name', keep="last", inplace=True)
df.sort_values(['year_voted_into_hof','committee'], inplace=True)
counts = df.year_voted_into_hof.value_counts()
counts = counts.rename_axis('year').reset_index()
counts.sort_values(['year'], inplace=True)
counts.rename(columns = {'year_voted_into_hof':'count'}, inplace = True)


line = alt.Chart(counts).mark_line(color='red ').encode(
    alt.X('year:O', axis=alt.Axis(values=list(range(1936, 2022, 2)), title = 'Year')),
    alt.Y('count', axis=alt.Axis( title = 'Number of Players Elected')), 
    tooltip = [alt.Tooltip('year'), alt.Tooltip('count', title="Players Elected")]
).interactive()

line
