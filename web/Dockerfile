FROM nginx:1.25-alpine

# Копируем наш конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем билд Unity
COPY Build/ /usr/share/nginx/html/Build/
COPY index.html /usr/share/nginx/html/index.html

# Если есть StreamingAssets:
# COPY StreamingAssets/ /usr/share/nginx/html/StreamingAssets/

# Убираем кэш
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
