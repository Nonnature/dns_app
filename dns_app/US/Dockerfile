FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests
COPY us_server.py .
EXPOSE 8080
CMD ["python","us_server.py"]