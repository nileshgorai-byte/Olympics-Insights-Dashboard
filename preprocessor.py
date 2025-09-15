import pandas as pd


def preprocess(df, region_df):

    # Filtering by season
    df = df[df["Season"]=="Summer"]

    # Merging the dataframes
    df = df.merge(region_df, on="NOC", how="left")

    # Dropping duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding "Medal" column
    df = pd.concat([df, pd.get_dummies(df["Medal"], dtype=int)], axis=1)

    return df