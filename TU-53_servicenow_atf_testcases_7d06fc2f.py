import requests
import json
import base64
import uuid

# Replace with actual ServiceNow instance and credentials
instance = 'dev209377.service-now.com'
user = 'admin'
pwd = '*4JQovn8Yd^R'
base_url = f'https://{instance}/api/now/'


# Setup common headers for all API calls
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode(f'{user}:{pwd}'.encode()).decode()
}

# Generate a GUID for prefix parameter
prefix_guid = str(uuid.uuid4())

# Common setup (import statements, credentials, and headers) remains the same...
# Function definitions for create_test_suite and create_test_case remain the same...
# Function to create a Record Query test step
# Create an ATF Test Suite
def create_test_suite(suite_name):
    data = {
        "name": suite_name,
        "description": "Automated Test Framework suite for EPA EVLAG creation testing."
    }
    response = requests.post(f'{base_url}/table/sys_atf_test_suite', headers=headers, data=json.dumps(data))
    suite_id = response.json()['result']['sys_id']
    return suite_id

# Create an ATF Test Case
def create_test_case(suite_id, test_name, description):
    data = {
        "test_suite": suite_id,
        "name": test_name,
        "description": description
    }
    response = requests.post(f'{base_url}/table/sys_atf_test', headers=headers, data=json.dumps(data))
    test_case_id = response.json()['result']['sys_id']
    return test_case_id

# Create an ATF Test Step
def create_test_step(test_case_id, step_config, inputs, expected):
    data = {
        "test_case": test_case_id,
        "step_config": step_config,
        "inputs": inputs,
        "expected": expected,
        "description": ""
    }
    response = requests.post(f'{base_url}/table/sys_atf_step', headers=headers, data=json.dumps(data))
    return response.json()

def create_record_query_test_step(test_case_id, table, query, expected_type, expected_role):
    # Define the inputs for the Record Query step
    inputs = {
        "table": table,
        "query": query
    }

    # The expected result is the existence of records matching the query
    expected = {
        "expected_type": expected_type,
        "expected_role": expected_role
    }

    # Fetch the sys_id for the "Record Query" step config
    step_config_response = requests.get(f'{base_url}/table/sys_atf_step_config?name=Record Query', headers=headers)
    if step_config_response.status_code != 200:
        raise ValueError(f"Error fetching Record Query step config: {step_config_response.text}")
    step_config_sys_id = step_config_response.json()['result'][0]['sys_id']

    # Create the test step with the Record Query step config sys_id
    return create_test_step(test_case_id, step_config_sys_id, json.dumps(inputs), json.dumps(expected))

def create_record_query_test_step_equipment(test_case_id, table, query, expected_results):
    # Define the inputs for the Record Query step
    inputs = {
        "table": table,
        "query": query
    }

    # The expected result is the existence of records matching the query
    expected = {
        "expected_results": expected_results  # This should be a list of dictionaries containing expected field-value pairs
    }

    # Fetch the sys_id for the "Record Query" step config
    step_config_response = requests.get(f'{base_url}/table/sys_atf_step_config?name=Record Query', headers=headers)
    if step_config_response.status_code != 200:
        raise ValueError(f"Error fetching Record Query step config: {step_config_response.text}")
    step_config_sys_id = step_config_response.json()['result'][0]['sys_id']

    # Create the test step with the Record Query step config sys_id
    return create_test_step(test_case_id, step_config_sys_id, json.dumps(inputs), json.dumps(expected))

def create_record_query_test_step_network_interface(test_case_id, table, query, expected_results):
    # Define the inputs for the Record Query step
    inputs = {
        "table": table,
        "query": query
    }

    # The expected result is the existence of records matching the query
    expected = {
        "expected_results": expected_results  # This should be a list of dictionaries containing expected field-value pairs
    }

    # Fetch the sys_id for the "Record Query" step config
    step_config_response = requests.get(f'{base_url}/table/sys_atf_step_config?name=Record Query', headers=headers)
    if step_config_response.status_code != 200:
        raise ValueError(f"Error fetching Record Query step config: {step_config_response.text}")
    step_config_sys_id = step_config_response.json()['result'][0]['sys_id']

    # Create the test step with the Record Query step config sys_id
    return create_test_step(test_case_id, step_config_sys_id, json.dumps(inputs), json.dumps(expected))

def create_record_query_test_step_physical_connection(test_case_id, table, query, expected_results):
    # Define the inputs for the Record Query step
    inputs = {
        "table": table,
        "query": query
    }

    # The expected result is the existence of records matching the query
    expected = {
        "expected_results": expected_results  # This should be a list of dictionaries containing expected field-value pairs
    }

    # Fetch the sys_id for the "Record Query" step config
    step_config_response = requests.get(f'{base_url}/table/sys_atf_step_config?name=Record Query', headers=headers)
    if step_config_response.status_code != 200:
        raise ValueError(f"Error fetching Record Query step config: {step_config_response.text}")
    step_config_sys_id = step_config_response.json()['result'][0]['sys_id']

    # Create the test step with the Record Query step config sys_id
    return create_test_step(test_case_id, step_config_sys_id, json.dumps(inputs), json.dumps(expected))

def create_run_script_test_step(test_case_id, script):
    # Define the inputs for the Run Server Side Script step
    inputs = {
        "script": script,
        "description": "Setup UC12ab EVLAG Circuits"
    }

    # Fetch the sys_id for the "Run Server Side Script" step config
    step_config_response = requests.get(f'{base_url}/table/sys_atf_step_config?name=Run Server Side Script', headers=headers)
    if step_config_response.status_code != 200:
        raise ValueError(f"Error fetching Run Server Side Script step config: {step_config_response.text}")
    step_config_sys_id = step_config_response.json()['result'][0]['sys_id']

    # Create the test step with the Run Server Side Script step config sys_id
    test_step_response = create_test_step(test_case_id, step_config_sys_id, json.dumps(inputs), "{}")
    return test_step_response


def create_acceptance_criteria_1_test(suite_id, test_case_id):
    # Define the expected values for the site's type and role
    expected_site_type = "CENTRAL_OFFICE"  # Replace with the actual expected type
    expected_site_role = "AOP_HUT"  # Replace with the actual expected role

    # Define the query for the Record Query step
    query = f"type={expected_site_type}^role={expected_site_role}^nameSTARTSWITH{prefix_guid}"

    # Create the Record Query test step
    test_step_response = create_record_query_test_step(test_case_id, "x_785744_test_auto_sites", query, expected_site_type, expected_site_role)

    # Check response
    if test_step_response.status_code == 200:
        print("Record Query test step for site creation verification created successfully.")
    else:
        print("Error creating Record Query test step: ", test_step_response.text)

def create_acceptance_criteria_2_test(suite_id,test_case_id):
    # Continuing from the previous test suite and case for Acceptance Criteria 1...
    # Assuming we're still working within the same test suite and test case for equipment creation
    # Define the expected results for the equipment's associated site
    # This is a simplified example and should be expanded based on actual equipment names and expected site associations
    expected_results = [
        {"equipment_name": "T1 P2EMUX", "associated_site": "expected_site_sys_id_T1_P2EMUX"},
        {"equipment_name": "OSP FDP", "associated_site": "expected_site_sys_id_OSP_FDP"},
        # Add more dictionaries for each piece of equipment and its associated site
    ]

    # Define the query for the Record Query step
    site_sys_id_A = ""
    site_sys_id_Z = ""
    query = f"nameIN(T1 P2EMUX,OSP FDP, FOT FDP)^siteIN({site_sys_id_A},{site_sys_id_Z})^nameSTARTSWITH{prefix_guid}"

    # Create the Record Query test step for equipment verification
    test_step_response = create_record_query_test_step_equipment(test_case_id, "x_785744_test_auto_equipment", query, expected_results)

    # Check response
    if test_step_response.status_code == 200:
        print("Record Query test step for equipment creation verification created successfully.")
    else:
        print("Error creating Record Query test step: ", test_step_response.text)

def create_acceptance_criteria_3_test(suite_id,test_case_id):
    # Continuing from the previous test suite and case for Acceptance Criteria 1 and 2...
    # Assuming we're still working within the same test suite and test case for network interface creation verification

    # Define the expected results for the network interfaces' association with equipment and their port position
    # This is a simplified example and should be expanded based on actual port names, equipment, and port positions
    expected_results = [
        {"port_name": "001-TX", "associated_equipment": "expected_equipment_sys_id_T1_P2EMUX", "port_position": "TX"},
        {"port_name": "002-RX", "associated_equipment": "expected_equipment_sys_id_T1_P2EMUX", "port_position": "RX"},
        # Add more dictionaries for each port, its associated equipment, and port position
    ]

    p2emux_sys_id=""

    # Define the query for the Record Query step
    query = f"nameIN(001-TX,002-RX)^equipmentIN{p2emux_sys_id}^port_positionIN(TX,RX)^nameSTARTSWITH{prefix_guid}"

    # Create the Record Query test step for network interface verification
    test_step_response = create_record_query_test_step_network_interface(test_case_id, "x_785744_test_auto_network_interface", query, expected_results)

    # Check response
    if test_step_response.status_code == 200:
        print("Record Query test step for network interface creation verification created successfully.")
    else:
        print("Error creating Record Query test step: ", test_step_response.text)

def create_acceptance_criteria_4_test(suite_id,test_case_id):
    # Continuing from the previous test suite and case for Acceptance Criteria 1, 2, and 3...
    # Assuming we're still working within the same test suite and test case for physical connection creation verification

    # Define the expected results for the physical connections' association with equipment A and Z
    expected_results = [
        {
            "connection_name": "expected_connection_name_1",
            "associated_equipment_A": "expected_equipment_sys_id_A1",
            "associated_equipment_Z": "expected_equipment_sys_id_Z1"
        },
        {
            "connection_name": "expected_connection_name_2",
            "associated_equipment_A": "expected_equipment_sys_id_A2",
            "associated_equipment_Z": "expected_equipment_sys_id_Z2"
        },
        # Add more dictionaries for each physical connection and its associated equipment A and Z
    ]

    expected_connection_name_1=""
    expected_connection_name_2=""
    expected_equipment_sys_id_A1=""
    expected_equipment_sys_id_A2=""
    expected_equipment_sys_id_Z1=""
    expected_equipment_sys_id_Z2=""
    # Define the query for the Record Query step
    query = f"nameIN{expected_connection_name_1,expected_connection_name_2,...}^equipment_aIN{expected_equipment_sys_id_A1,expected_equipment_sys_id_A2,...}^equipment_zIN{expected_equipment_sys_id_Z1,expected_equipment_sys_id_Z2,...}^nameSTARTSWITH{prefix_guid}"

    # Create the Record Query test step for physical connection verification
    test_step_response = create_record_query_test_step_physical_connection(test_case_id, "x_785744_test_auto_physical_connection", query, expected_results)

    # Check response
    if test_step_response.status_code == 200:
        print("Record Query test step for physical connection creation verification created successfully.")
    else:
        print("Error creating Record Query test step: ", test_step_response.text)

def create_run_test_script_step(suite_id,test_case_id):
    # The server-side script we want to run
    server_side_script = """
    var prefix = gs.generateGUID();
    var test = new x_785744_test_auto.test_script().create(prefix);
    """

    # Create the test case for running the server side script
    test_case_name = "Run Server Side Script for EVLAG Circuit Creation"
    test_case_description = "Test step to run server side script for setting up EVLAG circuit"
    test_case_id = create_test_case(suite_id, test_case_name, test_case_description)

    # Create the Run Server Side Script test step
    test_step_response = create_run_script_test_step(test_case_id, server_side_script)

    # Check response
    if test_step_response.status_code == 200:
        print("Run Server Side Script test step created successfully.")
    else:
        print("Error creating Run Server Side Script test step: ", test_step_response.text)



# Create the test case and steps
def main():
    suite_id = create_test_suite("EVLAG Circuit Creation Suite")
    test_case_id = create_test_case(suite_id, "Verify EVLAG Circuit Creation Details", "Test to verify that all components are setup, created and completed correctly.")

    create_run_test_script_step(suite_id,test_case_id)
    create_acceptance_criteria_1_test(suite_id,test_case_id)
    create_acceptance_criteria_2_test(suite_id,test_case_id)
    create_acceptance_criteria_3_test(suite_id,test_case_id)
    create_acceptance_criteria_4_test(suite_id,test_case_id)

    # ... To Be Continued

if __name__ == "__main__":
    main()