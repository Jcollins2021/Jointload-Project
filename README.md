# JointLoad Mapping with Neural Networks

## Project Overview

**JointLoad** is a machine learning project designed to demonstrate that data collected from **external, non-invasive sensors**—such as knee angle (via video) and foot pressure (via treadmill)—can be used to **predict internal joint pressure** captured by a **novel implantable biodegradable pressure sensor**.

This work supports the long-term goal of enabling **accurate force estimation in physical therapy** and post-operative recovery without requiring long-term invasive monitoring.

---

## Why This Matters

In rehabilitation from osteoarthritis-related surgeries (in both **humans and animals**), applying the **correct amount of force to the knee** is critical:

- **Too little force** → delayed healing  
- **Too much force** → potential re-injury or damage  

Implanting a pressure sensor in the knee provides direct feedback—but **removing traditional implants** can be risky or impractical. Our **biodegradable implantable sensor** solves this, but it **degrades before recovery is complete**.

This is where our model comes in: it enables clinicians to **continue estimating joint forces** after the sensor has degraded, using **external signals only**.

## How to Use

### 1. Clone the repository

git clone https://github.com/Jcollins2021/Jointload-Project
cd JointLoad
### 2. Run the analysis and training
Open and run data_analysis.ipynb to:

Load and clean the data

Train multiple neural network architectures (e.g., MLPs, CNNs, LSTMs)

Save trained models to the models/ directory

Generate result visualizations saved in Result Graphs/

### 3. View trained models
Use view_model.ipynb to:

Load and inspect the saved .keras models

Visualize architecture and model performance

## Key Results
Multiple deep learning models were tested.

The LSTM model performed the best, accurately mapping knee angle and foot pressure to internal joint forces.

This demonstrates the feasibility of replacing invasive sensors with model-based estimation after degradation.

## Applications & Future Work
This work has broad implications for:

Physical therapy monitoring in post-operative knee recovery

Animal model studies in biomechanics and rehabilitation

Any scenario where invasive sensors are not feasible long-term

Future directions may include:

Real-time deployment of the model

Expanding to more diverse subjects and motion types

Incorporating video-based pose estimation directly into the pipeline

## Collaborators
Developed in collaboration with PhD researchers at the Wireless Sensor and Systems Lab (WSSL) and Nguyen Research Group.