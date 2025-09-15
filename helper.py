def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values(by="Gold", ascending=False).reset_index()
    medal_tally["Total"] = (medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"])

    medal_tally["Gold"] = medal_tally["Gold"].astype(int)
    medal_tally["Silver"] = medal_tally["Silver"].astype(int)
    medal_tally["Bronze"] = medal_tally["Bronze"].astype(int)
    medal_tally["Total"] = medal_tally["Total"].astype(int)

    return medal_tally


def country_year_list(df):

    # Extracting years from df
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    # Extracting countries from df
    countries = df["region"].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, "Overall")

    return years, countries


def sport_list(df):
    
    # Extracting sport from df
    sports = df["Sport"].unique().tolist()
    sports.sort()
    sports.insert(0, "Overall")

    return sports


def fetch_medal_tally(df, year, country):
   
   medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
   flag = 0

   if year == "Overall" and country == "Overall":
    temp_df = medal_df
   if year == "Overall" and country != "Overall":
    flag = 1
    temp_df = medal_df[medal_df["region"] == country]
   if year != "Overall" and country == "Overall":
    temp_df = medal_df[medal_df["Year"] == int(year)]
   if year != "Overall" and country != "Overall":
    temp_df = medal_df[(medal_df["Year"] == int(year)) & (medal_df["region"] == country)]

   if flag == 1:
     x = temp_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values(by="Year").reset_index()
   else:
     x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values(by="Gold", ascending=False).reset_index()
     
   x["Total"] = (x["Gold"] + x["Silver"] + x["Bronze"])
    
   return x



def data_over_time(df, column):
  
  data_over_time = df.groupby("Year")[column].nunique().sort_index().to_frame().reset_index().rename(columns={column: "count"})

  return data_over_time



def most_successful_athlete_by_sport(df, sport="Overall"):
    # Keep only rows with medals
    temp_df = df.dropna(subset=["Medal"])

    # Filter by sport if needed
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    # Count medals per athlete
    athlete_medals = temp_df["Name"].value_counts().reset_index()
    athlete_medals.columns = ["Name", "Medal Count"]

    # Merge with original df to get Sport & Region
    merged = athlete_medals.merge(
        df.drop_duplicates("Name")[["Name", "Sport", "region"]],
        on="Name",
        how="left"
    )

    return merged



def yearwise_medal_count_for_country(df, country):
    
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    temp_df = temp_df.groupby(["region", "Year"])["Medal"].count().to_frame().reset_index()
    temp_df = temp_df[temp_df["region"] == country]

    return temp_df



def countrywise_sport_heatmap(df, country):
    
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    pivot_table = temp_df[temp_df["region"] == country].pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0)
    
    return pivot_table



def most_successful_athlete_by_country(df, country):
    # Keep only rows with medals
    temp_df = df.dropna(subset=["Medal"])

    # Filter by country if needed
    temp_df = temp_df[temp_df["region"] == country]

    # Count medals per athlete
    athlete_medals = temp_df["Name"].value_counts().reset_index()
    athlete_medals.columns = ["Name", "Medal Count"]

    # Merge with original df to get Sport & Region
    merged = athlete_medals.merge(
        df.drop_duplicates("Name")[["Name", "Sport"]],
        on="Name",
        how="left"
    )

    return merged



def medalist_age_dist(df):
   
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year", "Sport", "Event", "City"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    return [x1,x2,x3,x4]



def gold_medalist_age_dist_by_sport(df):
   
    athlete_df = df.drop_duplicates(
        subset=["Name", "region", "Year", "Sport", "Event", "City"]
    )

    # Get top 20 sports
    famous_sports = (
        athlete_df["Sport"]
        .value_counts()
        .head(20)
        .index
        .tolist()
    )

    y2 = []
    labels = []

    for sport in famous_sports:
        ages = athlete_df[
            (athlete_df["Medal"] == "Gold") & (athlete_df["Sport"] == sport)
        ]["Age"].dropna()
        
        # Ensure at least 2 unique values
        if ages.nunique() > 1:
            y2.append(ages.tolist())
            labels.append(sport)

    return y2, labels



def height_VS_weight(df, sport="Overall"):
    
    df["Medal"].fillna("No Medal", inplace=True)
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year", "Sport", "Event", "City"])
    if sport != "Overall":    
        athlete_df = athlete_df[athlete_df["Sport"] == sport]

    return athlete_df



def male_vs_female_participation(df):
   
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year", "Sport", "Event", "City"])
    men = athlete_df[athlete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index().rename(columns={"Name": "Male"})
    women = athlete_df[athlete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index().rename(columns={"Name": "Female"})
    temp_df = men.merge(women, on="Year", how="left")
    temp_df.fillna(0, inplace=True)

    return temp_df