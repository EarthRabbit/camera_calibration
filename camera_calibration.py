import numpy as np
import cv2 as cv

# extract images from the video with a keyboard
def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=20, wnd_name='Camera Calibration'):
    video = cv.VideoCapture(video_file)
    
    img_select = []
    while True:
        # Read an image from the video
        valid, img = video.read()
        if not valid:
            break
        
        if select_all: 
            img.select.append(img)
        else:
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)
            
            key = cv.waitKey(wait_msec)
            # if ' '(spacebar)key has pressed, chessboard corners would be displayed above video
            if key == ord(' '):
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                # if 'r'(Enter)key is pressed, stopped image would be appended to img_select
                if key == ord('\r'):
                    img_select.append(img)
            if key == 27:
                break
    
    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    # use img from img_select to find chessboard corners
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)
    # return value : rms, K, dist_coeff, flags
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::1], K, dist_coeff, flags=calib_flags)

if __name__ == '__main__':
    video_file = 'data/chessboard1.mp4'
    board_pattern = (8, 6)
    board_cellsize = 0.025
    
    img_select = select_img_from_video(video_file, board_pattern)
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)
    
    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')
    
    video = cv.VideoCapture(video_file)
    
    # rectify for reducing distortions
    show_rectify = True
    map1, map2 = None, None
    while True:
        valid, img = video.read()
        if not valid:
            break
        
        info = 'Original'
        if show_rectify:
            if map1 is None or map2 is None:
                map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1)
            img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
            info = 'Rectified'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        
        cv.imshow("Geometric Distortion Correction", img)
        key = cv.waitKey(20)
        if key == ord(' '):
            key = cv.waitKey()
        if key == 27:
            break
        elif key == ord('\t'):
            show_rectify = not show_rectify

video.release()
cv.destroyAllWindows()