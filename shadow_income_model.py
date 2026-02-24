
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load Data
data = pd.read_csv("sample_gig_data.csv")

X = data.drop("creditworthy", axis=1)
y = data["creditworthy"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, predictions))

# Example Prediction
sample_customer = [[45000, 0.3, 0.7, 0.8, 0.9]]
result = model.predict(sample_customer)
print("\nSample Customer Creditworthy Prediction:", result[0])
