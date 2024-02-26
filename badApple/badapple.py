import cv2
from PIL import Image

def split_video(path, outputPath, extraPath):
    video_capture = cv2.VideoCapture(path)

    if not video_capture.isOpened():
        print("Error: Could not open video file.")
        return
    
    # Create the output folder if it doesn't exist
    import os
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    # Initialize frame count
    frame_count = 0
    
    # Read the video frame by frame
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        
        # Break the loop if no frame is retrieved
        if not ret:
            break
        
        # Write the frame to disk
        frame_path = os.path.join(outputPath, f"{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)

        
        # Increment frame count
        frame_count += 1
    
    # Release the video capture object
    parth = os.path.join(outputPath,"0.jpg")
    count = 0
    print("now checking path = " + parth)
    newParth = os.path.join(extraPath,"0.ico")
    while os.path.exists(parth):
            convert_png_to_ico(parth, newParth)
            count += 1
            parth = os.path.join(outputPath, str(count) +".jpg")
            newParth = os.path.join(extraPath, str(count)+".ico")
            print("now checking " + parth)
        
    video_capture.release()
    print(f"Video frames extracted: {frame_count}")

def convert_png_to_ico(input_path, output_path):
    # Open the PNG image
     # Open the JPEG image
    img = Image.open(input_path)
    
    # Convert to RGBA mode (add alpha channel)
    img = img.convert("RGBA")
    
    # Resize to 256x256 (ICO format requirement)
    img = img.resize((256, 256), Image.LANCZOS)
    
    # Save as ICO format
    img.save(output_path, format='ICO')