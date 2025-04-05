# camera_calibration
Camera Calibration with a chessboard

## Modules used for this simple-tool
* Numpy
* cv2

## Description
openCV module has a function for calibrating camera with checkerboard, well known as chessboard.
We can use this function to find intrinsic params of our camera.
We will use additional function to reduce distortions of our video.

## So, how?

1. Take a video of chessboard with our smartphone camera, digital camera or something else. For instance, <a href = "https://github.com/EarthRabbit/webcam_recorder">webcam</a> from our labtop.

2. If you stop the video, you can see corners of the chessboard, and we can capture an image what you see for camera calibration with functions,
```bibtex
complete, pts = cv.findChessboardCorners(img, board_pattern)
cv.drawChessboardCorners(display, board_pattern, pts, complete)
```
 Repeat this process several times. For me, 10 times of selecting image gave me a nice result.
![Image](https://github.com/user-attachments/assets/7b526d90-a5f2-4f6d-bae3-608632983591)

3. We can find our camera's intrinsic values(RMS error, camera matrix K, Distortion coefficient k1, k2, p1, p2, k3) using images and function.
```bibtex
return cv.calibrateCamera(obj_points, img_points, gray.shape[::1], K, dist_coeff, flags=calib_flags)
```
![Image](https://github.com/user-attachments/assets/9a0573a6-241e-46c4-8043-00095a1012e6)

This is my smartphone camera intrinsic values.

4. Using this values we can reduce distortion of our video for chessboard.
By pressing tab we can toggle modes between Original version,
![Image](https://github.com/user-attachments/assets/8c84004d-6fd1-456d-b5a4-0ecebe1dc9f3)
and Rectified version.
![Image](https://github.com/user-attachments/assets/264bad4b-266f-43bd-934d-5d69f3f0dde2)