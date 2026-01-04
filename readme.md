# Heart Rate Data Processing and Transformation to FHIR 

## Overview

This project provides an end-to-end Python application for processing heart rate time-series data stored in CSV format. It performs data cleaning, interval analysis, segmentation, statistical aggregation, and transformation of the data into **FHIR (Fast Healthcare Interoperability Resources)**–compliant JSON.

---

## Features

- **CSV Data Cleaning**
  - Removes duplicate rows
  - Sorts data chronologically by timestamp
  - Saves a cleaned version of the dataset

- **Time-Series Interval Analysis**
  - Detects the most common time interval between readings
  - Segments data into continuous periods with consistent intervals

- **Heart Rate Statistics**
  - Computes overall average heart rate
  - Computes average heart rate per segment

- **FHIR Transformation**
  - Converts heart rate readings into FHIR `Observation` resources
  - Uses standard LOINC and HL7 codes
  - Outputs a FHIR `Bundle` in JSON format

---

## Project Structure

```text
.
├── heart_rate_processing.py
├── heart_rate_readings.csv              # Input file
├── heart_rate_readings_cleaned.csv      # Generated output
├── heart_rate_readings_fhir.json        # Generated output
└── readme.md
```

## Input Data Format

The input CSV file must contain at least the following columns:

| Column Name   | Description                                   |
|--------------|-----------------------------------------------|
| `timestamp`  | ISO 8601 timestamp (e.g. `2024-01-01T10:00:00`) |
| `heart_rate` | Heart rate value in beats per minute (bpm)    |

### Example

```csv
timestamp,heart_rate
2024-01-01T10:00:00,72
2024-01-01T10:00:05,73
2024-01-01T10:00:10,71
