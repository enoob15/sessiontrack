/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    PORT: process.env.PORT || 3025
  },
  serverRuntimeConfig: {
    port: process.env.PORT || 3025
  }
}

module.exports = nextConfig