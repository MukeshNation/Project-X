FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
COPY apps/api/package.json apps/api/package.json
COPY apps/web/package.json apps/web/package.json
RUN npm install
COPY apps/api apps/api
RUN npm run build -w apps/api
EXPOSE 4000
CMD ["node", "apps/api/dist/index.js"]
