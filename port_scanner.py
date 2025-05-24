import socket
from concurrent.futures import ThreadPoolExecutor

# Function to scan a single port
def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((host, port))  # Try to connect to the port
        if result == 0:
            return port  # Port is open
        return None  # Port is closed

# Function to scan a range of ports
def scan_ports(host, start_port, end_port):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}
        for future in futures:
            port = futures[future]
            try:
                result = future.result()
                if result is not None:
                    open_ports.append(result)
            except Exception as e:
                print(f"Error scanning port {port}: {e}")
    return open_ports

# Main function
if __name__ == "__main__":
    target_host = input("Enter the target host (IP address): ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))

    print(f"Scanning {target_host} from port {start_port} to {end_port}...")
    open_ports = scan_ports(target_host, start_port, end_port)

    if open_ports:
        print(f"Open ports on {target_host}: {', '.join(map(str, open_ports))}")
    else:
        print(f"No open ports found on {target_host}.")
