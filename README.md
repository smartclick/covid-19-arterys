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
    "bounding_boxes_2d": []
}
```

If image is x-ray result will be object with:  
`label : Not Healthy or Healthy`  
`probability : a number from 0 to 100`  


#### One image request output example
```
{
    "protocol_version":"1.0",
    "bounding_boxes_2d": [{ 
        "label": "Not Healthy", 
        "probability": 65.59,
        "SOPInstanceUID": "2.25.336451217722347364678629652826931415692", 
        "top_left": [0, 0], 
        "bottom_right": [1024, 1024]
    }]
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