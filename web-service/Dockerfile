FROM python:3

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /api
WORKDIR /api


# expose the app port
EXPOSE 5001



# run the app server
CMD ["python","app.py"]