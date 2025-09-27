# web/Dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html
COPY index.html ./
COPY Build ./Build
# если Unity положил TemplateData — раскомментируй
# COPY TemplateData ./TemplateData

EXPOSE 80
