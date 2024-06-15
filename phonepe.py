import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image  #python import Library

#dataframe creation

mydb=pymysql.connect(host="localhost",
                     user="root",
                     port=3306,
                     database="phonepe_data",
                     password="1234")

cursor=mydb.cursor()


#aggregate_transaction_df
cursor.execute("select * from aggregated_transaction")
mydb.commit()
table1=cursor.fetchall()

aggre_transaction=pd.DataFrame(table1,columns=("States","years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregate_user_df
cursor.execute("select * from aggregated_user")
mydb.commit()
table2=cursor.fetchall()

aggre_user=pd.DataFrame(table2,columns=("States","years","Quarter","Brands","Transaction_count","percentage"))

#map_transaction_df
cursor.execute("select * from mapped_transaction")
mydb.commit()
table3=cursor.fetchall()

map_transaction=pd.DataFrame(table3,columns=("States","years","Quarter","Districts","Transaction_count","Transaction_amount"))


#map_user_df
cursor.execute("select * from mapped_user")
mydb.commit()
table4=cursor.fetchall()

map_user=pd.DataFrame(table4,columns=("States","years","Quarter","Districts","registeredUsers","appOpens"))


#top_transaction_df
cursor.execute("select * from topped_transaction")
mydb.commit()
table5=cursor.fetchall()

top_transaction=pd.DataFrame(table5,columns=("States","years","Quarter","pincodes","Transaction_count","Transaction_amount"))

#top_user_df
cursor.execute("select * from topped_users")
mydb.commit()
table6=cursor.fetchall()

top_users=pd.DataFrame(table6,columns=("States","years","Quarter","pincodes","registeredUsers"))






def Transaction_amount_count_y(df,year):

    transc_accnt_amnt_year=df[df["years"] == year]
    transc_accnt_amnt_year.reset_index(drop=True,inplace=True)

    transc_accnt_amnt_year_group=transc_accnt_amnt_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    transc_accnt_amnt_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(transc_accnt_amnt_year_group, x="States", y="Transaction_amount", 
                        title=f"{year} YEAR  QUARTER TRANSACTION AMOUNT" ,
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=700 ,width=600)
        st.plotly_chart(fig_amount)




    with col2:

        fig_count=px.bar(transc_accnt_amnt_year_group, x="States", y="Transaction_count",   
                       title=f"{year} YEAR QUARTER TRANSACTION COUNT", 
                       color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for Feature in data1['features']:
            states_name.append(Feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(transc_accnt_amnt_year_group,geojson=data1,locations="States",featureidkey="properties.ST_NM",
        color="Transaction_amount",color_continuous_scale="Rainbow",
        range_color=(transc_accnt_amnt_year_group['Transaction_amount'].min(),transc_accnt_amnt_year_group['Transaction_amount'].max()),
        hover_name="States",title= f"{year}  TRANSACTION AMOUNT",fitbounds="locations",
        height=550,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)


    with col2:

        fig_india_2=px.choropleth(transc_accnt_amnt_year_group,geojson=data1,locations="States",featureidkey="properties.ST_NM",
        color="Transaction_count",color_continuous_scale="Rainbow",
        range_color=(transc_accnt_amnt_year_group['Transaction_count'].min(),transc_accnt_amnt_year_group['Transaction_count'].max()),
        hover_name="States",title= f"{year}  TRANSACTION COUNT",fitbounds="locations",
        height=550,width=550)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return transc_accnt_amnt_year

def Transaction_amount_count_y_Q(df,quarter):
    transc_accnt_amnt_year=df[df["Quarter"] == quarter]
    transc_accnt_amnt_year.reset_index(drop=True,inplace=True)

    transc_accnt_amnt_year_group=transc_accnt_amnt_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    transc_accnt_amnt_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(transc_accnt_amnt_year_group,x="States",y="Transaction_amount",title=f"{transc_accnt_amnt_year['years'].min()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=700,width=600)

        st.plotly_chart(fig_amount)



    with col2:
        fig_count=px.bar(transc_accnt_amnt_year_group,x="States",y="Transaction_count",title=f"{transc_accnt_amnt_year['years'].min()} YEAR {quarter}  QUARTER TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=600)
        
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for Feature in data1['features']:
            states_name.append(Feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(transc_accnt_amnt_year_group,geojson=data1,locations="States",featureidkey="properties.ST_NM",
        color="Transaction_amount",color_continuous_scale="Rainbow",
        range_color=(transc_accnt_amnt_year_group['Transaction_amount'].min(),transc_accnt_amnt_year_group['Transaction_amount'].max()),
        hover_name="States",title= f"{transc_accnt_amnt_year['years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
        height=650,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:   
 
        fig_india_2=px.choropleth(transc_accnt_amnt_year_group,geojson=data1,locations="States",featureidkey="properties.ST_NM",
        color="Transaction_count",color_continuous_scale="Rainbow",
        range_color=(transc_accnt_amnt_year_group['Transaction_count'].min(),transc_accnt_amnt_year_group['Transaction_count'].max()),
        hover_name="States",title= f"{transc_accnt_amnt_year['years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
        height=650,width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return transc_accnt_amnt_year

#aggregate_Transaction_analysis

def aggre_Transc_type(df,state):

    transc_accnt_amnt_year=df[df["States"] == state]
    transc_accnt_amnt_year.reset_index(drop=True, inplace=True)

    transc_accnt_amnt_year_group=transc_accnt_amnt_year.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    transc_accnt_amnt_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=transc_accnt_amnt_year_group, names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2=px.pie(data_frame=transc_accnt_amnt_year_group, names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pie_2)

#aggregate_user_analysis

def aggre_user_plot_1(df,year):
    agg_user_yr=df[df["years"]==year]
    agg_user_yr.reset_index(drop=True,inplace=True)

    agg_user_yr_grp=pd.DataFrame(agg_user_yr.groupby("Brands")["Transaction_count"].sum())
    agg_user_yr_grp.reset_index(inplace=True)
    
    fig_bar_1=px.bar(agg_user_yr_grp, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",width=800,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return agg_user_yr


#aggregate_user quarter anlysis
def aggr_user_plot2(df,quarter):
    agg_user_yr_qrtr=df[df["Quarter"]==quarter]
    agg_user_yr_qrtr.reset_index(drop=True,inplace=True)

    agg_user_yr_qrtr_grp=pd.DataFrame(agg_user_yr_qrtr.groupby("Brands")["Transaction_count"].sum())
    agg_user_yr_qrtr_grp.reset_index(inplace=True)

    fig_bar_1=px.bar(agg_user_yr_qrtr_grp, x="Brands", y="Transaction_count", title=f"{quarter}QUARTER, BRANDS AND TRANSACTION COUNT",width=800,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return agg_user_yr_qrtr

#agree_user states analysis 
def aggr_user_plot3(df,state):
    aggre_user_year_qrtr_state=df[df["States"]==state]
    aggre_user_year_qrtr_state.reset_index(drop=True,inplace=True)
    

    fig_line_1=px.line(aggre_user_year_qrtr_state, x="Brands", y="Transaction_count", hover_data="percentage",
                    title=f"{state.upper()} BRANDS , TRANSACTION_COUNT , PERCENTAGE",width=1000,markers=True)

    st.plotly_chart(fig_line_1)


#map_transaction district analysis

def map_district_Transc_type(df,state):

    transc_accnt_amnt_year=df[df["States"] == state]
    transc_accnt_amnt_year.reset_index(drop=True, inplace=True)
    
    transc_accnt_amnt_year_group=transc_accnt_amnt_year.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    transc_accnt_amnt_year_group.reset_index(inplace=True)

    col1,col2 =st.columns(2)

    with col1:
        fig_bar_1=px.bar(data_frame=transc_accnt_amnt_year_group, x="Transaction_amount",y="Districts",orientation="h", height=600,title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(data_frame=transc_accnt_amnt_year_group, x="Transaction_count",y="Districts",orientation="h",height=600,title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_2)

    return transc_accnt_amnt_year



# map_user year analysis
def map_user_plot_1(df,year):
    
    map_user_year=df[df["years"]==year]
    map_user_year.reset_index(drop=True,inplace=True)

    map_user_year_grp=map_user_year.groupby("States")[["registeredUsers","appOpens"]].sum()
    map_user_year_grp.reset_index(inplace=True) 


    fig_line_1=px.line(map_user_year_grp, x="States", y=["registeredUsers","appOpens"],
                        title=f"{year} REGISTERED USERS,APPOPENS",width=1000,height=800,markers=True)

    st.plotly_chart(fig_line_1)

    return map_user_year

# map_user year-quarter analysis
def map_user_plot_2(df,quarter):
    map_user_year_quarter=df[df["Quarter"]==quarter]
    map_user_year_quarter.reset_index(drop=True,inplace=True)

    map_user_year_quarter_grp=map_user_year.groupby("States")[["registeredUsers","appOpens"]].sum()
    map_user_year_quarter_grp.reset_index(inplace=True) 


    fig_line_1=px.line(map_user_year_quarter_grp, x="States", y=["registeredUsers","appOpens"],
                        title=f"{df['years'].min()} YEAR {quarter} QUARTER REGISTERED USERS,APPOPENS",width=1000,height=800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_line_1)

    return map_user_year_quarter


def map_user_plot_3(df,states):
    map_user_year_quarter_state=df[df["States"]==states]
    map_user_year_quarter_state.reset_index(drop=True,inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(map_user_year_quarter_state, x="registeredUsers",y="Districts",orientation="h",title=f"{states.upper()} REGISTERED USER",height=800,                        
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(map_user_year_quarter_state, x="appOpens",y="Districts",orientation="h",title=f"{states.upper()} APPOPENS",height=800,                        
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_map_user_bar_2)

        return map_user_year_quarter
    
    
#Top_transaction state analysis
def top_transaction_plot_1(df,state):
    top_user_year_states=df[df["States"]==state]
    top_user_year_states.reset_index(drop=True,inplace=True)

    
    fig_top_user_bar_1=px.bar(top_user_year_states, x="Quarter",y="Transaction_amount",hover_data="pincodes",
                            title="TRANSACTION AMOUNT",height=650,width=600,color_discrete_sequence=px.colors.sequential.GnBu_r)
        
    st.plotly_chart(fig_top_user_bar_1)

    fig_top_user_bar_2=px.bar(top_user_year_states, x="Quarter",y="Transaction_count",hover_data="pincodes",
                            title="Transaction_count",height=650,width=600,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        
    st.plotly_chart(fig_top_user_bar_2)

#top_user_year analysis
def top_user_plot_1(df,year):
    top_users_year=df[df["years"]==year]
    top_users_year.reset_index(drop=True,inplace=True)

    top_users_year_grp=pd.DataFrame(top_users_year.groupby(["States","Quarter"])["registeredUsers"].sum())
    top_users_year_grp.reset_index(inplace=True)

    fig_top_plot_1=px.bar(top_users_year_grp,x="States",y="registeredUsers",color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return top_users_year   

#top_user_state analysis
def top_user_plot_2(df,state):
    top_user_year_state=df[df['States']==state]
    top_user_year_state.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(top_user_year_state,x="Quarter",y="registeredUsers",title="REGISTEREDUSERS,PINCODES, QUARTERS",
                        width=1000, height=800, color="registeredUsers", hover_data="pincodes",
                        color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_2)

    return top_user_year_state


def top_chart_transaction_amount(table_name):
    mydb=pymysql.connect(host="localhost",
                        user="root",
                        port=3306,
                        database="phonepe_data",
                        password="1234")

    cursor=mydb.cursor()

    #plot 1
    query1= f'''select States,sum(Transaction_amount) as Transaction_amount from {table_name}
                group by States
                order by Transaction_amount DESC
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("States","Transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount1=px.bar(df_1,x="States",y="Transaction_amount",title= "TOP 10 OF TRANSACTION_AMOUNT",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #plot 2
    query2=f'''select States,sum(Transaction_amount) as Transaction_amount from {table_name}
                group by States
                order by Transaction_amount
                limit 10;'''

    cursor.execute(query2)
    table=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table,columns=("States","Transaction_amount"))

    with col2:
        fig_amount2=px.bar(df_2,x="States",y="Transaction_amount",title= "LAST 10 OF TRANSACTION_AMOUNT",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #plot 3
    query3=f'''select States, AVG(Transaction_amount) as Transaction_amount from {table_name}
                group by States
                order by Transaction_amount;'''

    cursor.execute(query3)
    table=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table,columns=("States","Transaction_amount"))

    fig_amount3=px.bar(df_3,x="Transaction_amount",y="States",title= "AVERAGE OF TRANSACTION_AMOUNT",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount3)


def top_chart_transaction_count(table_name):
    mydb=pymysql.connect(host="localhost",
                        user="root",
                        port=3306,
                        database="phonepe_data",
                        password="1234")

    cursor=mydb.cursor()

    #plot 1
    query1= f'''select States,sum(Transaction_count) as Transaction_count from {table_name}
                group by States
                order by Transaction_count DESC
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("States","Transaction_count"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount1=px.bar(df_1,x="States",y="Transaction_count",title= "TOP 10 OF TRANSACTION COUNT",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #plot 2
    query2=f'''select States,sum(Transaction_count) as Transaction_count from {table_name}
                group by States
                order by Transaction_count
                limit 10;'''

    cursor.execute(query2)
    table=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table,columns=("States","Transaction_count"))

    with col2:

        fig_amount2=px.bar(df_2,x="States",y="Transaction_count",title= "lAST 10 OF TRANSACTION COUNT",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #plot 3
    query3=f'''select States, AVG(Transaction_count) as Transaction_count from {table_name}
                group by States
                order by Transaction_count;'''

    cursor.execute(query3)
    table=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table,columns=("States","Transaction_count"))

    fig_amount3=px.bar(df_3,x="Transaction_count",y="States",title="AVERAGE OF TRANSACTION COUNT",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount3)


#TOP CHART REGISTEREDUSERS ANALYSIS

def top_chart_registered_user(table_name,state):
    mydb=pymysql.connect(host="localhost",
                        user="root",
                        port=3306,
                        database="phonepe_data",
                        password="1234")

    cursor=mydb.cursor()

    #plot 1
    query1= f'''select Districts,sum(registeredUsers) as registeredUsers
                from {table_name}
                where States='{state}'
                group by Districts
                order by registeredUsers DESC
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("Districts","registeredUsers"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount1=px.bar(df_1,x="Districts",y="registeredUsers",title= "TOP 1O OF REGISTEREDUSERS",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #plot 2
    query2=f'''select Districts,sum(registeredUsers) as registeredUsers
                from {table_name}
                where States='{state}'
                group by Districts
                order by registeredUsers 
                limit 10;'''

    cursor.execute(query2)
    table=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table,columns=("Districts","registeredUsers"))

    with col2:

        fig_amount2=px.bar(df_2,x="Districts",y="registeredUsers",title= "LAST 10 OF REGISTEREDUSERS",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #plot 3
    query3=f'''select Districts,AVG(registeredUsers) as registeredUsers
                from {table_name}
                where States='{state}'
                group by Districts
                order by registeredUsers'''

    cursor.execute(query3)
    table=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table,columns=("Districts","registeredUsers"))

    fig_amount3=px.bar(df_3,x="registeredUsers",y="Districts",title="AVG OF REGISTERED USERS",hover_name="Districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount3)

#TOP CHART AppOpens ANALYSIS

def top_chart_AppOpens(table_name,state):
    mydb=pymysql.connect(host="localhost",
                        user="root",
                        port=3306,
                        database="phonepe_data",
                        password="1234")

    cursor=mydb.cursor()

    #plot 1
    query1= f'''select Districts,sum(AppOpens) as AppOpens
                from {table_name}
                where States='{state}'
                group by Districts
                order by AppOpens DESC
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("Districts","AppOpens"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount1=px.bar(df_1,x="Districts",y="AppOpens",title= "TOP 1O OF AppOpens",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #plot 2
    query2=f'''select Districts,sum(AppOpens) as AppOpens
                from {table_name}
                where States='{state}'
                group by Districts
                order by AppOpens 
                limit 10;'''

    cursor.execute(query2)
    table=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table,columns=("Districts","AppOpens"))

    with col2:

        fig_amount2=px.bar(df_2,x="Districts",y="AppOpens",title= "LAST 10 OF AppOpens",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
    st.plotly_chart(fig_amount2)

    #plot 3
    query3=f'''select Districts,AVG(AppOpens) as AppOpens
                from {table_name}
                where States='{state}'
                group by Districts
                order by AppOpens'''

    cursor.execute(query3)
    table=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table,columns=("Districts","AppOpens"))

    fig_amount3=px.bar(df_3,x="AppOpens",y="Districts",title="AVG OF AppOpens",hover_name="Districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount3)


#TOP CHART REGISTEREDUSERS ANALYSIS

def top_chart_registered_users1(table_name):
    mydb=pymysql.connect(host="localhost",
                        user="root",
                        port=3306,
                        database="phonepe_data",
                        password="1234")

    cursor=mydb.cursor()

    #plot 1
    query1= f'''select States,sum(registeredUsers) as registeredUsers  from {table_name}
                group by States
                order by registeredUsers desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("States","registeredUsers"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount1=px.bar(df_1,x="States",y="registeredUsers",title= "TOP 1O OF REGISTEREDUSERS",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #plot 2
    query2=f'''select States,sum(registeredUsers) as registeredUsers  from {table_name}
                group by States
                order by registeredUsers 
                limit 10;'''

    cursor.execute(query2)
    table=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table,columns=("States","registeredUsers"))

    with col2:

        fig_amount2=px.bar(df_2,x="States",y="registeredUsers",title= "LAST 10 OF REGISTEREDUSERS",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #plot 3
    query3=f'''select States,avg(registeredUsers) as registeredUsers  from {table_name}
                group by States
                order by registeredUsers; '''

    cursor.execute(query3)
    table=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table,columns=("States","registeredUsers"))

    fig_amount3=px.bar(df_3,x="registeredUsers",y="States",title="AVG OF REGISTERED USERS",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount3)


# top 50 district
def top_districts():
    map_transaction_top=map_transaction[["Districts","Transaction_amount"]]
    map_transaction_top_group=map_transaction_top.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    map_transaction_top_group=pd.DataFrame(map_transaction_top_group).reset_index().head(50)

    fig_top_1=px.bar(map_transaction_top_group,x="Districts",y="Transaction_amount",title="DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_top_1)

#top Brands Mobile
def top_Brands():
    brand_mobile=aggre_user[["Brands","Transaction_count"]]
    brand_mobile_group=brand_mobile.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand_mobile_group=pd.DataFrame(brand_mobile_group).reset_index()

    fig_Brands=px.pie(brand_mobile_group, values= "Transaction_count", names= "Brands", 
                       color_discrete_sequence=px.colors.sequential.dense_r,
                    title= "Top Mobile Brands of Transaction_count")
    st.plotly_chart(fig_Brands)


def top_state_users():
    least_trans_count_pin=top_transaction[["States","Transaction_count"]]
    least_trans_count_pin_grp=least_trans_count_pin.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    least_trans_count_pin_grp=pd.DataFrame(least_trans_count_pin_grp).reset_index()

    fig_amount3=px.bar(least_trans_count_pin_grp,x="States",y="Transaction_count",title="Mostly using the venue",
                    color_discrete_sequence=px.colors.sequential.Bluered,height=500,width=600)
    st.plotly_chart(fig_amount3)























  


#create streamlit

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select=option_menu("main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select =="HOME":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"D:\capstone project guvi\phonepe images.jpeg"), width=600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"D:\capstone project guvi\phonepe\phone pe images.png"),width=400)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"D:\capstone project guvi\phonepe\phonepe images.png"), width=400)



elif select =="DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    ### transaction Analysis
    with tab1:
        method1 =st.radio("select the method",["Transaction Analysis","User Analysis"])

        if method1 =="Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("select the year",aggre_transaction["years"].min(),aggre_transaction["years"].max(),aggre_transaction["years"].min())
                 
            tranc_year=Transaction_amount_count_y(aggre_transaction,years)

            col1,col2= st.columns(2)
            with col1:
                
                states=st.selectbox("select the State",tranc_year["States"].unique())

            aggre_Transc_type(tranc_year,states)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider("select the Quarter",tranc_year["Quarter"].min(),tranc_year["Quarter"].max(),tranc_year["Quarter"].min())
            
            tranc_year_quarter=Transaction_amount_count_y_Q(tranc_year,quarters)

            col1,col2= st.columns(2)
            with col1:
                
                states=st.selectbox("select the State_trans",tranc_year_quarter["States"].unique())

            aggre_Transc_type(tranc_year_quarter,states)

            
        elif method1 =="User Analysis":

            col1,col2= st.columns(2)
            with col1:
    
                years=st.slider("select the year",aggre_user["years"].min(),aggre_user["years"].max(),aggre_user["years"].min())

                agg_user_yr=aggre_user_plot_1(aggre_user,years)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider("select the Quarter",agg_user_yr["Quarter"].min(),agg_user_yr["Quarter"].max(),agg_user_yr["Quarter"].min())
            
            agg_user_yr_qrtr=aggr_user_plot2(agg_user_yr,quarters)

            col1,col2= st.columns(2)
            with col1:
                
                states=st.selectbox("select the State",agg_user_yr_qrtr["States"].unique())

            aggr_user_plot3(agg_user_yr_qrtr,states)



    with tab2:
        
        method2 =st.radio("select the method",["Map Transaction","Map users"])

        if method2 == "Map Transaction":
       
            col1,col2= st.columns(2)
            with col1:
        
                years=st.slider("select the map_year",map_transaction["years"].min(),map_transaction["years"].max(),map_transaction["years"].min())
                 
            map_tranc_year=Transaction_amount_count_y(map_transaction,years)
     
            col1,col2= st.columns(2)
            with col1:

                states=st.selectbox("select the State map_trans",map_tranc_year["States"].unique())

            map_district_Transc_type(map_tranc_year,states)   

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider("select the Quarter_map",map_tranc_year["Quarter"].min(),map_tranc_year["Quarter"].max(),map_tranc_year["Quarter"].min())
            
            map_tranc_year_quarter=Transaction_amount_count_y_Q(map_tranc_year,quarters)

            col1,col2= st.columns(2)
            with col1:
                
                states_quarter=st.selectbox("select the State_map",map_tranc_year_quarter["States"].unique())

            map_district_Transc_type(map_tranc_year_quarter,states_quarter)


        elif method2 =="Map users":  

            col1,col2= st.columns(2)
            with col1:
                years=st.slider("select the map_year",map_user["years"].min(),map_user["years"].max(),map_user["years"].min())
                 
            map_user_year= map_user_plot_1(map_user,years)


            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the Quarter_map",map_user_year["Quarter"].min(),map_user_year["Quarter"].max(),map_user_year["Quarter"].min())
            
            map_user_year_quarter=map_user_plot_2(map_user_year,quarters)


            col1,col2= st.columns(2)
            with col1:
                
                states_quarter=st.selectbox("select the State_map_user",map_user_year_quarter["States"].unique())

            map_user_plot_3(map_user_year_quarter,states_quarter)

    with tab3:
        method_3=st.radio("select the method",["Top Transaction","Top users"])

        if method_3== "Top Transaction":

            col1,col2= st.columns(2)
            with col1:
        
                years=st.slider("select the top_year",top_transaction["years"].min(),top_transaction["years"].max(),top_transaction["years"].min())
                 
                top_tranc_year=Transaction_amount_count_y(top_transaction,years)



            col1,col2= st.columns(2)
            with col1:
                
                states=st.selectbox("select the top_State",top_tranc_year["States"].unique())

            top_transaction_plot_1(top_tranc_year,states)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider("select the top_Quarter",top_tranc_year["Quarter"].min(),top_tranc_year["Quarter"].max(),top_tranc_year["Quarter"].min())
            
            tranc_year_quarter=Transaction_amount_count_y_Q(top_tranc_year,quarters) 

        elif method_3=="Top users":

            col1,col2= st.columns(2)
            with col1:
        
                years=st.slider("select the top_user_year",top_users["years"].min(),top_users["years"].max(),top_users["years"].min())
                 
                top_user_year=top_user_plot_1(top_users,years)

            col1,col2= st.columns(2)
            with col1:
                
                states=st.selectbox("select the top_user_State",top_user_year["States"].unique())

            top_user_year_state=top_user_plot_2(top_user_year,states)
if select == "TOP CHARTS":
    question=st.selectbox("select the Question",["1.Transaction Amount and count of Aggregated Transaction",
                                                 "2.Transaction Amount and count of Mapped Transaction",
                                                 "3.Transaction Amount and count of Topped Transaction",
                                                 "4.Transaction count of aggregated user",
                                                 "5.Registered users of Mapped user",
                                                 "6.App opens of Mapped User",
                                                 "7.Registered users of topped User",
                                                 "8.Top Districts With Lowest Transaction Amount",
                                                 "9.Top Brands Of Mobiles Used",
                                                 "10.Mostly participate state in tranaction count"
                                                ])
    
    if question == "1.Transaction Amount and count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "2.Transaction Amount and count of Mapped Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("mapped_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("mapped_transaction")

    elif question == "3.Transaction Amount and count of Topped Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Topped_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Topped_transaction")

    elif question == "4.Transaction count of aggregated user":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question =="5.Registered users of Mapped user":

        states=st.selectbox("select the state",map_user['States'].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("mapped_user",states)

    elif question =="6.App opens of Mapped User":

        states=st.selectbox("select the state",map_user['States'].unique())
        st.subheader("APPOPENS")
        top_chart_AppOpens("mapped_user",states)

    elif question =="7.Registered users of topped User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users1("topped_users")

    elif question =="8.Top Districts With Lowest Transaction Amount":
        st.subheader("TOP DISTRICTS")
        top_districts()

    elif question=="9.Top Brands Of Mobiles Used":
        st.subheader("TOP BRANDS MOBILES")
        top_Brands()

    elif question=="10.Mostly participate state in tranaction count":
        st.subheader("TOP STATE USERS")
        top_state_users()











     







                            
















    









