from django.db import models
import os
import numpy as np
import joblib
import tensorflow as tf

# Create your models here.
class AirQData(models.Model):
	State = models.CharField(max_length=50)
	City = models.CharField(max_length=50)
	NO2_Mean = models.FloatField()
	NO2_1st_Max_Value = models.FloatField()
	NO2_AQI = models.FloatField()
	O3_Mean = models.FloatField()
	O3_1st_Max_Value = models.FloatField()
	O3_AQI = models.FloatField()
	SO2_Mean = models.FloatField()
	SO2_1st_Max_Value = models.FloatField()
	SO2_AQI = models.FloatField()
	CO_Mean = models.FloatField()
	CO_1st_Max_Value = models.FloatField()
	CO_AQI = models.FloatField()


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
  def from_path(cls):
    model = tf.keras.models.load_model('area1model.h5')
    with open('preprocessor1.sav', 'rb') as f:
      preprocessor = joblib.load(f)

    return cls(model, preprocessor)