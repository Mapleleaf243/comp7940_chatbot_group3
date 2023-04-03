FROM python AS mycontainer
COPY chatbot.py /
COPY requirements.txt /
RUN ["pip", "install", "pip", "update"]
RUN ["pip", "install", "-r", "requirements.txt"]
ENV ACCESS_TOKEN=6198028908:AAEb7UoBqkcL-pDltc8Tj6WRwoapF4sWkyI 
ENV HOST='redis-14873.c295.ap-southeast-1-1.ec2.cloud.redislabs.com' 
ENV PASSWORD='Pkg5KkGHrH57b4dnnjacR9vmQQa1uxSF' 
ENV REDISPORT=14873
CMD python chatbot.py