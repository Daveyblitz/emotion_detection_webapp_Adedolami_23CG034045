# Emotion Detector Project

## Overview
The Emotion Detector project is a web application that utilizes deep learning to detect human emotions from images and live video feeds. The application is built using Flask and integrates the DeepFace library for emotion analysis.

## Project Structure
```
emotion-detector
├── app.py                # Main application file
├── model.py              # Model training and architecture
├── requirements.txt      # Required libraries
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── templates             # HTML templates
│   ├── index.html        # Main page for uploading images
│   └── result.html       # Page displaying detection results
├── static                # Static files (CSS, JS)
│   ├── css
│   │   └── styles.css    # Styles for the web application
│   └── js
│       └── main.js       # JavaScript for client-side interactivity
├── models                # Directory for trained models
│   └── README.md         # Information about trained models
├── utils                 # Utility functions
│   └── camera.py         # Functions for webcam access
└── tests                 # Unit tests
    └── test_model.py     # Tests for the emotion detection model
```

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd emotion-detector
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- Upload an image or use the live capture feature to detect emotions.
- The results will be displayed on the result page, showing the detected emotion and additional information.

## Additional Information
- The trained model files are stored in the `models` directory. Refer to the `models/README.md` for details on the models and their usage.
- The `tests` directory contains unit tests to ensure the functionality of the emotion detection model.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.