---
title: "Sensu Go release notes"
linkTitle: "Release Notes"
description: "Read the Sensu Go release notes to learn about what's new in our latest release."
weight: -80
product: "Sensu Go"
toc: false
version: "5.21"
menu: "sensu-go-5.21"
---

- [5.21.3 release notes](#5213-release-notes)
- [5.21.2 release notes](#5212-release-notes)
- [5.21.1 release notes](#5211-release-notes)
- [5.21.0 release notes](#5210-release-notes)
- [5.20.2 release notes](#5202-release-notes)
- [5.20.1 release notes](#5201-release-notes)
- [5.20.0 release notes](#5200-release-notes)
- [5.19.3 release notes](#5193-release-notes)
- [5.19.2 release notes](#5192-release-notes)
- [5.19.1 release notes](#5191-release-notes)
- [5.19.0 release notes](#5190-release-notes)
- [5.18.1 release notes](#5181-release-notes)
- [5.18.0 release notes](#5180-release-notes)
- [5.17.2 release notes](#5172-release-notes)
- [5.17.1 release notes](#5171-release-notes)
- [5.17.0 release notes](#5170-release-notes)
- [5.16.1 release notes](#5161-release-notes)
- [5.16.0 release notes](#5160-release-notes)
- [5.15.0 release notes](#5150-release-notes)
- [5.14.2 release notes](#5142-release-notes)
- [5.14.1 release notes](#5141-release-notes)
- [5.14.0 release notes](#5140-release-notes)
- [5.13.2 release notes](#5132-release-notes)
- [5.13.1 release notes](#5131-release-notes)
- [5.13.0 release notes](#5130-release-notes)
- [5.12.0 release notes](#5120-release-notes)
- [5.11.1 release notes](#5111-release-notes)
- [5.11.0 release notes](#5110-release-notes)
- [5.10.2 release notes](#5102-release-notes)
- [5.10.1 release notes](#5101-release-notes)
- [5.10.0 release notes](#5100-release-notes)
- [5.9.0 release notes](#590-release-notes)
- [5.8.0 release notes](#580-release-notes)
- [5.7.0 release notes](#570-release-notes)
- [5.6.0 release notes](#560-release-notes)
- [5.5.1 release notes](#551-release-notes)
- [5.5.0 release notes](#550-release-notes)
- [5.4.0 release notes](#540-release-notes)
- [5.3.0 release notes](#530-release-notes)
- [5.2.1 release notes](#521-release-notes)
- [5.2.0 release notes](#520-release-notes)
- [5.1.1 release notes](#511-release-notes)
- [5.1.0 release notes](#510-release-notes)
- [5.0.1 release notes](#501-release-notes)
- [5.0.0 release notes](#500-release-notes)

### Versioning

Sensu Go adheres to [semantic versioning][2] using MAJOR.MINOR.PATCH release numbers, starting at 5.0.0.
MAJOR version changes indicate incompatible API changes.
MINOR versions add backward-compatible functionality.
PATCH versions include backward-compatible bug fixes.

### Upgrading

Read the [upgrade guide][1] for information about upgrading to the latest version of Sensu Go.

---

## 5.21.3 release notes

**October 14, 2020** &mdash; The latest release of Sensu Go, version 5.21.3, is now available for download.

This patch release includes a few fixes to improve stability and correctness.

See the [upgrade guide][1] to upgrade Sensu to version 5.21.3.

**FIXES:**

- Fixed a bug where HTTP connections could be left open after downloading assets.
- Fixed a bug where event filter or asset filter execution could cause a crash.
- ([Commercial feature][158]) Fixed a bug where PostgreSQL would refuse to store event with a negative check status.

## 5.21.2 release notes

**August 31, 2020** &mdash; The latest release of Sensu Go, version 5.21.2, is now available for download.

This patch release includes two fixes: one for PostgreSQL errors that could cause the backend to panic and one to ensure that failed check events are written to the event log file.

See the [upgrade guide][1] to upgrade Sensu to version 5.21.2.

**FIXES:**

- ([Commercial feature][158]) Fixed a bug where PostgreSQL errors could cause the backend to panic.
- Failed check events are now written to the event log file.

## 5.21.1 release notes

**August 5, 2020** &mdash; The latest release of Sensu Go, version 5.21.1, is now available for download.

This patch release includes fixes for a web UI crash when interacting with namespaces that contain 1000 or more events and regressions in logging various agent errors as well as an enhancement that provides additional context to websocket connection errors logged by the backend.

See the [upgrade guide][1] to upgrade Sensu to version 5.21.1.

**IMPROVEMENTS:**

- Backend log messages related to connection errors on the agent websocket API now provide more context about the error.

**FIXES:**

- Fixed a potential web UI crash when fetching events in namespace with 1000 or more events.
- Fixed a regression that prevented errors produced in the agent by assets, check validation, token substitution, or event unmarshaling from being logged.

## 5.21.0 release notes

**June 15, 2020** &mdash; The latest release of Sensu Go, version 5.21.0, is now available for download.

The latest release of Sensu Go, version 5.21.0, is now available for download! This release delivers several enhancements and fixes. The most significant enhancements involve user management: you can now generate a password hash, specify the resulting hash in your user definitions without having to store cleartext passwords, and create and update these users using `sensuctl create`. You can also reset user passwords via the backend API. We also tuned Sensu Go agent logging and changed the default log level from warning to info. Plus, we crushed a number of nasty bugs: checks configured with missing hooks can no longer crash the agent, proxy check request errors do not block scheduling for other entities, and more!

See the [upgrade guide][1] to upgrade Sensu to version 5.21.0.

**NEW FEATURES:**

- ([Commercial feature][158]) Added [entity count and limit][156] for each entity class in the tabular title in the response for `sensuctl license info` (in addition to the total entity count and limit).
- ([Commercial feature][158]) Added Linux amd64 OpenSSL-linked binaries for the Sensu agent and backend, with accompanying `--require-fips` and `--require-openssl` flags for the [agent][161] and [backend][160].
- Added `sensuctl user hash-password` command to generate password hashes.
- Added the ability to reset passwords via the backend API and `sensuctl user reset-password`.

**IMPROVEMENTS:**

- Changed the [default log level for `sensu-agent`][157] to `info` (instead of `warn`).

**FIXES:**

- The password verification logic when running `sensuctl user change-password` is now included in the backend API rather than sensuctl.
- Errors in publishing proxy check requests no longer block scheduling for other entities.
- Using the `--chunk-size` flag when listing namespaces in sensuctl now works properly.
- The agent no longer immediately exits in certain scenarios when components are disabled.
- Fixed a bug that could cause a GraphQL query to fail when querying a namespace that contained event data in excess of 2 GB.

## 5.20.2 release notes

**May 26, 2020** &mdash; The latest release of Sensu Go, version 5.20.2, is now available for download.

This patch release adds username to the API request log to help operators with troubleshooting and user activity reporting, as well as validation for subjects in role-based access control (RBAC) role binding and cluster role binding.
Release 5.20.2 also temporarily disables process discovery so we can investigate and resolve its performance impact on the backend (increased CPU and memory usage).

See the [upgrade guide][1] to upgrade Sensu to version 5.20.2.

**NEW FEATURES:**

- The API request log now includes the username.

**FIXES:**

- ([Commercial feature][141]) [Process discovery in the agent][155] is temporarily disabled.
- The system’s libc_type attribute is now properly populated for Ubuntu entities.
- Single-letter subscriptions are now allowed.
- Subjects are now validated in RBAC role binding and cluster role binding.
- [Sensuctl command][154] assets can now be retrieved and installed from Bonsai.

## 5.20.1 release notes

**May 15, 2020** &mdash; The latest release of Sensu Go, version 5.20.1, is now available for download.

This patch release includes a bug fix that affects the web UI federated homepage gauges when using the PostgreSQL datastore and several fixes for the data displayed in the web UI entity details.

See the [upgrade guide][1] to upgrade Sensu to version 5.20.1.

**FIXES:**

- ([Commercial feature][141]) Fixes a bug that prevented the federated homepage in the [web UI][153] from retrieving the keepalive and event gauges when PostgreSQL was configured as the event datastore.
- ([Commercial feature][141]) The [memory_percent and cpu_percent processes attributes][143] are now properly displayed in the [web UI][153].
- In the [web UI][153], the entity details page no longer displays float type (which applies only for MIPS architectures). Also on entity details pages, the system's libc type is now listed and process names are no longer capitalized.

## 5.20.0 release notes

**May 12, 2020** &mdash; The latest release of Sensu Go, version 5.20.0, is now available for download.

This release delivers several new features, substantial improvements, and important fixes. One exciting new feature is agent local process discovery to further enrich entities and their events with valuable context. Other additions include a web UI federation view that provides a single pane of glass for all of your Sensu Go clusters and token substitution for assets. And Windows users rejoice! This release includes many Windows agent fixes, as well as agent log rotation capabilities! 

See the [upgrade guide][1] to upgrade Sensu to version 5.20.0.

**NEW FEATURES:**

- ([Commercial feature][141]) Added a [`processes` field ][143] to the system type to store agent local processes for entities and events and a `discover-processes` flag to the [agent configuration flags][142] to populate the `processes` field in entity.system if enabled.
- ([Commercial feature][141]) Added a new resource, `GlobalConfig`, that you can use to [customize your web UI configuration][148].
- ([Commercial feature][141]) Added metricsd to collect metrics for the [web UI][153].
- ([Commercial feature][141]) Added process and additional system information to the entity details view in the [web UI][153].
- ([Commercial feature][141]) Added a PostgreSQL metrics suite so metricsd can collect metrics about events stored in PostgreSQL.
- ([Commercial feature][141]) Added [entity class limits][151] to the license.
- Added check hook output to event details page in the [web UI][153].
- Added the [sensuctl describe-type command][144] to list all resource types.
- Added `annotations` and `labels` as [backend configuration][145] options.
- Added [token substitution for assets][146].
- Added `event.is_silenced` and `event.check.is_silenced` [field selectors][138].
- Added `Edition` and `GoVersion` fields to version information. In commercial distributions, the `Edition` version attribute is set to `enterprise`
- Added ability to configure the Resty HTTP timeout. Also, sensuctl now suppresses messages from the Resty library.

**IMPROVEMENTS:**

- ([Commercial feature][141]) The web UI homepage is now a [federated view][152]. 
- You can now [increment the log level][140] by sending SIGUSR1 to the sensu-backend or sensu-agent process.
- [License metadata][149] now includes the [current entity count and license entity limit][150].
- In the [web UI][153], users will see a notification when they try to delete an event without appropriate authorization.
- The Windows agent now has [log rotation][139] capabilities.
- Notepad is now the default editor on Windows rather than vi.

**FIXES:**

- ([Commercial feature][141]) Database connections no longer leak after queries to the cluster health API.
- In the [web UI][153], any leading and trailing whitespace is now trimmed from the username when authenticating.
- The [web UI][153] preferences dialog now displays only the first five groups a user belongs to, which makes the sign-out button more accessible.
- In the [web UI][153], the deregistration handler no longer appears as `undefined` on the entity details page.
- You can now [escape quotes to express quoted strings][147] in token substitution templates.
- The Windows agent now accepts and remembers arguments passed to `service run` and `service install`.
- The Windows agent now synchronizes writes to its log file, so the file size will update with every log line written.
- The Windows agent now logs to both console and log file when you use `service run`.

## 5.19.3 release notes

**May 4, 2020** &mdash; The latest release of Sensu Go, version 5.19.3, is now available for download.
This is a patch release with many improvements and bug fixes, including a fix to close the event store when the backend restarts, a global rate limit for fetching assets, and fixes for goroutine leaks. Sensu Go 5.19.3 also includes several web UI updates, from fixes to prevent crashes to new color-blindness modes.

See the [upgrade guide][1] to upgrade Sensu to version 5.19.3.

**FIXES:**

- The event store now closes when the backend restarts, which fixes a bug that allowed Postgres connections to linger after the backend restarted interally.
- The etcd event store now returns exact matches when retrieving events by entity (rather than prefixed matches).
- `sensu-backend init` now logs any TLS failures encountered during initialization.
- `sensuctl logout` now resets the TLS configuration.
- `env_vars` values can now include the equal sign.
- Error logs now include underlying errors encountered when fetching an asset.
- The log level is now WARNING when an asset is not installed because none of the filters match.
- Fixes a bug in the [web UI][135] that could cause labels with links to result in a crash.
- Fixes a bug in the [web UI][135] that could cause the web UI to crash when using an unregistered theme.
- Fixes a bug that could cause the backend to crash.
- Fixes a bug in multi-line metric extraction that appeared in Windows agents.
- Fixes an authentication bug that restarted the sensu-backend when agents disconnected.
- Fixes a bug that meant check `state` and `last_ok` were not computed until the second instance of the event.
- Fixes a bug that caused messages like "unary invoker failed" to appear in the logs.
- Fixes several goroutine leaks.
- Fixes a bug that caused the backend to crash when the etcd client received the error "etcdserver: too many requests."

**IMPROVEMENTS:**

- In the [web UI][135], color-blindness modes are now available.
- In the [web UI][135], labels and annotations with links to images will now be displayed inline.
- Adds a global rate limit for fetching assets to prevent abusive asset retries, which you can configure with the `--assets-rate-limit` and `--assets-burst-limit` flags for the [agent][136] and [backend][137].
- Adds support for restarting the backend via SIGHUP.
- Adds a timeout flag to `sensu-backend init`.
- Deprecated flags for `sensuctl silenced update` subcommand have been removed.

## 5.19.2 release notes

**April 27, 2020** &mdash; The latest release of Sensu Go, version 5.19.2, is now available for download.
This patch release adds two database connection pool parameters for PostgreSQL so you can configure the maximum time a connection can persist before being destroyed and the maximum number of idle connections to retain.
The release also includes packages for Ubuntu 19.10 and 20.04.

See the [upgrade guide][1] to upgrade Sensu to version 5.19.2.

**FIXES:**

- ([Commercial feature][122]) Adds SQL database connection pool parameters `max_conn_lifetime` and `max_idle_conns` to store/v1.PostgresConfig132.

**IMPROVEMENTS:**

- Sensu packages are now available for Ubuntu 19.10 (Eoan Ermine) and 20.04 (Focal Fossa). See the [supported platforms][133] page for a complete list of Sensu’s supported platforms and the [installation guide][134] to install Sensu packages for Ubuntu.

## 5.19.1 release notes

**April 13, 2020** &mdash; The latest release of Sensu Go, version 5.19.1, is now available for download.
This is a patch release with a number of bug fixes, including several that affect keepalive events, as well as an addition to the help response for `sensu-backend start` and `sensu-agent start`: the default path for the configuration file.

See the [upgrade guide][1] to upgrade Sensu to version 5.19.1.

**FIXES:**

- ([Commercial feature][122]) Fixed a bug that caused the PostgreSQL store to be enabled too late upon startup, which caused keepalive bugs and possibly other undiscovered bugs.
- Keepalives now fire correctly when using the PostgreSQL event store.
- Keepalives can now be published via the HTTP API.
- `sensu-agent` no longer allows configuring keepalive timeouts that are shorter than the keepalive interval.
- Eventd no longer mistakes keepalive events for checks with TTL.
- Keepalives now generate a new event UUID for each keepalive failure event.
- Agents now correctly reset keepalive switches on reconnect, which fixes a bug that allowed older keepalive timeout settings to persist.
- Token substitution templates can now express escape-quoted strings.
- The REST API now uses a default timeout of 3 seconds when querying etcd health.
- Pipe handlers now must include a [command][131].
- The response for `sensu-backend start --help` and `sensu-agent start --help` now includes the configuration file default path.
- The system's `libc_type` attribute is now populated on Alpine containers.

## 5.19.0 release notes

**March 30, 2020** &mdash; The latest release of Sensu Go, version 5.19.0, is now available for download.
This release is packed with new features, improvements, and fixes, including our first alpha feature: declarative configuration pruning to help keep your Sensu instance in sync with Infrastructure as Code workflows.
Other exciting additions include the ability to save and share your filtered searches in the web UI, plus a new `matches` substring match operator that you can use to refine your filtering results!
Improvements include a new `created_by` field in resource metadata and a `float_type` field that stores whether your system uses hard float or soft float.
We've also added agent and sensuctl builds for MIPS architectures, moved Bonsai logs to the `debug` level, and added PostgreSQL health information to the health API payload.

See the [upgrade guide][1] to upgrade Sensu to version 5.19.0.

**NEW FEATURES:**

- ([Commercial feature][122]) In the [web UI][124], you can now [save, recall, and delete filtered searches][123].
- ([Commercial feature][122]) Added the `matches` substring matching operator for [API response][126], [sensuctl][127], and [web UI][128] filtering selectors.
- ([Commercial feature][122]) Added agent and sensuctl builds for Linux architectures: `mips`, `mipsle`, `mips64`, and `mips64le` (hard float and soft float).
- ([Commercial feature][122]) Sensu now automatically applies the `sensu.io/managed_by` label to resources created via `sensuctl create` for use in the [`sensuctl prune` alpha feature][129].

**IMPROVEMENTS:**

- ([Commercial feature][122]) The [health endpoint][125] now includes PostgreSQL health information.
- Resource metadata now includes the `created_by` field, which Sensu automatically populates with the name of the user who created or last updated each resource.
- The agent now discovers entity libc type, VM system, VM role, and cloud provider.
- System type now includes the `float_type` field, which stores the float type the system is using (hard float or soft float).
- The Bonsai client now logs at the `debug` level rather than the `info` level.
- The store can now create wrapped resources.
- [Tessen][130] now collects the type of store used for events (`etcd` or `postgres`) and logs numbers of authentication providers, secrets, and secrets providers. Tessen data helps us understand how we can improve Sensu, and all Tessen transmissions are logged locally for complete transparency.

**FIXES:**

- Fixed a bug where `event.Check.State` was not set for events passing through the pipeline or written to the event log.
- Fixed a bug that allowed the agent to connect to a backend using a nonexistent namespace.
- Fixed a bug that allowed `subscriptions` to be empty strings.
- Corrected the HTTP status codes for unauthenticated and permission denied errors in the REST API.
- Fixed a bug where check history was incorrectly formed when using the PostgreSQL event store.

## 5.18.1 release notes

**March 10, 2020** &mdash; The latest release of Sensu Go, version 5.18.1, is now available for download.
This release fixes bugs that caused SQL migration failure on PostgreSQL 12, nil pointer panic due to OICD login, and sensu-backend restart upon agent disconnection.
It also includes a reliability improvement &mdash; a change to use the gRPC client rather than the embedded etcd client.

See the [upgrade guide][1] to upgrade Sensu to version 5.18.1.

**FIXES:**

- ([Commercial feature][115]) Fixed a bug that caused SQL migrations to fail on PostgreSQL 12.
- ([Commercial feature][115]) Fixed a bug where OIDC login could result in a nil pointer panic.
- Changed to using the gRPC client (rather than the embedded etcd client) to improve reliability and avoid nil pointer panics triggered by shutting down the embedded etcd client.
- The Sensu backend no longer hangs indefinitely if a file lock for the asset manager cannot be obtained. Instead, the backend returns an error after 60 seconds.
- Fixed a bug that caused sensu-backend to restart when agents disconnected.
- Fixed a bug where the backend would panic on some 32-bit systems.

## 5.18.0 release notes

**February 25, 2020** &mdash; The latest release of Sensu Go, version 5.18.0, is now available for download.
This release delivers a number of improvements to the overall Sensu Go experience.
From automatic proxy entity creation to unique Sensu event IDs, it’s now much easier to use and troubleshoot your monitoring event pipelines!
If you’re working behind an HTTP proxy, you can now manage remote Sensu Go clusters, as sensuctl now honors proxy environment variables (e.g. HTTPS_PROXY).
This release also includes a number of fixes for usability bugs, making for the most polished release of Sensu Go yet, so go ahead and give it a download!

See the [upgrade guide][1] to upgrade Sensu to version 5.18.0.

**IMPROVEMENTS:**

- The `event.entity.entity_class` value now defaults to `proxy` for [`POST /events`][114] requests.
- If you use the [events API][118] to create a new event with an entity that does not already exist, the sensu-backend will automatically create a proxy entity when the event is published.
- Sensuctl now accepts Bonsai asset versions that include a prefix with the letter `v` (for example, `v1.2.0`).
- The version API now retrieves the Sensu agent version for the Sensu instance.
- Log messages now indicate which filter dropped an event.
- Sensu now reads and writes `initializationKey` to and from EtcdRoot, with legacy support (read-only) as a fallback.
- Sensu will now check for an HTTP response other than `200 OK` response when fetching assets.
- Updated Go version from 1.13.5 to 1.13.7.

**FIXES:**

- ([Commercial feature][115]) [Label selectors][116] and [field selectors][117] now accept single and double quotes to identify strings.
- Fixed a bug that prevented wrapped resources from having their namespaces set by the default sensuctl configuration.
- Fixed a bug that prevented [API response filtering][119] from working properly for the silenced API.
- Improved event payload validation for the [events API][118] so that events that do not match the URL parameters on the `/events/:entity/:check` endpoint are rejected.
- Sensuctl now supports the `http_proxy`, `https_proxy`, and `no_proxy` environment variables.
- The [`auth/test` endpoint][120] now returns the correct error messages.

## 5.17.2 release notes

**February 19, 2020** &mdash; The latest release of Sensu Go, version 5.17.2, is now available for download.
This release fixes a bug that could prevent commercial features from working after internal restart.

See the [upgrade guide][1] to upgrade Sensu to version 5.17.2.

**FIXES:**

- Fixed a bug that could cause commercial HTTP routes to fail to initialize after an internal restart, preventing commercial features from working.

## 5.17.1 release notes

**January 31, 2020** &mdash; The latest release of Sensu Go, version 5.17.1, is now available for download.
This release fixes a web UI issue that cleared selected filters when sorting an event list and a bug that prevented certain `.tar` assets from extracting.
It also includes sensuctl configuration improvements.

See the [upgrade guide][1] to upgrade Sensu to version 5.17.1.

**IMPROVEMENTS:**

- Asset names may now include capital letters.
- Running the `sensuctl configure` command now resets the sensuctl cluster configuration.
- When you use `--trusted-ca-file` to configure sensuctl, it now detects and saves the absolute file path in the cluster configuration.

**FIXES:**

- ([Commercial feature][106]) When a silencing entry expires or is removed, it is also removed from the silences view in the [web UI][107].
- Fixed a bug that prevented `.tar` assets from extracting if they contain hardlinked files.
- In the [web UI][107], sorting an event list view no longer clears the selected filters.

## 5.17.0 release notes

**January 28, 2020** &mdash; The latest release of Sensu Go, version 5.17.0, is now available for download.
This is a significant release, with new features, improvements, and fixes!
We’re ecstatic to announce the release of secrets management, which eliminates the need to expose sensitive information in your Sensu configuration.
When a Sensu component (e.g. check, handler, etc.) requires a secret (like a username or password), Sensu will be able to fetch that information from one or more external secrets providers (e.g. HashiCorp Vault) and provide it to the Sensu component via temporary environment variables.
Secrets management allows you to move secrets out of your Sensu configuration, giving you the ability to safely and confidently share your Sensu configurations with your fellow Sensu users!
This release also includes per-entity keepalive event handler configuration, a sought-after feature for users who have migrated from Sensu 1.x to Sensu Go.

See the [upgrade guide][1] to upgrade Sensu to version 5.17.0.

**NEW FEATURES:**

- ([Commercial feature][106]) Added [HTTP API for secrets management][108], with a built-in `Env` secrets provider and support for HashiCorp Vault secrets management. The secrets provider resource is implemented for checks, mutators, and handlers.
- Added the `keepalive-handlers` agent configuration flag to specify the keepalive handlers to use for an entity's events.

**IMPROVEMENTS:**

- ([Commercial feature][106]) Upgraded the size of the events auto-incremented ID in the PostgreSQL store to a 64-bit variant, which allows you to store many more events and avoids exhausting the sequence.
- ([Commercial feature][106]) [Initialization][109] via `sensu-backend init` is now implemented for Docker.
- ([Commercial feature][106]) UPN binding support has been re-introduced via the `default_upn_domain` configuration attribute.
- In the [web UI][107], labels that contain URLs are now clickable links.
- Added `event.entity.name` as a supported field for the [`fieldSelector`][110] query parameter.
- In the [web UI][107], users with implicit permissions to a namespace can now display resources within that namespace.
- Explicit access to namespaces can only be granted via [cluster-wide RBAC resources][111].
- You can now omit the namespace from an event in [`HTTP POST /events`][112] requests.
- Added support for the `--format` flag in the [sensuctl command list][113] subcommand.

**FIXES:**

- ([Commercial feature][106]) Fixed a bug where the event check state was not present when using the PostgreSQL event store.
- ([Commercial feature][106]) Agent TLS authentication does not require a license.
- Fixed a memory leak in the entity cache.
- Fixed a bug that prevented `sensuctl entity delete` from returning an error when attempting to delete a non-existent entity.
- In the [web UI][107], fixed a bug that duplicated event history in the event timeline chart.
- `sensuctl command` assets installed via Bonsai now use the `sensuctl` namespace.
- Fixed a bug where failing check TTL events could occur if keepalive failures had already occurred.

## 5.16.1 release notes

**December 18, 2019** &mdash; The latest release of Sensu Go, version 5.16.1, is now available for download.
This release fixes a performance regression that caused API latency to scale linearly as the number of connected agents increased and includes a change to display the `sensu_go_events_processed` Prometheus counter by default.

See the [upgrade guide][1] to upgrade Sensu to version 5.16.1.

**IMPROVEMENTS**

- The `sensu_go_events_processed` Prometheus counter now initializes with the `success` label so the count is always displayed.

**FIXES:**

- The performance regression introduced in 5.15.0 that caused API latency to scale linearly as the number of connected agents increased is fixed.

## 5.16.0 release notes

**December 16, 2019** &mdash; The latest release of Sensu Go, version 5.16.0, is now available for download.
This is another important release, with many new features, improvements, and fixes.
We introduced an initialization subcommand for **new** installations that allows you to specify an admin username and password instead of using a pre-defined default.
We also added new backend flags to help you take advantage of etcd auto-discovery features and agent flags you can use to define a timeout period for critical and warning keepalive events.

New web UI features include a switcher that makes it easier to switch between namespaces in the dashboard, breadcrumbs on every page, OIDC authentication in the dashboard, a drawer that replaces the app bar to make more room for content, and more.

We also fixed issues with `sensuctl dump` and `sensuctl cluster health`, installing sensuctl commands via Bonsai, and missing namespaces in keepalive events and events created through the agent socket interface.

See the [upgrade guide][1] to upgrade Sensu to version 5.16.0.

**IMPORTANT:**

- For Ubuntu/Debian and RHEL/CentOS installations, the backend is no longer seeded with a default admin username and password.
Users will need to [run 'sensu-backend init'][102] on every new installation and specify an admin username and password.

**NEW FEATURES:**

- ([Commercial feature][105]) Users can now authenticate with OIDC in the dashboard.
- ([Commercial feature][105]) Label selectors now match the event's check and entity labels.
- Added a new flag,`--etcd-client-urls`, which should be used with sensu-backend when it is not operating as an etcd member.
The flag is also used by the new `sensu-backend init` subcommand.
- Added the ['sensu-backend init' subcommand][102].
- Added the [`--etcd-discovery`][100] and [`--etcd-discovery-srv`][100] flags to sensu-backend, which allow users to take advantage of the embedded etcd's auto-discovery features.
- Added [`--keepalive-critical-timeout`][101] to define the time after which a critical keepalive event should be created for an agent and [`--keepalive-warning-timeout`][101], which is an alias of `--keepalive-timeout` for backward compatibility.

**IMPROVEMENTS:**

- ([Commercial feature][105]) The entity limit warning message is now displayed less aggressively and the warning threshold is proportional to the entity limit.
- A new switcher in the [web UI][103] makes it easier to switch namespaces in the dashboard.
Access the new component from the drawer or with the shortcut ctrl+k.
For users who have many namespaces, the switcher now includes fuzzy search and improved keyboard navigation.
- In the [web UI][103], replaced the app bar with an omnipresent drawer to increase the available space for content. Each page also now includes breadcrumbs.
- In the [Sensu documentation][104], links now point to the version of the product being run instead of the latest, which may be helpful when running an older version of Sensu.

**FIXES:**

- `sensuctl dump` help now shows the correct default value for the format flag.
- Installing sensuctl commands via Bonsai will now check for correct labels before checking if the asset has 1 or more builds.
- Listing assets with no results now returns an empty array.
- Fixed a panic that could occur when creating resources in a namespace that does not exist.
- Fixed an issue where keepalive events and events created through the agent's socket interface could be missing a namespace.
- Fixed an issue that could cause 'sensuctl cluster health' to hang indefinitely.
- ([Commercial feature][105]) The `agent.yml.example` file shipped with Sensu Agent for Windows packages now uses DOS-style line endings.

## 5.15.0 release notes

**November 19, 2019** &mdash; The latest release of Sensu Go, version 5.15.0, is now available for download.
This is a significant release for a number of reasons.
The changes to licensing make 100% of Sensu Go's commercial features available for free to all users, up to your first 100 entities!
This release also includes the long-awaited cluster federation features, supporting multi-cluster authentication, RBAC policy replication, and a single pane of glass for your Sensu monitoring data!
We added support for API keys, making it easy to integrate with the Sensu API (you no longer need to manage JWTs).
In addition, the 5.15.0 release includes support for sensu-backend environment variables and bug fixes that improve error logging for mutator execution and flap detection weighting for checks.

See the [upgrade guide][1] to upgrade Sensu to version 5.15.0.

**IMPORTANT:**
Sensu's free entity limit is now 100 entities.
All [commercial features][95] are available for free in the packaged Sensu Go distribution up to an entity limit of 100.
You will see a warning when you approach the 100-entity limit (at 75%).

If your Sensu instance includes more than 100 entities, [contact us][90] to learn how to upgrade your installation and increase your limit.
See [the blog announcement][91] for more information about our usage policy.

**NEW FEATURES:**

- ([Commercial feature][95]) Added support for [federation replicators and the federation cluster registration API][85] and the ability to view resources across clusters in the federation in the [web UI][80].
- ([Commercial feature][95]) Added MSI and NuGet builds for [sensuctl][89]. Also, MSI and NuGet installations now add the bin directory to the system PATH on Windows.
- ([Commercial feature][95]) Added HTTP DELETE access for the [license management API][92].
- Added the [APIKey resource][86], with HTTP API support for POST, GET, and DELETE and [sensuctl commands][87] to manage the APIKey resource.
- Added support for using [API keys for API authentication][88].
- Added support for [sensuctl commands][93] to install, execute, list, and delete commands from Bonsai or a URL.
- Added support for sensu-backend service environment variables.
- Added support for [timezones in check `cron` strings][94].

**SECURITY:**

- ([Commercial feature][95]) Removed support for UPN binding without a binding account or anonymous binding, which allows Sensu to effectively refresh claims during access token renewal.

**IMPROVEMENTS:**

- You can now use colons and periods in all resource names (except users).

**FIXES:**

- Added better error logging for mutator execution.
- Fixed the order of flap detection weighting for checks.
- Fixed the pprof server so it only binds to localhost.
- Moved `corev2.BonsaiAsset` to `bonsai.Asset` and moved `corev2.OutdatedBonsaiAsset` to `bonsai.OutdatedAsset`.

## 5.14.2 release notes

**November 4, 2019** &mdash; The latest release of Sensu Go, version 5.14.2, is now available for download.
This release includes an etcd upgrade, fixes that improve stability and performance, and a Sensu Go package for CentOS 8.

See the [upgrade guide][1] to upgrade Sensu to version 5.14.2.

**IMPROVEMENTS:**

- Upgraded etcd to 3.3.17.
- Added build package for CentOS 8 (`el/8`).
- Sensu Go now uses serializable event reads, which helps improve performance.

**FIXES:**

- As a result of upgrading etcd, TLS etcd clients that lose their connection will successfully reconnect when using `--no-embed-etcd`.
- Check TTL and keepalive switches are now correctly buried when associated events and entities are deleted.
As a result, Sensu now uses far fewer leases for check TTLs and keepalives, which improves stability for most deployments.
- Corrected a minor UX issue in interactive filter commands in sensuctl.

## 5.14.1 release notes

**October 16, 2019** &mdash; The latest release of Sensu Go, version 5.14.1, is now available for download.
This release adds Prometheus gauges for check schedulers and fixes several bugs, including a bug discovered in 5.14.0 that prevented OIDC authentication providers from properly loading on start-up.

See the [upgrade guide][1] to upgrade Sensu to version 5.14.1.

**NEW FEATURES:**

- Added Prometheus gauges for check schedulers.

**FIXES:**

- ([Commercial feature][79]) Sensuctl will not incorrectly warn of entity limits for unlimited licenses.
- ([Commercial feature][79]) `oidc` authentication providers will now properly load on start-up.
- When opening a Bolt database that is already open, `sensu-agent` will not hang indefinitely.
- Running [`sensuctl dump`][84] for multiple resource types with the output format as YAML will not result in separators being printed to `STDOUT` instead of the specified file.
- Fixed a crash in sensu-backend (panic: send on closed channel).

## 5.14.0 release notes

**October 8, 2019** &mdash; The latest release of Sensu Go, version 5.14.0, is now available for download.
This release includes feature additions like two new configuration options for backends using embedded etcd and a new SemVer field in entity resources.
In addition, this release includes enhanced TLS authentication support and bug fixes that restore check execution after a network error and enable round robin schedule recovery after quorum loss.

See the [upgrade guide][1] to upgrade Sensu to version 5.14.0.

**NEW FEATURES:**

- The [web UI][80] now includes an error dialog option that allows users to wipe the application's persisted state (rather than having to manually wipe their local/session storage).
This can help in the rare case that something in the persisted state is leading to an uncaught exception.
- The [web UI][80] now respects the system preference for operating systems with support for selecting a preferred light or dark theme.
- `sensuctl dump` can now list the types of supported resources with `sensuctl dump --types`.
- The [entity resource][82] now includes the `sensu_agent_version` field, which reflects the Sensu Semantic Versioning (SemVer) version of the agent entity.
- There are two new [advanced configuration options][83] for `sensu-backend` using embedded etcd: `etcd-heartbeat-interval` and `etcd-election-timeout`.

**IMPROVEMENTS:**

- ([Commercial feature][79]) Added support for mutual TLS authentication between agents and backends.
- ([Commercial feature][79]) Added support for CRL URLs for mTLS authentication.
- ([Commercial feature][79]) Support agent [TLS authentication][81] is usable with the sensu-backend.
- In the web UI, feedback is directed to Discourse rather than the GitHub repository's Issues page to facilitate discussion about feature requests.
- In the [web UI][80], when a user lands on a page inside a namespace that no longer exists or they do not have access to, the drawer opens to that namespace switcher to help clarify next steps.
- Updated Go version from 1.12.3 to 1.13.1.

**FIXES:**

- ([Commercial feature][79]) `sensuctl` on Windows can now create Postgres resources.
- ([Commercial feature][79]) Fixed a bug that resulted in event metrics being ignored when using the Postgres store.
- Fixed a bug that caused checks to stop executing after a network error.
- Fixed a bug that prevented `sensuctl create` with `stdin` from working.
- Splayed proxy checks are executed every interval (instead of every interval + interval * splay_coverage).
- Proxy entity labels and annotations are now redacted in the web UI as expected.
- Fixed a bug in the ring that prevented round robin schedules from recovering after quorum loss.
- Updated [web UI][80] so that unauthorized errors emitted while creating silences or resolving events are caught and a notification is presented to communicate what occurred.
- [Web UI][80] does not report internal errors when a user attempts to queue an ad hoc check for a keepalive.
- Fixed a bug in the [web UI][80] that may have prevented users with appropriate roles from resolving events, queuing checks, and creating silenced entries.
- Asset builds are not separated into several assets unless the the tabular format is used in `sensuctl asset list`.
- The 'flag accessed but not defined' error is corrected in `sensuctl asset outdated`.

## 5.13.2 release notes

**September 19, 2019** &mdash; The latest release of Sensu Go, version 5.13.2, is now available for download.
This is a stability release that fixes a bug for users who have the PostgreSQL event store enabled.

See the [upgrade guide][1] to upgrade Sensu to version 5.13.2.

**FIXES:**

- Metrics handlers now correctly receive metric points when the postgresql event store is enabled.

## 5.13.1 release notes

**September 10, 2019** &mdash; The latest release of Sensu Go, version 5.13.1, is now available for download.
This is a stability release with bug fixes for multi-build asset definitions causing a panic when no matching filters are found.

See the [upgrade guide][1] to upgrade Sensu to version 5.13.1.

**FIXES:**

- Multi-build asset definitions with no matching filters will no longer cause a panic.
- Fixed the `oidc` authentication provider resource.

## 5.13.0 release notes

**September 9, 2019** &mdash; The latest release of Sensu Go, version 5.13.0, is now available for download.
This is one of the most user-friendly releases yet!
Sensuctl now integrates with Bonsai, the Sensu asset hub, making it easier than ever to fetch and use countless Sensu monitoring plugins and integrations.
Additionally, sensuctl now supports loading resource configuration files (e.g. checks) from directories and URLs.
But that's not all!
Sensuctl now provides a subcommand for exporting its configuration and API tokens to your shell environment.
Use sensuctl to provide cURL and custom scripts with fresh API access information!

See the [upgrade guide][1] to upgrade Sensu to version 5.13.0.

**NEW FEATURES:**

- Sensuctl now integrates with Bonsai, the Sensu asset hub.
Run a single sensuctl command to add an asset to your Sensu cluster (e.g. `sensuctl asset add sensu/sensu-pagerduty-handler:1.1.0`).
Check to see which assets are outdated (new releases available) with the `outdated` subcommand (e.g. `sensuctl asset outdated`).
- Sensuctl now supports the `env` subcommand for exporting sensuctl configuration and API tokens to your shell environment (e.g. `eval $(sensuctl env)`).
- Sensuctl now supports loading multiple resource configuration files (e.g. checks and handlers) from directories!
Sensuctl can also load a file using a URL (e.g. `sensuctl create -r -f ./checks` and `sensuctl create -f https://my.blog.ca/sensu-go/check.yaml`).

**FIXES:**

- Sensuctl interactive check create and update modes now have `none` for the metric output format as the first highlighted option instead of `nagios-perfdata`.
- Fixed a bug where silences would not expire on event resolution.

## 5.12.0 release notes

**August 26, 2019** &mdash; The latest release of Sensu Go, version 5.12.0, is now available for download.
There are some exciting feature additions in this release, including the ability to output resources to a file from sensuctl and more granular control of check and check hook execution with an agent allow list.
Additionally, this release includes the ability to delete assets and more stability fixes around watcher functionality.

See the [upgrade guide][1] to upgrade Sensu to version 5.12.0.

**IMPORTANT:**

Due to changes in the release process, Sensu binary-only archives are now named following the pattern `sensu-go_5.12.0_$OS_$ARCH.tar.gz`, where `$OS` is the operating system name and `$ARCH` is the CPU architecture.
These archives include all files in the top level directory.
See the [installation guide][16] for the latest download links.

**NEW FEATURES:**

- Operators can now authenticate to Sensu via OpenID Direct Connect (OIDC) using sensuctl.
See our [authentication documentation][17] for details.
- Added sensu-agent and sensuctl binary builds for FreeBSD.
- Added sensuctl dump command to output resources to a file or STDOUT, making it easier to back up your Sensu backends.
- Agents can now be configured with a list of executables that are allowed to run as check and hook commands.
See the [agent reference][78] for more information.

**IMPROVEMENTS:**

- Assets now support defining multiple builds, reducing the number of individual assets needed to cover disparate platforms in your infrastructure.
- ([Commercial feature][53]) Namespaces listed in both the web UI and sensuctl are now limited to the namespace to which the user has access.
- Hooks now support the use of assets.
- The event.check.name field has been added as a supported field selector.
- Both the API and sensuctl can now be used to delete assets.
- The use of ProtoBuf serialization/deserialization over WebSocket can now be negotiated between agent and backend.
- Web UI performance has been improved for deployments with many events and entities.
- The resource caches can now rebuild themselves in case of failures.
- Event and entity resources can now be created via the API without an explicit namespace.
The system will refer to the namespace in the request URL.
- Event and entity resources can now be created via the API using the POST verb.

**SECURITY:**

- To prevent writing sensitive data to logs, the backend no longer logs decoded check result and keepalive payloads.

**FIXES:**

- Tabular display of filters via sensuctl now displays `&&` or `||` as appropriate for inclusive and exclusive filters, respectively.
- Requesting events from the `GET /events/:entity` API endpoint now returns events only for the specified entity.
- Running sensuctl config view without configuration no longer causes a crash.
- Creating an entity via sensuctl with the `--interactive` flag now prompts for the entity name when it is not provided on the command line.
- Check hooks with `stdin: true` now receive actual event data on STDIN instead of an empty event.
- Some issues with check scheduling and updating have been fixed by refactoring the backend's watcher implementation.

**KNOWN ISSUES:**

- Authentication via OIDC is not yet supported in the web UI.
- Deleting an asset will not remove references to said asset.
It is the operator's responsibility to remove the asset from the runtime_assets field of the check, hook, filter, mutator, or handler.
- Deleting an asset will not remove the tarball or downloaded files from disk.
It is the operator's responsibility to clear the asset cache if necessary.

## 5.11.1 release notes

**July 18, 2019** &mdash; The latest release of Sensu Go, version 5.11.1, is now available for download.
This is a stability release with bug fixes for UPN format binding token renewal and addition of agent heartbeats and configurable WebSocket connection negotiation.

See the [upgrade guide][1] to upgrade Sensu to version 5.11.1.

**FIXES:**

- Fixed access token renewal when UPN format binding was enabled.
- The agent now sends heartbeats to the backend to detect network failures and reconnect more quickly.
- The default handshake timeout for the WebSocket connection negotiation was lowered from 45 to 15 seconds and is now configurable.

## 5.11.0 release notes

**July 10, 2019** &mdash; The latest release of Sensu Go, version 5.11.0, is now available for download.
There are some exciting feature additions in this release, including the ability to delete resources from sensuctl and manage filter and mutator resources in the web UI.
Additionally, this release includes bug fixes for proxy checks and enhanced performance tuning for the PostgreSQL event store.

See the [upgrade guide][1] to upgrade Sensu to version 5.11.0.

**NEW FEATURES:**

- The Sensu [web UI][67] now includes a filters page that displays available event filters and filter configuration.
- ([Commercial feature][68]) Manage your Sensu event filters from your browser: Sensu's [web UI][67] now supports creating, editing, and deleting filters.
- The Sensu [web UI][67] now includes a mutators page that displays available mutators and mutator configuration.
- ([Commercial feature][68]) Manage your Sensu mutators from your browser: Sensu's [web UI][67] now supports creating, editing, and deleting mutators.
- Sensuctl now includes the `sensuctl delete` command, letting you use resource definitions to delete resources from Sensu in the same way as `sensuctl create`.
See the [sensuctl reference][72] for more information.
- Assets now include a `headers` attribute to include HTTP headers in requests to retrieve assets, allowing you to access secured assets.
See the [asset reference][70] for examples.
- Sensu agents now support the `disable-assets` configuration flag, allowing you to disable asset retrieval for individual agents.
See the [agent reference][71] for examples.
- Sensu [binary-only distributions][69] are now available as zip files.

**IMPROVEMENTS:**

- ([Commercial feature][68]) The [Active Directory authentication provider][74] now supports the `default_upn_domain` attribute, letting you appended a domain to a username when a domain is not specified during login.
- ([Commercial feature][68]) The [Active Directory authentication provider][74] now supports the `include_nested_groups` attribute, letting you search nested groups instead of just the top-level groups of which a user is a member.
- The `sensuctl config view` command now returns the currently configured username.
See the [sensuctl reference][76] for examples.
- The [Sensu API][75] now returns the `201 Created` response code for POST and PUT requests instead of `204 No Content`.
- The Sensu backend now provides [advanced configuration options][77] for buffer size and worker count of keepalives, events, and pipelines.
- Sensu Go now supports Debian 10.
For a complete list of supported platforms, see the [platforms page][73].

**FIXES:**

- The web UI now returns an error when attempting to create a duplicate check or handler.
- Silenced entries are now retrieved from the cache when determining whether an event is silenced.
- The Sensu API now returns an error when trying to delete an entity that does not exist.
- The agent WebSocket connection now performs basic authorization.
- The events API now correctly applies the current timestamp by default, fixing a regression in 5.10.0.
- Multiple nested set handlers are now flagged correctly, fixing an issue in which they were flagged as deeply nested.
- Round robin proxy checks now execute as expected in the event of updated entities.
- The Sensu backend now avoids situations of high CPU usage in the event that watchers enter a tight loop.
- Due to incompatibility with the Go programming language, Sensu is incompatible with CentOS/RHEL 5.
As a result, CentOS/RHEL 5 has been removed as a [supported platform][73] for all versions of Sensu Go.

## 5.10.2 release notes

**June 27, 2019** &mdash; The latest release of Sensu Go, version 5.10.2, is now available for download.
This is a stability release with a bug fix for expired licenses.

See the [upgrade guide][1] to upgrade Sensu to version 5.10.2.

**FIXES:**

- Sensu now handles expired licenses as expected.

## 5.10.1 release notes

**June 25, 2019** &mdash; The latest release of Sensu Go, version 5.10.1, is now available for download.
This is a stability release with key bug fixes for proxy checks and entity deletion.

See the [upgrade guide][1] to upgrade Sensu to version 5.10.1.

**FIXES:**

- The proxy_requests entity_attributes are now all considered when matching entities.
- Events are now removed when their corresponding entity is deleted.

## 5.10.0 release notes

**June 19, 2019** &mdash; The latest release of Sensu Go, version 5.10.0, is now available for download.
There are some exciting feature additions in this release, including the ability to perform advanced filtering in the web UI and use PostgreSQL as a scalable event store.
This release also includes key bug fixes, most notably for high CPU usage.

See the [upgrade guide][1] to upgrade Sensu to version 5.10.0.

**NEW FEATURES:**

- ([Commercial feature][60]) The Sensu web UI now includes fast, predictive filtering for viewing checks, entities, events, handlers, and silences, including the ability to filter based on custom labels.
Select the filter bar and start building custom views using suggested attributes and values.
For more information, see the [web UI docs][66].
- Free Sensu instances can now delete entities in the web UI entities page.
See the [docs][65] to get started using the Sensu web UI.
- ([Commercial feature][60]) Sensu now supports using an external PostgreSQL instance for event storage in place of etcd.
PostgreSQL can handle significantly higher volumes of Sensu events, letting you scale Sensu beyond etcd's storage limits.
See the [datastore reference][61] for more information.
- Sensu now includes a cluster ID API endpoint and `sensuctl cluster id` command to return the unique Sensu cluster ID.
See the [cluster API docs][62] for more information.

**IMPROVEMENTS:**

- The `sensuctl create` command now supports specifying the namespace for a group of resources at the time of creation, allowing you to replicate resources across namespaces without manual editing.
See the [sensuctl reference][63] for more information and usage examples.
- Sensu cluster roles can now include permissions to manage your Sensu license using the `license` resource type.
See the [RBAC reference][64] to create a cluster role.
- The web UI now displays up to 100,000 events and entities on the homepage.

**FIXES:**

- Sensu now optimizes scheduling for proxy checks, solving an issue with high CPU usage when evaluating proxy entity attributes.
- The Sensu API now validates resource namespaces and types in request bodies to ensure RBAC permissions are enforced.
- Check `state` and `total_state_change` attributes now update as expected based on check history.
- Incident and entity links in the web UI homepage now navigate to the correct views.
- The web UI now displays non-standard cron statements correctly (e.g. `@weekly`).
- On sign-in, the web UI now ensures that users are directed to a valid namespace.
- In the web UI, code block scrollbars now display only when necessary.
- The web UI now displays the handler `timeout` attribute correctly.
- When editing resources, the web UI now fetches the latest resource prior to editing.
- The web UI now handles array values correctly when creating and editing resources.

## 5.9.0 release notes

**May 28, 2019** &mdash; The latest release of Sensu Go, version 5.9.0, is now available for download.
There are some exciting feature additions in this release, including the ability to log raw events to a file (commercial feature) and view event handlers in the web UI.

See the [upgrade guide][52] to upgrade Sensu to version 5.9.0.
If you're upgrading a Sensu cluster from 5.7.0 or earlier, see the [instructions for upgrading a Sensu cluster from 5.7.0 or earlier to 5.8.0 or later][59].

**NEW FEATURES:**

- The Sensu web UI now includes a handlers page that displays available event handlers and handler configuration.
See the [docs][54] to get started using the Sensu web UI.
- ([Commercial feature][53]) Manage your Sensu event handlers from your browser: Sensu's web UI now supports creating, editing, and deleting handlers.
See the [docs][54] to get started using the Sensu web UI.
- ([Commercial feature][53]) Sensu now supports event logging to a file using the `event-log-file` and `event-log-buffer-size` configuration flags.
You can use this event log file as an input source for your favorite data lake solution.
See the [backend reference][55] for more information.

**IMPROVEMENTS:**

- The Sensu web UI now includes simpler, more efficient filtering in place of filtering using Sensu query expressions.
- Sensu packages are now available for Ubuntu 19.04 (Disco Dingo). See the [supported platforms page][56] for a complete list of Sensu's supported platforms and the [installation guide][57] to install Sensu packages for Ubuntu.

**FIXES:**

- The `occurrences` and `occurrences_watermark` event attributes now increment as expected, giving you useful information about recent events.
See the [events reference][58] for an in-depth discussion of these attributes.
- The `/silenced/subscriptions/:subscription` and `/silenced/checks/:check` API endpoints now return silences by check or subscription.
- Sensu now handles errors when seeding initial data, avoiding a panic state.

## 5.8.0 release notes

**May 22, 2019** &mdash; The latest release of Sensu Go, version 5.8.0, is now available for download.
This is mainly a stability release with bug fixes and performance improvements.
Additionally, we have added support for configurable etcd cipher suites.

See the [upgrade guide][51] to upgrade Sensu to version 5.8.0.

**IMPORTANT:**

- To upgrade to Sensu Go 5.8.0, Sensu clusters with multiple backend nodes must be shut down during the upgrade process.
See the [upgrade guide][51] for more information.

**IMPROVEMENTS:**

- The sensuctl command line tool now supports the `--chunk-size` flag to help you handle large datasets.
See the [sensuctl reference][45] for more information.
- Sensu backends now support the `etcd-cipher-suites` configuration option, letting you specify the cipher suites that can be used with etcd TLS configuration.
See the [backend reference][47] for more information.
- The Sensu API now includes the version API, returning version information for your Sensu instance.
See the [API docs][46] for more information.
- Tessen now collects the numbers of events processed and resources created, giving us better insight into how we can improve Sensu.
As always, all Tessen transmissions are logged for complete transparency.
See the [Tessen reference][48] for more information.
- Sensu licenses now include the entity limit attached to your Sensu licensing package.
See the [license management docs][49] to learn more about entity limits.
- Sensu backends now perform better at scale using increased worker pool sizes for events and keepalives.
- The maximum size of the etcd database and etcd requests is now configurable using the `etcd-quota-backend-bytes` and `etcd-max-request-bytes` backend configuration options.
These are advanced configuration options requiring familiarly with etcd. 
Use with caution.
See the [backend reference][50] for more information.
- Most Sensu resources now use ProtoBuf serialization in etcd.

**FIXES:**

- Events produced by checks now execute the correct number of write operations to etcd.
- API pagination tokens for the users and namespaces APIs now work as expected.
- Keepalive events for deleted and deregistered entities are now cleaned up as expected.

**KNOWN ISSUES:**

- Auth tokens may not be purged from etcd, resulting in a possible impact to performance.

## 5.7.0 release notes

**May 9, 2019** &mdash; The latest release of Sensu Go, version 5.7.0, is now available for download.
This is mainly a stability release with bug fixes.
Additionally, we have added support for Windows packages and [updated our usage policy][44].

See the [upgrade guide][1] to upgrade Sensu to version 5.7.0.

**IMPROVEMENTS:**

- The Sensu agent for Windows is now available as an MSI package, making it easier to install and operate.
See the [installation guide][41] and the [agent reference][42] to get started.

**FIXES:**

- Sensu now enforces resource separation between namespaces sharing a similar prefix.
- The `sensuctl cluster` commands now output correctly in JSON and wrapped JSON formats.
- The API now returns an error message if [label and field selectors][43] are used without a license.

## 5.6.0 release notes

**April 30, 2019** &mdash; The latest release of Sensu Go, version 5.6.0, is now available for download.
We have added some exciting new features in this release, including API filtering and the ability to create and manage checks through the web UI with the presence of a valid license key.

See the [upgrade guide][1] to upgrade Sensu to version 5.6.0.

**NEW FEATURES:**

- ([Commercial feature][33]) Manage your Sensu checks from your browser: Sensu's web user interface now supports creating, editing, and deleting checks.
See the [docs][32] to get started using the Sensu web UI.
- ([Commercial feature][33]) The Sensu web UI now includes an option to delete entities.
- ([Commercial feature][33]) Sensu now supports resource filtering in the Sensu API and sensuctl command line tool.
Filter events using custom labels and resource attributes, such as event status and check subscriptions.
See the [API docs][34] and [sensuctl reference][35] for usage examples.

**IMPROVEMENTS:**

- ([Commercial feature][33]) Sensu's LDAP and Active Directory integrations now support mutual authentication using the `trusted_ca_file`, `client_cert_file`, and `client_key_file` attributes.
See the [guide to configuring an authentication provider][37] for more information.
- ([Commercial feature][33]) Sensu's LDAP and Active Directory integrations now support connecting to an authentication provider using anonymous binding.
See the [LDAP][38] and [Active Directory][39] binding configuration docs to learn more.
- The [health API][36] response now includes the cluster ID.
- The `sensuctl cluster health` and `sensuctl cluster member-list` commands now include the cluster ID in tabular format.

**FIXES:**

- You can now configure labels and annotations for Sensu agents using command line flags.
For example: `sensu-agent start --label example_key="example value"`.
See the [agent reference][40] for more examples.
- The Sensu web UI now displays the correct checkbox state when no resources are present.

## 5.5.1 release notes

**April 17, 2019** &mdash; The latest release of Sensu Go, version 5.5.1, is now available for download.
This is a stability release with key bug fixes, including addressing an issue with backend CPU utilization.
Additionally, we have added support for honoring the source attribute for events received via agent socket.

See the [upgrade guide][1] to upgrade Sensu to version 5.5.1.

**IMPROVEMENTS:**

- Sensu agents now support annotations (non-identifying metadata) that help people or external tools interacting with Sensu.
See the [agent reference][29] to add annotations in the agent configuration file.
- The [agent socket event format][30] now supports the `source` attribute to create a proxy entity.
- Sensu 5.5.1 is built with Go version 1.12.3.

**FIXES:**

- Backends now reinstate etcd watchers in the event of a watcher failure, fixing an issue causing high CPU usage in some components.

## 5.5.0 release notes

**April 4, 2019** &mdash; The latest release of Sensu Go, version 5.5.0, is now available for download.
This release has some key bug fixes and additions, including the introduction of Tessen into Sensu Go.
For more information, read Sean Porter’s [blog post][28] on Tessen.

See the [upgrade guide][1] to upgrade Sensu to version 5.5.0.

**NEW FEATURES:**

- Tessen, the Sensu call-home service, is now enabled by default in Sensu backends.
See the [Tessen docs][27] to learn about the data that Tessen collects.

**IMPROVEMENTS:**

- Sensu now includes more verbose check logging to indicate when a proxy request matches an entity according to its entity attributes.

**FIXES:**

- The Sensu web UI now displays silences created by LDAP users.
- The web UI now uses a secondary text color for quick-navigation buttons.

## 5.4.0 release notes

**March 27, 2019** &mdash; The latest release of Sensu Go, version 5.4.0, is now available for download.
This release has some very exciting feature additions, including the introduction of our new homepage.
It also includes support for API pagination to handle large datasets more efficiently and agent buffering for robustness in lower-connectivity situations, along with key bug fixes.

See the [upgrade guide][1] to upgrade Sensu to version 5.4.0.

**NEW FEATURES:**

- The Sensu dashboard now includes a homepage designed to highlight the most important monitoring data, giving you instant insight into the state of your infrastructure.
See the [web UI docs][23] for a preview.
- The Sensu API now supports pagination using the `limit` and `continue` query parameters, letting you limit your API responses to a maximum number of objects and making it easier to handle large datasets.
See the [API overview][22] for more information.
- Sensu now surfaces internal metrics using the metrics API.
See the [metrics API reference][31] for more information.

**IMPROVEMENTS:**

- Sensu now lets you specify a separate TLS certificate and key to secure the dashboard.
See the [backend reference][24] to configure the `dashboard-cert-file` and `dashboard-key-file` flags, and check out the [guide to securing Sensu][25] for the complete guide to making your Sensu instance production-ready.
- The Sensu agent events API now queues events before sending them to the backend, making the agent events API more robust and preventing data loss in the event of a loss of connection with the backend or agent shutdown.
See the [agent reference][26] for more information.

**FIXES:**

- The backend now processes events without persisting metrics to etcd.
- The events API POST and PUT endpoints now add the current timestamp to new events by default.
- The users API now returns a 404 response code if a username cannot be found.
- The sensuctl command line tool now correctly accepts global flags when passed after a subcommand flag (e.g. `--format yaml --namespace development`).
- The `sensuctl handler delete` and `sensuctl filter delete` commands now correctly delete resources from the currently configured namespace.
- The agent now terminates consistently on SIGTERM and SIGINT.
- In the event of a loss of connection with the backend, the agent now attempts to reconnect to any backends specified in its configuration.
- The dashboard now handles cases in which the creator of a silence is inaccessible.
- The dashboard event details page now displays "-" in the command field if no command is associated with the event.

## 5.3.0 release notes

**March 11, 2019** &mdash; The latest release of Sensu Go, version 5.3.0, is now available for download.
This release has some very exciting feature additions and key bug fixes.
Active Directory can be configured as an authentication provider (commercial feature).
Additionally, round robin scheduling has been fully re-implemented and is available for use.

See the [upgrade guide][1] to upgrade Sensu to version 5.3.0.

**NEW FEATURES:**

- Round robin check scheduling lets you distribute check executions evenly over a group of Sensu agents.
To enable round robin scheduling, set the `round_robin` check attribute to `true`.
See the [check reference][18] for more information.
- Sensu now provides [commercial][19] support for using Microsoft Active Directory as an external authentication provider.
Read the [authentication guide][20] to configure Active Directory, and check out the [getting started guide][19] for more information about commercial features.
- The dashboard now features offline state detection and displays an alert banner if the dashboard loses connection to the backend.

**IMPROVEMENTS:**

- The agent socket event format now supports the `handlers` attribute, giving you the ability to send socket events to a Sensu pipeline.
See the [agent reference][21] to learn more about creating and handling monitoring events using the agent socket.
- Assets now feature improved download performance using buffered I/O.
- The sensuctl CLI now uses a 15-second timeout period when connecting to the Sensu backend.
- The dashboard now includes expandable configuration details sections on the check and entity pages.
You can now use the dashboard to review check details like command, subscriptions, and scheduling as well as entity details like platform, IP address, and hostname.

**SECURITY:**

- Sensu Go 5.3.0 fixes all known TLS vulnerabilities affecting the backend, including increasing the minimum supported TLS version to 1.2 and removing all ciphers except those with perfect forward secrecy.
- Sensu now enforces uniform TLS configuration for all three backend components: `apid`, `agentd`, and `dashboardd`.
- The backend no longer requires the `trusted-ca-file` flag when using TLS.
- The backend no longer loads server TLS configuration for the HTTP client.

**FIXES:**

- Sensu can now download assets with download times of more than 30 seconds without timing out.
- The agent now communicates entity subscriptions to the backend in the correct format.
- Sensu no longer includes the `edition` configuration attribute or header.
- DNS resolution in Alpine Linux containers now uses the built-in Go resolver instead of the glibc resolver.
- The `sensuctl user list` command can now output `yaml` and `wrapped-json` formats when used with the `--format` flag.
- The dashboard check details page now displays long commands correctly.
- The dashboard check details page now displays the `timeout` attribute correctly.

## 5.2.1 release notes

**February 11, 2019** &mdash; The latest release of Sensu Go, version 5.2.1, is now available for download.
This is a stability release with a key bug fix for proxy check functionality.

See the [upgrade guide][1] to upgrade Sensu to version 5.2.1.

**FIXES:**

- Sensu agents now execute checks for proxy entities at the expected interval.

## 5.2.0 release notes

**February 7, 2019** &mdash; The latest release of Sensu Go, version 5.2.0, is now available for download.
This release has a ton of exciting content, including the availability of our first enterprise-only features.
For more details on these features, see our [blog post][14].
Release 5.2.0 also has some key improvements and fixes: we added support for self-signed CA certificates for sensuctl, check output truncation, and the ability to manage silencing from the event details page in our web UI, to name a few.

See the [upgrade guide][1] to upgrade Sensu to version 5.2.0.

**IMPORTANT:**

- Due to changes in the release process, Sensu binary-only archives are now named following the pattern `sensu-enterprise-go_5.2.0_$OS_$ARCH.tar.gz`, where `$OS` is the operating system name and `$ARCH` is the CPU architecture.
These archives include all files in the top-level directory.
See the [installation guide][16] for the latest download links.

**NEW FEATURES:**

- Our first enterprise-only features for Sensu Go: [LDAP authentication][96], the [Sensu ServiceNow handler][97], and the [Sensu JIRA handler][98].
See the [getting started guide][99].
- Sensu now provides the option to limit check output size or to drop check outputs following metric extraction.
See the [checks reference][15] for more information.

**IMPROVEMENTS:**

- Sensu now includes support for Debian 8 and 9.
See the [installation guide][16] to install Sensu for Debian.
- Sensu's binary-only distribution for Linux is now available for `arm64`, `armv5`, `armv6`, `armv7`, and `386` in addition to `amd64`.
See the [installation guide][16] for download links.
- The Sensu dashboard now provides the ability to silence and unsilence events from the Events page.
- The Sensu dashboard Entity page now displays the platform version and deregistration configuration.
- Sensuctl now supports TLS configuration options, allowing you to use a self-signed certificate without adding it to the operating system's CA store, either by explicitly trusting the signer or by disabling TLS hostname verification.
See the [sensuctl reference][17] for more information.
- sensuctl now provides action-specific confirmation messages, like `Created`, `Deleted`, and `Updated`.

**FIXES:**

- Check TTL failure events now persist through cluster member failures and cluster restarts.
- The Sensu backend now correctly handles errors for missing keepalive events.
- Token-substituted values are now omitted from event data to protect sensitive information.
- Sensu now correctly processes keepalive and check TTL states after entity deletion.
- Sensuctl can now run `sensuctl version` without being configured.
- When disabling users, sensuctl now provides the correct prompt for the action.

## 5.1.1 release notes

**January 24, 2019** &mdash; The latest patch release of Sensu Go, version 5.1.1, is now available for download.
This release includes some key fixes and improvements, including refactored keepalive functionality with increased reliability.
Additionally, based on community feedback, we have added support for the Sensu agent and sensuctl for 32-bit Windows systems.

See the [upgrade guide][1] to upgrade Sensu to version 5.1.1.

**NEW FEATURES:**

- Sensu now includes a sensuctl command and API endpoint to test user credentials.
See the [access control reference][10] and [API docs][11] for more information.

**IMPROVEMENTS:**

- The Sensu agent and sensuctl tool are now available for 32-bit Windows.
See the [installation guide][12] for instructions.
- Keepalive events now include an output attribute specifying the entity name and time last sent.
- The Sensu backend includes refactored authentication and licensing to support future enterprise features.

**SECURITY:**

- Sensu 5.1.1 is built with Go version 1.11.5.
Go 1.11.5 addresses a security vulnerability that affects TLS handshakes and JWT tokens.
See the [CVE][13] for more information.

**FIXES:**

- Keepalive events now continue to execute after a Sensu cluster restarts.
- When requested, on-demand check executions now correctly retrieve asset dependencies.
- Checks now maintain a consistent execution schedule after updates to the check definition.
- Proxy check request errors now include the check name and namespace.
- When encountering an invalid line during metric extraction, Sensu now logs an error and continues extraction.
- Sensuctl now returns an error when attempting to delete a non-existent entity.
- Sensuctl now removes the temporary file it creates when executing the `sensuctl edit` command.
- The Sensu dashboard now recovers from errors correctly when shutting down.
- The Sensu dashboard includes better visibility for buttons and menus in the dark theme.

## 5.1.0 release notes

**December 19, 2018** &mdash; The latest release of Sensu Go, version 5.1.0, is now available for download.
This release includes an important change to the Sensu backend state directory as well as support for Ubuntu 14.04 and some key bug fixes.

See the [upgrade guide][1] to upgrade Sensu to version 5.1.0.

**IMPORTANT:**

{{% notice note %}}
**NOTE**: This applies only to Sensu backend binaries downloaded from `s3-us-west-2.amazonaws.com/sensu.io/sensu-go`, not to Sensu RPM or DEB packages.
{{% /notice %}}

- For Sensu backend binaries, the default `state-dir` is now `/var/lib/sensu/sensu-backend` instead of `/var/lib/sensu`.
To upgrade your Sensu backend binary to 5.1.0, make sure your `/etc/sensu/backend.yml` configuration file specifies a `state-dir`.
See the [upgrade guide][3] for more information.

**NEW FEATURES:**

- Sensu [agents][4] now include `trusted-ca-file` and `insecure-skip-tls-verify` configuration flags, giving you more flexibility with certificates when connecting agents to the backend over TLS.

**IMPROVEMENTS:**

- Sensu now includes support for Ubuntu 14.04.

**FIXES:**

- The Sensu backend now successfully connects to an external etcd cluster.
- SysVinit scripts for the Sensu agent and backend now include correct run and log paths.
- Once created, keepalive alerts and check TTL failure events now continue to occur until a successful event is observed.
- When querying for an empty list of assets, sensuctl and the Sensu API now return an empty array instead of null.
- The sensuctl `create` command now successfully creates hooks when provided with the correct definition.
- The Sensu dashboard now renders status icons correctly in Firefox.

## 5.0.1 release notes

**December 12, 2018** &mdash; Sensu Go 5.0.1 includes our top bug fixes following last week's general availability release.

See the [upgrade guide][1] to upgrade Sensu to version 5.0.1.

**FIXED:**

- The Sensu backend can now successfully connect to an external etcd cluster.
- The Sensu dashboard now sorts silences in ascending order, correctly displays status values, and reduces shuffling in the event list.
- Sensu agents on Windows now execute command arguments correctly.
- Sensu agents now correctly include environment variables when executing checks.
- Command arguments are no longer escaped on Windows.
- Sensu backend environments now include handler and mutator execution requests.

## 5.0.0 release notes

**December 5, 2018** &mdash; We're excited to announce the general availability release of Sensu Go!
Sensu Go is the flexible monitoring event pipeline written in Go and designed for container-based and hybrid-cloud infrastructures.
Check out the [Sensu blog][6] for more information about Sensu Go and version 5.0.

For a complete list of changes from Beta 8-1, see the [Sensu Go changelog][5].
This page will be the official home for the Sensu Go changelog and release notes.

To get started with Sensu Go:

- [Download the sandbox][7].
- [Install Sensu Go][8].
- [Get started monitoring server resources][9].

[1]: /sensu-go/latest/operations/maintain-sensu/upgrade/
[2]: https://semver.org/spec/v2.0.0.html
[3]: /sensu-go/5.1/installation/upgrade#upgrading-sensu-backend-binaries-to-5-1-0
[4]: /sensu-go/5.1/reference/agent/
[5]: https://www.github.com/sensu/sensu-go/blob/master/CHANGELOG.md#500---2018-11-30
[6]: https://blog.sensu.io/sensu-go-is-here/
[7]: https://www.github.com/sensu/sandbox/tree/master/sensu-go/core/
[8]: /sensu-go/5.0/installation/install-sensu/
[9]: /sensu-go/5.0/guides/monitor-server-resources/
[10]: /sensu-go/5.1/reference/rbac#managing-users
[11]: /sensu-go/5.1/api/auth/
[12]: /sensu-go/5.1/installation/install-sensu/
[13]: https://nvd.nist.gov/vuln/detail/CVE-2019-6486/
[14]: https://blog.sensu.io/enterprise-features-in-sensu-go/
[15]: https://docs.sensu.io/sensu-go/5.2/reference/checks/#check-output-truncation-attributes
[16]: /sensu-go/5.2/installation/install-sensu/
[17]: /sensu-go/5.2/sensuctl/reference/#global-flags
[18]: /sensu-go/5.3/reference/checks#spec-attributes
[19]: /sensu-go/5.3/getting-started/enterprise/
[20]: /sensu-go/5.3/installation/auth/
[21]: /sensu-go/5.3/reference/agent#creating-monitoring-events-using-the-agent-tcp-and-udp-sockets
[22]: /sensu-go/5.4/api/overview#pagination
[23]: /sensu-go/5.4/dashboard/overview/
[24]: /sensu-go/5.4/reference/backend#dashboard-configuration-flags
[25]: /sensu-go/5.4/guides/securing-sensu/
[26]: /sensu-go/5.4/reference/agent#events-post
[27]: /sensu-go/5.5/reference/tessen/
[28]: https://blog.sensu.io/announcing-tessen-the-sensu-call-home-service/
[29]: /sensu-go/5.5/reference/agent#general-configuration-flags
[30]: /sensu-go/5.5/reference/agent#creating-monitoring-events-using-the-agent-tcp-and-udp-sockets
[31]: /sensu-go/5.4/api/metrics/
[32]: /sensu-go/5.6/dashboard/overview/
[33]: /sensu-go/5.6/getting-started/enterprise/
[34]: /sensu-go/5.6/api/overview#filtering
[35]: /sensu-go/5.6/sensuctl/reference#filtering
[36]: /sensu-go/5.6/api/health/
[37]: /sensu-go/5.6/installation/auth/
[38]: /sensu-go/5.6/installation/auth/#binding-attributes
[39]: /sensu-go/5.6/installation/auth/#active-directory-binding-attributes
[40]: /sensu-go/5.6/reference/agent#general-configuration-flags
[41]: /sensu-go/5.7/installation/install-sensu#windows-agent
[42]: /sensu-go/5.7/reference/agent#operation
[43]: /sensu-go/5.7/api/overview#filtering
[44]: https://discourse.sensu.io/t/introducing-usage-limits-in-the-sensu-go-free-tier/1156/
[45]: /sensu-go/5.8/sensuctl/reference#handling-large-datasets
[46]: /sensu-go/5.8/api/version/
[47]: /sensu-go/5.8/reference/backend#etcd-cipher-suites
[48]: /sensu-go/5.8/reference/tessen/
[49]: /sensu-go/5.8/reference/license/
[50]: /sensu-go/5.8/reference/backend#advanced-configuration-options
[51]: /sensu-go/5.8/installation/upgrade#upgrading-sensu-clusters-from-5-7-0-or-earlier-to-5-8-0-or-later
[52]: /sensu-go/5.9/installation/upgrade/
[53]: /sensu-go/5.9/getting-started/enterprise/
[54]: /sensu-go/5.9/dashboard/overview/
[55]: /sensu-go/5.9/reference/backend#event-logging
[56]: /sensu-go/5.9/installation/platforms/
[57]: /sensu-go/5.9/installation/install-sensu/
[58]: /sensu-go/5.9/reference/events#occurrences-and-occurrences-watermark
[59]: /sensu-go/5.9/installation/upgrade/#upgrading-sensu-clusters-from-5-7-0-or-earlier-to-5-8-0-or-later
[60]: /sensu-go/latest/getting-started/enterprise/
[61]: /sensu-go/5.10/reference/datastore/
[62]: /sensu-go/5.10/api/cluster#the-clusterid-API-endpoint
[63]: /sensu-go/5.10/sensuctl/reference#creating-resources-across-namespaces
[64]: /sensu-go/5.10/reference/rbac/#assigning-group-permissions-across-all-namespaces
[65]: /sensu-go/5.10/dashboard/overview/
[66]: /sensu-go/5.10/dashboard/filtering/
[67]: /sensu-go/5.11/dashboard/overview/
[68]: /sensu-go/5.11/getting-started/enterprise/
[69]: /sensu-go/5.11/installation/verify/
[70]: /sensu-go/5.11/reference/assets#examples
[71]: /sensu-go/5.11/reference/agent#disable-assets
[72]: /sensu-go/5.11/sensuctl/reference#deleting-resources
[73]: /sensu-go/5.11/installation/platforms/
[74]: /sensu-go/5.11/installation/auth#active-directory-authentication
[75]: /sensu-go/5.11/api/overview/
[76]: /sensu-go/5.11/sensuctl/reference#view-sensuctl-config
[77]: /sensu-go/5.11/reference/backend#advanced-configuration-options
[78]: /sensu-go/5.12/reference/agent/#allow-list
[79]: /sensu-go/5.14/getting-started/enterprise/
[80]: /sensu-go/5.14/dashboard/overview/
[81]: /sensu-go/5.14/guides/securing-sensu#sensu-agent-tls-authentication
[82]: /sensu-go/5.13/reference/entities/
[83]: /sensu-go/5.14/reference/backend/#advanced-configuration-options
[84]: /sensu-go/5.14/sensuctl/reference/#exporting-resources
[85]: /sensu-go/5.15/api/federation/
[86]: /sensu-go/5.15/reference/apikeys/
[87]: /sensu-go/5.15/guides/use-apikey-feature/#sensuctl-management-commands
[88]: /sensu-go/5.15/api/overview/#authenticate-with-the-api-key-feature
[89]: /sensu-go/5.15/sensuctl/reference/
[90]: https://sensu.io/contact/
[91]: https://blog.sensu.io/one-year-of-sensu-go/
[92]: /sensu-go/5.15/api/license/
[93]: /sensu-go/5.15/sensuctl/sensuctl-bonsai#extend-sensuctl-with-commands
[94]: /sensu-go/5.15/reference/checks/#cron-scheduling
[95]: /sensu-go/5.15/getting-started/enterprise/
[96]: /sensu-go/5.2/installation/auth/
[97]: https://bonsai.sensu.io/assets/sensu/sensu-servicenow-handler/
[98]: https://bonsai.sensu.io/assets/sensu/sensu-jira-handler/
[99]: /sensu-go/5.2/getting-started/enterprise/
[100]: /sensu-go/5.16/reference/backend/#datastore-and-cluster-configuration-flags
[101]: /sensu-go/5.16/reference/agent/#keepalive-configuration-flags
[102]: /sensu-go/5.16/reference/backend/#initialization
[103]: /sensu-go/5.16/dashboard/overview
[104]: /sensu-go/5.16/
[105]: /sensu-go/5.16/getting-started/enterprise/
[106]: /sensu-go/5.17/commercial/
[107]: /sensu-go/5.17/web-ui/sign-in
[108]: /sensu-go/5.17/api/secrets
[109]: /sensu-go/5.17/reference/backend/#docker-initialization
[110]: /sensu-go/5.17/api/overview/#field-selector
[111]: /sensu-go/5.17/reference/rbac/#cluster-wide-resource-types
[112]: /sensu-go/5.17/api/events/#events-post
[113]: /sensu-go/5.17/sensuctl/reference/#list-commands
[114]: /sensu-go/5.18/api/events#create-a-new-event
[115]: /sensu-go/5.18/commercial/
[116]: /sensu-go/5.18/api#label-selector
[117]: /sensu-go/5.18/api#field-selector
[118]: /sensu-go/5.18/api/events/
[119]: /sensu-go/5.18/api#response-filtering
[120]: /sensu-go/5.18/api/auth#authtest-get
[122]: /sensu-go/5.19/commercial/
[123]: /sensu-go/5.19/web-ui/filter/#save-a-filtered-search
[124]: /sensu-go/5.19/web-ui/
[125]: /sensu-go/5.19/reference/health/
[126]: /sensu-go/5.19/api#response-filtering
[127]: /sensu-go/5.19/sensuctl/filter-responses
[128]: /sensu-go/5.19/web-ui/filter/
[129]: /sensu-go/5.19/sensuctl/create-manage-resources#sensuctl-prune
[130]: /sensu-go/5.19/reference/tessen/
[131]: /sensu-go/5.19/reference/handlers/#pipe-handler-command
[133]: /sensu-go/5.19/platforms/
[134]: /sensu-go/5.19/operations/deploy-sensu/install-sensu/
[135]: /sensu-go/5.19/web-ui/
[136]: /sensu-go/5.19/reference/agent/#configuration-via-flags
[137]: /sensu-go/5.19/reference/backend/#configuration
[138]: /sensu-go/5.20/api#field-selector
[139]: /sensu-go/5.20/reference/backend/#log-rotation
[140]: /sensu-go/5.20/operations/maintain-sensu/troubleshoot/#increment-log-level-verbosity
[141]: /sensu-go/5.20/commercial/
[142]: /sensu-go/5.20/reference/agent/#configuration-via-flags
[143]: /sensu-go/5.20/reference/entities/#processes-attributes
[144]: /sensu-go/5.20/sensuctl/create-manage-resources/#sensuctl-describe-type-resource-types
[145]: /sensu-go/5.20/reference/backend/#configuration-summary
[146]: /sensu-go/5.20/reference/tokens/#manage-assets
[147]: /sensu-go/5.20/reference/tokens/#token-substitution-with-quoted-strings
[148]: /sensu-go/5.20/reference/webconfig/
[149]: /sensu-go/5.20/api/license#get-the-active-license-configuration
[150]: /sensu-go/5.20/reference/license/#view-entity-count-and-entity-limit
[151]: /sensu-go/5.20/reference/license/#entity-limit
[152]: /sensu-go/5.20/web-ui/#federated-webui
[153]: /sensu-go/5.20/web-ui/
[154]: /sensu-go/5.20/sensuctl/sensuctl-bonsai/#extend-sensuctl-with-commands
[155]: /sensu-go/5.20/reference/agent/#discover-processes
[156]: /sensu-go/5.21/reference/license/#view-entity-count-and-entity-limit
[157]: /sensu-go/5.21/reference/agent/#log-level
[158]: /sensu-go/5.21/commercial/
[160]: /sensu-go/5.21/reference/backend#fips-openssl
[161]: /sensu-go/5.21/reference/agent#fips-openssl
