FROM        ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN         apt-get update && apt-get -y install python2.7 \
                    python2.7-dev python-pip gcc make supervisor libmysqlclient-dev
RUN         pip install -U flask requests gunicorn gevent flask-cli MySQL-python \
        jieba Flask-JSON Flask-SQLAlchemy
COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR     /data/www/mangosteen
EXPOSE 		5000
CMD         ["/usr/bin/supervisord"]