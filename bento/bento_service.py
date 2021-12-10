from typing import List

import numpy as np
import tensorflow as tf
from PIL import Image
from bentoml import api, artifacts, env, BentoService
from bentoml.frameworks.keras import KerasModelArtifact
from bentoml.adapters import ImageInput
from bentoml.types import InferenceResult
from prometheus_client import Summary

MNIST_CLASSES = [str(x) for x in range(10)]
               
REQUEST_TIME = Summary(name='request_processing_time', documentation='Time spend processing request', namespace='PREFIX')

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
        
        return InferenceResult(
                        data=output,
                        http_status=200,
                        http_headers={"Content-Type": "application/json"},
                )


        # return np.round(output, 10)
