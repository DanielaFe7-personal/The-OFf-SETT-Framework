from full_packages import *

"Function that creates a list of complete seasonal dates from e.g., 1985-2023; This will support to identify missing data in the data frames"
def obtain_complete_dates(init_date, end_date, is_Seasonal=False, season=None):
    complete_true_dates = list()
    if is_Seasonal == False:
        for i in range(init_date, end_date):  # 2023 is not included
            true_time_a = (datetime.strptime(str(i) + "-01-15", "%Y-%m-%d")).date()
            true_time_b = (datetime.strptime(str(i) + "-04-15", "%Y-%m-%d")).date()
            true_time_c = (datetime.strptime(str(i) + "-07-15", "%Y-%m-%d")).date()
            true_time_d = (datetime.strptime(str(i) + "-10-15", "%Y-%m-%d")).date()
            complete_true_dates.append(true_time_a)
            complete_true_dates.append(true_time_b)
            complete_true_dates.append(true_time_c)
            complete_true_dates.append(true_time_d)
    else:
        if season == "winter":
            month = "-01-15"
        elif season == "spring":
            month = "-04-15"
        elif season == "summer":
            month = "-07-15"
        elif season == "autumn":
            month = "-10-15"

        for i in range(init_date, end_date):  # 2023 is not included
            true_time = (datetime.strptime(str(i) + month, "%Y-%m-%d")).date()
            complete_true_dates.append(true_time)
    return complete_true_dates

def nearest(items, pivot):
    ##print("Beast cp: ",pivot, "closest date in beast fractional data: ",min(items, key=lambda x: abs(x - pivot)))
    return min(items, key=lambda x: abs(x - pivot))

"Very important function: It takes the beast output (o) and reformat the dates and the breakpoints accordingly to our data. e.g., from Fractional dates to Datatime dates"
def dates_cal(o,init_date, end_date):
    "Calculates full list of dates, it works for both All-seasons and season data"
    complete_true_dates = obtain_complete_dates(init_date, end_date, is_Seasonal=False, season=None)
    'Beast output time from Fractional format to date format and string/datetime'

    list_dates_format_datatime = list() # Datatime format
    list_dates_official = list() # Nearest to our dates
    for frac_time_beast in (o.time):
        date = fractional_date_to_date(frac_time_beast)
        list_dates_format_datatime.append(date)  # Datatime format
    list_dates_format_datatime = sorted(list_dates_format_datatime)

    "After parsing from Fractional to date/string format, BEAST dates are not coherent with original data, e.g., 1985-01-16 does not exist in our Data dates"
    "As with Breakpoints, we will choose the nearest date from original and complete dates list"
    for beast_date in list_dates_format_datatime:
        close_date = nearest(complete_true_dates, beast_date)  # Look date point, in datatime formatm in BEAST output in date format
        list_dates_official.append(str(close_date))  # String format

    'Trend breakpoints (or change ppints (cp)) time list from Fractional to date format and string/datetime'
    list_dates_cps_datatime = list() # Datatime format
    list_dates_cps_format_str_official = list() # Nearest to our dates

    for frac_cp_beast in (o.trend.cp): # o.trend.cp is part of BEAST output and returns the possible breakpoints found in the time series
        if np.isnan(frac_cp_beast):
            # print("nan CP fra: ",frac_cp_beast)
            continue
        date = fractional_date_to_date(frac_cp_beast)
        # print("Beast CP frac date: ",frac_cp_beast, " to date fromat: ",str(date))
        list_dates_cps_datatime.append(date)  # Datatime format
    list_dates_cps_datatime = sorted(list_dates_cps_datatime)
    ###print("Sorted ...",list_dates_cps_datatime)

    'Beast breakpoints not always belong to the original data, returning the closest datapoint available'
    for cp in list_dates_cps_datatime:
        close_date = nearest(complete_true_dates, cp)  # Look cp in date format in BEAST output in date format
        list_dates_cps_format_str_official.append(str(close_date))  # String format
    # print(list_dates_cps_format_str)
    # return list_dates, list_dates, list_dates_format, list_dates_cps_format, list_dates_cps_format, list_dates_cps_format_str
    return list_dates_official, list_dates_format_datatime, list_dates_cps_format_str_official, list_dates_cps_datatime


def fractional_date_to_date(fractional_year):
    # Extract the year
    year = math.floor(fractional_year)  # math.floor emulates the -0.5 in BEAST

    # Calculate the number of days in the year (365 for non-leap years)
    days_in_year = 365 if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0) else 366

    # Calculate the day of the year
    day_of_year = (fractional_year - year) * days_in_year
    day_of_year = round(day_of_year)

    # Construct the date
    # print("    ",day_of_year, " is day of the year: ",timedelta(days=day_of_year)) #timedelta already rounds the year, inside BEAST they substract (0.5); here is no necessary
    date = datetime(year, 1, 1) + timedelta(
        days=day_of_year - 1)  # -1 because the only way to sum year plus the th day is init in 1,
    return date.date()  # Remove info about hour, etc,


def date_to_fractional_date(date_str):
    # Convert the input date string to a datetime object
    date = datetime.strptime(date_str, '%Y-%m-%d')

    # Get the year from the date
    year = date.year

    # Calculate the total number of days in the year (365 for non-leap years)
    days_in_year = 365 if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0) else 366

    # Get the ordinal day of the year for the date
    ordinal_day = date.timetuple().tm_yday
    # print("    ordinal_day: ",ordinal_day)

    # Calculate the fractional year
    fractional_year = year + ordinal_day / days_in_year

    # Round the fractional year to 4 digits
    # fractional_year = round(fractional_year, 4)

    return fractional_year


