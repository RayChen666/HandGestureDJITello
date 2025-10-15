from djitellopy import Tello

def test_drone_connection():
    try:
        print('1. Connection test:')
        tello = Tello()
        tello.connect()
        print('\n')

        print('2. Video stream test:')
        tello.streamon()
        print('\n')

        tello.end()
        return True
    except Exception as e:
        print(str(e))
        return False