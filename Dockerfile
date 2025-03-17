# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Spark dependencies (Java + Spark)
RUN apt-get update && apt-get install -y \
    openjdk-11-jre \
    && rm -rf /var/lib/apt/lists/*
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
RUN curl -L https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar -xz -C /opt/ \
    && ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Copy your project files
COPY src/ src/
COPY config/ config/
COPY data/ data/

# Set environment variables (optional, overridden by docker-compose if needed)
ENV PYTHONUNBUFFERED=1

# Command to run your application (default: consumer.py with Spark)
CMD ["spark-submit", "src/processing/consumer.py"]