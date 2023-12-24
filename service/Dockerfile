FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir /staticfiles
RUN python manage.py collectstatic --noinput


RUN python manage.py makemigrations --noinput && python manage.py migrate --noinput


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000


# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "service.wsgi:application"]