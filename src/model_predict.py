import joblib
import numpy as np

class ModelPredictor:
    def __init__(self, model_path):
        """
        Initialize the predictor with a path to a trained model file.
        :param model_path: str, path to the .pkl or .joblib model file.
        """
        self.model = joblib.load(model_path)

    def predict(self, input_data: np.ndarray):
        """
        Make a prediction using the loaded model.
        :param input_data: np.ndarray containing the features for prediction.
        :return: np.ndarray of model predictions.
        """
        # Input validation or preprocessing can be handled here
        predictions = self.model.predict(input_data)
        return predictions

if __name__ == "__main__":
    # Example usage:
    # 1. Instantiate the predictor
    predictor = ModelPredictor(model_path="../models/my_trained_model.joblib")

    # 2. Create some sample input data
    sample_input = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example shape for an Iris model

    # 3. Get predictions
    preds = predictor.predict(sample_input)
    print("Predictions:", preds)