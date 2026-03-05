import * as tf from '@tensorflow/tfjs';
import { useState, useEffect } from 'react';

export const useASLModel = (modelUrl) => {
  const [model, setModel] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadModel = async () => {
      try {
        // Ensure the webgl backend is used for high-performance inference
        await tf.ready();
        const loadedModel = await tf.loadLayersModel(modelUrl);
        setModel(loadedModel);
        setLoading(false);
        console.log("ASL Model Loaded Successfully");
      } catch (err) {
        console.error("Failed to load model", err);
      }
    };
    loadModel();
  }, [modelUrl]);

  const predict = (landmarks) => {
    if (!model) return null;

    // Reshape landmarks to [1, 63] to match your Python training input
    const inputTensor = tf.tensor2d([landmarks], [1, 63]);
    const prediction = model.predict(inputTensor);
    
    // Get the index of the highest probability
    const labelIndex = prediction.argMax(1).dataSync()[0];
    
    // Cleanup tensors to prevent memory leaks in the browser
    inputTensor.dispose();
    prediction.dispose();

    return labelIndex;
  };

  return { predict, loading };
};
