from climatenet.utils.data import ClimateDatasetLabeled, ClimateDataset
from climatenet.models import CGNet
from climatenet.utils.utils import Config
import pandas as pd
import argparse
from os import path

# Parse script input to define data and model paths
parser = argparse.ArgumentParser(description='Train a CGNet model on ClimateNet data.')
parser.add_argument('-m', '--model_path', type=str, help='path to the model directory')
parser.add_argument('-d', '--data_path', type=str, help='path to the data directory')

args = parser.parse_args()

model_path = args.model_path
data_path = args.data_path

# Load model architecture and hyperparameters
config = Config(model_path + 'config.json')
cgnet = CGNet(config)

# Train model
train = ClimateDatasetLabeled(path.join(data_path, 'train'), config)
val = ClimateDatasetLabeled(path.join(data_path, 'val'), config)
train_history = cgnet.train(train, val)

# Evaluate model performance
test = ClimateDatasetLabeled(path.join(data_path, 'test'), config)
test_history = cgnet.evaluate(test)


class_masks = cgnet.predict(test) # masks with 1==TC, 2==AR

# Save model weights
cgnet.save_model(model_path)

# Save training history
history = pd.concat([train_history, test_history])
history.to_csv(model_path + 'history.csv')
