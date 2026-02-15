import pandas as pd
import random

data = []

for _ in range(1500):
    donor_age = random.randint(18, 65)
    patient_age = random.randint(1, 75)

    blood_match = random.choice([0, 1])
    organ_match = random.choice([0, 1])
    city_match = random.choice([0, 1])

    health_score = round(random.uniform(0.6, 1.0), 2)

    # Matching logic (label)
    if organ_match == 1 and blood_match == 1 and health_score > 0.75:
        match = 1
    else:
        match = 0

    data.append([
        donor_age,
        patient_age,
        blood_match,
        organ_match,
        city_match,
        health_score,
        match
    ])

df = pd.DataFrame(data, columns=[
    "donor_age",
    "patient_age",
    "blood_match",
    "organ_match",
    "city_match",
    "health_score",
    "match"
])

df.to_csv("organ_match_dataset.csv", index=False)
print("Dataset created successfully")
