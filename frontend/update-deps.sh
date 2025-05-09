#!/bin/bash

echo "Installing npm-check-updates globally..."
sudo npm install -g npm-check-updates

echo "Running npm-check-updates (ncu)..."
ncu -u

echo "Installing updated dependencies..."
npm install

echo "Running npm audit..."
npm audit