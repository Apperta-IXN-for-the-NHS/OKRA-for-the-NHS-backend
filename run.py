from app import app
import threading
import auto_update

if __name__ == '__main__':
    flaskThread = threading.Thread(target= app.run)
    auto_update_thread = threading.Thread(target=auto_update.start_scheduler)
    flaskThread.start()
    auto_update_thread.start()
