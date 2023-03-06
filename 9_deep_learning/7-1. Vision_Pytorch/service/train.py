"""
Trains a PyTorch image classification model using device-agnostic code.
"""

import os
import torch
import sys
import argparse
import data_setup, engine, model_builder, utils

from torchvision import transforms

if __name__ == "__main__":
  # Setup hyperparameters
  NUM_EPOCHS = 5
  BATCH_SIZE = 32
  HIDDEN_UNITS = 10
  LEARNING_RATE = 0.001
  MODEL_NAME = 'LearningModular.pth'

  print('-'*50)
  parser = argparse.ArgumentParser()
  parser.add_argument("--model_name", default="LearningModular.pth") 
  parser.add_argument("--batch_size", default=32, type=int) 
  parser.add_argument("--lr", default=0.001, type=float) 
  parser.add_argument("--num_epochs", default=5, type=int) 
  parser.add_argument("--hidden_units", default=10, type=int) 
  args = parser.parse_args()

  print(f'NUM_EPOCHS: {args.num_epochs} / BATCH_SIZE: {args.batch_size}')
  print('-'*50)

  # Setup directories
  train_dir = "data/pizza_steak_sushi/train"
  test_dir = "data/pizza_steak_sushi/test"

  # Setup target device
  device = "cuda" if torch.cuda.is_available() else "cpu"

  # Create transforms
  data_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
  ])

  # Create DataLoaders with help from data_setup.py
  train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders(
      train_dir=train_dir,
      test_dir=test_dir,
      transform=data_transform,
      batch_size=args.batch_size
  )

  # Create model with help from model_builder.py
  model = model_builder.TinyVGG(
      input_shape=3,
      hidden_units=args.hidden_units,
      output_shape=len(class_names)
  ).to(device)

  # Set loss and optimizer
  loss_fn = torch.nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(model.parameters(),
                              lr=args.lr)

  # Start training with help from engine.py
  engine.train(model=model,
              train_dataloader=train_dataloader,
              test_dataloader=test_dataloader,
              loss_fn=loss_fn,
              optimizer=optimizer,
              epochs=args.num_epochs,
              device=device)

  # Save the model with help from utils.py
  utils.save_model(model=model,
                  target_dir="models",
                  model_name=args.model_name)
