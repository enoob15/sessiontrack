FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Explicitly set npm configuration
RUN npm config set cache /tmp/npm-cache

# Install dependencies with verbose logging
COPY package.json package-lock.json* ./
RUN npm ci --verbose || (cat npm-debug.log && exit 1)

# Build the application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Create necessary directories
RUN mkdir -p /app/public
RUN mkdir -p /app/.next/static

# Copy build artifacts
COPY --from=builder /app/public /app/public
COPY --from=builder /app/.next/standalone /app
COPY --from=builder /app/.next/static /app/.next/static

USER nextjs

EXPOSE 3025

ENV PORT 3025
ENV HOSTNAME localhost

CMD ["node", "server.js"]