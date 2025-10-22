from threading import Lock

l = Lock()
file_name = "execution_report.txt"


def persist_error(event_id, error_message, source_message):
    l.acquire()
    with open(file_name, "a") as myfile:
        myfile.write(str(event_id)+','+str(error_message)+','+str(source_message)+'\n')
    l.release()


def handle_error(rawEvent, source_message, error_message):
    event_id = rawEvent.get('id') if rawEvent else None
    persist_error(event_id, error_message, source_message)


def flush_error_file():
    open(file_name, "w").close()
    with open(file_name, "w") as file:
        file.write("EVENT_ID,ERROR_MESSAGE,SOURCE_MESSAGE\n")
