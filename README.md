# Real-Time Air Quality Monitoring and Anomaly Detection in Halifax, Nova Scotia

## Overview
Streams hourly PM2.5 data from ECCC NAPS, detects anomalies (e.g., PM2.5 > 50 µg/m³), and stores them in InfluxDB using Kafka and Spark.

## Setup
1. **Install Python 3.9**:
   - Download from [python.org](https://www.python.org/downloads/), check "Add to PATH".
   - Verify: `python --version`.

2. **Install Spark 3.5.0**:
   - Download from [spark.apache.org](https://spark.apache.org/downloads/), extract to `C:\spark`.
   - Add `C:\spark\spark-3.5.0-bin-hadoop3\bin` to PATH.
   - Install Java 11 (e.g., OpenJDK from [adoptium.net](https://adoptium.net/)).
   - Verify: `spark-submit --version`.

3. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt