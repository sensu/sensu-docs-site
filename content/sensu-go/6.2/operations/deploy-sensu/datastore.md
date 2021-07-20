---
title: "Datastore reference"
linkTitle: "Datastore Reference"
reference_title: "Datastore"
type: "reference"
description: "Sensu stores observability events using an etcd database by default. You can also configure external PostgreSQL for enterprise-scale event storage."
weight: 160
version: "6.2"
product: "Sensu Go"
menu:
  sensu-go-6.2:
    parent: deploy-sensu
---

Sensu stores the most recent event for each entity and check pair using either an etcd (default) or PostgreSQL database.
Using Sensu with an external etcd cluster requires etcd 3.3.2.
Follow etcd's [clustering guide][21] using the same store configuration to stand up an external etcd cluster.

You can access observability event data with the [Sensu web UI][9] Events page, [`sensuctl event` commands][10], and the [events API][11].
For longer retention of observability event data, integrate Sensu with a time-series database like [InfluxDB][12] or a searchable index like ElasticSearch or Splunk.

## Use default event storage

By default, Sensu uses its embedded etcd database to store configuration and event data.
This embedded database allows you to get started with Sensu without deploying a complete, scalable architecture.
Sensu's default embedded etcd configuration listens for unencrypted communication on [ports][19] 2379 (client requests) and 2380 (peer communication).

Sensu can be configured to disable the embedded etcd database and use one or more [external etcd nodes][8] for configuration and event storage instead.
To stand up an external etcd cluster, follow etcd's [clustering guide][7] using the same store configuration.
Do not configure external etcd in Sensu via backend command line flags or the backend configuration file (`/etc/sensu/backend.yml`).

As your deployment grows beyond the proof-of-concept stage, review [Deployment architecture for Sensu][6] for more information about deployment considerations and recommendations for a production-ready Sensu deployment.

Sensu requires at least etcd 3.3.2 and is tested against releases in the 3.3.x series.
etcd version 3.4.0 is compatible with Sensu but may result in slower performance than the 3.3.x series.

## Scale event storage

{{% notice commercial %}}
**COMMERCIAL FEATURE**: Access enterprise-scale event storage in the packaged Sensu Go distribution.
For more information, see [Get started with commercial features](../../../commercial/).
{{% /notice %}}

Sensu supports using an external PostgreSQL instance for event storage in place of etcd.
PostgreSQL can handle significantly higher volumes of Sensu events, which allows you to scale Sensu beyond etcd's 8-GB limit.

When configured with a PostgreSQL event store, Sensu connects to PostgreSQL to store and retrieve event data in place of etcd.
Etcd continues to store Sensu entity and configuration data.
You can access event data stored in PostgreSQL using the same Sensu web UI, API, and sensuctl processes as etcd-stored events.

## PostgreSQL requirements

Sensu supports PostgreSQL 9.5 and later, including [Amazon Relational Database Service][3] (Amazon RDS) when configured with the PostgreSQL engine.
See the [PostgreSQL docs][14] to install and configure PostgreSQL.

For optimal performance, use the following PostgreSQL configuration settings in your `postgresql.conf` file:

{{< code postgresql >}}
max_connections = 200

shared_buffers = 10GB

maintenance_work_mem = 1GB

vacuum_cost_delay = 10ms
vacuum_cost_limit = 10000

bgwriter_delay = 50ms
bgwriter_lru_maxpages = 1000

max_worker_processes = 8
max_parallel_maintenance_workers = 2
max_parallel_workers_per_gather = 2
max_parallel_workers = 8

synchronous_commit = off

wal_sync_method = fdatasync
wal_writer_delay = 5000ms
max_wal_size = 5GB
min_wal_size = 1GB

checkpoint_completion_target = 0.9

autovacuum_naptime = 10s
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_scale_factor = 0.025
{{< /code >}}

Read the [PostgreSQL parameters documentation][20] for information about setting parameters.

## Configure the PostgreSQL event store

When you enable the PostgreSQL event store, event data cuts over from etcd to PostgreSQL.
This results in a loss of recent event history.
No restarts or Sensu backend configuration changes are required to enable the PostgreSQL event store.

When you successfully enable PostgreSQL as the Sensu Go event store, the Sensu backend log will include a message like this:

{{< code shell >}}
Mar 10 17:44:45 sensu-centos sensu-backend[1365]: {"component":"store-providers","level":"warning","msg":"switched event store to postgres","time":"2020-03-10T17:44:45Z"}
{{< /code >}}

After you [install and configure PostgreSQL][14], configure Sensu by creating a `PostgresConfig` resource like the following example.
See [Datastore specification][18] for more information.

{{< language-toggle >}}

{{< code yml >}}
---
type: PostgresConfig
api_version: store/v1
metadata:
  name: my-postgres
spec:
  batch_buffer: 0
  batch_size: 1
  batch_workers: 0
  dsn: "postgresql://user:secret@host:port/dbname"
  max_conn_lifetime: 5m
  max_idle_conns: 2
  pool_size: 20
  strict: true
  enable_round_robin: true
{{< /code >}}

{{< code json >}}
{
  "type": "PostgresConfig",
  "api_version": "store/v1",
  "metadata": {
    "name": "my-postgres"
  },
  "spec": {
    "batch_buffer": 0,
    "batch_size": 1,
    "batch_workers": 0,
    "dsn": "postgresql://user:secret@host:port/dbname",
    "max_conn_lifetime": "5m",
    "max_idle_conns": 2,
    "pool_size": 20,
    "strict": true,
    "enable_round_robin": true
  }
}
{{< /code >}}

{{< /language-toggle >}}

Save your `PostgresConfig` resource definition to a file (in this example, `postgres.yml` or `postgres.json`).
Then, use sensuctl [configured as the admin user][1] to activate the PostgreSQL event store.

{{< language-toggle >}}

{{< code shell "YML" >}}
sensuctl create --file postgres.yml
{{< /code >}}

{{< code shell "JSON" >}}
sensuctl create --file postgres.json
{{< /code >}}

{{< /language-toggle >}}

To update your Sensu PostgreSQL configuration, repeat the `sensuctl create` process.
You can expect to see PostgreSQL status updates in the [Sensu backend logs][2] at the `warn` log level and PostgreSQL error messages in the [Sensu backend logs][2] at the `error` log level.

## Disable the PostgreSQL event store

To disable the PostgreSQL event store, use `sensuctl delete` with your `PostgresConfig` resource definition file:

{{< language-toggle >}}

{{< code shell "YML" >}}
sensuctl delete --file postgres.yml
{{< /code >}}

{{< code shell "JSON" >}}
sensuctl delete --file postgres.json
{{< /code >}}

{{< /language-toggle >}}

The Sensu backend log will include a message to record that you successfully disabled PostgreSQL as the Sensu Go event store:

{{< code shell >}}
Mar 10 17:35:04 sensu-centos sensu-backend[1365]: {"component":"store-providers","level":"warning","msg":"switched event store to etcd","time":"2020-03-10T17:35:04Z"}
{{< /code >}}

When you disable the PostgreSQL event store, event data cuts over from PostgreSQL to etcd, which results in a loss of recent event history.
No restarts or Sensu backend configuration changes are required to disable the PostgreSQL event store.

## Datastore specification

### Top-level attributes

type         |      |
-------------|------
description  | Top-level attribute that specifies the [`sensuctl create`][16] resource type. PostgreSQL datastore configs should always be type `PostgresConfig`.
required     | true
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
type: PostgresConfig
{{< /code >}}
{{< code json >}}
{
  "type": "PostgresConfig"
}
{{< /code >}}
{{< /language-toggle >}}

api_version  |      |
-------------|------
description  | Top-level attribute that specifies the Sensu API group and version. For PostgreSQL datastore configs, the `api_version` should be `store/v1`.
required     | true
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
api_version: store/v1
{{< /code >}}
{{< code json >}}
{
  "api_version": "store/v1"
}
{{< /code >}}
{{< /language-toggle >}}

metadata     |      |
-------------|------
description  | Top-level scope that contains the PostgreSQL datastore `name` and `created_by` field.
required     | true
type         | Map of key-value pairs
example      | {{< language-toggle >}}
{{< code yml >}}
metadata:
  name: my-postgres
  created_by: admin
{{< /code >}}
{{< code json >}}
{
  "metadata": {
    "name": "my-postgres",
    "created_by": "admin"
  }
}
{{< /code >}}
{{< /language-toggle >}}

spec         |      |
-------------|------
description  | Top-level map that includes the PostgreSQL datastore config [spec attributes][17].
required     | true
type         | Map of key-value pairs
example      | {{< language-toggle >}}
{{< code yml >}}
spec:
  batch_buffer: 0
  batch_size: 1
  batch_workers: 0
  dsn: 'postgresql://user:secret@host:port/dbname'
  max_conn_lifetime: 5m
  max_idle_conns: 2
  pool_size: 20
  strict: true
  enable_round_robin: true
{{< /code >}}
{{< code json >}}
{
  "spec": {
    "batch_buffer": 0,
    "batch_size": 1,
    "batch_workers": 0,
    "dsn": "postgresql://user:secret@host:port/dbname",
    "max_conn_lifetime": "5m",
    "max_idle_conns": 2,
    "pool_size": 20,
    "strict": true,
    "enable_round_robin": true
  }
}
{{< /code >}}
{{< /language-toggle >}}

### Metadata attributes

name         |      |
-------------|------
description  | PostgreSQL datastore name used internally by Sensu.
required     | true
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
name: my-postgres
{{< /code >}}
{{< code json >}}
{
  "name": "my-postgres"
}
{{< /code >}}
{{< /language-toggle >}}

| created_by |      |
-------------|------
description  | Username of the Sensu user who created the datastore or last updated the datastore. Sensu automatically populates the `created_by` field when the datastore is created or updated.
required     | false
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
created_by: admin
{{< /code >}}
{{< code json >}}
{
  "created_by": "admin"
}
{{< /code >}}
{{< /language-toggle >}}

### Spec attributes

batch_buffer |      |
-------------|------
description  | Maximum number of requests to buffer in memory.<br>{{% notice warning %}}
**WARNING**: The batcher is sensitive to configuration values, and some `batch_buffer`, `batch_size`, and `batch_workers` combinations will not work optimally. We do not recommend configuring this attribute while we are testing and improving it.
{{% /notice %}}
required     | false
default      | 0
type         | Integer
example      | {{< language-toggle >}}
{{< code yml >}}
batch_buffer: 0
{{< /code >}}
{{< code json >}}
{
  "batch_buffer": 0
}
{{< /code >}}
{{< /language-toggle >}}

batch_size   |      |
-------------|------
description  | Number of requests in each PostgreSQL write transaction, as specified in the PostgreSQL configuration.<br>{{% notice warning %}}
**WARNING**: The batcher is sensitive to configuration values, and some `batch_buffer`, `batch_size`, and `batch_workers` combinations will not work optimally. We do not recommend configuring this attribute while we are testing and improving it.
{{% /notice %}}
required     | false
default      | 1
type         | Integer
example      | {{< language-toggle >}}
{{< code yml >}}
batch_size: 1
{{< /code >}}
{{< code json >}}
{
  "batch_size": 1
}
{{< /code >}}
{{< /language-toggle >}}

batch_workers |      |
-------------|------
description  | Number of Goroutines sending data to PostgreSQL, as specified in the PostgreSQL configuration.<br>{{% notice warning %}}
**WARNING**: The batcher is sensitive to configuration values, and some `batch_buffer`, `batch_size`, and `batch_workers` combinations will not work optimally. We do not recommend configuring this attribute while we are testing and improving it.
{{% /notice %}}
required     | false
default      | Current PostgreSQL pool size
type         | Integer
example      | {{< language-toggle >}}
{{< code yml >}}
batch_workers: 0
{{< /code >}}
{{< code json >}}
{
  "batch_workers": 0
}
{{< /code >}}
{{< /language-toggle >}}

dsn          |      |
-------------|------
description  | Data source names. Specified as a URL or [PostgreSQL connection string][15]. The Sensu backend uses the golang pq library, which supports a [subset of the PostgreSQL libpq connection string parameters][4].
required     | true
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
dsn: 'postgresql://user:secret@host:port/dbname'
{{< /code >}}
{{< code json >}}
{
  "dsn": "postgresql://user:secret@host:port/dbname"
}
{{< /code >}}
{{< /language-toggle >}}

max_conn_lifetime    |      |
-------------|------
description  | Maximum time a connection can persist before being destroyed. Specify values with a numeral and a letter indicator: `s` to indicate seconds, `m` to indicate minutes, and `h` to indicate hours. For example, `1m`, `2h`, and `2h1m3s` are valid. 
required     | false
type         | String
example      | {{< language-toggle >}}
{{< code yml >}}
max_conn_lifetime: 5m
{{< /code >}}
{{< code json >}}
{
  "max_conn_lifetime": "5m"
}
{{< /code >}}
{{< /language-toggle >}}

max_idle_conns    |      |
-------------|------
description  | Maximum number of number of idle connections to retain. 
required     | false
default      | `2`
type         | Integer
example      | {{< language-toggle >}}
{{< code yml >}}
max_idle_conns: 2
{{< /code >}}
{{< code json >}}
{
  "max_idle_conns": 2
}
{{< /code >}}
{{< /language-toggle >}}

pool_size    |      |
-------------|------
description  | Maximum number of connections to hold in the PostgreSQL connection pool. We recommend `20` for most instances. 
required     | false
default      | `0` (unlimited)
type         | Integer
example      | {{< language-toggle >}}
{{< code yml >}}
pool_size: 20
{{< /code >}}
{{< code json >}}
{
  "pool_size": 20
}
{{< /code >}}
{{< /language-toggle >}}

<a id="strict-attribute"></a>

strict       |      |
-------------|------
description  | If `true`, when the PostgresConfig resource is created, configuration validation will include connecting to the PostgreSQL database and executing a query to confirm whetherthe connected user has permission to create database tables. Otherwise, `false`.<br><br>We recommend setting `strict: true` in most cases. If the connection fails or the user does not have permission to create database tables, resource configuration will fail and the configuration will not be persisted. This extended configuration is useful for debugging when you are not sure whether the configuration is correct or the database is working properly.
required     | false
default     | false
type         | Boolean
example      | {{< language-toggle >}}
{{< code yml >}}
strict: true
{{< /code >}}
{{< code json >}}
{
  "strict": true
}
{{< /code >}}
{{< /language-toggle >}}

<a id="round-robin-postgresql"></a>

enable_round_robin |      |
-------------|------
description  | If `true`, enables [round robin scheduling][5] on PostgreSQL. Any existing round robin scheduling will stop and migrate to PostgreSQL as entities check in with keepalives. Sensu will gradually delete the existing etcd scheduler state as keepalives on the etcd scheduler keys expire over time. Otherwise, `false`.<br><br>We recommend using PostgreSQL rather than etcd for round robin scheduling because etcd leases are not reliable enough to produce precise [round robin behavior][5]. 
required     | false
default      | false
type         | Boolean
example      | {{< language-toggle >}}
{{< code yml >}}
enable_round_robin: true
{{< /code >}}
{{< code json >}}
{
  "enable_round_robin": true
}
{{< /code >}}
{{< /language-toggle >}}


[1]: ../../../sensuctl/#first-time-setup-and-authentication
[2]: ../../maintain-sensu/troubleshoot/
[3]: https://aws.amazon.com/rds/
[4]: https://pkg.go.dev/github.com/lib/pq@v1.2.0#hdr-Connection_String_Parameters
[5]: ../../../observability-pipeline/observe-schedule/checks/#round-robin-checks
[6]: ../deployment-architecture/
[7]: https://etcd.io/docs/latest/op-guide/clustering/
[8]: ../cluster-sensu/#use-an-external-etcd-cluster
[9]: ../../../web-ui/
[10]: ../../../sensuctl/create-manage-resources/#sensuctl-event
[11]: ../../../api/events/
[12]: ../../../observability-pipeline/observe-process/populate-metrics-influxdb/
[14]: https://www.postgresql.org
[15]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
[16]: ../../../sensuctl/create-manage-resources/#create-resources
[17]: #spec-attributes
[18]: #datastore-specification
[19]: ../install-sensu/#ports
[20]: https://www.postgresql.org/docs/current/config-setting.html
[21]: https://etcd.io/docs/v3.3.13/op-guide/clustering/
