FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY fs_server.py .
EXPOSE 9090
CMD ["python","fs_server.py"]