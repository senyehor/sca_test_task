import os

bind = f"[::]:{os.getenv('APP_PORT')}"
workers = 1
# Whether to send Django output to the error log
capture_output = True
loglevel = "info"
redirect_stderr = True
