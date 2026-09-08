import numpy as np    # Generates random numbers.
import pandas as pd   # Creates and saves the dataset as a CSV file.

np.random.seed(42)    # A random seed ensures that every time you run the program, you get the same dataset.
num_samples = 1000    # dataset will contain 1000 disaster tasks.

severity_score = np.random.randint(1, 11, num_samples)    # This generates random integers between 1 and 10.
population_affected = np.random.randint(50, 10001, num_samples) # This generates values between 50 and 10,000.
hours_since_reported = np.random.randint(0, 73, num_samples) # This generates values from 0 to 72 hours.
noise = np.random.normal(0, 4, num_samples)

# Calculate the Urgency Score
urgency_score = (
    severity_score * 8
    + population_affected * 0.005
    + hours_since_reported * 0.6
    + noise
)

# Keep  Urgency Scores Between 0 and 100
urgency_score = np.clip(urgency_score, 0, 100)

# Create the Dataset
df = pd.DataFrame({
    "severity_score": severity_score,
    "population_affected": population_affected,
    "hours_since_reported": hours_since_reported,
    "urgency_score": urgency_score
})

# Save the dataset
df.to_csv("data/synthetic_tasks.csv", index=False)

print("Dataset generated successfully!")
print(df.head())