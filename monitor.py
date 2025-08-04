import cv2
import numpy as np
import subprocess
import time
import sys
import os

# Correct path to adb.exe (note the added adb.exe at the end)
ADB_PATH = r"C:\Users\PRATEEK BALMI\OneDrive - Nettur Technical Training Foundation\Desktop\New folder (2)\platform-tools\adb.exe"

def capture_screenshot():
    """Capture screenshot with error handling"""
    try:
        process = subprocess.Popen(
            [ADB_PATH, 'exec-out', 'screencap', '-p'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        image_bytes, errors = process.communicate(timeout=10)
        
        if process.returncode != 0:
            print(f"ADB Error: {errors.decode().strip()}")
            return None
            
        if not image_bytes.startswith(b'\x89PNG'):
            print("Warning: Received non-PNG data")
            return None
            
        return image_bytes
    except Exception as e:
        print(f"Capture error: {str(e)}")
        return None

def display_stream(width=350, height=500):
    """Main display loop with resize capability"""
    try:
        while True:
            start_time = time.time()
            
            # Capture frame
            image_bytes = capture_screenshot()
            if image_bytes is None:
                time.sleep(1)  # Wait before retry
                continue
                
            # Decode frame
            frame = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                print("Decode failed - Possible data corruption")
                continue
                
            # Resize frame
            if height == 0:  # Maintain aspect ratio
                ratio = width / frame.shape[1]
                dim = (width, int(frame.shape[0] * ratio))
            else:
                dim = (width, height)
            resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            
            # Display
            cv2.imshow("Android Screen (Press Q to quit)", resized)
            
            # Handle keypress
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
                
            # Calculate FPS
            fps = 1/(time.time() - start_time)
            print(f"Streaming at {fps:.1f} FPS", end='\r')
    finally:
        cv2.destroyAllWindows()

def main():
    try:
        # Verify ADB exists
        if not os.path.exists(ADB_PATH):
            raise FileNotFoundError(f"ADB executable not found at {ADB_PATH}")

        # Verify ADB connection
        test = subprocess.run([ADB_PATH, 'devices'], capture_output=True, text=True, shell=True)
        if 'device' not in test.stdout:
            print("No devices connected. Please connect your Android device.")
            print("ADB Output:", test.stdout.strip())
            print("\nTroubleshooting tips:")
            print("1. Enable USB Debugging in Developer Options")
            print("2. Check USB cable connection")
            print("3. Try different USB port")
            print("4. Run 'adb kill-server' then 'adb start-server'")
            sys.exit(1)
            
        display_stream(width=350)
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please ensure:")
        print(f"1. ADB is installed at {ADB_PATH}")
        print("2. The path is correct (no special characters or spaces)")
        sys.exit(1)
    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Run as admin if on Windows
    if sys.platform == 'win32':
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("Warning: ADB often requires admin rights on Windows")
                print("Try running this script as Administrator")
        except:
            pass
    
    main()