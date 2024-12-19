# Author: B.G Ranuga Gamage
# Date: 3/12/2024
# Student ID: 20231264

from graphics import *
from w2120198_abc import *
import math

# Task D: Histogram Display


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.win = GraphWin("Vehicle Frequency Histogram", 1080 + 440, 848)

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.win.setCoords(0, -3, 24, 40)
        self.win.setBackground("white")

    def bar_height_calculator(self, count):
        """
        Calculate the bar height according to the number of count
        """
        min_height = 10  # Minimum bar height
        max_height = 30
        log_min = math.log(1)  # Log of the smallest possible value
        log_max = math.log(
            50 + 1
        )  # Log of the largest possible value in your data range
        log_range = log_max - log_min if log_max != log_min else 1
        # Scale the current value
        return min_height + ((math.log(count + 1) - log_min) / log_range) * (
            max_height - min_height
        )

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Extract unique locations
        locations = list(next(iter(self.traffic_data.values())).keys())

        # Prepare data for plotting
        time_periods = list(self.traffic_data.keys())

        # Draw the histogram bars
        bar_width = 0.45
        gap_between_groups = 0.0875

        for i, time_period in enumerate(time_periods):
            x_base = i * (len(locations) * bar_width + gap_between_groups) + 0.25

            for j, location in enumerate(locations):
                # Calculate bar height
                count = self.traffic_data[time_period][location]
                bar_height = self.bar_height_calculator(count)

                # Create rectangle for the bar
                bar_bottom_left = Point(x_base + j * bar_width, 0)
                bar_top_right = Point(x_base + j * bar_width + bar_width, bar_height)
                bar = Rectangle(bar_bottom_left, bar_top_right)

                # Alternate colors for different locations
                bar.setFill("green" if j % 2 == 0 else "red")
                bar.setOutline("black")
                bar.draw(self.win)

                # Add count label on top of bar
                count_text = Text(
                    Point(x_base + j * bar_width + bar_width / 2, bar_height + 0.5),
                    str(count),
                )
                count_text.setSize(8)
                count_text.draw(self.win)

                # Add time period label at the bottom
                if j == 0:
                    time_label = Text(
                        Point(x_base + (len(locations) * bar_width) / 2, -1),
                        time_period,
                    )
                    time_label.setSize(8)
                    time_label.draw(self.win)

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Add title
        title = Text(
            Point(7.5, 37), f"Histogram of Vehicle Frequency per Hour ({self.date})"
        )
        title.setSize(12)
        title.setStyle("bold")
        title.draw(self.win)

        # Add legend
        legend_items = [
            ("Elm Avenue/Rabbit Road", "green"),
            ("Hanley Highway/Westway", "red"),
        ]
        y_position = 34
        for label, color in legend_items:
            # Draw colored rectangle for legend
            legend_rect = Rectangle(Point(2.5, y_position), Point(2.75, y_position + 1))
            legend_rect.setFill(color)
            legend_rect.setOutline(color)
            legend_rect.draw(self.win)

            # Add text label next to the rectangle
            legend_text = Text(Point(4, y_position + 0.5), label)
            legend_text.setSize(10)
            legend_text.draw(self.win)

            y_position -= 2

        # Add axis labels
        x_label = Text(Point(12, -2), "Hours (00:00 to 24:00)")
        x_label.setSize(10)
        x_label.draw(self.win)

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.win.getMouse()
        self.win.close()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        data = load_csv_file(file_path)
        features = {}
        for idx, time_of_day in enumerate(data["timeOfDay"]):
            hour = time_of_day.split(":")[0]
            if hour not in features:
                features[hour] = {
                    "Elm Avenue/Rabbit Road": 0,
                    "Hanley Highway/Westway": 0,
                }
            features[hour][data["JunctionName"][idx]] += 1
        self.current_data = features

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        yes_or_no = input(
            "Do you want to select a data file for a different date? (Y/N) "
        ).upper()  # get the user input and upper case it
        if yes_or_no not in ["Y", "N"]:  # check if the input is in the valid inputs
            print("Invalid input - please enter Y or N.")  # print out error message
            return self.handle_user_interaction()  # return the function itself
        return yes_or_no  # return the user input

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:  # loop until the user wants to stop
            day, month, year = validate_date_input()  # validate the date input
            filepath = get_csv_file_name(day, month, year)  # get the file path
            outcomes = process_csv_data(filepath)  # process the data
            tot_str = display_outcomes(outcomes)  # display the outcomes
            save_results_to_file(tot_str)  # save the outcomes to the file
            self.load_csv_file(filepath)
            ha = HistogramApp(self.current_data, f"{day}/{month}/{year}")
            ha.run()
            self.clear_previous_data()
            if (
                self.handle_user_interaction() == "N"
            ):  # check if the user wants to continue
                break  # if not break the loop


def main():
    """
    Main function to run the application.
    """
    mcp = MultiCSVProcessor()  # create an instance of MultiCSVProcessor
    mcp.process_files()  # run the main loop for handling multiple CSV files


if __name__ == "__main__":
    main()
