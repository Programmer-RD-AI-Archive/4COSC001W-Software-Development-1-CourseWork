import os

# Author: B.G Ranuga Gamage
# Date: 3/12/2024
# Student ID: 20231264


def date_verification(
    msg, range_check_start, range_check_end, error_message, dtype=int
) -> type:
    date = input(msg)
    if not date.isnumeric() or not range_check_start <= int(date) <= range_check_end:
        print(error_message)
        return date_verification(msg, range_check_start, range_check_end, error_message)
    return dtype(date)


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
    )
    month = date_verification(
        "Please enter the month of the survey in the format mm: ",
        1,
        12,
        "Out of range - values must be in the range 1 to 12.",
    )
    year = date_verification(
        "Please enter the year of the survey in the format yyyy: ",
        2000,
        2024,
        "Out of range - values must range from 2000 and 2024.",
    )
    file_path = get_csv_file_name(day, month, year)
    if not valid_path(file_path):
        print(f"Invalid path: {file_path}")
        return validate_date_input()
    return day, month, year


def validate_continue_input() -> str:
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    yes_or_no = input("Do you want to load another dataset? (Y/N): ").upper()
    if yes_or_no not in ["Y", "N"]:
        print("Invalid input - please enter Y or N.")
        return validate_continue_input()
    return yes_or_no


# Task B: Processed Outcomes
def get_csv_file_name(day, month, year) -> str:
    return f"traffic_data{day:02d}{month:02d}{year}.csv"


def valid_path(file_path: str) -> bool:
    return file_path in os.listdir("./")


def load_csv_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = {key: [] for key in file.readline().strip().split(",")}
        for line in file.readlines():
            for idx, value in enumerate(line.strip().split(",")):
                data[list(data.keys())[idx]].append(value)
    return data


def access_specific_data(data: dict, column: str, equal_value: str):
    return [
        idx for idx, iter_value in enumerate(data[column]) if iter_value in equal_value
    ]


def get_metric(requirement: object, data: dict) -> object:
    return requirement(data)


def get_hour_count(data: dict, idxs: list) -> dict:
    """
    Calculates the count of vehicles for each hour based on the provided indexes.
    Parameters:

    data (dict): A dictionary containing traffic data with keys as column names and values as lists of data.
    idxs (list): A list of indexes representing the rows of data to consider for the calculation.

    Returns:
    dict: A dictionary where keys are hours (0-23) and values are the count of vehicles for each hour.
    """
    hour_count = {}
    for idx in idxs:
        hour = int(data["timeOfDay"][idx][:2])
        hour_count[hour] = hour_count.get(hour, 0) + 1
    return hour_count


def process_csv_data(file_path: str) -> dict:
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics.
    """
    data = load_csv_file(file_path)
    outcomes = {}

    def count_vehicles(vehicle_types=None):
        """Counts vehicles of specific types."""
        if vehicle_types is None:
            return len(data["VehicleType"])
        return len(access_specific_data(data, "VehicleType", vehicle_types))

    def count_buses_north_elmrabbit():
        """Counts buses heading north at Elm Avenue/Rabbit Road."""
        count = 0
        for idx in range(len(data["VehicleType"])):
            if (
                data["VehicleType"][idx] == "Bus"
                and data["travel_Direction_out"][idx] == "North"
                and data["JunctionName"][idx] == "Elm Avenue/Rabbit Road"
            ):
                count += 1
        return count

    def count_same_direction_vehicles():
        """Counts vehicles traveling without turning."""
        count = 0
        for dir_in, dir_out in zip(
            data["travel_Direction_in"], data["travel_Direction_out"]
        ):
            if dir_in == dir_out:
                count += 1
        return count

    def count_vehicles_over_speed_limit():
        """Counts vehicles recorded as over the speed limit."""
        count = 0
        for idx in range(len(data["VehicleType"])):
            if data["VehicleType"][idx] == "Car" and int(
                data["VehicleSpeed"][idx]
            ) > int(data["JunctionSpeedLimit"][idx]):
                count += 1
        return count

    def calculate_percentage(numerator, denominator):
        """Calculates the percentage, rounded to an integer."""
        return round(numerator / denominator * 100)

    def find_peak_traffic_hour(hour_count):
        """Finds the peak traffic hour(s)."""
        max_count = max(hour_count.values())
        peak_hours = [hour for hour, count in hour_count.items() if count == max_count]
        if len(peak_hours) == 1:
            return f"Between {peak_hours[0]}:00 and {peak_hours[0] + 1}:00"
        return f"Between {peak_hours[0]}:00 and {peak_hours[-1] + 1}:00"

    # Total vehicle counts
    total_vehicles = count_vehicles()
    outcomes[
        "The total number of vehicles passing through all junctions for the selected date"
    ] = total_vehicles
    outcomes[
        "The total number of trucks passing through all junctions for the selected date"
    ] = count_vehicles(["Truck"])
    outcomes[
        "The total number of electric vehicles passing through all junctions for the selected date"
    ] = count_vehicles(["True"])
    outcomes[
        "The number of 'two wheeled' vehicles through all junctions for the date (bikes, motorbike, scooters)"
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
    outcomes[
        "The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)"
    ] = calculate_percentage(count_vehicles(["Scooter"]), elm_avenue_vehicles)
    print(
        round(
            len(access_specific_data(data, "JunctionName", ["Elm Avenue/Rabbit Road"]))
            / len(access_specific_data(data, "VehicleType", ["Scooter"]))
        )
    )
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
    tot_str = []
    for outcome in outcomes.keys():
        tot_str.append(f"{outcome}: {outcomes[outcome]}")
    print("\n".join(tot_str))
    return tot_str


# Task C: Save Results to Text File
def save_results_to_file(outcomes: list, file_name: str = "results.txt") -> None:
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open(file_name, "a") as file:
        file.write(
            f"""\n{"*"*25}\n\n"""
            if open(file_name).read().strip() != ""
            else "" + outcomes
        )
        file.write("\n".join(outcomes))


def main():
    while True:
        day, month, year = validate_date_input()
        filepath = get_csv_file_name(day, month, year)
        outcomes = process_csv_data(filepath)
        tot_str = display_outcomes(outcomes)
        save_results_to_file(tot_str)
        if validate_continue_input() == "N":
            break


if __name__ == "__main__":
    main()
