FROM python:3.7.5-slim
WORKDIR home/repositories/html-diff
RUN python -m pip -r requirements.txt
COPY storage.py , check_cahnges.py.
CMD ["python", "check_changes.py"]