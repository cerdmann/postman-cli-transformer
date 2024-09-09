newman run Craig\ Private\ Pinball\ Map\ Collection.postman_collection.json Craig\ Private\ Pinball\ Map\ Collection.postman_collection.json --environment Pinball\ Prod.postman_environment.json --reporters json,htmlextra,junit,cli --reporter-htmlextra-export ./results/newman-htmlextra-results.html --reporter-junit-export ./results/newman-junit-report.xml --reporter-json-export ./results/newman-json-results.json

postman collection run 33123329-c0e8c839-7ec2-4d32-a577-5932b2a72304 -e 33123329-dc25303c-b56c-4d1c-b7fb-bdb2e95d4b9e > ./results/postman-cli-run.txt
