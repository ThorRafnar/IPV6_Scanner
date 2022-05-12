import subprocess
print("Starting subprocesses")
country = input("Enter country code: ")
process_count = int(input("Enter number of processes: "))
for i in range(process_count):
    subprocess.Popen(['python3', 'scannernmap.py', country, str(i), str(process_count)])
print("Running...")

