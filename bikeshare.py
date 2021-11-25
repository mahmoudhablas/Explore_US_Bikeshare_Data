import time
import pandas as pd
import numpy as np
import PySimpleGUI as sg
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    # get file path from CITY_DATA dictionary using city input, then read the file using the path
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime to be able to get month and hour from it 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # print(city,month,day)
    return df


def time_stats(df):
    """
    Calculating statistics on the most frequent times of travel.

    Args:
        (DataFrame) df: the dataframe that will be processed
    Returns:
        month: the most popular month in df
        month_count: the most popular month count in df
        day: most popular day_of_week in df
        day_count: most popular day_of_week count in df
        hour: most popular hour in df
        hour_count: most popular hour count in df
        time_diff: time which is taken during calculation
    """
    start_time = time.time()
    # df.to_csv("result.csv")
    month = df['month'].value_counts().idxmax()
    month_count =  df['month'].value_counts().iloc[0]
    day = df['day_of_week'].value_counts().idxmax()
    day_count =  df['day_of_week'].value_counts().iloc[0]
    hour= df['hour'].value_counts().idxmax()
    hour_count = df['hour'].value_counts().iloc[0]
    time_diff =  (time.time() - start_time)
    # print(df['month'].value_counts())
    return month,month_count,day,day_count,hour,hour_count,time_diff


def station_stats(df):
    """
    Calculating statistics on the most popular stations and trip.

    Args:
        (DataFrame) df: the dataframe that will be processed
    Returns:
        start_station: the most popular start station in df
        start_station_count: the most popular start station count in df
        end_station: the most popular end station in df
        end_station_count: the most popular end station count in df
        start_end_station: the most frequent combination of start station and end station trip in df
        start_end_station_count: the most frequent combination of start station and end station trip count in df
        time_diff: time which is taken during calculation
    """
    start_time = time.time()
    start_station = df['Start Station'].value_counts().idxmax()
    start_station_count = df['Start Station'].value_counts().iloc[0]
    end_station = df['End Station'].value_counts().idxmax()
    end_station_count = df['End Station'].value_counts().iloc[0]
    start_end_station = df.groupby(['Start Station','End Station']).size().idxmax()
    start_end_station_count = df.groupby(['Start Station','End Station']).size().max()
    time_diff = time.time() - start_time
    return start_station,start_station_count,end_station,end_station_count,start_end_station,start_end_station_count,time_diff

def trip_duration_stats(df):
    """
    Calculating statistics on Trip Duration.

    Args:
        (DataFrame) df: the dataframe that will be processed
    Returns:
        sum_trip_duration: total travel time
        average_trip_duration: mean travel time
        time_diff: time which is taken during calculation
    """

    start_time = time.time()
    sum_trip_duration = df['Trip Duration'].sum()
    average_trip_duration = df['Trip Duration'].mean()
    time_diff = time.time() - start_time
    return sum_trip_duration,average_trip_duration ,time_diff 

def user_stats(df):
    """
    Calculating statistics on bikeshare users.

    Args:
        (DataFrame) df: the dataframe that will be processed
    Returns:
        user_type: user type
        gender: gender of the user
        earlist_year: Earlist year of birth
        recent_year: most recent year
        common_year: most common year
        time_diff: time which is taken during calculation
    """
    start_time = time.time()
    # as there is missing columns in Washington dataset
    # to avoid this, we will send nothing 
    try:    
        user_type = df['User Type'].value_counts()
        gender = df['Gender'].value_counts()
        earlist_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].value_counts().idxmax()
        time_diff = time.time() - start_time
        return user_type,gender,earlist_year,recent_year,common_year,time_diff
    except:
        print("Data isn't available for this part")
        return "","","","","",""
    

def main():
    # init variable for layout design
    screen_width = 50
    headline_color = '#744c3c'
    sub_headline_color = '#464646'
    details_desc_color = '#4b5453'
    details_value_color = 'white'
    # define available cites to be in the drop menu
    cities = ['Chicago', 'New York', 'Washington']
    # define months to be in the drop menu
    months = ['All','January','February','March','April','May','June','July','August','September','October','November','December']
    #define days to be in the drop menu
    days = ['All','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

    #design layout for inputs
    layout = [
                [sg.Text("Would you like to see data for Chicago, New York, or Wshington? ",size=(screen_width,1)),
                sg.Combo(cities,key="selected_city",default_value="Chicago",size=(screen_width,1))],
                [sg.Text("Would you like to filter the data by month, day, both, or not at all? ",size=(screen_width,1)),
                sg.Button('Both'), sg.Button('None'), sg.Button('Month'), sg.Button('Day')],
                [sg.Text("Which month? ",visible = False, key="text_month",size=(screen_width,1)),
                sg.Combo(months,key="month",visible = False,default_value="All",size=(screen_width,1))],
                [sg.Text("Which Day? ",visible = False,key="text_day",size=(screen_width,1)),
                sg.Combo(days,key="day",visible = False,default_value="All",size=(screen_width,1))],
                [sg.Button('Show statistics'), sg.Button('Show Data'),sg.Text("",key="message")]
             ]
    window = sg.Window("Explore US Bikeshare Data",layout)

    # Event Loop
    while True:             
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # if user select both, show month drop menu and day drop menu
        if event == 'Both':
            window['text_month'].update(visible=True)
            window['month'].update(visible=True)
            window['text_day'].update(visible=True)
            window['day'].update(visible=True)   
        # if user select day, show day drop menu and disable month drop menu
        if event == 'Day':
            window['text_day'].update(visible=True)
            window['day'].update(visible=True)  
            window['text_month'].update(visible=False)
            window['month'].update(visible=False)
            # return to month default value
            window['month'].update(value = 'All')
        # if user select month, show month drop menu and disable day drop menu
        if event == 'Month':
            window['text_month'].update(visible=True)
            window['month'].update(visible=True)
            window['text_day'].update(visible=False)
            window['day'].update(visible=False) 
            # return to day default value
            window['day'].update(value = 'All')
        # if user select none, disable month drop menu and day drop menu
        if event == 'None':
            window['text_month'].update(visible=False)
            window['month'].update(visible=False)
            window['text_day'].update(visible=False)
            window['day'].update(visible=False)
             # return to month default value
            window['day'].update(value = 'All')
            window['month'].update(value = 'All')
        if event == 'Show statistics':
            print('Calcaulting Statistics.......')
            # load the df with filter
            df =  load_data(values['selected_city'].lower(),values['month'].title(),values['day'].title())
            month,month_count,day,day_count,hour,hour_count,time_diff_times = time_stats(df)
            start_station,start_station_count,end_station,end_station_count,start_end_station,start_end_station_count,time_diff_trips = station_stats(df)
            sum_trip_duration,average_trip_duration ,time_diff_duration = trip_duration_stats(df)
            user_type,gender,earlist_year,recent_year,common_year,time_diff_user = user_stats(df)
            # design layout for output Statistics
            details_layout = [
                [sg.Column([
                 [sg.Text("Statistics on Times of Travel",font='Lucida', text_color=headline_color,size=(screen_width,1))],
                 [sg.Text("Most popular month", text_color=sub_headline_color, size=(screen_width,1))],
                 [sg.Text("Month: ", text_color=details_desc_color), sg.Text("{}".format(months[month]), text_color=details_value_color)],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(month_count), text_color=details_value_color)],
                 [sg.Text("Most popular day of week", text_color=sub_headline_color,size=(screen_width,1))],
                 [sg.Text("Day: ", text_color=details_desc_color), sg.Text("{}".format(day), text_color=details_value_color)],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(day_count), text_color=details_value_color)],
                 [sg.Text("Most popular hour", text_color=sub_headline_color, size=(screen_width,1))],
                 [sg.Text("Hour: ", text_color=details_desc_color), sg.Text("{}".format(hour), text_color=details_value_color)],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(hour_count), text_color=details_value_color)],
                 [sg.Text("That took: ", text_color=details_desc_color),sg.Text("{}".format(time_diff_times), text_color=details_value_color)],

                 [sg.Text("Statistics on Stations and Trip",font='Lucida', text_color=headline_color,size=(screen_width,1))],
                 [sg.Text("Most popular start station",  text_color=sub_headline_color,size=(screen_width,1) )],
                 [sg.Text("Start Station: ", text_color=details_desc_color), sg.Text("{}".format(start_station), text_color=details_value_color)],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(start_station_count), text_color=details_value_color)],
                 [sg.Text("Most popular end station",text_color=sub_headline_color,size=(screen_width,1) )],
                 [sg.Text("End Station: ", text_color=details_desc_color), sg.Text("{}".format(end_station), text_color=details_value_color)],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(end_station_count), text_color=details_value_color)],
                 [sg.Text("Most popular Combination",text_color=sub_headline_color,size=(screen_width,1) )],
                 [sg.Text("Start Station, End Station: ", text_color=details_desc_color), sg.Text("{},{}".format(start_end_station[0], start_end_station[1]), text_color=details_value_color,size=(screen_width//2,2))],
                 [sg.Text("Count: ", text_color=details_desc_color), sg.Text("{}".format(start_end_station_count), text_color=details_value_color)],
                 [sg.Text("That took:", text_color=details_desc_color),sg.Text("{}".format(time_diff_trips),text_color=details_value_color )],

                 [sg.Text("Statistics on the total and average trip duration",font='Lucida', text_color=headline_color,size=(screen_width,1))],
                 [sg.Text("Total travel time: ", text_color=details_desc_color),sg.Text("{}".format(sum_trip_duration), text_color=details_value_color)],
                 [sg.Text("Average travel time: ", text_color=details_desc_color),sg.Text("{}".format(average_trip_duration), text_color=details_value_color)],
                 [sg.Text("That took: ", text_color=details_desc_color),sg.Text("{}".format(time_diff_duration), text_color=details_value_color)],

                 [sg.Text("Statistics on bikeshare users",font='Lucida', text_color=headline_color,size=(screen_width,1))],
                 [sg.Text("Counts of user types: ", text_color=details_desc_color),sg.Text("{}".format(user_type), text_color=details_value_color)],
                 [sg.Text("Counts of gender: ", text_color=details_desc_color),sg.Text("{}".format(gender), text_color=details_value_color)],
                 [sg.Text("Earlist year of birth: ", text_color=details_desc_color),sg.Text("{}".format(earlist_year), text_color=details_value_color)],
                 [sg.Text("Most recent year: ", text_color=details_desc_color),sg.Text("{}".format(recent_year), text_color=details_value_color)],
                 [sg.Text("Most common year: ", text_color=details_desc_color),sg.Text("{}".format(common_year), text_color=details_value_color)],
                 [sg.Text("That took: ", text_color=details_desc_color),sg.Text("{}".format(time_diff_user),text_color=details_value_color, size=(screen_width,1))]
                ] ,  scrollable=True)]
                

            ]
            details = sg.Window("Details", details_layout, modal=True)
            while True:
                event, values = details.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
        
            details.close()
        if event == 'Show Data':
            window['message'].update("Loading Data..........")
            print('Loading Data..........')
            headers = {'Id':[], 'Start Time':[], 'End Time':[],
            'Trip Duration':[],'Start Station':[], 'End Station': [], 'User Type': [], 'Gender': [],'Birth Year': []}
            df =  load_data(values['selected_city'].lower(),values['month'].title(),values['day'].title())
            headings = list(headers)
            values = df.values.tolist()
            sg.set_options(font=("Courier New", 16))
            layout = [[sg.Table(values = values, headings = headings,
                # Set column widths for empty record of table
                auto_size_columns=False,
                num_rows=20,
                col_widths=list(map(lambda x:len(x)+1, headings)))]]

            data_window = sg.Window('Data Rows',  layout)
            # window['message'].update(value="")
            while True:
                event, value = data_window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
            data_window.close()

    #close first window
    window.close()

    

if __name__ == "__main__":
	main()
