FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Expose the port used by the socket server
EXPOSE 5001

CMD ["python", "main.py"]