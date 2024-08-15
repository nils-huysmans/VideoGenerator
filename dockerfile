FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libgomp1 \
    fonts-liberation \
    fontconfig

# Install ImageMagick 7
RUN cd /tmp && \
    git clone https://github.com/ImageMagick/ImageMagick.git ImageMagick-7.1.1 && \
    cd ImageMagick-7.1.1 && \
    ./configure && \
    make && \
    make install && \
    ldconfig /usr/local/lib && \
    rm -rf /tmp/ImageMagick-7.1.1

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Set environment variable for ImageMagick
ENV MAGICK_HOME=/usr/local

# Update font cache
RUN fc-cache -f -v

EXPOSE 5000

CMD ["python", "app.py"]
