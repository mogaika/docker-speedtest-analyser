FROM alpine:3.9

# greet me :)
MAINTAINER Tobias Rös - <roes@amicaldo.de>

# install dependencies
RUN apk update && apk add \
  bash \
  git \
  nodejs \
  nodejs-npm \
  nginx \
  nginx-mod-http-lua \
  python3 \
  py-pip && \
  pip install requests prometheus_client && \
  rm -R /var/www/* && \
  mkdir -p /etc/nginx /run/nginx /etc/nginx/global /var/www/html && \
  touch /var/log/nginx/access.log && touch /var/log/nginx/error.log

# install webroot files
ADD ./ /var/www/html/

RUN npm install -g yarn && cd /var/www/html/ && yarn install

EXPOSE 80
EXPOSE 9999

# install vhost config
ADD config/vhost.conf /etc/nginx/conf.d/default.conf
ADD config/nginxEnv.conf /etc/nginx/modules/nginxEnv.conf

RUN chown -R nginx:nginx /var/www/html/
RUN chmod +x /var/www/html/config/run.sh
ENTRYPOINT ["/var/www/html/config/run.sh"]
