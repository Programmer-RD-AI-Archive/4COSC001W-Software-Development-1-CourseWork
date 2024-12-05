import os

# Author: B.G Ranuga Gamage
# Date: 3/12/2024
# Student ID: 20231264


def validate_inputs(
    general_validations: dict[object:str], requirements: dict[str:[object, str]]  # -
) -> list:
    """
    This function validates the inputs provided by the user for the given requirements.
    It takes two parameters:
    1. `general_validations`: A dictionary containing general validation functions for the inputs. Each key in the dictionary represents a validation function, and the corresponding value is a string describing the required input type.
    2. `requirements`: A dictionary containing key-value pairs, where the key is a prompt for the user input, and the value is a tuple containing a validation function and an error message.
    The function returns a list of validated user inputs.
    """
    check_general_validations = lambda text: (
        "\n".join(
            [
                list(general_validations.values())[idx]
                for idx, general_validation in enumerate(general_validations)
                if not general_validation(text)
            ]
        )
        if any(not validation(text) for validation in general_validations)
        else True
    )
    valid_user_inputs = []
    for key, value in requirements.items():
        user_input = input(key)
        general_confirms = check_general_validations(user_input)
        specific_statement = (
            value[0](float(user_input)) if general_confirms is True else None,
        )
        while not all([general_confirms, specific_statement[0]]):
            print(general_confirms) if general_confirms is not True else None
            print(value[1]) if specific_statement else None
            user_input = input(key)
            general_confirms = check_general_validations(user_input)
            specific_statement = (
                value[0](float(user_input)) if general_confirms is True else None,
            )
        valid_user_inputs.append(user_input)
    return valid_user_inputs


# Task A: Input Validation
def validate_date_input() -> tuple[int, int, int]:
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    general_validations = {lambda data: data.isnumeric(): "Integer Required"}
    requirements = {
        "Please enter the day of the survey in the format dd: ": [
            lambda date: 1 <= date <= 31,
            "Out of range - values must be in the range 1 and 31.",
        ],
        "Please enter the month of the survey in the format mm: ": [
            lambda month: 1 <= month <= 12,
            "Out of range - values must be in the range 1 to 12.",
        ],
        "Please enter the year of the survey in the format yyyy: ": [
            lambda year: 2000 <= year <= 2024,
            "Out of range - values must range from 2000 and 2024.",
        ],
    }
    day, month, year = validate_inputs(general_validations, requirements)
    file_path = get_csv_file_name(day, month, year)
    if not valid_path(file_path):
        print(f"Invalid path: {file_path}")
        return validate_date_input()
    return day, month, year


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    general_validations = {}
    requirements = {
        "Do you want to load another dataset? (Y/N): ": [
            lambda data: data.upper() in ["Y", "N"],
            "Invalid input - please enter Y or N.",
        ]
    }
    yes_or_no = validate_inputs(general_validations, requirements)


# Task B: Processed Outcomes
def get_csv_file_name(day, month, year) -> str:
    return f"traffic_data{day}{month}{year}.csv"


def valid_path(file_path: str) -> boool:
    return file_path in os.listdir("./")


def get_metric(requirement: object, data: dict) -> object:
    return requirement(data)


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
    - Two-wheeled vehicles, and other requested metrics
    """
    data = load_csv_file(file_path)
    requirements = {
        "The total number of vehicles passing through all junctions for the selected date": lambda data: len(
            data["VehicleType"]
        ),
        "The total number of trucks passing through all junctions for the selected date": lambda data: len(
            access_specific_data(data, "VehicleType", ["Truck"])
        ),
        "The total number of electric vehicles passing through all junctions for the selected date": lambda data: len(
            access_specific_data(data, "elctricHybrid", [True])
        ),
        "The number of “two wheeled” vehicles through all junctions for the date (bikes, motorbike, scooters)": lambda data: len(
            access_specific_data(
                data, "VehicleType", ["Bicycle", "Motorcycle", "Scooter"]
            )
        ),
        "The total number of busses leaving Elm Avenue/Rabbit Road junction heading north": lambda data: len(
            [
                vehicle
                for idx, vehicle in enumerate(data["VehicleType"])
                if vehicle == "Bus"
                and data["travel_Direction_out"][idx] == "North"
                and data["JunctionName"][idx] == "Elm Avenue/Rabbit Road"
            ]
        ),
        "The total number of vehicles passing through both junctions without turning left or right": lambda data: len(
            [
                1
                for dir_in, dir_out in zip(
                    data["travel_Direction_in"], data["travel_Direction_out"]
                )
                if dir_in == dir_out
            ]
        ),
        "The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer)": lambda data: round(
            len(access_specific_data(data, "VehicleType", ["Truck"]))
            / len(data["VehicleType"])
            * 100
        ),
        "The average number Bicycles per hour for the selected date (rounded to an integer)": lambda data: round(
            len(access_specific_data(data, "VehicleType", ["Bicycle"])) / 24
        ),
        "The total number of vehicles recorded as over the speed limit for the selected date": lambda data: len(
            [
                vehicle
                for idx, vehicle in enumerate(data["VehicleType"])
                if vehicle == "Car"
                and int(data["VehicleSpeed"][idx])
                > int(data["JunctionSpeedLimit"][idx])
            ]
        ),
        "The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date": lambda data: len(
            access_specific_data(data, "JunctionName", ["Elm Avenue/Rabbit Road"])
        ),
        "The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date": lambda data: len(
            access_specific_data(data, "JunctionName", ["Hanley Highway/Westway"])
        ),
        "The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)": lambda data: round(
            len(access_specific_data(data, "JunctionName", ["Elm Avenue/Rabbit Road"]))
            / len(access_specific_data(data, "VehicleType", ["Scooter"]))
        ),
        "The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway": lambda data: max(
            get_hour_count(
                data,
                access_specific_data(data, "JunctionName", ["Hanley Highway/Westway"]),
            ).values()
        ),
        "The total number of hours of rain on the selected date": lambda data: len(
            get_hour_count(
                data,
                access_specific_data(
                    data, "Weather_Conditions", ["Heavy Rain", "Light Rain"]
                ),
            ).values()
        ),
    }
    outcomes = {}
    for requirement in requirements.keys():
        outcomes[requirement] = get_metric(requirements[requirement], data)
    hour_count = get_hour_count(
        data, access_specific_data(data, "JunctionName", ["Hanley Highway/Westway"])
    )
    hr_counts = list(hour_count.values())
    max_hr = max(hr_counts)
    peak_hour = (
        list(hour_count.keys())[hr_counts.index(max_hr)]
        if hr_counts.count(max_hr) == 1
        else [hour for hour, count in hour_count.items() if count == max_hr]
    )
    txt = f"Between {peak_hour}:00 " + (
        f"and {peak_hour[-1]}" if type(peak_hour) == list else f"and {peak_hour+1}:00"
    )
    outcomes[
        "The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway in the format Between 18:00 and 19:00. – (note this may be multiple hours)."
    ] = txt
    return outcomes


def display_outcomes(outcomes: dict) -> str:
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    tot_str = ""
    for outcome in outcomes.keys():
        tot_str += f"{outcome}: {outcomes[outcome]}\n"
    print(tot_str)
    return tot_str


# Task C: Save Results to Text File
def save_results_to_file(outcomes: str, file_name: str = "results.txt") -> None:
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open(file_name, "a") as file:
        file.write(
            f"""\n{"*"*25}\n\n"""
            if open(file_name).read().strip() != ""
            else "" + outcomes
        )
