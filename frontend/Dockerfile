FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY yohoho/dist/ /etc/nginx/www/
EXPOSE 80
CMD [ "nginx", "-c", "/etc/nginx/nginx.conf", "-g", "daemon off;"]
