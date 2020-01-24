FROM python:3.7
ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
CMD ["python", "check_changes.py"]
