import configargparse
import cv2 as cv

from gesture_recognition import GestureRecognition, GestureBuffer
from go2_controller import Go2Controller
from utils import CvFpsCalc


def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int)
    parser.add("--width", help='cap width', type=int)
    parser.add("--height", help='cap height', type=int)
    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float)
    parser.add("--buffer_len",
               help='Length of gesture buffer',
               type=int)

    args = parser.parse_args()

    return args


def main():
    # init global vars
    global gesture_buffer
    global gesture_id

    WRITE_CONTROL = False

    # Argument parsing
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence,
                                          args.min_tracking_confidence)
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    # Controller
    controller = Go2Controller()
    mode = 0
    number = -1

    while True:
        fps = cv_fps_calc.get()

        # Process Key (ESC: end)
        key = cv.waitKey(1) & 0xff
        if key == 27:  # ESC
            break
        if key == 110:  # n
            WRITE_CONTROL = False
            mode = 0
        if key == 107:  # k
            WRITE_CONTROL = True
            mode = 1
        if key == 104:  # h
            WRITE_CONTROL = True
            mode = 2

        if WRITE_CONTROL:
            number = -1
            if 48 <= key <= 57:  # 0 ~ 9
                number = key - 48

        ret, image = cap.read()
        if not ret:
            break

        debug_image, gesture_id = gesture_detector.recognize(image, number, mode)
        gesture_buffer.add_gesture(gesture_id)
        controller.control(gesture_buffer)

        debug_image = gesture_detector.draw_info(debug_image, fps, mode, number)

        # Image rendering
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
