#!/bin/bash
# deploy.sh


gcloud run deploy workspace-mcp \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-secrets GOOGLE_OAUTH_CLIENT_ID=GOOGLE_OAUTH_CLIENT_ID:latest \
  --set-secrets GOOGLE_OAUTH_CLIENT_SECRET=GOOGLE_OAUTH_CLIENT_SECRET:latest \
  --set-env-vars MCP_ENABLE_OAUTH21=true \
  --set-env-vars WORKSPACE_MCP_STATELESS_MODE=true \
  --memory 1Gi \
  --timeout 300