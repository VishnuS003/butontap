FROM nginx:alpine

# наш конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# корень для статики
WORKDIR /usr/share/nginx/html

# HTML и Unity build
COPY index.html ./
COPY Build ./Build
# если есть TemplateData — раскомментируй строку ниже
# COPY TemplateData ./TemplateData

EXPOSE 80
