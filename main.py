from fastapi import FastAPI, Path, HTTPException
import json

# Initialize FastAPI app
app = FastAPI()

# Load inventory data from JSON file
with open("inventory.json") as f:
    data = json.load(f)

# Root endpoint to check if the service is running
@app.get("/")
def root():
    return {"message": "Inventory Management System is running"}


# To get all inventory items
@app.get("/all")
def get_config():
    return data


#to get specific host details
@app.get("/host/{hostname}")
def get_host_details(hostname: str = Path(..., description="The name of the host to retrieve", example="Host1")):
    host = data.get(hostname)
    if host:
        return host
    raise HTTPException(status_code=404, detail="Host not found")


#to get hosts by cloud provider 
@app.get("/cloud/{cloud_name}")
def get_hosts_by_cloud(cloud_name: str = Path(..., description="The name of the cloud provider", example="AWS")):
    results = []

    for host_name, info in data.items():
        if info["Cloud"].lower() == cloud_name.lower():
            results.append({host_name: info})

    if not results:
        raise HTTPException(status_code=404, detail="No hosts found for the specified cloud provider (AWS/Azure/GCP)")

    return results

#To get host by region
@app.get("/region/{region_name}")
def get_hosts_by_region(region_name: str = Path(..., description="The name of the region", example="us-east-1")):
    results = []

    for host_name, info in data.items():
        if info["region"].lower() == region_name.lower():
            results.append({host_name: info})

    if not results:
        raise HTTPException(status_code=404, detail="No hosts found for the specified region")

    return results  

#To get active/inactive hosts
@app.get("/status/{status}")
def get_hosts_by_status(status: str = Path(..., description="The status of the hosts to retrieve", example="active")):
    is_active = status.lower() == "active"
    results = []

    for host_name, info in data.items():
        if info["active"] == is_active:
            results.append({host_name: info})

    if not results:
        raise HTTPException(status_code=404, detail="No hosts found for the specified status")

    return results

#To get hosts by tag
@app.get("/tag/{tag_key}/{tag_value}")
def get_hosts_by_tag(tag_key: str = Path(..., description="The key of the tag to filter by", example="Environment"), tag_value: str = Path(..., description="The value of the tag to filter by", example="Production")):
    results = []

    for host_name, info in data.items():
        tags = info.get("Tags", {})
        if tags.get(tag_key) and tags.get(tag_key).lower() == tag_value.lower():
            results.append({host_name: info})

    if not results:
        raise HTTPException(status_code=404, detail="No hosts found for the specified tag")

    return results

#To get host by private IP
@app.get("/private_ip/{private_ip}")
def get_host_by_private_ip(private_ip: str = Path(..., description="The private IP address of the host", example="192.168.1.1")):
    results = []


    for host_name, info in data.items():
        if info["Private_ip"] == private_ip:
            results.append({host_name: info})
    if not results:
        raise HTTPException(status_code=404, detail="No host found with the specified private IP")
    return results

#To get host by public IP
@app.get("/public_ip/{public_ip}")
def get_host_by_public_ip(public_ip: str = Path(..., description="The public IP address of the host", example="1.1.1.1")):
    results = []

    for host_name, info in data.items():
        if info["Public_ip"] == public_ip:
            results.append({host_name: info})
    if not results:
        raise HTTPException(status_code=404, detail="No host found with the specified public IP")
    return results
