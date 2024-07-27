import pandas as pd
import numpy as np

# Set the parameters
num_households = 50000  # 50,000 households
chunk_size = 10000  # Generate 10,000 households at a time
wards = 50
areas_per_ward = 10
months = 12

# Function to generate a chunk of data
def generate_chunk(start_id, chunk_size, months):
    household_ids = np.arange(start_id, start_id + chunk_size)
    ward_ids = np.random.randint(1, wards + 1, chunk_size)
    area_ids = np.random.randint(1, areas_per_ward + 1, chunk_size)
    
    # Generate water usage with seasonal effect
    base_water_usage = np.random.randint(1000, 3000, (chunk_size, months))
    seasonal_effect = np.sin(np.linspace(0, 2 * np.pi, months)).reshape(1, -1)
    monthly_water_usage = base_water_usage + (seasonal_effect * 500).astype(int)
    
    leakage_detected = np.random.choice(['Yes', 'No'], chunk_size, p=[0.1, 0.9])
    disparity_in_supply = np.random.choice(['Yes', 'No'], chunk_size, p=[0.05, 0.95])
    income_level = np.random.choice(['Low', 'Medium', 'High'], chunk_size, p=[0.3, 0.5, 0.2])
    household_size = np.random.randint(1, 10, chunk_size)
    sensor_error = np.random.normal(0, 50, (chunk_size, months)).astype(int)
    
    # Adjust water usage for income level and household size
    income_adjustment = np.where(income_level == 'Low', -200, np.where(income_level == 'High', 200, 0)).reshape(-1, 1)
    monthly_water_usage += income_adjustment
    household_size_adjustment = ((household_size - 4) * 50).reshape(-1, 1)
    monthly_water_usage += household_size_adjustment
    monthly_water_usage += sensor_error  # Add sensor error

    # Ensure no negative values
    monthly_water_usage = np.maximum(monthly_water_usage, 0).flatten()
    
    # Create repeated arrays to match the number of months
    household_ids_repeated = np.repeat(household_ids, months)
    ward_ids_repeated = np.repeat(ward_ids, months)
    area_ids_repeated = np.repeat(area_ids, months)
    leakage_detected_repeated = np.repeat(leakage_detected, months)
    disparity_in_supply_repeated = np.repeat(disparity_in_supply, months)
    income_level_repeated = np.repeat(income_level, months)
    household_size_repeated = np.repeat(household_size, months)
    dates_repeated = np.tile(pd.date_range(start='2024-01-01', periods=months, freq='M'), chunk_size)

    # Create DataFrame for the chunk
    df_chunk = pd.DataFrame({
        'Household ID': household_ids_repeated,
        'Ward': ward_ids_repeated,
        'Area': area_ids_repeated,
        'Monthly Water Usage (Liters)': monthly_water_usage,
        'Leakage Detected (Yes/No)': leakage_detected_repeated,
        'Disparity in Supply (Yes/No)': disparity_in_supply_repeated,
        'Income Level': income_level_repeated,
        'Household Size': household_size_repeated,
        'Date': dates_repeated
    })

    return df_chunk

# File to save the data
output_file = 'indore_water_usage_data_difficult.csv'

# Initialize the CSV file with the header
initial_chunk = generate_chunk(1, chunk_size, months)
initial_chunk.to_csv(output_file, index=False)

# Generate and append the rest of the data in chunks
for start_id in range(chunk_size + 1, num_households + 1, chunk_size):
    df_chunk = generate_chunk(start_id, chunk_size, months)
    df_chunk.to_csv(output_file, mode='a', header=False, index=False)
    print(f"Appended data for households {start_id} to {start_id + chunk_size - 1}")

print("Dataset generation completed and saved as 'indore_water_usage_data_difficult.csv'")
