import requests
import json
import time

def fetch_commodity_data():
    # List of districts
    districts = [
        "Ahmedabad",
        "Amreli", 
        "Anand",
        "Banaskanth",
        "Dahod",
        "Gandhinagar"
    ]
    
    # Base URL and API key
    base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
    
    # Dictionary to store all district data
    all_districts_data = {}
    
    for district in districts:
        try:
            # Construct URL with district filter
            url = f"{base_url}?api-key={api_key}&format=json&filters[district]={district}"
            print(url)
            print(f"Fetching data for {district}...")
            
            # Make API request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse JSON response
            district_data = response.json()
            
            # Store data with district name as key
            all_districts_data[district] = district_data
            
            print(f"Successfully fetched data for {district}")
            
            # Add a small delay to be respectful to the API
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {district}: {e}")
            all_districts_data[district] = {"error": str(e)}
        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {district}: {e}")
            all_districts_data[district] = {"error": f"JSON decode error: {str(e)}"}
    
    # Save all data to single JSON file
    try:
        import os
        
        # Create directory if it doesn't exist
        output_dir = "project-root/scripts"
        os.makedirs(output_dir, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(output_dir, "commodities.json")
        
        with open(file_path, "w") as f:
            json.dump(all_districts_data, f, indent=2, ensure_ascii=False)
        
        print(f"All district data saved to {file_path}")
        
    except Exception as e:
        print(f"Error saving data to file: {e}")
    
    return all_districts_data

if __name__ == "__main__":
    fetch_commodity_data()