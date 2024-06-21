import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    nations_over_time.sort_values('Edition', inplace=True)
    return nations_over_time

def data_over_time1(df, col):
    print("Original DataFrame:\n", df.head())
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    print("After dropping duplicates and value counts:\n", nations_over_time.head())
    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'count'}, inplace=True)
    print("After renaming columns:\n", nations_over_time.head())
    nations_over_time.sort_values('Edition', inplace=True)
    print("After sorting by Edition:\n", nations_over_time.head())
    return nations_over_time

def data_over_time1(df, col):
    # Drop duplicates based on 'Year' and the specified column
    unique_years = df.drop_duplicates(['Year', col])
    print("Unique Years:\n", unique_years.head())
    # Count the occurrences of each year
    year_counts = unique_years['Year'].value_counts().reset_index()
    print("Year Counts Before:\n", year_counts.head())
    # Rename the columns appropriately
    year_counts.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    print("Year Counts After:\n", year_counts.head())
    # Sort the DataFrame by 'Edition'
    year_counts.sort_values('Edition', inplace=True)
    return year_counts

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise1(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def most_successful_countrywise(df, country):
    print("Original DataFrame:\n", df.head())

    # Drop rows with missing values in the 'Medal' column
    temp_df = df.dropna(subset=['Medal'])
    print("After dropping NaNs in 'Medal' column:\n", temp_df.head())

    # Filter the DataFrame for the specified country
    temp_df = temp_df[temp_df['region'] == country]
    print(f"After filtering for country ({country}):\n", temp_df.head())

    # Get the top 10 names by medal count
    name_counts = temp_df['Name'].value_counts().reset_index().head(10)
    print("Top 10 names by medal count:\n", name_counts)

    # Rename columns for clarity before merge
    name_counts.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
    print("After renaming columns in name_counts:\n", name_counts)

    # Merge with the original DataFrame
    x = name_counts.merge(df, on='Name', how='left')
    print("After merging with original DataFrame:\n", x.head())

    # Select and drop duplicate columns
    x = x[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    print("After selecting columns and dropping duplicates:\n", x.head())

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final