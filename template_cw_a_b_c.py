import os

# Author: B.G Ranuga Gamage
# Date: 3/12/2024
# Student ID: 20231264


def date_verification(
    msg, range_check_start, range_check_end, error_message, dtype=int
) -> type:
    # getting the input with the parameter `msg`
    value = input(msg)
    if (
        not value.isnumeric() or not range_check_start <= int(value) <= range_check_end
    ):  # checking the requirements
        print(error_message)  # print the error message
        return date_verification(
            msg, range_check_start, range_check_end, error_message
        )  # calling the same function again
    return dtype(value)  # returning value with the data type that is expected


# Task A: Input Validation
def validate_date_input() -> tuple[int, int, int]:
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    day = date_verification(
        "Please enter the day of the survey in the format dd: ",
        1,
        31,
        "Out of range - values must be in the range 1 and 31.",
    )  # getting the day verified
    month = date_verification(
        "Please enter the month of the survey in the format mm: ",
        1,
        12,
        "Out of range - values must be in the range 1 to 12.",
    )  # getting the day verified
    year = date_verification(
        "Please enter the year of the survey in the format yyyy: ",
        2000,
        2024,
        "Out of range - values must range from 2000 and 2024.",
    )  # getting the day verified
    file_path = get_csv_file_name(
        day, month, year
    )  # getting the file path using the day, month, and year
    if not valid_path(file_path):  # checking if the path is valid
        print(
            f"Invalid path: {file_path}"
        )  # if it is not then the error message will be shown
        return validate_date_input()  # and the function will be called again
    return day, month, year  # returning the day, month, and year


def validate_continue_input() -> str:
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    yes_or_no = input(
        "Do you want to load another dataset? (Y/N): "
    ).upper()  # get the user input and upper case it
    if yes_or_no not in ["Y", "N"]:  # check if the input is in the valid inputs
        print("Invalid input - please enter Y or N.")  # print out error message
        return validate_continue_input()  # return the function itself
    return yes_or_no  # return the user input


# Task B: Processed Outcomes
def get_csv_file_name(day, month, year) -> str:
    return f"traffic_data{day:02d}{month:02d}{year}.csv"  # return the file name string


def valid_path(file_path: str) -> bool:
    return file_path in os.listdir("./")  # checking if the file exists in the path


def load_csv_file(file_path: str) -> dict:
    with open(file_path, "r") as file:  # open the file on read mode
        data = {
            key: [] for key in file.readline().strip().split(",")
        }  # add the keys to the dictionary
        for line in file.readlines():  # read line per line
            for idx, value in enumerate(
                line.strip().split(",")
            ):  # split the line and iterate
                data[list(data.keys())[idx]].append(
                    value
                )  # add the value to the corresponding key
    return data  # return the finalized dictionary


def access_specific_data(data: dict, column: str, equal_value):
    return [
        idx for idx, iter_value in enumerate(data[column]) if iter_value in equal_value
    ]  # return the finalized list of indexes for the given column


def get_hour_count(data: dict, idxs: list) -> dict:
    """
    Calculates the count of vehicles for each hour based on the provided indexes.
    Parameters:

    data (dict): A dictionary containing traffic data with keys as column names and values as lists of data.
    idxs (list): A list of indexes representing the rows of data to consider for the calculation.

    Returns:
    dict: A dictionary where keys are hours (0-23) and values are the count of vehicles for each hour.
    """
    hour_count = {}  # initialize the dictionary
    for idx in idxs:  # iterating over the index
        hour = int(data["timeOfDay"][idx][:2])  # getting the hour from the time
        hour_count[hour] = hour_count.get(hour, 0) + 1  # increment the count
    return hour_count  # return the dictionary


def process_csv_data(file_path: str) -> dict:
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics.
    """
    data = load_csv_file(file_path)  # load the data from the file
    outcomes = {}  # initialize the dictionary for the outcomes

    def count_vehicles(vehicle_types=None):
        """Counts vehicles of specific types."""
        if vehicle_types is None:  # no vehicle types specified
            return len(data["VehicleType"])  # count the vehicles and return the count
        return len(
            access_specific_data(data, "VehicleType", vehicle_types)
        )  # count the vehicles and return the count

    def count_buses_north_elmrabbit():
        """Counts buses heading north at Elm Avenue/Rabbit Road."""
        count = 0  # initialize the count
        for idx in range(
            len(data["VehicleType"])
        ):  # iterate through the no of vehicle types
            if (
                data["VehicleType"][idx] == "Bus"
                and data["travel_Direction_out"][idx] == "North"
                and data["JunctionName"][idx] == "Elm Avenue/Rabbit Road"
            ):  # check if the vehicle type is busy and the travel direction is north and the junction name is Elm Avenue/Rabbit Road
                count += 1  # increment the count
        return count  # return the count

    def count_same_direction_vehicles():
        """Counts vehicles traveling without turning."""
        count = 0  # initialize the count
        for dir_in, dir_out in zip(
            data["travel_Direction_in"], data["travel_Direction_out"]
        ):  # iterate over the travel directions in and out
            if dir_in == dir_out:  # checking if the in and out directions are the same
                count += 1  # increment the count
        return count  # return the count

    def count_vehicles_over_speed_limit():
        """Counts vehicles recorded as over the speed limit."""
        count = 0  # initialize the count
        for idx in range(
            len(data["VehicleType"])
        ):  # iterate over the idx's of the data
            if data["VehicleType"][idx] == "Car" and int(
                data["VehicleSpeed"][idx]
            ) > int(
                data["JunctionSpeedLimit"][idx]
            ):  # checking if the cars speed limit is higher than the speed limit allowed in the junction
                count += 1  # iterate the count
        return count  # return the count

    def calculate_percentage(numerator, denominator, dtype=round):
        """Calculates the percentage, rounded to an integer."""
        return dtype(
            numerator / denominator * 100
        )  # return the rounded up or down value

    def find_peak_traffic_hour(hour_count: dict):
        """Finds the peak traffic hour(s)."""
        max_count = max(
            hour_count.values()
        )  # get the maximum count of the values in the hour_count dict
        peak_hours = [
            hour for hour, count in hour_count.items() if count == max_count
        ]  # finding the peak hours
        if len(peak_hours) == 1:  # if the length is 1
            return f"Between {peak_hours[0]}:00 and {peak_hours[0] + 1}:00"
        return f"Between {peak_hours[0]}:00 and {peak_hours[-1] + 1}:00"

    # Total vehicle counts
    total_vehicles = count_vehicles()  # get the total number of vehicle counts
    outcomes[
        "The total number of vehicles passing through all junctions for the selected date"
    ] = total_vehicles
    outcomes[
        "The total number of trucks passing through all junctions for the selected date"
    ] = count_vehicles(["Truck"])
    outcomes[
        "The total number of electric vehicles passing through all junctions for the selected date"
    ] = len(access_specific_data(data, "elctricHybrid", ["True"]))
    outcomes[
        "The number of “two wheeled” vehicles through all junctions for the date (bikes, motorbike, scooters)"
    ] = count_vehicles(["Bicycle", "Motorcycle", "Scooter"])

    # Specific counts and percentages
    outcomes[
        "The total number of busses leaving Elm Avenue/Rabbit Road junction heading north"
    ] = count_buses_north_elmrabbit()
    outcomes[
        "The total number of vehicles passing through both junctions without turning left or right"
    ] = count_same_direction_vehicles()
    outcomes[
        "The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer)"
    ] = calculate_percentage(count_vehicles(["Truck"]), total_vehicles)
    outcomes[
        "The average number of Bicycles per hour for the selected date (rounded to an integer)"
    ] = round(count_vehicles(["Bicycle"]) / 24)
    outcomes[
        "The total number of vehicles recorded as over the speed limit for the selected date"
    ] = count_vehicles_over_speed_limit()

    # Elm Avenue and Hanley Highway specific counts
    elm_avenue_vehicles = len(
        access_specific_data(data, "JunctionName", ["Elm Avenue/Rabbit Road"])
    )
    outcomes[
        "The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date"
    ] = elm_avenue_vehicles
    hanley_vehicles = access_specific_data(
        data, "JunctionName", ["Hanley Highway/Westway"]
    )
    outcomes[
        "The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date"
    ] = len(hanley_vehicles)
    scooter_count = len(
        [
            vehicle_type
            for vehicle_type, junction_name in zip(
                data["VehicleType"], data["JunctionName"]
            )
            if junction_name == "Elm Avenue/Rabbit Road" and vehicle_type == "Scooter"
        ]
    )

    outcomes[
        "The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)"
    ] = calculate_percentage(scooter_count, elm_avenue_vehicles, int)
    outcomes[
        "The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway"
    ] = max(
        get_hour_count(
            data,
            hanley_vehicles,
        ).values()
    )
    outcomes["The total number of hours of rain on the selected date"] = len(
        get_hour_count(
            data,
            access_specific_data(
                data, "Weather_Conditions", ["Heavy Rain", "Light Rain"]
            ),
        ).values()
    )
    # Peak traffic hour calculation
    hour_count = get_hour_count(data, range(len(data["VehicleType"])))
    peak_hour = find_peak_traffic_hour(hour_count)
    outcomes["The peak hour for traffic during the selected date"] = peak_hour

    return outcomes


def display_outcomes(outcomes: dict) -> str:
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    tot_str = []  # initialize the list
    for outcome in outcomes.keys():  # iterate over the keys of the outcomes
        tot_str.append(
            f"{outcome}: {outcomes[outcome]}"
        )  # append the outcome to the list
    print("\n".join(tot_str))  # print the list
    return tot_str  # return the list


# Task C: Save Results to Text File
def save_results_to_file(outcomes: list, file_name: str = "results.txt") -> None:
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open(file_name, "a") as file:  # open the file in append mode
        file.write(
            f"""\n{"*"*25}\n\n"""
            if open(file_name).read().strip() != ""
            else ""  # write the line if the file is not empty
        )
        file.write("\n".join(outcomes))  # write the outcomes to the file


def main():
    while True:  # loop until the user wants to stop
        day, month, year = validate_date_input()  # validate the date input
        filepath = get_csv_file_name(day, month, year)  # get the file path
        outcomes = process_csv_data(filepath)  # process the data
        tot_str = display_outcomes(outcomes)  # display the outcomes
        save_results_to_file(tot_str)  # save the outcomes to the file
        if validate_continue_input() == "N":  # check if the user wants to continue
            break  # if not break the loop


if __name__ == "__main__":
    main()  # run the main function
