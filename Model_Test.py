import tensorflow as tf
from tensorflow.keras.preprocessing import image

img_height = 150
img_width = 150

loaded_model = tf.keras.models.load_model('/workspaces/ImageClassifier/model_P3.h5')

# Define the path to your single image file
img_path = '/workspaces/ImageClassifier/Web_Photo_Editor.jpg' # Replace with the actual path to your image

# Load the image and resize it
img = image.load_img(img_path, target_size=(img_height, img_width))

# Convert the image to a numpy array
img_array = image.img_to_array(img)

# Add a batch dimension
img_array = tf.expand_dims(img_array, 0) # Create a batch

# Make the prediction
predictions = loaded_model.predict(img_array)

# Get the predicted class (0 or 1)
predicted_class = tf.round(predictions[0]).numpy().item()

print(f"The predicted class for the image is: {predicted_class}")
