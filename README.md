![CI/CD Status](https://github.com/yuyue1999/IDS706_Team_Project/actions/workflows/cicd.yml/badge.svg)
![CI/CD Status](https://github.com/yuyue1999/IDS706_Team_Project/actions/workflows/format.yml/badge.svg)
![CI/CD Status](https://github.com/yuyue1999/IDS706_Team_Project/actions/workflows/lint.yml/badge.svg)
![CI/CD Status](https://github.com/yuyue1999/IDS706_Team_Project/actions/workflows/test.yml/badge.svg)



# IDS706 Team Project

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features and Components](#features-and-components)
- [Technical Stack](#technical-stack)
- [Performance and Load Testing](#performance-and-load-testing)
- [Data Engineering Integration](#data-engineering-integration)
- [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
- [Continuous Integration and Continuous Delivery (CI/CD)](#continuous-integration-and-continuous-delivery-cicd)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Limitations](#limitations)
- [Potential Areas for Improvement](#potential-areas-for-improvement)
- [Use of AI Pair Programming Tools](#use-of-ai-pair-programming-tools)
- [Teamwork Reflection](#teamwork-reflection)
- [License](#license)

## Overview
This project is a containerized microservice that interfaces with a data pipeline, providing both a simple RESTful API endpoint and integration with a data storage layer using Redis. It also employs Infrastructure as Code (IaC) for managing and deploying its infrastructure, and includes a comprehensive CI/CD pipeline. The goal is to demonstrate a scalable, testable, and maintainable application that can handle high request throughput (10,000+ requests per second) under load, with strong DevOps practices.

**Key Objectives:**
- Microservice supporting a high volume of requests.
- Integration with a data pipeline using Redis.
- Containerized with Distroless Docker for minimal attack surface.
- AWS-based deployment, with Redis now migrated to AWS Elasticache (Redis Cloud).
- IaC using AWS CDK or CloudFormation.
- CI/CD pipeline with GitHub Actions.
- Quantitative performance assessment using data science approaches (e.g., latency analysis, reliability metrics).
- Clear documentation and reproducible development environment (Codespaces with `.devcontainer`).

## Architecture
Below is a high-level architectural diagram of the system:

```
                +------------------------+
                |   Client / Frontend    |
                +-----------+------------+
                            |
                            v
                    +-------+---------+
                    |   Microservice  |
                    | (Python/Rust)   |
                    +--------+--------+
                             |
                             |  REST API Calls
                             v
                    +--------+---------+
                    |      Redis       |
                    |  (AWS ElastiCache|
                    |   for Redis)     |
                    +--------+---------+
                             |
                             |  Data Pipeline Integration
                             v
                       +-----+------+
                       |  Data Lake |
                       |  or Spark  |
                       | Processing |
                       +------------+
```

- **Microservice:** A RESTful service that provides endpoints to `POST /testitems`, store metadata in Redis, and potentially integrate with Spark or Pandas for data processing.
- **Redis (AWS ElastiCache):** Serves as the in-memory data store to support high-throughput and low-latency requests.
- **Data Pipeline:** Could involve Spark (running on AWS EMR) or Pandas for batch processing, data transformations, or analytics downstream.
- **IaC (AWS CDK / CloudFormation):** Manages the creation and configuration of the AWS infrastructure.

## Features and Components
1. **Microservice:**  
   - Handles `POST /testitems` requests.
   - Uses a data store (Redis) to cache information for quick retrieval.
   - Written in Python and containerized using a Distroless base image for security and minimal footprint.
   
2. **Load Testing:**  
   - A Python script `load_test.py` to verify the application can handle 10,000 requests per second.
   - Generates a CSV report with key performance metrics (latency, success rate, etc.).

3. **Data Engineering Integration:**  
   - Uses Redis as a key-value store.
   - Potential integration with data processing tools (Spark, Pandas) demonstrated in code and pipeline setup.
   
4. **IaC (Infrastructure as Code):**  
   - AWS CDK or CloudFormation templates to provision:
     - Compute resources (ECS or EC2).
     - AWS ElastiCache (Redis) instance.
     - Networking (VPC, Subnets, etc.).
   - All infrastructure managed and version-controlled in the repository.
   - Link: https://8ck4buzifx.us-east-1.awsapprunner.com/

5. **CI/CD Pipeline:**  
   - GitHub Actions workflows for:
     - Build, lint, test, and format checks.
     - Deployments to staging/production.
   - Includes badges for build status and code quality.

6. **Devcontainers / Codespaces:**  
   - A `.devcontainer` configuration ensures a reproducible development environment.
   - Simplifies onboarding and dependency setup.

## Technical Stack
- **Language:** Python (with potential Rust integration if needed).
- **Frameworks/Libraries:**  
  - Flask for the microservice REST endpoints.
  - Requests and concurrent.futures for load testing.
  - Redis-py for Redis integration.
  - Pandas/Spark for data pipeline operations (optional components).
- **Infrastructure:** AWS (ElastiCache for Redis etc.).
- **Docker:** Distroless base image.
- **IaC:** AWS CDK / CloudFormation.
- **CI/CD:** GitHub Actions.

## Performance and Load Testing
A load test script `load_test.py` was run to assess the service’s performance:

**Sample Results:**
```
Total requests: 10000
Success: 10000
Fail: 0
Success rate: 100.00%
Total time: 47.85 seconds
Average latency: 0.4777 seconds
Max latency: 1.2162 seconds
Min latency: 0.0694 seconds
Requests per second: 208.98
```

**Analysis:**
- The service achieved ~209 requests/second in the given test environment (local test conditions).  
- To reach 10,000 requests/second, horizontal scaling, load balancing, and better-optimized infrastructure (e.g., AWS EC2 M5 instances, ECS tasks with autoscaling, or a more optimized code path in Rust) would be employed.
- Detailed latency distribution, percentiles (P95, P99), and scaling tests at various RPS levels (100, 1,000, 10,000) are documented in the `performance_results.csv` and additional metrics notebooks included in the repository.

## Data Engineering Integration
- The microservice integrates with Redis as the primary data storage for handling high-throughput requests.  
- Downstream processing could utilize Pandas for data analysis or transformations if needed. Currently, Redis is the sole component of the data pipeline to ensure minimal latency and simplicity.  
- This integration supports rapid prototyping and performance testing without adding unnecessary complexity.  

## Infrastructure as Code (IaC)
- AWS CDK scripts (or CloudFormation templates) are included in the `infrastructure/` directory.
- Running `cdk deploy` provisions all required resources:
  - ECS service with the microservice container.
  - AWS ElastiCache (Redis) cluster.
  - Networking components.
  
**Note:** Update the `.env` or configuration files with correct AWS credentials and region details before deploying.

## Continuous Integration and Continuous Delivery (CI/CD)
- GitHub Actions workflows are included in `.github/workflows/`.
- Actions include:
  - **Install:** Installs dependencies.
  - **Lint:** Runs `flake8` or `black --check` on code.
  - **Test:** Executes unit tests with `pytest`.
  - **Format:** Ensures code formatting.
  - **Build & Deploy:** Builds Docker images and deploys to AWS on merge to `main`.
  
The repository includes badges reflecting the status of these actions.

## Setup and Installation
1. **Prerequisites:**
   - Docker & Docker Compose
   - AWS CLI configured for your account (for IaC)
   - Python 3.8+ (optional, if running locally)
   
2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yuyue1999/IDS706_Team_Project.git
   cd IDS706_Team_Project
   ```

3. **Set Up Redis Connection:**
   - Update environment variables (e.g., `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`) in `.env` file with your AWS ElastiCache connection details.

4. **Build the Docker Image:**
   ```bash
   docker compose build
   ```

## Running the Application
**Local Run (Docker Compose):**
```bash
docker compose up
```
The microservice should now be available at `http://localhost:8080/testitems` (if configured).

**Load Testing:**
```bash
python load_test.py
```
This will run a series of POST requests and produce a `performance_results.csv` file.

## Configuration
**Environment Variables (in `.env`):**
- `REDIS_HOST`: Hostname of your Redis instance.
- `REDIS_PORT`: Port for Redis.
- `REDIS_PASSWORD`: Password for Redis if set.
- Additional variables for Spark or other data tooling as needed.

## Dependencies
- **Python Libraries:**
  - `requests`, `concurrent.futures` for load testing.
  - `redis` for Redis integration.
  - `statistics` for latency analysis.
  - `pandas` or `pyspark` if using data engineering features.
  
- **System/Infra:**
  - Docker (for containerization)
  - AWS CLI and CDK (for IaC)
  
All Python dependencies are listed in `requirements.txt` and installed automatically in the devcontainer environment.

## Usage
Once running, you can `POST` data to:
```bash
curl -X POST http://localhost:8080/testitems -d "name=example&description=test"
```
The microservice will store this data in Redis and potentially trigger downstream processing.

## Limitations
- **Throughput:** Current local testing shows ~200 RPS. Achieving 10,000 RPS requires scaling out and possibly optimizing code paths or switching to a compiled language (e.g., Rust) for the critical path.
- **Observability:** Basic logging is in place, but more advanced observability (metrics, distributed tracing) could be improved.
- **Security:** While using a Distroless image, further security hardening (e.g., IAM roles, TLS for Redis) is recommended.
- **Error Handling:** Basic error handling is implemented, but more robust retry and fallback mechanisms could be used.

## Potential Areas for Improvement
- **Horizontal Scaling:** Deploy behind an Application Load Balancer (ALB) with ECS or Kubernetes, and auto-scale based on CPU/memory metrics.
- **Caching and Data Layer Improvements:** Add request-level caching strategies, potentially integrate with a CDN or a write-behind cache strategy to reduce load on Redis.
- **Data Pipeline Extensions:** Implement actual Spark jobs or Pandas workflows that consume data from Redis or an S3 snapshot, applying transformations and producing analytics reports.
- **Advanced Observability:** Integrate Prometheus/Grafana or AWS CloudWatch dashboards for metrics, Jaeger or AWS X-Ray for tracing.
- **CI/CD Enhancements:** Automate the load test in CI/CD pipeline to continuously measure performance regressions.

## Use of AI Pair Programming Tools
During development, the team leveraged:
- **GitHub Copilot:** To suggest code snippets, boilerplate Dockerfiles, and CI/CD configuration.
- **OpenAI ChatGPT:** For brainstorming architectural approaches, refining IaC templates, and drafting documentation.

We used these tools to quickly iterate on solutions, generate initial code scaffolding, and then refined the output manually to ensure correctness and compliance with the project’s requirements.

## Teamwork Reflection

#### Application of Principles from Teamwork Reference Materials

Our team utilized principles from the teamwork reference materials to foster collaboration, communication, and productivity:

1. **Clear Roles and Responsibilities:**
   - At the outset of the project, we defined roles for each team member to align with their strengths and interests. For example, one member focused on infrastructure setup using IaC, another worked on microservice development, and another on performance testing and data analysis.

2. **Effective Communication:**
   - Regular team meetings were held twice a week to discuss progress, blockers, and upcoming tasks.
   - We used a shared task management tool to track deliverables and assign deadlines, ensuring transparency in workload distribution.

3. **Constructive Feedback:**
   - Feedback sessions were scheduled bi-weekly to evaluate our progress and identify areas for improvement. Team members were encouraged to share ideas and constructive criticism openly.

4. **Conflict Resolution:**
   - Disagreements were resolved through discussion, focusing on the project’s goals rather than personal preferences. For example, when debating the choice of a library for data integration, we conducted a quick cost-benefit analysis to make an informed decision.

5. **Adaptability:**
   - We adjusted our approach as challenges arose, such as revising our Redis setup by migrating to AWS Elasticache to enhance scalability and reliability.

---

#### Contributions, Strengths, and Areas of Improvement

| **Team Member** | **Contributions**                                                                                               | **Strengths**                                              | **Areas for Improvement**                                |
|-----------------|----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|---------------------------------------------------------|
| **yy373**       | Developed the microservice and Dockerized the application using a Distroless image. Implemented logging.        | Strong coding skills, attention to security and efficiency. | Could improve on documentation clarity.                 |
| **hx84**        | Set up AWS infrastructure using AWS CDK, handled Redis migration, and managed CI/CD pipeline.                  | Expertise in cloud infrastructure, quick troubleshooting. | Should engage more in cross-functional discussions.     |
| **ys386**          | Conducted performance testing, implemented `load_test.py`, and produced data analysis reports.                 | Analytical mindset, excellent debugging skills.           | Needs to manage time more effectively under deadlines.  |
| **th331**          | Designed the architectural diagram and worked on Pandas integration for data engineering tasks.                | Strong visualization and data processing skills.          | Could contribute more actively to performance testing. |

---

#### Peer Evaluations and Feedback Session Outcomes

1. **yy373:**
   - Positive: Strong technical execution, especially in creating a secure and efficient microservice.
   - Improvement: Enhance communication during infrastructure discussions.
   - Grade: 8.5/10.

2. **hx84:**
   - Positive: Delivered robust AWS infrastructure and streamlined the CI/CD pipeline effectively.
   - Improvement: Provide more input on microservice design.
   - Grade: 8.5/10.

3. **ys386:**
   - Positive: Delivered detailed performance insights and ensured load testing reliability.
   - Improvement: Plan workload better to avoid last-minute rushes.
   - Grade: 8/10.

4. **th331:**
   - Positive: Created a clear architectural diagram and delivered Pandas integration seamlessly.
   - Improvement: More proactive in collaborative tasks like CI/CD pipeline setup.
   - Grade: 8/10.

---

#### Outcomes of the Feedback Session

1. **Actionable Improvements:**
   - yy agreed to provide more insights on infrastructure to align her security expertise with the cloud setup.
   - hj committed to participating more actively in discussions about microservice implementation.

2. **New Strategies:**
   - Pair programming sessions were planned for tasks requiring cross-functional expertise.
   - A dedicated time for documentation review was added before submission deadlines to ensure clarity and consistency.

3. **Team Dynamics:**
   - The team appreciated the open communication culture and agreed to continue bi-weekly feedback sessions for future projects.

Overall, the feedback process was productive, and all team members agreed that the collaborative environment contributed significantly to the project's success.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the software, subject to the following conditions:

- **Permission:** You are permitted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.
- **Attribution:** The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.
- **Warranty Disclaimer:** The software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability.
