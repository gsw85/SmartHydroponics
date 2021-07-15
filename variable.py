thread_state = False

def stop_thread():
    global thread_state 
    thread_state = True

def start_thread():
    global thread_state 
    thread_state = False

def thread_status():
    global thread_state 
    return thread_state
