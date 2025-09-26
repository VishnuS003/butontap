FROM nginx:1.25-alpine
WORKDIR /usr/share/nginx/html
COPY Build/ ./Build/
COPY TemplateData/ ./TemplateData/
COPY index.html ./
COPY nginx.conf /etc/nginx/nginx.conf
