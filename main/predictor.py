import random
import pandas as pd
import numpy as np
from scipy.optimize import minimize

class ClimberGradePredictor:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        self.max_grade = self.df["grade"].max()
        self.expanded_df = self.expand_attempts()
        self.success_rates = self.calculate_success_rates()

    def expand_attempts(self):
        expanded_rows = []
        for _, row in self.df.iterrows():
            for attempt_num in range(row["attempts"]):
                success = row["success"] if attempt_num == row["attempts"] - 1 else 0
                expanded_rows.append({"grade": row["grade"], "success": success})
        return pd.DataFrame(expanded_rows)

    def calculate_success_rates(self):
        return self.expanded_df.groupby("grade")["success"].mean()

    def success_probability(self, climber_grade, route_grade, m):
        return 1 / (np.exp(-m * (climber_grade - route_grade)) + 1)

    def loss_function(self, params):
        climber_grade, m = params
        predicted_probs = np.array([
            self.success_probability(climber_grade, grade, m) 
            for grade in self.success_rates.index
        ])
        return np.sum((predicted_probs - self.success_rates.values) ** 2)

    def predict_climber_grade(self, initial_params=[5.0, 1.0]):
        bounds = [
            (0, self.max_grade),
            (1e-6, None)
        ]
        result = minimize(
            self.loss_function, 
            initial_params, 
            bounds=bounds, 
            method="L-BFGS-B"
        )
        climber_grade, m = result.x
        return climber_grade, m
    
def generate_suggestion(styles):
    if not styles:
        return "You haven't logged any climbs yet!"
    
    ideal_distribution = {
        "Powerful": 0.30,
        "Technical": 0.25,
        "Dynamic": 0.25,
        "Balance": 0.20,
    }

    total_climbs = sum(styles.values())
    if total_climbs == 0:
        return "You haven't logged any climbs yet! Start logging your climbs to get personalized training suggestions."
    
    if total_climbs < 10:
        return random.choice([
            "You’ve logged only a few climbs so far. Keep climbing and logging to get personalized insights!",
            "Great start! Log more climbs to unlock training suggestions.",
            "You're on your way! Log at least 10 climbs to get tailored advice for balancing your skills.",
            "Keep climbing! The more climbs you log, the better your training suggestions will be.",
            "You're building a solid foundation. Log more climbs to see how your style distribution evolves!"
        ])

    # Calculate the actual distribution
    actual_distribution = {style: count / total_climbs for style, count in styles.items()}

    # Compare actual distribution to ideal distribution
    suggestions = []
    for style, ideal_percentage in ideal_distribution.items():
        actual_percentage = actual_distribution.get(style, 0)
        if actual_percentage < ideal_percentage * 0.75:  # Underrepresented
            suggestions.append(f"Consider focusing more on {style} climbs to balance out your skills.")
        elif actual_percentage > ideal_percentage * 1.25:  # Overrepresented
            suggestions.append(f"You seem to favor {style} climbs. Try diversifying your sessions.")

    # If no specific suggestions, provide a general positive message
    if not suggestions:
        return random.choice([
            "Great balance between styles! Keep up the good work.",
            "Your climbing distribution looks well-balanced. Keep pushing your limits!",
            "You're doing a fantastic job balancing different climbing styles. Keep it up!"
        ])

    # Randomize phrasing for variety
    return random.choice(suggestions)

if __name__ == "__main__":
    data = {
        "grade": [4, 4, 3],
        "attempts": [1, 9, 6],
        "success": [1, 1, 1],
    }

    predictor = ClimberGradePredictor(data)
    climber_grade, m = predictor.predict_climber_grade()
    print(f"\nEstimated Climber Grade: V{climber_grade:.2f}")
    print(f"Estimated Steepness (m): {m:.2f}")