import os
import subprocess
import shutil
import zipfile
from datetime import datetime

def clone_repo(repo_url, dest_dir):
    """Clone a git repository to a specified destination directory."""
    subprocess.call(["git", "clone", repo_url, dest_dir])

def run_sast(project_dir):
    """Run a SAST analyzer on a specified project directory."""
    subprocess.call(["sast-analyzer", project_dir])

def generate_report(project_dir, output_file):
    """Generate a report based on the SAST analysis results."""
    with open(output_file, "w") as f:
        f.write("SAST Analysis Report\n")
        f.write("---------------------\n")
        f.write("Project: {}\n".format(project_dir))
        f.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("\n")

        # Read the results of the SAST analysis
        with open(os.path.join(project_dir, "sast-results.txt"), "r") as results_file:
            results = results_file.readlines()

        # Count the number of vulnerabilities found
        num_vulnerabilities = 0
        for line in results:
            if "Vulnerability" in line:
                num_vulnerabilities += 1

        # Write the summary to the report
        f.write("Number of vulnerabilities found: {}\n".format(num_vulnerabilities))
        f.write("\n")

        # Write the details of each vulnerability to the report
        for line in results:
            if "Vulnerability" in line:
                f.write(line)

def main():
    # Define the GitHub repository URL and destination directory
    repo_url = "https://github.com/Orihalk/123.git"
    dest_dir = "D:\test"

    # Clone the repository
    clone_repo(repo_url, dest_dir)

    # Run the SAST analyzer
    run_sast(dest_dir)

    # Generate the report
    output_file = "sast-report.txt"
    generate_report(dest_dir, output_file)

    # Zip the project directory and the report
    zip_file = "project-and-report.zip"
    with zipfile.ZipFile(zip_file, "w") as zip:
        zip.write(dest_dir)
        zip.write(output_file)

    # Clean up the temporary directory
    shutil.rmtree(dest_dir)

if __name__ == "__main__":
    main()