# import required libraries
from vidgear.gears import StreamGear
import cv2

# Open suitable video stream, such as webcam on first index(i.e. 0)
stream = cv2.VideoCapture('rtsp://admin:Water44!@10.0.0.190:554/cam/realmonitor?channel=1&subtype=0') 

# describe a suitable manifest-file location/name
streamer = StreamGear(output="dash_out.mpd")

# loop over
while True:

    # read frames from stream
    (grabbed, frame) = stream.read()

    # check for frame if not grabbed
    if not grabbed:
      break

    # {do something with the frame here}
    # lets convert frame to gray for this example
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # send frame to streamer
    streamer.stream(frame)

    # Show output window
    cv2.imshow("Output Gray Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.release()

# safely close streamer
streamer.terminate()
