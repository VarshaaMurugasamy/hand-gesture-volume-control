\# ✋ Hand Gesture Volume Control



Control your system volume in real time using just hand gestures — no mouse, no keyboard, just your webcam.



\## 🎯 How it works



The app uses your webcam to track your hand landmarks live. It measures the distance between your \*\*thumb tip\*\* and \*\*index finger tip\*\*:



\- 🤏 Pinch fingers together → volume decreases

\- ✋ Spread fingers apart → volume increases



A live volume bar and percentage are displayed on screen as visual feedback.



\## 🛠️ Tech Stack



\- \*\*Python\*\*

\- \*\*OpenCV\*\* – webcam feed and visual overlays

\- \*\*MediaPipe\*\* – real-time hand landmark detection

\- \*\*Pycaw\*\* – Windows system volume control



\## 📦 Setup



1\. Clone this repository

```bash

git clone https://github.com/VarshaaMurugasamy/hand-gesture-volume-control.git

cd hand-gesture-volume-control

```



2\. Create a virtual environment

```bash

python -m venv venv

venv\\Scripts\\activate   # Windows

```



3\. Install dependencies

```bash

pip install -r requirements.txt

```



4\. Run the project

```bash

python volume\_control.py

```



\## 🎮 Usage



\- Show your hand to the webcam

\- Pinch thumb and index finger together to lower volume

\- Spread them apart to raise volume

\- Press \*\*q\*\* to quit



\## 📋 Requirements



\- Python 3.9–3.12 (MediaPipe does not yet support 3.13)

\- Windows (for volume control via Pycaw) — Mac/Linux users can adapt the volume control section using `osascript` or `amixer`



\## 📸 Demo



\*(Add a screenshot or GIF of the project running here)\*



\## 📄 License



Free to use and modify for learning purposes.

