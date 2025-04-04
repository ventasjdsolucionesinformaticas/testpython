#!/bin/bash

# Configuración
USER="jdiaz@latinia.com"
TOKEN="5JuJowZyyiaNR6MvtBjV2cJuNwysyI-eu"
AUTH=$(echo -n "$USER:$TOKEN" | base64)  # Generar autenticación en Base64
BASE_URL="https://latinia.atlassian.net/rest/api/3/issue"

# Lista de issues a consultar
ISSUES=("LATSUP-4951" "LATSUP-4817" "LATSUP-4831")

# Recorre cada issue y extrae su issueId
for issue in "${ISSUES[@]}"; do
  echo "Consultando $issue..."
  
  response=$(curl -s -X GET "$BASE_URL/$issue" \
       -H "Authorization: Basic $AUTH" \
       -H "Accept: application/json")

  issue_id=$(echo "$response" | jq -r '.id')

  if [[ "$issue_id" != "null" ]]; then
    echo "Issue: $issue → ID: $issue_id"
  else
    echo "⚠️ No se encontró issueId para $issue"
  fi
done