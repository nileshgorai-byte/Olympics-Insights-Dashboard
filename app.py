import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor,helper


df = pd.read_csv("athlete_events.zip")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Insights Dashboard (1896-2016)")
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm9Woez6whjI8eUvdrZF6ISbsIZcCgYpie0A&s')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)



if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    flag = 1
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year:", years)
    selected_country = st.sidebar.selectbox("Select Country:", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.header(f"Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.header(f"Medal Tally in {selected_year} Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        if (medal_tally["Total"] ==0).all() :
            flag = 0
        st.header(f"{selected_country} Overall Olympics Medal Tally")
    if selected_year != "Overall" and selected_country != "Overall":
        if (medal_tally["Total"] ==0).all() :
            flag = 0
        st.header(f"{selected_country} Medal Tally in {selected_year} Olympics")

    filtered_tally = medal_tally[medal_tally["Total"] != 0]
    if flag == 1:
        fig = px.choropleth(filtered_tally,
                    locations='region',
                    locationmode='country names', # Or 'ISO-3', 'USA-states', etc.
                    color='Total',
                    color_continuous_scale='Viridis')

        fig.update_geos(
        projection_type="natural earth",
        showcountries=True, countrycolor="Black",
        )
        st.plotly_chart(fig)
    else:
        pass

    st.table(medal_tally)




if user_menu == 'Overall Analysis':

    editions = df["Year"].nunique()
    cities = df["City"].nunique()
    events = df["Event"].nunique()
    sports = df["Sport"].nunique()
    athletes = df["Name"].nunique()
    nations = df["region"].nunique()

    st.title("Top Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)


    nations_over_time = helper.data_over_time(df, column="region")
    fig = px.line(
        data_frame=nations_over_time,
        x="Year",
        y="count",
    )
    fig.update_layout(xaxis_title="Edition [Year]", yaxis_title="Nations [count]")
    st.header("Participating Nations over the years")
    st.plotly_chart(fig)


    events_over_time = helper.data_over_time(df, column="Event")
    fig = px.line(
        data_frame=events_over_time,
        x="Year",
        y="count",
    )
    fig.update_layout(xaxis_title="Edition [Year]", yaxis_title="Events [count]")
    st.header("Events over the years")
    st.plotly_chart(fig)


    athletes_over_time = helper.data_over_time(df, column="Name")
    fig = px.line(
        data_frame=athletes_over_time,
        x="Year",
        y="count",
    )
    fig.update_layout(xaxis_title="Edition [Year]", yaxis_title="Athletes [count]")
    st.header("Athletes over the years")
    st.plotly_chart(fig)


    st.header("Sport-wise events over the years")
    x = df.drop_duplicates(subset=["Year", "Event", "Sport"])
    fig,ax = plt.subplots(figsize=(15,15))
    sns.heatmap((x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)), annot=True, ax=ax)
    st.pyplot(fig)


    st.header("Most successful Athlete")
    sports = helper.sport_list(df)
    selected_sport = st.selectbox("Select Sport:", sports)
    x = helper.most_successful_athlete_by_sport(df, sport=selected_sport)
    st.table(x.head(100))




if user_menu == "Country-wise Analysis":

    st.title("Country-wise Analysis")
    
    countries = helper.country_year_list(df)[1]
    selected_country_y = st.sidebar.selectbox("Select country:", countries[1:])
    y = helper.yearwise_medal_count_for_country(df, country=selected_country_y)
    fig = px.line(
        data_frame = y,
        x = "Year",
        y = "Medal",
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Medal [Count]")
    st.header(f"{selected_country_y}: Olympics Medal count")
    st.plotly_chart(fig)


    st.header(f"Sports contributing most Medals to {selected_country_y}")
    pivot_table = helper.countrywise_sport_heatmap(df, country=selected_country_y)
    fig, ax = plt.subplots(figsize=(15,15))
    sns.heatmap(pivot_table, annot=True, ax=ax)
    st.pyplot(fig)


    st.header(f"Most celebrated Athletes of {selected_country_y}")
    x = helper.most_successful_athlete_by_country(df, country=selected_country_y)
    st.table(x.head(10))



if user_menu == "Athlete-wise Analysis":

    st.title("Athlete-wise Analysis")
    st.header("Age Distribution of Medalists")
    medalist_age_list = helper.medalist_age_dist(df)
    fig = ff.create_distplot(medalist_age_list,
                              ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                                show_hist=False, 
                                show_rug=False)
    fig.update_layout(xaxis_title="Age [Year]", yaxis_title="Probability of winning Medal", width=800, height=600)
    st.plotly_chart(fig)


    
    st.header("Gold Medalist Age distribution by Sport")
    y2, labels = helper.gold_medalist_age_dist_by_sport(df)
    # Create distplot
    if y2:  # only plot if we have valid data
        fig = ff.create_distplot(y2, labels, show_hist=False, show_rug=False)
        fig.update_layout(xaxis_title="Age [Year]", yaxis_title="Probability of winning Medal", width=800, height=600)
        st.plotly_chart(fig)
    else:
        st.write("Not enough data to plot distribution.")



    st.header("Height VS Weight")
    sports = helper.sport_list(df)
    selected_sport = st.selectbox("Select Sport:", sports)
    z = helper.height_VS_weight(df, selected_sport)
    fig,ax = plt.subplots(1,2,figsize=(18,9))
    sns.scatterplot(data=z[z["Sex"]=="M"], x="Weight", y="Height", hue="Medal", s=100, ax=ax[0])
    sns.scatterplot(data=z[z["Sex"]=="F"], x="Weight", y="Height", hue="Medal", s=100, ax=ax[1])
    ax[0].set_xlabel("Weight [Kg]")
    ax[0].set_ylabel("Height [cm]")
    ax[1].set_xlabel("Weight [Kg]")
    ax[1].set_ylabel("Height [cm]")
    ax[0].set_title("Male")
    ax[1].set_title("Female")
    st.pyplot(fig)


    st.header("Participation over the Years")
    z1 = helper.male_vs_female_participation(df)
    fig = px.line(
        data_frame=z1,
        x="Year",
        y=["Male","Female"],
    )
    fig.update_layout(xaxis_title="Edition [Year]", yaxis_title="Count")
    st.plotly_chart(fig)



st.markdown(
    """
    <div style="margin-top: 50px; padding: 10px; background-color: #f5f5f5;
                border-top: 1px solid #ddd; text-align: center; font-size: 13px; color: #555;">
        ⚠️ <b>Disclaimer:</b> The analysis may contain discrepancies due to political renaming of nations 
        and the 1906 Intercalated Games, which are no longer recognized as official Olympics.
    </div>
    """,
    unsafe_allow_html=True

)

