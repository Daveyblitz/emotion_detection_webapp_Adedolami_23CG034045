import unittest
from model import EmotionModel  # Assuming EmotionModel is the class handling the model logic

class TestEmotionModel(unittest.TestCase):

    def setUp(self):
        self.model = EmotionModel()
        self.model.load_model('models/emotion_model.h5')  # Adjust the filename as necessary

    def test_model_prediction(self):
        test_image = 'path/to/test/image.jpg'  # Replace with an actual test image path
        prediction = self.model.predict(test_image)
        self.assertIn(prediction['dominant_emotion'], ['happy', 'sad', 'angry', 'surprised', 'neutral'])  # Add other emotions as needed

    def test_model_accuracy(self):
        accuracy = self.model.evaluate()  # Assuming evaluate method returns accuracy
        self.assertGreaterEqual(accuracy, 0.7)  # Assuming we want at least 70% accuracy

if __name__ == '__main__':
    unittest.main()