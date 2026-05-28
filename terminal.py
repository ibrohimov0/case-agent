import subprocess
import logging
logging.basicConfig(
    filename='tasks_cache.log',
    level=logging.DEBUG,
    filemode='a',
    format='%(asctime)s - %(message)s',
)


def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode('utf-8')}"

    
if __name__ == "__main__":
    while True:
        task = input("CASE > ")
        logging.info(f"Received command: {task}")
        if task.lower() == 'exit':
            logging.info("Exiting terminal interface.")
            break