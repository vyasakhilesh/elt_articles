import paramiko

# SFTP server details
hostname = "127.0.0.1"
port = 2222
username = "user1"
password = "password"

try:
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SFTP server
    ssh.connect(hostname, port, username, password)
    sftp = ssh.open_sftp()

    # List files in the directory
    directory = "/"
    files = sftp.listdir(directory)

    print("Files in directory:", files)

    # Close the SFTP connection
    sftp.close()
    ssh.close()

except Exception as e:
    print("Error:", e)
