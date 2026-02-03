/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    PORT: process.env.PORT || 3025,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8005'
  },
  serverRuntimeConfig: {
    port: process.env.PORT || 3025,
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8005'
  }
}

module.exports = nextConfig