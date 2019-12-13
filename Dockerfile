FROM python:3.7


# install requirements as root
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# make this availabe for e.g. flask shell use
ENV FLASK_APP login.py

# run web app as web user
RUN adduser --disabled-password --gecos '' web
USER web

WORKDIR /home/web

COPY login.py login.py
COPY templates templates
COPY run.sh ./

# runtime
EXPOSE 5000
ENTRYPOINT ["./run.sh"]
