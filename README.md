# Teste A - Service Status Monitoring with Docker, REST, and Ansible

This project demonstrates how to monitor the status of services (httpd, postgres, rabbitmq) using a combination of Docker, REST calls, and Ansible. It also includes an example of data processing with Python and Excel file generation.

## Prerequisites

*   Docker and Docker Compose installed.

## Starting the Services

1.  Navigate to the root directory of the project.
2.  Start the services in the background with the following command:

    ```bash
    docker-compose up -d
    ```

3.  **Wait for the complete initialization.** Initializing all containers may take 3 to 4 minutes after the `docker-compose up -d` command finishes.

## Checking the Initial Status

1.  After the containers have started, check the status of the services by accessing the `/healthcheck` endpoint:

    ```bash
    curl -X GET "http://localhost:5000/healthcheck"
    ```

2.  You should receive a response similar to this:

    ```json
    {"application_status":"UP","services":{"httpd":"UP","postgres":"UP","rabbitmq":"UP"}}
    ```

    This indicates that all services (httpd, postgres, and rabbitmq) are operational.

## Simulating a Service Failure

1.  To simulate the failure of the rabbitmq service, run the following command:

    ```bash
    curl -X POST "http://localhost:5000/add" -H "Content-Type: application/json" -d '{"service_name": "rabbitmq", "status": "DOWN", "host_name": "localhost"}'
    ```

2.  Check the status again with the health check:

    ```bash
    curl -X GET "http://localhost:5000/healthcheck"
    ```
3. You should receive a response similar to this:
    ```json
    {"application_status":"DOWN","services":{"httpd":"UP","postgres":"UP","rabbitmq":"DOWN"}}
    ```
    This demonstrates that the status of rabbitmq has changed to "DOWN", and the application status is "DOWN" due to an unavailable service.

## Running Ansible for Status Verification

1.  Ansible can be used to check the status of the services and update the endpoint. Run the following command to perform the initial check:

    ```bash
    docker-compose run --rm ansible -e "task_action=check-status"
    ```

2.  You will see output similar to this:

    ```
    Creating ivedha_test_ansible_run ... done

    PLAY [Manage rbcapp1 services and monitoring] ***************************************************************************************************************************************************************************************************************

    TASK [Debug task_action variable] ***************************************************************************************************************************************************************************************************************************
    ok: [httpd_server] => {
        "task_action": "check-status"
    }
    ok: [rabbitmq_server] => {
        "task_action": "check-status"
    }
    ok: [postgres_db] => {
        "task_action": "check-status"
    }

    TASK [Get httpd status from REST endpoint] ******************************************************************************************************************************************************************************************************************
    skipping: [rabbitmq_server]
    skipping: [postgres_db]
    ok: [httpd_server -> localhost]

    TASK [Get rabbitmq status from REST endpoint] ***************************************************************************************************************************************************************************************************************
    skipping: [httpd_server]
    skipping: [postgres_db]
    ok: [rabbitmq_server -> localhost]

    TASK [Get postgresql status from REST endpoint] *************************************************************************************************************************************************************************************************************
    skipping: [httpd_server]
    skipping: [rabbitmq_server]
    ok: [postgres_db -> localhost]

    TASK [Determine rbcapp1 status] *****************************************************************************************************************************************************************************************************************************
    ok: [httpd_server]
    ok: [rabbitmq_server]
    ok: [postgres_db]

    TASK [Push status to REST endpoint] *************************************************************************************************************************************************************************************************************************
    ok: [postgres_db -> localhost]
    ok: [httpd_server -> localhost]
    ok: [rabbitmq_server -> localhost]

    TASK [Display rbcapp1 status and down services] *************************************************************************************************************************************************************************************************************
    ok: [httpd_server] => {
        "msg": "rbcapp1 status: UP, Services: []"
    }
    ok: [rabbitmq_server] => {
        "msg": "rbcapp1 status: DOWN, Services: ['rabbitmq']"
    }
    ok: [postgres_db] => {
        "msg": "rbcapp1 status: UP, Services: []"
    }

    PLAY RECAP **************************************************************************************************************************************************************************************************************************************************
    httpd_server               : ok=5    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
    postgres_db                : ok=5    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
    rabbitmq_server            : ok=5    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
    ```

    Note that Ansible correctly detected that `rabbitmq` is "DOWN".

3. Wait 30 seconds; if you don't pause, the next step might fail.
4.  Run Ansible again:

    ```bash
    docker-compose run --rm ansible -e "task_action=check-status"
    ```
5. Or before this step, execute:
    ```bash
    curl -X POST "http://localhost:5000/add" -H "Content-Type: application/json" -d '{"service_name": "rabbitmq", "status": "UP", "host_name": "localhost"}'
    ```
    ```bash
    curl -X GET "http://localhost:5000/healthcheck"
    ```
    The return should be:
    ```json
    {"application_status":"UP","services":{"httpd":"UP","postgres":"UP","rabbitmq":"UP"}}
    ```
6. Then run Ansible again:
    ```bash
    docker-compose run --rm ansible -e "task_action=check-status"
    ```

## Generating the Excel Sales File

This section describes how to generate the Excel file containing sales data using Python within a Docker container.

1.  **Navigate to the `sales_data` directory:**

    ```bash
    cd sales_data
    ```

2.  **Build the Docker image:**

    ```bash
    docker build -t sales-data .
    ```

3.  **Run the Docker container in interactive mode:**

    ```bash
    docker run -it sales-data bash
    ```

4.  **List the files before execution:**

    ```bash
    ls
    ```
    This will show you the initial files present within the container.

5.  **Execute the Python script:**

    ```bash
    python sales_data.py
    ```
    This command runs the `sales_data.py` script, which is responsible for generating the Excel file.

6.  **List the files after execution:**

    ```bash
    ls
    ```
    This will show you the files present after the Python script execution, including the newly generated Excel file.

