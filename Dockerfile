FROM django:python2

RUN mkdir -p /var/www/efforia
WORKDIR /var/www/efforia
COPY requirements.txt /var/www/efforia/
COPY . /var/www/efforia

RUN apt-get update
RUN apt-get install apache2 libapache2-mod-wsgi -y
COPY deploy/apache.conf /etc/apache2/sites-available/django.conf
COPY deploy/ports.conf /etc/apache2/ports.conf
COPY deploy/envvars /etc/apache2/envvars
RUN a2dissite 000-default && a2ensite django

RUN apt-get install libffi-dev -y
RUN apt-get install locales -y
RUN apt-get install mime-support -y
RUN echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput --settings="store.production"
RUN chown -R www-data:www-data /var/www/efforia/store/static
RUN chmod -R 775 /var/www/efforia/store/static

RUN psql -U postgres -h db -c "create database efforia;"
RUN python manage.py syncdb --noinput --settings="store.production"
RUN python manage.py migrate --noinput --settings="store.production"

EXPOSE 8080
CMD ["apache2ctl", "-D", "FOREGROUND"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
