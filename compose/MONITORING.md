# Temporal Monitoring

## 🚀 Interface Access

### Temporal UI

- **URL:** http://localhost:8085
- **Description:** Main Temporal web interface for viewing workflows, activities and namespaces

### Prometheus

- **URL:** http://localhost:9090
- **Description:** Metrics collection system
- **Targets:** http://localhost:9090/targets - status of all monitored services

### Grafana

- **URL:** http://localhost:3001
- **Login:** admin
- **Password:** admin
- **Description:** Metrics visualization system with pre-configured dashboards

## 📊 Available Dashboards

### Temporal Dashboards

1. **Temporal Server Metrics** - general server metrics
1. **SDK Metrics** - SDK client metrics
1. **Frontend Service Dashboard** - frontend service metrics
1. **History Service Dashboard** - history service metrics
1. **Matching Service Dashboard** - matching service metrics
1. **Worker Service Dashboard** - worker service metrics
1. **Visibility Dashboard** - advanced visibility metrics (Elasticsearch)

### Infrastructure Dashboards

8. **Prometheus Stats** - Prometheus self metrics
1. **MySQL Overview** - detailed MySQL metrics
1. **Node Exporter Full** - host system metrics
1. **Elasticsearch Overview** - Elasticsearch metrics

## 🔧 Exporters and Ports

### Prometheus Exporters

- **Node Exporter** - port 9100 (system metrics)
- **MySQL Exporter** - port 9104 (MySQL metrics)
- **Elasticsearch Exporter** - port 9108 (Elasticsearch metrics)

### Main Services

- **Prometheus** - port 9090
- **Grafana** - port 3001
- **Temporal UI** - port 8085

## 🔍 Configuration

### Prometheus

- Configuration: `monitoring/prometheus.yml`
- Scrape interval: 10 seconds for Temporal services, 15 seconds for exporters
- Retention: 200 hours

### Grafana

- Datasources: `monitoring/grafana/provisioning/datasources/`
- Dashboard providers: `monitoring/grafana/provisioning/dashboards/`
- Dashboards: `monitoring/grafana/dashboards/`

### Temporal Metrics

All Temporal services export metrics on port 9090:

- Frontend: `temporalio-frontend:9090/metrics`
- History: `temporalio-history:9090/metrics`
- Matching: `temporalio-matching:9090/metrics`
- Worker: `temporalio-worker:9090/metrics`
- Internal-Frontend: `temporalio-internal-frontend:9090/metrics`

## 📈 Key Metrics

### Temporal Metrics

- `temporal_request_total` - total number of requests
- `temporal_request_latency` - request latency
- `temporal_workflow_task_schedule_to_start_latency` - time from scheduling to execution

### MySQL Metrics

- `mysql_up` - MySQL availability
- `mysql_global_status_connections` - number of connections
- `mysql_global_status_slow_queries` - slow queries count
- `mysql_global_status_innodb_buffer_pool_pages_total` - buffer pool pages

### Elasticsearch Metrics

- `elasticsearch_cluster_health_status` - cluster health status
- `elasticsearch_indices_docs` - document count
- `elasticsearch_indices_store_size_bytes` - index storage size
- `elasticsearch_jvm_memory_used_bytes` - JVM memory usage

### System Metrics

- `node_cpu_seconds_total` - CPU utilization
- `node_memory_MemAvailable_bytes` - available memory
- `node_filesystem_avail_bytes` - free disk space
- `node_load1` - system load (1min)

## 🚨 Recommended Alerts

### Temporal Alerts

- High request latency (>1s)
- Large task queue in matching service
- Workflow execution errors

### Infrastructure Alerts

- MySQL unavailable (mysql_up == 0)
- Elasticsearch unavailable (elasticsearch_cluster_health_status != 1)
- High memory consumption (>80%)
- Low disk space (\<10%)
- High CPU load (>80%)
