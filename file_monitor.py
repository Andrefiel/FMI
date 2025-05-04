import os
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from db import insert_log

class FileMonitor(FileSystemEventHandler):
    def __init__(self, path_to_watch, callback=None):
        self.path_to_watch = path_to_watch
        self.observer = Observer()
        self.callback = callback

    def start(self):
        self.observer.schedule(self, self.path_to_watch, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def on_created(self, event):
        self._log_event("criação", event)

    def on_modified(self, event):
        self._log_event("modificação", event)

    def on_deleted(self, event):
        self._log_event("exclusão", event)

    def _log_event(self, event_type, event):
        if not event.is_directory:
            user = getpass.getuser()
            path = event.src_path
            insert_log(event_type, path, user)
            if self.callback:
                self.callback(f"{event_type.upper()} - {path} (Usuário: {user})")
