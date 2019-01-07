import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june'] # creates a list of all the months
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] # creates a list of all the days
time_filters = ['month', 'day', 'both', 'none'] # creates a list of all the time filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) time_filter - the time filter that has been selected by the user; month, day, both or none.    
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    
    while True:        
        city = input("Would you like to see the data from Chicago, New York City or Washington?\n").lower()
        if city in CITY_DATA:
            while True:
                time_filter = input("Would you like to filter the data by month, day, both or not at all? Type 'none' for no time filter.\n").lower()
                if time_filter in time_filters:
                    if time_filter == 'month':
                        # get user input for month (all, january, february, ... , june)
                        while True:
                            month = input("Which month?\n").lower()
                            if month in months:
                                day = 'all'
                                break
                            else:
                                print("Invalid input. Data only available for months january through june.")
                                continue
                    elif time_filter == 'day':                        
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        while True:
                            day = input("Which day?\n").lower()
                            if day in days:
                                month = 'all'
                                break
                            else:
                                print("Unrecognized input.")
                                continue
                    elif time_filter == 'both':
                        # get user input for month (all, january, february, ... , june)
                        while True:
                            month = input("Which month?\n").lower()
                            if month in months:
                                day = 'all'
                                break
                            else:
                                print("Invalid input. Data only available for months january through june.")
                                continue
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        while True:
                            day = input("Which day?\n").lower()
                            if day in days:
                                month = 'all'
                                break
                            else:
                                print("Unrecognized input.")
                                continue
                    elif time_filter == 'none':
                        month = 'all'
                        day = 'all'
                    break
                else:
                    print("Invalid input. Please type one of the following acceptable inputs: month, day, both or none.")
                    continue    
            break
        else:
            print("Invalid input. Please select one of the aforementioned three cities.")
            continue    
    
    print('-'*40)
    return city, month, day, time_filter

# the while loops used above were referenced from:- https://stackoverflow.com/questions/22971667/how-to-check-if-a-variable-matches-any-item-in-list-using-the-any-function

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        original_df - unfiltered dataframe obtained from reading the csv data-file
        filtered_df - Pandas DataFrame containing city data filtered by month and day
    """
    original_df = pd.read_csv(CITY_DATA[city])
    # change values in start time column to datetime format
    original_df['Start Time'] = pd.to_datetime(original_df['Start Time'])
    # make a new column titled month with month value taken from start time of corresponding trip
    original_df['month'] = original_df['Start Time'].dt.month
    # make a new column titled day_of_week with week-day value taken from start time of corresponding trip
    original_df['day_of_week'] = original_df['Start Time'].dt.weekday_name
    # change values in End Time column to datetime format
    original_df['End Time'] = pd.to_datetime(original_df['End Time'])
    filtered_df = original_df.copy(deep=True)
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        filtered_df = filtered_df[filtered_df['month'] == month]
            
    if day != 'all':
        # filter by day of week to create the new dataframe
        filtered_df = filtered_df[filtered_df['day_of_week'] == day.title()]
    
    return filtered_df, original_df

def time_stats(df, tf):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    if tf != 'month' and tf != 'both':
        most_common_month = df['Start Time'].dt.month.mode()[0]
        print("The modal month is: ", most_common_month)

    # display the most common day of week    
    if tf != 'day' and tf != 'both':
        most_common_day = df['Start Time'].dt.weekday_name.mode()[0]
        print("The modal day of the week is: ", most_common_day)

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("The modal hour is: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode().to_string(index=False)
    
    print("The most commonly used start station: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode().to_string(index=False)
    
    print("The most commonly used end station: ", most_common_end_station)

    # display most frequent combination of start station and end station trip    
    df['Trip Route'] = df['Start Station'].combine(df['End Station'], lambda x, y: "From " + x + " to " + y) # creates a column called Trip Route; ideas taken from https://stackoverflow.com/questions/47598343/merge-two-columns-in-the-same-pandas-dataframe to create the column        
    trip_frequency = df['Trip Route'].value_counts() # calculates the frequency of different routes
    print("The most frequent combination(s) of start station and end station trip alongwith corresponding frequency:\n", trip_frequency[trip_frequency == trip_frequency.max()])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_in_days_hours_mins_secs(s):
    if s < 60:
        print("{} seconds".format(s))
    elif s < 3600:
        t_m = s // 60
        t_s = s % 60
        print("{} minutes and {} seconds".format(t_m, t_s))
    elif s < 86400:
        t_hr = s // 3600
        t_min = (s % 3600) // 60
        t_sec = (s % 3600) % 60
        print("{} hours, {} minutes and {} seconds".format(t_hr, t_min, t_sec))
    else:
        t_days = s // 86400
        t_hours = (s % 86400) // 3600
        t_minutes = ((s % 86400) % 3600) // 60
        t_seconds = ((s % 86400) % 3600) % 60
        print("{} days, {} hours, {} minutes, {} seconds.".format(t_days, t_hours, t_minutes, t_seconds))    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    print("Total travel time: \n")
    time_in_days_hours_mins_secs(trip_duration)
    
    # display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print("Average travel time: \n")
    time_in_days_hours_mins_secs(average_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The number of people belonging to different user types:\n", df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print("The number of males and females: \n", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("The earliest year of birth: {}, the most recent year of birth: {}, the most common year of birth: {}.".format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(dataframe, row):
    """Displays first five lines of the original dataframe on user's request; 
    displays the next five lines on user's further response"""
    while True:
        see_dataframe = input("Would you like to see individual journey data? Respond with a 'yes' or 'no'.\n")
        if see_dataframe == 'yes':        
            dp = dataframe.iloc[row: row+5]
            print(dp)
            row += 5
            return display_data(dataframe, row)            
        elif see_dataframe == 'no':
            break
        else:
            print("Invalid input.")
            continue
    

def main():
    while True:
        
        city, month, day, time_filter = get_filters()
        
        df, original_df = load_data(city, month, day)

        time_stats(df, time_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(original_df, 0)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
