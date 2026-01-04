import csv
from datetime import datetime
from collections import Counter
import json
from decimal import Decimal
from typing import List, Dict

# Function that loads the data and removes duplicates found within (1a)
def load_and_clean_the_data(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    unique_data = [dict(t) for t in {tuple(d.items()) for d in data}]
    unique_data.sort(key=lambda x: x['timestamp'])
    return unique_data

# Follow-up function that saves the cleaned data to a new CSV file
def save_cleaned_data(data: List[Dict[str, str]], file_path: str) -> str:
    cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
    with open(cleaned_file_path, mode='w', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return cleaned_file_path

# Function that finds the most common interval (1b)
def find_most_common_interval(data: List[Dict[str, str]]) -> int:
    timestamps = [datetime.fromisoformat(d['timestamp']) for d in data]
    intervals = [(timestamps[i] - timestamps[i-1]).seconds for i in range(1, len(timestamps))]
    most_common_interval = Counter(intervals).most_common(1)[0][0]
    return most_common_interval

# Function that produces segments containing homogeneous intervals in-between (1c)
def segment_data(data: List[Dict[str, str]], interval: int) -> List[List[Dict[str, str]]]:
    timestamps = [datetime.fromisoformat(d['timestamp']) for d in data]
    segments = []
    current_segment = [data[0]]
    for i in range(1, len(data)):
        if (timestamps[i] - timestamps[i-1]).seconds == interval:
            current_segment.append(data[i])
        else:
            segments.append(current_segment)
            current_segment = [data[i]]
    segments.append(current_segment)
    return segments

# Functions that analyze the data
# This part calculates the average heart rate across all segments of the data (2a)
def calculate_average_heart_rate(data: List[Dict[str, str]]) -> float:
    heart_rates = [int(d['heart_rate']) for d in data]
    average_heart_rate = sum(heart_rates) / len(heart_rates)
    return average_heart_rate

# This part calculates the average heart rate across each segment only (2b)
def calculate_average_heart_rate_per_segment(segments: List[List[Dict[str, str]]]) -> List[float]:
    segment_averages = [calculate_average_heart_rate(segment) for segment in segments]
    return segment_averages

# Helper function to convert Decimals to floats for JSON serialization
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Transform the data to FHIR format (3a)
def transform_to_fhir(data: List[Dict[str, str]]) -> Dict:
    from fhir.resources.observation import Observation
    from fhir.resources.patient import Patient
    from fhir.resources.quantity import Quantity
    from fhir.resources.codeableconcept import CodeableConcept
    from fhir.resources.coding import Coding
    from fhir.resources.meta import Meta

    patient = Patient(
        id="example-patient",
        name=[{"use": "official", "family": "Doe", "given": ["John"]}],
        gender="male",
        birthDate="1980-01-01"
    )

    observations = []
    for entry in data:
        observation = Observation(
            status="final",
            category=[CodeableConcept(coding=[Coding(system="http://terminology.hl7.org/CodeSystem/observation-category", code="vital-signs", display="Vital Signs")])],
            code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="8867-4", display="Heart rate")]),
            subject={"reference": "Patient/example-patient"},
            valueQuantity=Quantity(value=int(entry['heart_rate']), unit="beats/minute", system="http://unitsofmeasure.org", code="bpm"),
            meta=Meta(profile=["http://hl7.org/fhir/StructureDefinition/HeartRate"])
        )
        observations.append(observation.dict())  # Changed from as_json() to dict()

    fhir_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": obs} for obs in observations]
    }
    return fhir_bundle

# Main function that will run all the previous functions 
def main(): # Make sure to change the file path depending on where the .csv file is
    file_path = 'C:\\Users\\Neveen\\Desktop\\FOHI Exam\\heart_rate_readings.csv'
    cleaned_data = load_and_clean_the_data(file_path)
    cleaned_file_path = save_cleaned_data(cleaned_data, file_path)
    
    most_common_interval = find_most_common_interval(cleaned_data)
    segments = segment_data(cleaned_data, most_common_interval)
    
    average_heart_rate = calculate_average_heart_rate(cleaned_data)
    segment_averages = calculate_average_heart_rate_per_segment(segments)
    
    fhir_data = transform_to_fhir(cleaned_data)
    
    # Save the FHIR JSON to file
    output_file_path =  'C:\\Users\\Neveen\\Desktop\\FOHI Exam\\heart_rate_readings_fhir.json'
    with open(output_file_path, 'w') as f:
        json.dump(fhir_data, f, indent=2, default=decimal_default)

    # Output results for viewing 
    print(f"Most common interval (seconds): {most_common_interval}")
    print(f"Segments with homogeneous intervals (seconds): {segments}")
    print(f"Average heart rate across all segments: {average_heart_rate:.2f}")
    print(f"Average heart rate in each segment: {segment_averages}")
    print(f"FHIR data has been saved to '{output_file_path}'")
    print(f"Cleaned data has been saved to '{cleaned_file_path}'")

if __name__ == "__main__":
    main()