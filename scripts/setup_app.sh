#!/usr/bin/env bash
set -e
echo "=== Setting up NichePulse Next.js App ==="
cd /home/openclaw/nichepulse/app

echo "1. Installing dependencies..."
npm install 2>&1 | tail -5

echo "2. Creating Next.js config..."
cat > next.config.mjs << 'NEXTEOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}
export default nextConfig
NEXTEOF

echo "3. Creating directory structure..."
mkdir -p app/niche data scripts lib

echo "=== Setup complete ==="
echo "Run: cd /home/openclaw/nichepulse/app && npm run dev"
