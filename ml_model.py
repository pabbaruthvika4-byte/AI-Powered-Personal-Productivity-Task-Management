from sklearn.tree import DecisionTreeClassifier


# ---------------------------------
# Priority Prediction Function
# ---------------------------------

def predict_priority(urgency, importance):

    # Convert text values to numbers
    mapping = {
        "Low": 0,
        "Medium": 1,
        "High": 2
    }

    # Training data
    X = [
        [0, 0],  # Low urgency, Low importance
        [0, 1],  # Low urgency, Medium importance
        [0, 2],  # Low urgency, High importance
        [1, 0],  # Medium urgency, Low importance
        [1, 1],  # Medium urgency, Medium importance
        [1, 2],  # Medium urgency, High importance
        [2, 0],  # High urgency, Low importance
        [2, 1],  # High urgency, Medium importance
        [2, 2]   # High urgency, High importance
    ]

    # Expected priority
    y = [
        "Low",
        "Medium",
        "High",
        "Medium",
        "Medium",
        "High",
        "High",
        "High",
        "High"
    ]

    # Create model
    model = DecisionTreeClassifier(
        random_state=42
    )

    # Train model
    model.fit(X, y)

    # Convert user input
    user_input = [
        [
            mapping[urgency],
            mapping[importance]
        ]
    ]

    # Predict
    prediction = model.predict(user_input)

    return prediction[0]