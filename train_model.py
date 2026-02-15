import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/dataset.csv")

# Encode urgency
le_urg = LabelEncoder()
df['urgency_level'] = le_urg.fit_transform(df['urgency_level'])

# Feature engineering
df['blood_match'] = (df['donor_blood_group'] == df['recipient_blood_group']).astype(int)
df['organ_match'] = (df['donor_organ'] == df['recipient_organ']).astype(int)

X = df[
    ['donor_age', 'recipient_age',
     'blood_match', 'organ_match',
     'tissue_compatibility', 'urgency_level']
]

y = (df['matched_status'] == 'Matched').astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, "organ_match_model.pkl")
joblib.dump(le_urg, "urgency_encoder.pkl")

print("Model trained & saved successfully")
