# aware-api
Microsoft Hackathon: Azure Series

[![Build Status](https://dev.azure.com/aware-devops/aware-api/_apis/build/status/CamiloGarciaLaRotta.aware-api)](https://dev.azure.com/aware-devops/aware-api/_build/latest?definitionId=2)

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
