# BMRB-DATA-COLLECTOR
BMRB Data Collector
A Python script to automate the process of extracting BMRB (Biological Magnetic Resonance Data Bank) data, secondary structure information, and related metadata for selected entries. This tool scrapes data from BMRB and PDB websites and saves it in CSV format for further analysis.

Features
Extracts chemical shift data (C, CA, CB) for residues from BMRB validation pages.
Collects related PDB IDs from BMRB database links.
Scrapes secondary structure information (e.g., HELIX, SHEET) from PDB entries.
Automates the entire process for multiple BMRB IDs.
Prerequisites
Before running the script, ensure the following are installed:

Python 3.8 or higher
pip (Python package installer)
Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/yourusername/bmrb-data-collector.git
cd bmrb-data-collector
Install Required Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Usage
Open main.py in a text editor or IDE (e.g., VS Code).

Run the script:

bash
Copy
Edit
python main.py
Main Functionalities:

Scrape Single BMRB Entry: The script processes data for a single BMRB ID (configured in the script).
Batch Process Multiple Entries: Specify the number of BMRB IDs to scrape from the query page.
The extracted data is saved in:

shift_data_<BMRB_ID>.csv: Contains chemical shift data for the specified BMRB ID.
final_data_<BMRB_ID>.csv: Contains chemical shift data combined with secondary structure information.
Automating Multiple BMRB IDs
Configure the scrape_bmrb_ids_from_query function to specify how many BMRB IDs to extract.
The script will loop through the IDs and save data for each.
Example Output
final_data_<BMRB_ID>.csv
Residue	C	CA	CB	Secondary_Structure
V6	175.69(2.03)	62.48(3.04)	32.66(1.91)	HELIX
L13	176.97(2.09)	55.65(2.21)	42.37(1.86)	HELIX
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Fork the repository.
Create a new branch:
bash
Copy
Edit
git checkout -b feature/your-feature-name
Commit your changes:
bash
Copy
Edit
git commit -m "Add your message here"
Push to your branch:
bash
Copy
Edit
git push origin feature/your-feature-name
Create a pull request.
Acknowledgments
BMRB (Biological Magnetic Resonance Data Bank) for their publicly available data.
PDBe for secondary structure data.