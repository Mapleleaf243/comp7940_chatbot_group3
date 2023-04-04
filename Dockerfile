FROM python AS mycontainer
COPY chatbot_v0.py /
COPY requirements.txt /
COPY config.json /
RUN ["pip", "install", "pip", "update"]
RUN ["pip", "install", "-r", "requirements.txt"]
CMD python chatbot_v0.py