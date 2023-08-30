FROM nikolaik/python-nodejs:python3.7-nodejs16-slim


RUN mkdir build

WORKDIR /build

RUN apt update;  apt install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /build

EXPOSE 80:80

ENTRYPOINT [ "python", "main.py"]