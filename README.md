**_A gesture-controlled solution for accessible urban gardening_**

## Overview
This project aims to create a vision-based AI system that allows users to control plant watering using simple hand gestures, with no physical touch or mobile app required. It’s built using MediaPipe for hand tracking and a webcam for input, making it highly accessible and intuitive. The system is designed with a strong focus on enabling **elderly** and **specially-abled individuals** to care for plants independently and sustainably.

## Problem Statement
Particularly the elderly and specially-abled, face challenges in maintaining home gardens due to physical limitations, lack of technical knowledge, or inaccessible interfaces. Existing smart gardening systems often rely on mobile apps or touchscreens, which may not be inclusive for all user groups.
This project addresses the need for a **low-cost, non-contact, camera-based plant care system** that can be operated with simple gestures, making urban gardening more inclusive, manageable, and engaging.

## Features
- **Open palm gesture**: Waters all trays automatically
- **Pointing gesture**: Waters specific trays (Tray 1, Tray 2, etc.)
- **Real-time detection** using webcam and MediaPipe
- Easy to adapt to real pumps/motors using microcontrollers (like ESP32)
- Designed for **non-technical users**, especially senior citizens

## Directory Structure

```
Vision-ai-plant-watering/
│
├── README.md                 <- Overview of the project
├── architecture-diagram.png <- Visual layout of your system
├── Hand_detect_Cv/
│   └── mediapipe_gesture_demo.ipynb  <- Working prototype notebook
├── Project_Docs/
│   ├
│   └──Projecct_expaliner.pdf
├── Ecommerce_files   <-how people can sell crops
└── assets/           <- Images, sketches, screenshots
```

## How It Works
Using a simple webcam, the system continuously tracks hand gestures:
- When an **open palm** is detected, all trays are watered.
- When the user points in a certain fingers, the corresponding tray (Tray 1, Tray 2, etc.) is watered.
This removes the need for apps, buttons, or sensors and creates a frictionless experience for the user.

## Real-World Impact
- Enables independent gardening for users with mobility or visual limitations.
- Supports mental health and well-being through accessible interaction with plants.
- Encourages **sustainable micro-farming** in urban areas.
- Reduces the complexity typically involved in IoT-based gardening systems.
- Designed to be **low-cost and scalable**, ideal for homes, schools, and community centers.
- Introduces an innovative model where **surplus produce** grown in trays can be **sold via an e-commerce platform**—turning gardening into a self-sustaining activity and opening income opportunities for users.

## Future Scope
- Integration with **IoT controllers (e.g., ESP32)** for real-time pump control.
- Add-on features like **soil moisture sensing**, **weather prediction**, and **automated alerts**.
- Expansion into **community gardens** with shared dashboards and gesture zones.
- Build a **marketplace app** or web dashboard where users can **list and sell extra crops**, creating a hyperlocal farm-to-table network.

## Getting Started
To run the prototype:
1. Install dependencies:
   ```bash
   pip install mediapipe opencv-python
   ```
2. Ensure your webcam is connected and well-lit.
3. Perform gestures in front of the camera to see the tray watering logic in action.
