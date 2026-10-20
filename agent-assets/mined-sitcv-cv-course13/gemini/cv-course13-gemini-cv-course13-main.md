# GEMINI.md

## Project Overview

This project demonstrates how to compute optical flow between video frames using OpenCV in Python. The goal is to track motion between frames using the Lucas-Kanade method.

## Task

Write a Python script that:
- Loads a video file or webcam stream.
- Detects good features to track using `cv2.goodFeaturesToTrack`.
- Computes optical flow using `cv2.calcOpticalFlowPyrLK`.
- Visualizes the flow vectors on the video frames.

## Input

- A video file (e.g., `video.mp4`) or webcam stream.
- the old code  is  in opiticalflow.py file
- the new code should be saved to opiticalflow-v2.py file

## Output

- A window displaying the video with optical flow vectors drawn.
- Optionally, save the output video with flow visualization.

## Constraints

- Use only OpenCV and NumPy.
- Keep the code modular and well-commented.
- Ensure compatibility with Python 3.8+.

## Prompt Examples

```bash
gemini > Write a Python script to compute optical flow using OpenCV.
gemini > Modify the script to save the output video with flow vectors.
gemini > Explain how the Lucas-Kanade method works in this context.
```