#!/bin/bash
# Integration test script
# Tests the full job flow end to end
# Usage: ./integration_test.sh

set -e

echo "Starting integration test..."

# Submit a job through the frontend
echo "Submitting job..."
RESPONSE=$(curl -s -X POST http://localhost:3000/submit)
echo "Response: $RESPONSE"

# Extract job_id
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('job_id',''))" 2>/dev/null)

if [ -z "$JOB_ID" ]; then
  echo "ERROR: No job_id in response"
  exit 1
fi

echo "Job ID: $JOB_ID"

# Poll for completion with timeout
MAX_ATTEMPTS=30
ATTEMPT=0
TIMEOUT=60

echo "Polling for completion (timeout: ${TIMEOUT}s)..."

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS=$(curl -s "http://localhost:3000/status/$JOB_ID" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)

  echo "Attempt $((ATTEMPT + 1))/$MAX_ATTEMPTS: status = $STATUS"

  if [ "$STATUS" = "completed" ]; then
    echo "SUCCESS: Job completed"
    exit 0
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 2
done

echo "FAILED: Job did not complete within ${TIMEOUT} seconds"
exit 1