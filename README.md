## Endpoints

- GET /healthcheck: to tell whether the server is ready to handle requests  
- POST /: to handle inference requests

## Inference requests

The parts in the multipart request are parsed into a JSON object and an array of buffers containing contents of input DICOM files.
```
# Request JSON content
{
    "inference_command": "covid19"
}
```

## Output 
For each input image program return one item in the `parts` array. 
```
{
    "protocol_version":"1.0",
    "parts": []
}
```

If image is x-ray result will be object with:  
`result : POSITIVE or NEGATIVE`  
`type : Not Healthy or Healthy`  
`probability : a number from 0 to 100`  

For invalid or not x-ray images result object contains only  `result: Invalid Image`

#### One image request output example
```
{
    "protocol_version":"1.0",
    "parts": [
        {
            "result": "POSITIVE", 
            "type": "Not Healthy", 
            "probability": 65.59
        }
    ]
}
```

## Build and run the mock inference service container

```
# Start the service
docker-compose up -d

# View the logs
docker-compose logs -f

# Test the service
curl localhost:8900/healthcheck
```
    
## Testing the inference server

To send an inference request to the mock inference server
```
./send-inference-request.sh [-h] [-s] [--host HOST] [-p PORT] /path/to/dicom/files
```
#### Example

```
./send-inference-request.sh --host 0.0.0.0 -p 8900 /opt/images
```