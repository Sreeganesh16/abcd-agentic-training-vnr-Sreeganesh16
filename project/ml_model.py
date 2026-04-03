import pickle
import random
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = Path(__file__).with_name("model.pkl")
FEATURE_NAMES = [
    "time_spent",
    "task_switch_count",
    "idle_time",
    "task_difficulty",
]


def create_synthetic_dataset():
    random.seed(42)
    features = []
    labels = []

    # High focus: low idle, limited switching, and sustained but not excessive work.
    for _ in range(70):
        task_difficulty = random.randint(1, 3)
        time_spent = random.randint(20, 90) + random.randint(-4, 4) + (task_difficulty - 2) * 2
        task_switch_count = random.randint(0, 2)
        idle_time = random.randint(0, 5)

        features.append([max(20, time_spent), task_switch_count, max(0, idle_time), task_difficulty])
        labels.append("High")

    # Medium focus: some switching is normal if inactivity stays controlled.
    for _ in range(70):
        task_difficulty = random.randint(1, 3)
        time_spent = random.randint(35, 110) + random.randint(-5, 5) + (task_difficulty - 2) * 3
        task_switch_count = random.randint(2, 4)
        idle_time = random.randint(5, 15)

        features.append([max(20, time_spent), task_switch_count, max(0, idle_time), task_difficulty])
        labels.append("Medium")

    # Low focus: repeated switching plus inactivity and extended time suggest fatigue.
    for _ in range(70):
        task_difficulty = random.randint(1, 3)
        time_spent = random.randint(91, 180) + random.randint(-6, 6) + (task_difficulty - 1) * 2
        task_switch_count = random.randint(6, 10)
        idle_time = random.randint(16, 35)

        features.append([max(20, time_spent), task_switch_count, max(0, idle_time), task_difficulty])
        labels.append("Low")

    # Productive switching cases: frequent switches with low idle should not always mean low focus.
    for _ in range(15):
        task_difficulty = random.randint(2, 3)
        time_spent = random.randint(30, 85)
        task_switch_count = random.randint(5, 7)
        idle_time = random.randint(0, 4)

        features.append([time_spent, task_switch_count, idle_time, task_difficulty])
        labels.append(random.choice(["Medium", "High"]))

    # Short sessions: avoid overly strong conclusions when there is little evidence.
    for _ in range(15):
        task_difficulty = random.randint(1, 3)
        time_spent = random.randint(1, 9)
        task_switch_count = random.randint(0, 3)
        idle_time = random.randint(0, 6)

        features.append([time_spent, task_switch_count, idle_time, task_difficulty])
        labels.append("Medium")

    return features, labels


def train_model():
    features, labels = create_synthetic_dataset()
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
    )
    model.fit(features, labels)
    return model


def save_model(model, model_path=MODEL_PATH):
    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(model_path=MODEL_PATH):
    with open(model_path, "rb") as model_file:
        return pickle.load(model_file)


def train_and_save_model():
    model = train_model()
    save_model(model)
    return model


def predict_focus(input_data):
    if not MODEL_PATH.exists():
        train_and_save_model()

    model = load_model()
    feature_values = [input_data[feature] for feature in FEATURE_NAMES]
    prediction = model.predict([feature_values])[0]
    return str(prediction)


if __name__ == "__main__":
    train_and_save_model()
