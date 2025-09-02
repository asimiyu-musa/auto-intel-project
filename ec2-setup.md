# EC2 Deployment Guide for Auto Intel Project

This guide will help you deploy your Auto Intel Project to an Amazon EC2 instance.

## Prerequisites

1. **AWS Account** with EC2 access
2. **EC2 Instance** (recommended: t3.medium or larger)
3. **Security Group** with ports 22 (SSH), 8080 (Airflow), and 5555 (Flower) open

## EC2 Instance Setup

### 1. Launch EC2 Instance

**Recommended specifications:**
- **Instance Type**: t3.medium or larger
- **OS**: Ubuntu 22.04 LTS
- **Storage**: At least 20GB
- **Security Group**: Allow SSH (port 22) and HTTP (port 8080)

### 2. Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3. Update System and Install Dependencies

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y curl wget git
```

## Project Deployment

### 1. Clone Your Project

```bash
# Clone your repository
git clone <your-repository-url>
cd auto_intel_project
```

### 2. Make Deployment Script Executable

```bash
chmod +x deploy.sh
```

### 3. Deploy the Project

You have several deployment options:

#### Option A: Full Stack (Airflow + Scrapy)
```bash
./deploy.sh full
```

#### Option B: Scrapy Only
```bash
./deploy.sh scrapy
```

#### Option C: Run Tests
```bash
./deploy.sh test
```

#### Option D: Run Spiders Manually
```bash
./deploy.sh spiders
```

## Accessing Your Services

### Airflow Web UI
- **URL**: `http://your-ec2-public-ip:8080`
- **Username**: `admin`
- **Password**: `admin123`

### Flower (Celery Monitoring)
- **URL**: `http://your-ec2-public-ip:5555`

## Management Commands

### View Logs
```bash
./deploy.sh logs
```

### Stop Services
```bash
./deploy.sh stop
```

### Restart Services
```bash
./deploy.sh restart
```

### Get Help
```bash
./deploy.sh help
```

## Docker Commands

### Build Image
```bash
docker-compose build auto-intel-scrapy
```

### Run Specific Spider
```bash
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
```

### Run All Spiders
```bash
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
```

### Run Tests
```bash
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
```

### Access Container Shell
```bash
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh shell
```

## Monitoring and Logs

### View Container Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs auto-intel-scrapy
docker-compose logs airflow-scheduler

# Follow logs in real-time
docker-compose logs -f
```

### Check Service Status
```bash
docker-compose ps
```

### Monitor Resource Usage
```bash
docker stats
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8080
   sudo netstat -tulpn | grep :8080
   
   # Kill the process if needed
   sudo kill -9 <PID>
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   chmod +x deploy.sh
   chmod +x entrypoint.sh
   ```

3. **Docker Service Not Running**
   ```bash
   # Start Docker service
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. **Out of Disk Space**
   ```bash
   # Clean up Docker
   docker system prune -a
   docker volume prune
   ```

### Health Checks

```bash
# Check if containers are healthy
docker-compose ps

# Check specific service health
docker-compose exec auto-intel-scrapy python -c "import scrapy; print('Scrapy OK')"
```

## Security Considerations

### 1. Change Default Passwords
Edit the `.env` file to change Airflow credentials:
```bash
_AIRFLOW_WWW_USER_USERNAME=your_username
_AIRFLOW_WWW_USER_PASSWORD=your_secure_password
```

### 2. Use HTTPS
Consider setting up a reverse proxy (nginx) with SSL certificates for production.

### 3. Firewall Configuration
Ensure your security group only allows necessary ports:
- Port 22 (SSH)
- Port 8080 (Airflow)
- Port 5555 (Flower, optional)

## Backup and Recovery

### Backup Data
```bash
# Backup logs and data
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ data/

# Backup Docker volumes
docker run --rm -v auto_intel_project_postgres-db-volume:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### Restore Data
```bash
# Restore from backup
tar -xzf backup-YYYYMMDD.tar.gz

# Restore database
docker run --rm -v auto_intel_project_postgres-db-volume:/data -v $(pwd):/backup ubuntu tar xzf /backup/postgres-backup-YYYYMMDD.tar.gz -C /data
```

## Scaling Considerations

### For Production Use

1. **Use Larger Instance Types**: Consider t3.large or c5.large for better performance
2. **Add Load Balancer**: For high availability
3. **Use RDS**: Instead of PostgreSQL in Docker for better reliability
4. **Add Monitoring**: Consider CloudWatch or similar monitoring solutions
5. **Use ECS/EKS**: For better container orchestration

### Performance Optimization

1. **Increase Docker Resources**: Allocate more CPU and memory to Docker
2. **Use SSD Storage**: For better I/O performance
3. **Optimize Scrapy Settings**: Adjust concurrent requests and delays
4. **Use Redis Cluster**: For better Celery performance

## Cost Optimization

1. **Use Spot Instances**: For non-critical workloads
2. **Right-size Instances**: Monitor usage and adjust instance types
3. **Use Reserved Instances**: For predictable workloads
4. **Clean Up Unused Resources**: Regular cleanup of logs and data

## Support

For issues or questions:
1. Check the logs: `./deploy.sh logs`
2. Run tests: `./deploy.sh test`
3. Check container status: `docker-compose ps`
4. Review this documentation
5. Check the main README.md file 