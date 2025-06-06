# Docker Compose Configurations for Temporal Load Testing

This directory contains multiple Docker Compose configurations for testing Temporal under different scenarios and backend configurations.

## 📁 Directory Structure

```
compose/
├── docker-compose-mysql-es.yaml           # Standard MySQL + Elasticsearch setup
├── docker-compose-cass-es.yaml            # Cassandra + Elasticsearch setup
├── docker-compose-mysql-es-py-worker.yaml # MySQL + Python workers
├── config_sql.yaml                        # SQL backend configuration
├── config_cassandra.yaml                  # Cassandra backend configuration
├── my.cnf                                 # MySQL configuration file
├── dynamicconfig/                         # Temporal dynamic configuration
│   ├── dynamic_config_sql.yaml           # SQL backend runtime settings
│   └── dynamic_config_cass.yaml          # Cassandra backend runtime settings
├── monitoring/                            # Monitoring configurations
│   ├── prometheus.yml                     # Prometheus configuration
│   └── grafana/                          # Grafana dashboards and datasources
├── MONITORING.md                          # Monitoring documentation
└── README.md                             # This file
```

## 🚀 Quick Start Commands

### MySQL + Elasticsearch (Recommended)

```bash
cd compose
docker-compose -f docker-compose-mysql-es.yaml up -d
```

### Cassandra + Elasticsearch (Production-like)

```bash
cd compose
docker-compose -f docker-compose-cass-es.yaml up -d
```

### MySQL + Python Workers

```bash
cd compose
docker-compose -f docker-compose-mysql-es-py-worker.yaml up -d
```

## 📊 Configuration Details

### docker-compose-mysql-es.yaml

- **Backend**: MySQL 8.0 with optimized configuration
- **Visibility**: Elasticsearch 7.x
- **Temporal Services**: 5 replicas of history, matching, worker, frontend
- **Load Generation**: 15 benchmark workers
- **Monitoring**: Full Prometheus + Grafana stack
- **Resource Usage**: ~6GB RAM, 4 cores
- **Best For**: General testing, development, CI/CD

### docker-compose-cass-es.yaml

- **Backend**: Cassandra 3.x cluster (6 nodes)
- **Visibility**: Elasticsearch 7.x
- **Temporal Services**: 1 replica each (lighter footprint)
- **Load Generation**: 15 benchmark workers
- **Monitoring**: Full monitoring stack
- **Resource Usage**: ~8GB RAM, 6 cores
- **Best For**: Production testing, high availability

### docker-compose-mysql-es-py-worker.yaml

- **Backend**: MySQL 8.0
- **Visibility**: Elasticsearch 7.x
- **Temporal Services**: 5 replicas each
- **Load Generation**: Custom Python workers
- **Monitoring**: Full monitoring stack
- **Resource Usage**: ~5GB RAM, 4 cores
- **Best For**: Custom Python workflow testing

## ⚙️ Configuration Files

### Database Configurations

- **config_sql.yaml**: MySQL backend with optimized connection pools
- **config_cassandra.yaml**: Cassandra backend with multi-datacenter support
- **my.cnf**: MySQL performance tuning settings

### Dynamic Configuration

Runtime settings for Temporal services:

- **dynamic_config_sql.yaml**: SQL backend tuning
- **dynamic_config_cass.yaml**: Cassandra backend tuning

Key performance settings:

```yaml
worker.persistenceMaxQPS: 5000
history.persistenceMaxQPS: 3000
worker.ESProcessorBulkActions: 2500
```

### Monitoring Configuration

- **prometheus.yml**: Metrics collection from all services
- **grafana/**: Pre-configured dashboards and datasources

## 🔍 Service Access

After starting any configuration:

- **Temporal UI**: http://localhost:8085
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📈 Load Testing Features

### Built-in Load Generation

All configurations include benchmark workers that automatically generate load:

- 15 concurrent benchmark workers
- Configurable workflow types and rates
- Metrics export to Prometheus

### Custom Load Testing

Use with the Python scheduler service:

```bash
# From project root
SCHEDULER_INFINITE_MODE=true \
SCHEDULER_CONCURRENCY=50 \
python -m playground.apps.test_sheduler.main
```

## 🛠️ Customization

### Scaling Services

```bash
# Scale Temporal services
docker-compose scale temporalio-history=10

# Scale benchmark workers
docker-compose scale benchmark-workers=30
```

### Resource Limits

Uncomment resource limits in compose files:

```yaml
deploy:
  resources:
    limits:
      memory: 16G
      cpus: '8.0'
```

## 🔧 Troubleshooting

### Common Issues

1. **Services won't start**: Check logs with `docker-compose logs <service>`
1. **High memory usage**: Reduce replica counts or enable resource limits
1. **Slow performance**: Tune dynamic configuration files

### Health Checks

```bash
# Check all services
docker-compose ps

# Verify Temporal is ready
curl -s http://localhost:8085/health
```

## 📚 Related Documentation

- [Main README](../README.md) - Complete project overview
- [MONITORING.md](MONITORING.md) - Detailed monitoring guide
- [Scheduler Documentation](../README_SCHEDULER.md) - Custom load testing tools
