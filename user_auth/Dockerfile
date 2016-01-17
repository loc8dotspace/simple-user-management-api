FROM python:2.7

MAINTAINER Sid Thakur <sid.thakur@outlook.com>

RUN apt-get update && apt-get install -y nginx \
    supervisor \
    uwsgi-plugin-python

RUN mkdir -p /var/log/nginx/app && mkdir -p /var/log/uwsgi/app/

RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY uwsgi.ini /var/www/app/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf


RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY app/requirements.txt /home/ 
RUN pip install -r /home/requirements.txt
COPY app /var/www/app

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
