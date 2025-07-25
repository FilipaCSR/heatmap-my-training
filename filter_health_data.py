import pandas as pd
import xml.etree.ElementTree as ET

def filter_apple_health_xml(input_xml_path, output_csv_path, types_to_keep):
    """
    Reads a large Apple Health export.xml file and filters only specific data types
    into a smaller CSV for use in lightweight apps.

    Args:
        input_xml_path (str): Path to original export.xml file.
        output_csv_path (str): Path where the filtered CSV will be saved.
        types_to_keep (list of str): Apple Health data types to extract.
    """
    print(f"Reading XML from: {input_xml_path}")
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    filtered_records = []
    for record in root.findall("Record"):
        rec = record.attrib
        if rec.get("type") in types_to_keep:
            filtered_records.append(rec)

    print(f"Found {len(filtered_records)} matching records.")

    df = pd.DataFrame(filtered_records)

    if df.empty:
        print("No records matched the given types.")
        return

    # Parse dates and convert values
    df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
    df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')
    df['creationDate'] = pd.to_datetime(df['creationDate'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    print(f"Saving filtered data to: {output_csv_path}")
    df.to_csv(output_csv_path, index=False)
    print("✅ Done.")


# --- Example usage ---
# Just set your own file paths and run this locally
input_file = "export.xml"
output_file = "filtered_health_data.csv"

types_we_want = [
    'HKQuantityTypeIdentifierAppleExerciseTime',
    'HKQuantityTypeIdentifierStepCount',
    'HKQuantityTypeIdentifierVO2Max',
    'HKCategoryTypeIdentifierSleepAnalysis'
]

filter_apple_health_xml(input_file, output_file, types_we_want)
