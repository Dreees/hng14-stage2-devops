FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./

RUN npm ci --omit=dev


FROM node:18-alpine
WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules

COPY --chown=appuser:appgroup . .

USER appuser
EXPOSE 3000


HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode===200?0:1))" || exit 1

CMD ["node", "app.js"]