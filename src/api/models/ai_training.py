import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# ✅ File Paths
data_file = r"F:\MelloNex-c 2.0\data\processed\Wpl_Processed_Stats_Advanced.csv"
model_file = r"F:\MelloNex-c 2.0\src\api\models\wpl_winner_prediction.pkl"

# ✅ Load Data
df = pd.read_csv(data_file)

# ✅ Standardize Column Names
df.rename(columns={"total matches": "matches"}, inplace=True)

# ✅ Ensure Required Columns Exist
required_columns = ["team1", "team2", "toss_winner", "toss_decision", "matches", "toss_wins", "winner"]
missing_columns = set(required_columns) - set(df.columns)
if missing_columns:
    raise KeyError(f"❌ Missing columns in dataset: {missing_columns}")

# ✅ Encode Categorical Data
label_encoders = {}
for col in ["team1", "team2", "toss_winner", "toss_decision", "winner"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ✅ Prepare Features & Target
X = df[["team1", "team2", "toss_winner", "toss_decision", "matches", "toss_wins"]]
y = df["winner"]

# ✅ Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train AI Model
model = RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42)
model.fit(X_train, y_train)

# ✅ Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
print("\n🔍 Classification Report:\n", classification_report(y_test, y_pred))

# ✅ Save Model & Encoders
with open(model_file, "wb") as f:
    pickle.dump((model, label_encoders), f)

print(f"🎯 AI Model Saved Successfully: {model_file}")
