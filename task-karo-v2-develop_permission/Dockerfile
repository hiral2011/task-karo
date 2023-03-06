FROM python:3.10


WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN pip3 install virtualenv
# RUN  pip3 install virtualenv && virtualenv sports && source sports/bin/activate

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./ ./


EXPOSE 8000

# RUN python3 manage.py makemigrations --no-input
# RUN python3 manage.py migrate --no-input

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]