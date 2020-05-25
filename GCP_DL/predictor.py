import os
import numpy as np
import keras
import joblib
class MyPredictor(object):
	
  def __init__(self, model, preprocessor):
    self._model = model
    self._preprocessor = preprocessor

  def predict(self, instances, **kwargs):
    instances = [instances]
    inputs = np.asarray(instances)
    preprocessed_inputs = self._preprocessor.transform(inputs)
    preprocessed_inputs = np.array([preprocessed_inputs])  
    outputs = self._model.predict(preprocessed_inputs)
    outputs = self._preprocessor.inverse_transform(outputs)
    outputs = outputs[0].tolist()
    outputs = list(map(float,list(map("{:.2f}".format,outputs))))
    return outputs

  @classmethod
  def from_path(cls, model_dir):
    model_path = os.path.join(model_dir, 'area1model.h5')
    model = keras.models.load_model(model_path)

    preprocessor_path = os.path.join(model_dir, 'preprocessor1.sav')
    with open(preprocessor_path, 'rb') as f:
      preprocessor = joblib.load(f)

    return cls(model, preprocessor)
