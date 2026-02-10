#!/bin/bash

# Build script for local testing (production mode)
echo "Building static site for production..."

# Temporarily set DEBUG=False for production build
sed -i '' 's/DEBUG = True/DEBUG = False/g' portfolio/settings.py

# Collect static files
python manage.py collectstatic --noinput

# Generate static site
python manage.py distill-local dist --force

# Copy static and media files
cp -r staticfiles dist/static
cp -r media dist/media

# Fix URLs for GitHub Pages subdirectory
find dist -name "*.html" -type f -exec sed -i '' -e 's|href="/"|href="/portfolio/"|g' -e 's|href="/portfolio/project/|href="/portfolio/project/|g' {} +

# Restore DEBUG=True for local development
sed -i '' 's/DEBUG = False/DEBUG = True  # Set to False for production builds/g' portfolio/settings.py

echo "✅ Build complete! Serve with: cd dist && python -m http.server 8080"
echo "📍 Visit: http://localhost:8080/portfolio/"
