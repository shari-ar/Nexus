---
title: Nexus Technical Documentation
nav_order: 1
---

# Nexus Technical Documentation

Nexus is a local-first, self-hosted, hierarchical multi-agent AI platform. It coordinates specialized agents, tools, workflows, and local models to complete complex tasks from a single user request while keeping data and execution under local ownership.

## Start Here

- [Architecture Overview]({{ site.baseurl }}/docs/architecture/overview/) explains system boundaries, components, control flow, and design rules.
- [Agent System]({{ site.baseurl }}/docs/agents/overview/) describes supervisor responsibilities, specialized agents, delegation rules, and configuration expectations.
- [Workflow System]({{ site.baseurl }}/docs/workflows/overview/) explains how Nexus routes tasks through configuration-driven workflows.
- [Deployment Guide]({{ site.baseurl }}/docs/deployment/overview/) defines the Docker-native deployment model and environment layout.
- [Operations Guide]({{ site.baseurl }}/docs/operations/overview/) covers observability, artifacts, backups, validation, and maintenance.

## Core Principles

1. Local-first infrastructure and data ownership.
2. Strict separation between orchestration and execution.
3. YAML-driven agent, model, permission, and workflow configuration.
4. Adapter-isolated integrations for external subsystems.
5. Docker-native services that can later move to distributed infrastructure.
6. Generated user artifacts separated from system files.
7. Minimal custom code when mature open-source tools already exist.
