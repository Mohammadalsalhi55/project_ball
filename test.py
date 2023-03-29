import project_ball
import cv2
pid = project_ball.Ball()
pid.Trackbar()
while True:
    pid.show()
    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        break
pid.get_vid().release()
cv2.destroyAllWindows()