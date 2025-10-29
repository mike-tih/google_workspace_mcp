#!/bin/bash
# deploy.sh


gcloud run deploy workspace-mcp \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-secrets GOOGLE_OAUTH_CLIENT_ID=GOOGLE_OAUTH_CLIENT_ID:latest \
  --set-secrets GOOGLE_OAUTH_CLIENT_SECRET=GOOGLE_OAUTH_CLIENT_SECRET:latest \
  --set-env-vars WORKSPACE_MCP_STATELESS_MODE=true \
  --set-env-vars MCP_ENABLE_OAUTH21=true \
  --set-env-vars EXTERNAL_OAUTH21_PROVIDER=true \
  --set-env-vars WORKSPACE_EXTERNAL_URL=https://workspace-mcp-288536791057.europe-west1.run.app \
  --memory 1Gi \
  --timeout 300 \