import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

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

st.title("Major League Baseball Hall of Fame Inductees")
st.header("HOF Voting, Rules, and History")

col1, col2, col3 = st.columns(3)

with col1:
    df=df[(df.hof == "Yes")]
    df = df.drop(df.columns[[0,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]], axis = 1)
    df.drop_duplicates(subset='name', keep="last", inplace=True)
    df.sort_values(['year_voted_into_hof','committee'], inplace=True)
    df.rename(columns = {'year_voted_into_hof':'Year','name' : 'Name', 'committee' : 'Committee'}, inplace = True)
    df = df[['Name', 'Year']].reset_index(drop=True)
    new_row= pd.DataFrame({'Year':'', 'Name':''}, index=[0])
    df2 = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)
    name_choice = st.sidebar.selectbox('Select a Player:', df2.Name)
    if name_choice =="":
        df
    else:       
        df.loc[(df['Name']==name_choice)]

with col2:
    st.write("Of the 4 major United States sports, no sport places Hall of Fame (HOF) voting under as much importance and scuitny as Major League Baseball (MLB). MLB HOF voting has been taking place since 1936.  The voting for hall of fame election is held annually by the Baseball Writers' Association of America (BBWAA).")
    st.write("Players become eligible for HOF voting if they have played for at least 10 Major League seasons, some of which must have occurred between 20 years before and 5 years prior to the election (assuming the player is still living). When voting, a BBWAA comittee elector can vote for no more than 10 eligible candidates on the ballot. Players that receive votes on 75% or more of the total ballots cast shall be elected into the National Baseball Hall of Fame. Players were eligible to be on the HOF ballot for 15 years until the 2015 voting when it was reduced to 10 years. If a player is not elected on their final appearance on the ballot then they may be eligible to appear on a future ballot made up of a small committee of voters that are associated with MLB (former players, executives, coaches, etc. ).")

with col3: 
    st.write("In recent years, the ballot has been clouded in controversy because numerous off the field stories have dominated the voting discussion. Many of the notable alleged performance enhancing drug (PED) users from the Steroid Era, including most recently Barry Bonds, Roger Clemens, and Sammy Sosa, have fallen off the ballot. Manny Ramirez and Alex Rodriguez, both of whom were suspended during their careers because of PED use, are on the ballot but neither have garnered even 35% of the votes needed for election. Curt Schilling, known for his turbulent relations with the media and failed business that cost taxpayers roughly $112 million, also fell off the ballot. Andruw Jones was arrested for domestic violence and Omar Vizquel has been accused of domestic violence.")


def page2():
    st.markdown("Player Elections by Year")
    st.sidebar.markdown("Player Elections by Year")

def page3():
    st.markdown("Breakdown by Committee")
    st.sidebar.markdown("Breakdown by Committee")

def page4():
    st.markdown("HOF by WAR")
    st.sidebar.markdown("HOF by WAR")

def page5():
    st.markdown("HOF Offensive Production")
    st.sidebar.markdown("HOF Offensive Production")

def page6():
    st.markdown("HOF Pitching Production")
    st.sidebar.markdown("HOF Pitching Production")
