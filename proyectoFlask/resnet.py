from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
import keras
model = keras.applications.ResNet50V2(
    weights="imagenet"
)

model.save('models/model_resnet.h5')