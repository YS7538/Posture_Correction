# Posture Correction Utility

A real-time posture monitoring application built using **MediaPipe**, **OpenCV**, and **Python**.

The application uses computer vision to monitor posture through a webcam and alerts the user when poor posture is detected for an extended period of time.

> This project is currently under active development. Desktop packaging and background execution support are planned next.

---

## Features

### Real-Time Posture Detection

Uses MediaPipe Pose Landmarker to continuously track body landmarks through a webcam feed.

### Personalized Calibration

The application performs a calibration phase when started.

During calibration:

* The user sits in their ideal posture
* Forward lean measurements are collected
* A personalized posture baseline is generated
* Detection thresholds are automatically adjusted

This allows posture monitoring to adapt to different users instead of relying on fixed values.

### Multi-Metric Posture Analysis

The current posture evaluation uses:

#### Forward Lean Detection

Measures the depth difference between:

* Right Ear
* Right Shoulder

Used to detect slouching forward or backward.

#### Head Offset Detection

Measures horizontal displacement of the nose relative to the midpoint of both shoulders.

Used to detect leaning to one side.

#### Shoulder Tilt Detection

Measures vertical asymmetry between shoulders.

Used to detect uneven posture and side tilting.

### Audio Alerts

If poor posture is maintained for a configurable duration, an audio alert is played to remind the user to correct their posture.

### Threaded Audio Playback

Audio alerts are executed in a separate thread to prevent webcam freezing or UI lag while sounds are being played.

### Portable Asset Loading

The project uses `pathlib` to load assets through relative paths, making the project easier to move between systems.

---

## Technologies Used

* Python
* MediaPipe
* OpenCV
* NumPy
* Threading
* Playsound

---

## Project Structure

```text
Posture_Correction/
│
├── assets/
│   ├── beep.mp3
│   └── pose_landmarker_full.task
│
├── docs/
│   ├── LANDMARKS_REFERENCE.md
│   ├── PROJECT_LEARNINGS.md
│   └── FUTURE_IMPROVEMENTS.md
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How It Works

### Step 1: Calibration

When the application starts:

1. Sit in your normal upright posture
2. Remain still during calibration
3. The system records posture measurements
4. Personalized thresholds are generated

### Step 2: Monitoring

After calibration:

* Landmarks are tracked in real time
* Posture metrics are calculated
* Current posture is classified as good or bad

### Step 3: Alerting

If bad posture is maintained longer than the configured delay:

* An audio alert is triggered
* The alert plays only once until posture is corrected

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Posture_Correction
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## Current Limitations

* Webcam must remain visible to the user
* Landmark occlusion can reduce accuracy
* No smoothing/filtering of landmark data yet
* Desktop packaging is not completed
* Does not currently run in the system tray or background

---

## Future Improvements

* System tray integration
* Startup on boot
* Executable packaging with PyInstaller
* Background monitoring mode
* Landmark confidence filtering
* Temporal smoothing
* Posture analytics dashboard
* Daily posture statistics
* Multiple user profiles

---

## Key Learnings

This project was built primarily as a learning exercise in:

* Computer Vision
* MediaPipe
* Real-Time Systems
* Threading
* Event-Driven Programming
* Software Architecture
* Debugging and Performance Optimization

---

## License

This project is currently provided for educational and personal use.
