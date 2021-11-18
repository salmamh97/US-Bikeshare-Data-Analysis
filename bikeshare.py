import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        #take input and check if it exists
        city= input("Please select a city from New York City, Washington and Chicago ").lower()
        if city not in CITY_DATA:
            print("Please enter a valid city name ")
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month= input("Please select a month from January to June or type 'all' to select all months ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #check for valid inputs
        if month != 'all' and month not in months:
            print("Please enter a valid month ")
        else:
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input("Please select a day of the week or type 'all' to select all days ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #check for valid inputs
        if day != 'all' and day not in days:
            print("Please enter a valid day ")
        else:
            break



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert start time column to datetime datatype and break it into days, months
    #Note: there's another way to do this by parsing the date while reading the file but I found this one easier
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    #filter by month
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        #filter by month to create new data frame
        df = df[df['month'] == month]
    #filter by day of week
    if day != 'all':
        #just like above we filter by day of week to create data frame
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #notice we use [0] in case mode(x) is an array so [0] always takes the first one by default
    #handling errors
    try:
        most_common_month= df['month'].mode()[0]
        print("Most common month is: {} ".format(calendar.month_name[most_common_month]))

    except KeyError:
        print("please try again")
    #df.reset_index(drop=True) didn't handle the error
    #month is now in numbers so to display it in names we use calendar API
    #calendar.month_name[] returns the equivelent name of a certain month number
    #and the array index of 0 is the empty string, so there's no need to worry about zero-indexing
    #i.e calendar.month_name[3] would return March
    print('\n\n')

    # TO DO: display the most common day of week
    #handle errors while using the project:

    try:
        most_common_day = df['day_of_week'].mode()[0]
        print("Most common day of week is: {} ".format(most_common_day))
        print('\n\n')

    except KeyError:
        print("please try again")
    # TO DO: display the most common start hour
    #first extract hour from start time
    try:
        df['hour'] = df['Start Time'].dt.hour
        most_common_hour= df['hour'].mode()[0]
        print("Most common start hour is: {} ".format(most_common_hour))
        print('\n\n')
    except KeyError:
        print("please try again")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #handling errors
    try:
        common_start_station= df['Start Station'].mode()[0]
        print("Most commonly used start station is: {} ".format(common_start_station))
        print('\n\n')
    except KeyError:
        print("please try again")
    # TO DO: display most commonly used end station
    try:
        common_end_station= df['End Station'].mode()[0]
        print("Most commonly used end station is: {} ".format(common_end_station))
        print('\n\n')
    except KeyError:
        print("please try again")
    # TO DO: display most frequent combination of start station and end station trip
    try:
        common_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
        print("Most frequent combination of start station and end station is: {} ".format(common_trip))
        print('\n\n')
    except KeyError:
        print("please try again")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    try:
        total_travel_time = df['Trip Duration'].sum()
    #convert to hours, minutes, seconds ...Note: this can be done faster by datetime
        travel_days = total_travel_time//(24*3600)
        travel_seconds = total_travel_time % (24 * 3600)
        travel_hours= travel_seconds//3600
        travel_seconds %= 3600
        travel_minutes= travel_seconds//60
        travel_seconds %= 60
        print("Total travel time is {} seconds or {} days, {} hours, {} minutes and {} seconds ".format(total_travel_time, travel_days, travel_hours, travel_minutes, travel_seconds))
    # TO DO: display mean travel time
        mean_travel_time= df['Trip Duration'].mean()
    #convert seconds to hh:mm:ss format by using datetime
    #could have usef this but it kept returning errors I couldn't fix
    #formatted_mean = datetime.timedelta(seconds =mean_travel_time)
        m, s = divmod(mean_travel_time, 60)
        h, m = divmod(m, 60)
        print("Mean travel time is {} seconds or {} hours, {} minutes and {} seconds".format(mean_travel_time, h, m, s))
        print('\n\n')
    except KeyError:
        print("please try again")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_type = df['User Type'].value_counts()
        print("The count of user types is {} ".format(user_type))
        print('\n\n')

    # TO DO: Display counts of gender
    #we need to handle empty values (NAN) first
        if 'Gender' in df:
            gender_type = df['Gender'].value_counts()
            print("The count of gender is {} ".format(gender_type))
            print('\n\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    #convert year to an integer to display it without the (.0)
    #use nanmin to handle empty values
        try:
            earliest_year = int(np.nanmin(df['Birth Year'].replace(0, np.nan).values))
            print("Earliest year of birth is {} ".format(earliest_year))
            print('\n\n')
        except ValueError: #raised if 'earliest_year' is empty
            pass

        birth_year = df['Birth Year'].fillna(0).astype('int64')
        recent_year= birth_year.max()
        print("Most recent year of birth is {} ".format(recent_year))
        print('\n\n')

        common_year=birth_year.mode()[0]
        print("Most common of birth is {} ".format(common_year))
        print('\n\n')
    except KeyError:
        print("please try again")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
        """
        Displays 5 rows of Data from the selected city file based on whether
        the user wants to diaplay them or not

        Args:
            (df) the data frame we're working with
        Returns:
            NONE
        """
        answer=input("Do you wish to display the first 5 rows or not, please respond with 'yes' or 'no' ").lower()
    #display max number of rows
        pd.set_option('display.max_rows', None)
        i=0
        while True:
            if answer=='yes':
                print(df.iloc[i: i+5])
                answer=input("Do you wish to display the next 5 rows or not?, please respond with 'yes' or 'no' ").lower()
                i+=5
                if answer=='yes':
                    continue
                else:
                    break

            else:
                break






def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
