FROM python:3

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python", "api.py"]
#EXPOSE 8080
#ENTRYPOINT [ "/app/bootstrap.sh" ]