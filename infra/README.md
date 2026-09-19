# Deferred infrastructure

No services are configured or needed for bootstrap. Activate PostgreSQL or Qdrant only when a selected experiment needs them. n8n may later use an optional profile. Select versions deliberately, bind ports to localhost, use named persistent volumes and validated health checks, and document local-only credentials and backup/reset behavior.

Future commands, usable only after infra/compose.yaml exists and is validated:

```bash
docker compose -f infra/compose.yaml config
docker compose -f infra/compose.yaml up -d
docker compose -f infra/compose.yaml down
# Only if an automation profile is implemented:
docker compose -f infra/compose.yaml --profile automation up -d
```

`down` should preserve named volumes; destructive volume deletion requires explicit approval. No GPU containers, model downloads, Kubernetes or full self-hosted Langfuse stack are planned for bootstrap.
