FROM python:3.6  
ENV PYTHONUNBUFFERED 1  
RUN mkdir /config 
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ADD /config/requirements.pip /config/  
RUN pip install -r /config/requirements.pip  
COPY ./src /src
WORKDIR /src
EXPOSE 8080
CMD gunicorn LaborTracker.wsgi -b web:8080 --reload
#ENTRYPOINT /entrypoint.sh