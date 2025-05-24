# Hand-Volume-Control
Python script to control system volume using hand gestures with OpenCV and MediaPipe.


# Hand Gesture Volume Control ✋🔊

Control your system volume using hand gestures with OpenCV and MediaPipe.

## Features
- 📏 Distance-based volume adjustment (thumb and index finger)
- 📊 Real-time volume bar visualization
- � Smooth audio transitions
- 📷 Camera feed with FPS counter


```mermaid
---
config:
  theme: neo-dark
  layout: elk
  look: neo
title: Hand Gesture Controlled Volume Control Flowchart
---
flowchart TD
    A[("Start")] --> B{"Initialize Libraries"}
    B --> C["Capture Video Feed"]
    C --> D{"Detect Hand"}
    D -- No --> C
    D -- Yes --> E["Identify Hand Gesture"]
    E --> F{"Is Gesture Mapped?"}
    F -- No --> C
    F -- Yes --> G["Map Gesture to Volume Level"]
    G --> H["Adjust PC Volume"]
    H --> C

```


## Installation
1. Clone the repo:
   ```bash
      git clone https://github.com/shlok165/Hand-Volume-Control.git
      cd Hand-Volume-Control

2. Install Requirements:
   ```bash
      pip install -r requirements.txt

3. Run the main script:
   ```bash
      python volume_control.py

![demo](https://github.com/user-attachments/assets/aab41cf5-9d31-4e37-9f32-9490a6cbf92f)

