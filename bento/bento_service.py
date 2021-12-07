from typing import List

import numpy as np
import tensorflow as tf
from PIL import Image
from bentoml import api, artifacts, env, BentoService
from bentoml.frameworks.keras import KerasModelArtifact
from bentoml.adapters import ImageInput
from bentoml.configuration.containers import BentoMLContainer

MNIST_CLASSES = [str(x) for x in range(10)]
               
metrics_client = BentoMLContainer.metircs_client.get()
REQUEST_TIME = metrics_client.Summary('request_processing_time', 'Time spend processing request')

@env(pip_packages=["tensorflow", "pillow", "numpy", "typing", "imageio==2.9.0"])
@artifacts([KerasModelArtifact("model")])
class MnistService(BentoService):

    @REQUEST_TIME.time()
    @api(input=ImageInput(pilmode="L"), batch=True)
    def predict(self, imgs: List[np.ndarray]) -> List[str]:
        inputs = []
        for img in imgs:
            img = Image.fromarray(img).resize((28, 28))
            img = np.array(img.getdata()).reshape((28, 28, 1))
            inputs.append(img)
        inputs = np.stack(inputs)
        output = self.artifacts.model.predict(inputs)
        
        return np.round(output, 10)
