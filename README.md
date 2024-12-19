# 4COSC001W-Software-Development-1-CourseWork: Traffic Data Analysis System

## Overview

A Python-based traffic data analysis system that processes and visualizes vehicle traffic data from CSV files. The system includes features for data validation, analysis, visualization, and result storage.

## Features

- Date input validation for DD/MM/YYYY format
- CSV file processing and data analysis
- Vehicle traffic statistics calculation including:
  - Total vehicle counts
  - Vehicle type distributions
  - Speed limit violations
  - Peak traffic hours
  - Weather conditions analysis
- Interactive histogram visualization using graphics.py
- Results storage in text files
- Multi-file processing capability

## Requirements

- Python 3.x
- graphics.py library (included)

## Project Structure

```
.
├── w2120198_de.py          # Main script for visualization and multi-file processing
├── graphics.py             # Graphics library for visualization
├── w2120198_a_b_c.zip     # Archive containing Tasks A, B, and C
├── w2120198_d_e.zip       # Archive containing Tasks D and E
├── traffic_data*.csv      # Sample traffic data files:
│   ├── traffic_data15062024.csv
│   ├── traffic_data16062024.csv
│   └── traffic_data21062024.csv
├── results - ABC.txt      # Results output for Tasks A, B, and C
├── results - DE.txt       # Results output for Tasks D and E
├── Design: FlowChart - DE.png  # Design flowchart for Tasks D and E
├── FlowChart - ABC.png    # Flowchart for Tasks A, B, and C
├── Test Cases - ABC.pdf   # Test cases for Tasks A, B, and C
├── Test Cases - DE.pdf    # Test cases for Tasks D and E
├── LICENSE                # Project license file
├── .gitignore            # Git ignore configuration
└── README.md             # This documentation file
```

## Key Functions

### Data Validation

- `validate_date_input()`: Validates user input for date selection
- `validate_continue_input()`: Handles user input for continuing analysis

### Data Processing

- `process_csv_data()`: Main function for analyzing traffic data
- `load_csv_file()`: Reads and parses CSV files
- `get_csv_file_name()`: Generates file names based on dates

### Visualization

- `HistogramApp`: Class for creating and displaying traffic data histograms
- Features logarithmic scaling for better visualization of varying traffic volumes

### Multi-file Processing

- `MultiCSVProcessor`: Handles processing of multiple CSV files
- Maintains data integrity between file processing

## Usage

1. Run the main script:
   ```python
   python w2120198_de.py
   ```
2. Enter the date when prompted (DD MM YYYY)
3. View the analysis results and histogram
4. Choose to process another file or exit

## Documentation

- Test cases and expected results are provided in the PDF files
- Flowcharts illustrate the program design and logic flow
- Results are stored in separate text files for different task groups
