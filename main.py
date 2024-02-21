import paramiko
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=2, max=10))
def connect_to_sftp(hostname, username, password=None,):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file('../sftp_python/paramiko.log')
        
        ssh_client.connect(hostname, username=username, password=password, look_for_keys=False)

        print("Connected to SFTP server")

        # remoteFilePath = '/outbound/erc' # bad remote path, this raises an error and retry
        remoteFilePath = '/pub/example'
        file_name = "readme.txt"
        remote_path = f"{remoteFilePath}/{file_name}"
        downloaded_file_path = file_name
            
        with ssh_client.open_sftp() as sftp_client:
            sftp_client.get(remote_path, downloaded_file_path)

        sftp_client.close()
        ssh_client.close()

    except Exception as e:
        print(f"{connect_to_sftp.retry.statistics}: An error occurred:", e)
        raise e


# Example usage with test server https://test.rebex.net/
hostname = 'test.rebex.net'
username = 'demo'
password = 'password'

connect_to_sftp(hostname, username, password)