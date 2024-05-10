FROM python:3.9.19-bookworm
WORKDIR app
COPY app/. .
RUN pip install -r requirements.txt
RUN python prep.py
CMD ["python", "app.py"]
