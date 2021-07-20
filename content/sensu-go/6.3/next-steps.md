---
title: "Next steps with Sensu"
description: "With Sensu Go running in a local development environment, read this page to envision where you can go from here. Take a few more steps in your local installation, take the work you’ve already done to a pre-production or production environment, or learn more in our Sensu Go workshop."
version: "6.3"
product: "Sensu Go"
---

Welcome to Sensu’s documentation!

Congratulations on getting Sensu Go up and running in a local development environment via the Sensu.io quick start guide ([here's a link][1] if you need a refresher).
This page guides you through a few more details about Sensu Go and helps you envision where you can go from here, whether that’s taking a few more steps in your local installation or taking the work you’ve already done to a pre-production or production environment.

Here’s an overview of the differences between local Sensu Go installations and production-level Sensu Go deployments:

Environment | Purpose | Features
----------- | ------- | --------
**Local installation** | Provides a high-level view of a Sensu deployment and a development environment for evaluation | Facilitates proof-of-concept development and testing for observability workflows
**Production deployment** | Meets the needs of enterprise-scale implementations with multiple apps and thousands of events per second | Supports high availability, secrets management to keep sensitive information private, and other features designed for observability at scale

Sensu Go’s monitoring as code solution allows you to [export your locally created and tested workflows][2], deploy them in a production environment, and replicate any monitoring configuration from one environment to another.

But for now, let’s focus on the Sensu Go installation you’re already running locally if you've followed our [quick start guide][1] or our [self-guided workshop][3].

## Your local Sensu installation

Here’s an overview of the elements at work in your quick start local installation: the Sensu backend, a Sensu agent running on one entity, two checks (a keepalive check and an NTP check for monitoring system clock drift), and sensuctl, Sensu’s command line interface.

Element | Description
------- | -----------
`sensu-backend` | The Sensu backend schedules monitoring checks and processes the resulting observation data (events) with event filters, mutators, and handlers. The Sensu backend is the observability pipeline &mdash; the events that checks create move through it.
`sensu-agent` | The Sensu agent is a lightweight client that runs on the infrastructure components you want to monitor (entities). Sensu agents self-register with the backend, send keepalive messages, and execute monitoring checks.
`keepalive` | Sensu agents automatically execute keepalive checks to ensure that all registered agents are operating and can reach the Sensu backend. Although the agent starts keepalive monitoring automatically, you can specify details like how often the agent will publish keepalive events and when Sensu should consider an agent unresponsive. 
`monitoring-plugins` | `monitoring-plugins` is an asset: a shareable, reusable package that helps deploy Sensu plugins. Plugins are executable scripts that you can use as Sensu checks, handlers, and mutators. In other words, assets give you access to preconfigured resources for common observability tasks. You don’t have to write all of your resources from scratch.
`ntp-check` | In addition to keepalives, Sensu agents also execute checks that you create or add via assets to monitor entities, collect metrics, and produce events. The NTP check is part of the `monitoring-plugins` asset -- it monitors system clock drift, and it’s useful for compensating for servers with known and expected clock skew. In fact, you can deploy ntp-check for every server in your infrastructure and have Sensu start collecting NTP observation data.
`sensuctl` | The sensuctl command line interface calls Sensu’s underlying APIs so you can create, read, update, and delete Sensu resources, events, and entities.
Event list | Events are observation data that represent the state of an entity at a point in time. Observation data in events include check status or metric results (or both), the executing agent, and a timestamp. The `sensuctl event list` command retrieves the most recent events for each check you’re running.

{{% notice protip %}}
**PRO TIP**: If you're not familiar with these concepts, try the [self-guided Sensu Go Workshop](https://github.com/sensu/sensu-go-workshop).
To register for an interactive instructor-led session, visit the [Sensu Go Workshop registration page](https://sensu.io/sensu-go-workshop).
{{% /notice %}}

### Examine a resource definition

In the quick start guide, you used sensuctl for ad hoc configuration when you added the NTP check and retrieved a list of events.
But Sensu resources like checks and events also have detailed definitions that you can store, maintain, and reuse just like you would store, maintain, and reuse code.
Combining Sensu’s flexible APIs with this monitoring as code approach allows you to scale everything we’re describing on this page.

Here’s how to retrieve the resource definition for your NTP check and copy it to a YAML or JSON file.
Run:

{{< language-toggle >}}

{{< code shell "YML" >}}
sensuctl check info ntp --format yaml >> ntp.yaml
{{< /code >}}

{{< code shell "JSON" >}}
sensuctl check info ntp --format wrapped-json >> ntp.json
{{< /code >}}

{{< /language-toggle >}}

The file will include the NTP check definition in the format you specified:

{{< language-toggle >}}

{{< code yml >}}
---
type: CheckConfig
api_version: core/v2
metadata:
  created_by: admin
  name: ntp
  namespace: default
spec:
  check_hooks: null
  command: check_ntp_time -H time.nist.gov --warn 0.5 --critical 1.0
  env_vars: null
  handlers: []
  high_flap_threshold: 0
  interval: 30
  low_flap_threshold: 0
  output_metric_format: nagios_perfdata
  output_metric_handlers: null
  proxy_entity_name: ""
  publish: true
  round_robin: false
  runtime_assets:
  - sensu/monitoring-plugins
  secrets: null
  stdin: false
  subdue: null
  subscriptions:
  - linux
  timeout: 10
  ttl: 0
{{< /code >}}

{{< code json "Wrapped JSON">}}
{
  "type": "CheckConfig",
  "api_version": "core/v2",
  "metadata": {
    "created_by": "admin",
    "name": "ntp",
    "namespace": "default"
  },
  "spec": {
    "check_hooks": null,
    "command": "check_ntp_time -H time.nist.gov --warn 0.5 --critical 1.0",
    "env_vars": null,
    "handlers": [],
    "high_flap_threshold": 0,
    "interval": 30,
    "low_flap_threshold": 0,
    "output_metric_format": "nagios_perfdata",
    "output_metric_handlers": null,
    "proxy_entity_name": "",
    "publish": true,
    "round_robin": false,
    "runtime_assets": [
      "sensu/monitoring-plugins"
    ],
    "secrets": null,
    "stdin": false,
    "subdue": null,
    "subscriptions": [
      "linux"
    ],
    "timeout": 10,
    "ttl": 0
  }
}
{{< /code >}}

{{< /language-toggle >}}

Look at the `spec` object in the resource definition to learn a bit more about what the NTP check does:

- Checks the system time against the time.nist.gov standard every 30 seconds.
- Creates a warning event when system time differs from the standard by half a second and a critical event when your system time differs by one second.
- Collects the event data in [Nagios Performance Data format][4].

You can configure these settings as needed.
For example, set the interval to 60 so that the check runs every minute instead of every 30 seconds.
Or export the metrics data in a different [supported output metric format][5].

This describes what the NTP check does, but to access, visualize, receive alerts, and take action based on the observability data the NTP check is collecting, you’ll need to learn how to add event filters, mutators, and handlers to your workflow.

## Take what you’ve done with you

Before you move on to deploy Sensu in production, remember that you can take your work with you.

After you’ve created some Sensu resources in your local environment, export your resources to create a [monitoring as code][6] repository.
When you implement Sensu in production, you can use the resource definitions in your repository.
Use the `sensuctl dump` command to [export your local configuration][7] to a YAML or JSON file and start building a portable monitoring as code repo.

Keep experimenting in your local installation, following our [guides][8] or the [self-guided workshop][3] to test different observability pipeline configurations.
Or [move to a more robust deployment][9], learning and configuring as you go.
No matter how you move forward, you won’t lose any of the Sensu resources you create.

You’ll also be able to reproduce one environment’s configuration in a new environment.
When you are ready to initialize a new Sensu environment with all the entities, checks, and handlers you’ve already created, use the `sensuctl create` command.

## Next steps

Follow [Install Sensu][9] to deploy Sensu Go in production.

If something doesn’t go as planned, please let us know!
Contact the [Sensu account team][11].
You can also ask questions and join discussions in the Sensu Community [Discourse][12] or [Slack][13].


[1]: https://sensu.io/#getting-started
[2]: #take-what-youve-done-with-you
[3]: https://github.com/sensu/sensu-go-workshop
[4]: https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/perfdata.html
[5]: ../observability-pipeline/observe-schedule/metrics/#supported-output-metric-formats
[6]: ../operations/monitoring-as-code/
[7]: ../operations/monitoring-as-code/#export-existing-resources 
[8]: ../guides/
[9]: ../operations/deploy-sensu/install-sensu/
[10]: ../operations/deploy-sensu/deployment-architecture/
[11]: https://sensu.io/contact
[12]: https://discourse.sensu.io
[13]: https://sensucommunity.slack.com
