FROM python AS mycontainer
COPY chatbot.py /
COPY requirements.txt /
COPY config.json /
RUN ["pip", "install", "pip", "update"]
RUN ["pip", "install", "-r", "requirements.txt"]
CMD python chatbot.py