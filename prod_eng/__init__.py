"""

CORE STEPS:

    1. Receive the client's HTTPS/TCP request.
    2. Select a backend using Round Robin.
    3. Forward the request to that backend.
    4. Wait for the backend's response.
    5. Return the response to the client.
    6. Advance the pointer to the next backend.
    7. Skip any backends that have failed health checks.

"""