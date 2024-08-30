import sys
import socket
import pyfiglet
from datetime import datetime

# Banner
banner = pyfiglet.figlet_format("DANTICO")
print(banner)

# Use a valid hostname
target = "www.google.com"
host = socket.gethostbyname(target)

try:
    file = open("port_scanner.txt", "a")
except FileNotFoundError:
    print("The file does not exist")
    sys.exit()  # Exit if the file cannot be opened

# Correct usage of datetime to get the date
t1 = datetime.now()
print("Start time: {}".format(t1.strftime("%H:%M:%S")))
file.write("Start time: {} \n".format(t1.strftime("%H:%M:%S")))

# Error handling and port scanning logic
try:
    for port in range(1, 1025):
        # AF_INET is used for IPv4 while SOCK_STREAM is used for TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.001)
        result = sock.connect_ex((host, port))

        if result == 0:  # port is open
            try:
                service_name = socket.getservbyport(port, "tcp")
            except OSError:  # use OSError to handle getservbyport exception
                service_name = "unknown service"

            print(f"Port [*] : {port} open, protocol service name: {service_name}")
            file.write(f"Port [*] : {port} open, protocol service name: {service_name}\n")
        else:  # port is closed
            try:
                service_name = socket.getservbyport(port, "tcp")
            except OSError:
                service_name = "unknown service"
                
            print(f"Port [*] : {port} closed, protocol service name: {service_name}")
            file.write(f"Port [*] : {port} closed, protocol service name: {service_name}\n")

except socket.gaierror:
    print("Host name could not be resolved. Exiting")
    file.write("Host name could not be resolved. Exiting\n")
    sys.exit()

except socket.error:
    print("Could not connect to server")
    file.write("Could not connect to server\n")
    sys.exit()

t2 = datetime.now()

print("End time: {}".format(t2.strftime("%H:%M:%S")))
file.write("End time: {}\n".format(t2.strftime("%H:%M:%S")))

total_time = t2 - t1
print("Total time: {}".format(total_time))
file.write("Total time: {}\n".format(total_time))

file.close()
