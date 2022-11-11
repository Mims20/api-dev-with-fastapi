FROM python:3.9.6

WORKDIR /usr/src/app

# copy and run requirements.txt for optimization. This doesnt get run again unless there's change in requirements.txt file
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy everything in current directory to WORKDIR-which is current working directory for docker
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]