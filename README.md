# aware-api
Microsoft Hackathon: Azure Series

[![Build Status](https://dev.azure.com/aware-devops/aware-api/_apis/build/status/CamiloGarciaLaRotta.aware-api)](https://dev.azure.com/aware-devops/aware-api/_build/latest?definitionId=2)

This repository contains the RESTful Aware's API server.

# Tech Stack
- Flask
- Docker
- OpenCV
- Azure Image Recognition
- Azure DevOps
- Azure Container Registry
- Azure App Service
- Azure CosmosDB

# The Release Pipeline
![Architecture](https://i.imgur.com/IZ9VQNl.jpg)
1.  `Azure DevOps` fetches the latest commit to master from Aware's GitHub repo. It will build and test the source code.
2. If succesful, `DevOps` will then build a Docker image of the web api and push it to the `Azure Container Registry`.
3. After succesfully releasing the docker image, `DevOps` will deploy the web api via `Azure App Service`.
4. `Azure App Services` will fetch the corresponding image from the `Container Registry` and make it available online.
5. The mobile client can then access Aware's API through the web.
`

## Starting the API server
- Development
  ```bash
    python run.py
  ```
- Production
  ```bash
    # through Docker
    docker build -t aware-api .
    docker run --rm -t -p 8080:8080 aware-api
    # or through CLI
    waitress-serve --call 'aware_api:create_app'
  ```
 - You can now test the api in another terminal
    ```bash
        curl -i \
            -X POST \
            -H "Content-Type: application/json" \
            -d '{"id":"42", "picture": "some_base64_str"}' \
            localhost:8000/api
    ```
- When you are done you can shutdown the api with `ctrl-C`
