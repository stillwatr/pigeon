FROM ubuntu:22.04

LABEL MAINTAINER "Claudius Korzen <korzen@cs.uni-freiburg.de>"

ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV LC_CTYPE "C.UTF-8"
ENV DEBIAN_FRONTEND "noninteractive"

# ==================================================================================================

RUN apt-get update && apt-get install -y python3 python3-pip sqlite3

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# ==================================================================================================

COPY telegram_commons telegram_commons
COPY setup.py .

RUN pip3 install .

# ==================================================================================================