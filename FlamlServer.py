import joblib
import numpy as np
import seldon_core
from seldon_core.user_model import SeldonComponent
from typing import Dict, List, Union, Iterable
import os
import logging

logger = logging.getLogger(__name__)


JOBLIB_FILE = "model.joblib"


class FlamlServer(SeldonComponent):
    def __init__(self, model_uri: str = None,  method: str = "predict"):
        super().__init__()
        self.model_uri = model_uri
        self.method = method
        self.ready = False
        logger.info("Model uri:", self.model_uri)
        logger.info("method:", self.method)

    def load(self):
        print("load")
        model_file = os.path.join(seldon_core.Storage.download(self.model_uri), JOBLIB_FILE)
        print("model file", model_file)
        self._joblib = joblib.load(model_file)
        self.ready = True
        print("Model has been loaded")

    def predict(self, X: np.ndarray, names: Iterable[str], meta: Dict = None) -> Union[np.ndarray, List, str, bytes]:
        try:
            if not self.ready:
                self.load()
            if self.method == "predict_proba":
                logger.info("Calling predict_proba")
                result = self._joblib.predict_proba(X)
            else:
                logger.info("Calling predict")
                result = self._joblib.predict(X)
            return result
        except Exception as ex:
            logging.exception("Exception during predict")
