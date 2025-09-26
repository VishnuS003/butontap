# web/Dockerfile
FROM nginx:alpine

# наши конфиги nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Unity WebGL билд кладём в корень
WORKDIR /usr/share/nginx/html
COPY index.html ./
COPY Build ./Build
COPY TemplateData ./TemplateData

EXPOSE 80
