import xml.etree.ElementTree as ET

def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    depot = None
    customers = []
    demands = {}
    vehicle_capacity = None

    for node in root.find("network").find("nodes"):
        node_id = int(node.attrib["id"])
        node_type = int(node.attrib["type"])
        x = float(node.find("cx").text)
        y = float(node.find("cy").text)

        if node_type == 0:  # Depot
            depot = {"id": node_id, "x": x, "y": y}
        else:
            customers.append({"id": node_id, "x": x, "y": y})

    vehicle_profile = root.find("fleet").find("vehicle_profile")
    vehicle_capacity = float(vehicle_profile.find("capacity").text)

    for request in root.find("requests"):
        node_id = int(request.attrib["node"])
        demand = float(request.find("quantity").text)
        demands[node_id] = demand

    return {
        "depot": depot,
        "customers": customers,
        "demands": demands,
        "capacity": vehicle_capacity,
    }
