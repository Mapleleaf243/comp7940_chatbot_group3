FROM python AS mycontainer
COPY chatbot_v0.py /
COPY requirements.txt /
COPY config.json /
RUN ["pip", "install", "pip", "update"]
RUN ["pip", "install", "-r", "requirements.txt"]
ENV ACCESS_TOKEN=6097704169:AAGXJq3uZXedkZSlsphbqeFq48Ts-1eZfes
CMD python chatbot_v0.py