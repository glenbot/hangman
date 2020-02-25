import os

# Server settings
SERVER_ADDRESS = os.environ.get('SERVER_ADDRESS', '0.0.0.0')
SERVER_PORT = os.environ.get('SERVER_PORT', '8888')

# probe file locations
LIVENESS_PROBE_FILE = '/tmp/liveness'
READINESS_PROBE_FILE = '/tmp/readiness'
