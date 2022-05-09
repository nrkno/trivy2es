## Github action to post output from trivy scan to Elastic Search

NB: This is to be considered WIP for now, however check LICENSE 

This Github Action is meant to be used to send the json output of a [Trivy scan Github Action](https://github.com/aquasecurity/trivy-action)
to an Elasticsearch cloud instance.

For example: 

```
      # Checkout repo code
      - uses: actions/checkout@v2
      # Trivy test action
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: '${{ secrets.PLATTFORM_CONTAINER_REGISTRY }}/${{ env.IMAGE_NAME }}/${{ env.BRANCH }}:latest'
          format: 'json'
          exit-code: '0'
          ignore-unfixed: true
          vuln-type: 'os,library'
          severity: 'CRITICAL,HIGH'
          output: 'test.json'
        env:
          TRIVY_USERNAME: ${{ secrets.PLATTFORM_ACR_PUSH_CLIENT_ID }}
          TRIVY_PASSWORD: ${{ secrets.PLATTFORM_ACR_PUSH_CLIENT_SECRET }}
      # Use our internal made action for posting to ES
      - name: Send to ES
        uses: nrkno/trivy2es@v1.3
        with:
          elasticApiAddress: 'XXXXXXXXXXXXXXXXX.westeurope.azure.elastic-cloud.com'
          targetIndex: 'github-actions'
          githubRepository: 'organization/repository'
          jsonInput: 'test.json'
```

In addition to the mandatory fields shown in the example (URL of the ES cloud instance, a target index where to store the json data, a referral github repository and the json file), 
the action expects an Elasticsearch API key stored as a "ELASTIC_API_KEY" secret. This key can be obtained by [following the Elasticsearch documentation](https://www.elastic.co/guide/en/kibana/master/api-keys.html) and stored in a secret called "ELASTIC_API_KEY" in the repo. 

## Moving parts
This is one of our first attempts to create a custom Github Action, so be patient if the implementation is not particularly brilliant. There is no way, as far as we understood, to create custom Github Actions without making them public, so we have to expose ourselves to the international shame this will obviously cause. Said that, we tried to follow [this HOWTO](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action) to create a Docker container based custom Github Action.

We are using a Docker container running a Python script that manipulates the json output from the trivy-action Github Action. 
The reason why manipulation is necessary is mostly related to how Elasticsearch translates numbers containing a comma (they are not always considered a float) so that it can be necessary to force this type. Otherwise it's just a simple payload posting using a standard request Python library. 



