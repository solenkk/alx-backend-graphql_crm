CRM Task Scheduling Setup
This guide explains how to set up Celery and Celery Beat for generating weekly CRM reports, along with required dependencies.

1. Install Dependencies
Install Redis and required Python packages:

# Install Redis (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install redis-server

# Install Python dependencies
pip install -r requirements.txt

✔ Install Redis & dependencies  
✔ Run migrations  
✔ Start Redis  
✔ Start Celery worker  
✔ Start Celery Beat  
✔ Verify logs

# Celery CRM Report Setup Guide

## Prerequisites

- Redis server installed and running
- Python dependencies installed

## Installation Steps

### 1. Install Redis

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

# Celery CRM Report Setup Guide

## Prerequisites

- Redis server installed and running
- Python dependencies installed

## Installation Steps

### 1. Install Redis

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

# Install Redis (Ubuntu/Debian)

sudo apt-get update
sudo apt-get install redis-server

# Install Python dependencies

pip install -r requirements.txt

✔ Install Redis & dependencies  
✔ Run migrations  
✔ Start Redis  
✔ Start Celery worker  
✔ Start Celery Beat  
✔ Verify logs

