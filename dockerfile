FROM python:3.8.12-slim-buster

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install libsndfile1 (linux soundfile package)
RUN apt-get update && apt-get install -y gcc git wget libsndfile1 ffmpeg sox libsox-fmt-all \
&& rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# installing jupyter lab inside
RUN pip install jupyterlab

RUN pip install pandas

# declare port used by jupyterlab
EXPOSE 8888

# set default command for jupyterlab
CMD ["jupyter" ,"lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''", "--allow-root"]

WORKDIR /preproc