from threading import Lock
import os

l = Lock()
file_name = "execution_report.txt"

# In-memory error storage for Vercel compatibility
error_logs = []


def persist_error(event_id, error_message, source_message):
    """Persist error to file or memory based on environment"""
    try:
        # Try to write to file (works in local environment)
        l.acquire()
        with open(file_name, "a") as myfile:
            myfile.write(str(event_id)+','+str(error_message)+','+str(source_message)+'\n')
        l.release()
    except (OSError, IOError):
        # Fallback to in-memory storage for Vercel
        error_entry = {
            'event_id': event_id,
            'error_message': error_message,
            'source_message': source_message
        }
        error_logs.append(error_entry)
        print(f"ERROR LOGGED: {error_entry}")


def handle_error(rawEvent, source_message, error_message):
    event_id = rawEvent.get('id') if rawEvent else None
    persist_error(event_id, error_message, source_message)


def flush_error_file():
    """Clear error logs"""
    try:
        # Try to clear file (works in local environment)
        open(file_name, "w").close()
        with open(file_name, "w") as file:
            file.write("EVENT_ID,ERROR_MESSAGE,SOURCE_MESSAGE\n")
    except (OSError, IOError):
        # Fallback to in-memory storage for Vercel
        error_logs.clear()
        print("Error logs cleared (in-memory)")


def get_error_logs():
    """Get error logs (for debugging)"""
    return error_logs
