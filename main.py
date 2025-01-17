import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import random


def process_bmrb_data(search_url, n):
    """
    Process the first N BMRB IDs found on the given search URL and collect data.

    Parameters:
        search_url (str): URL of the BMRB search page.
        n (int): Number of BMRB IDs to process.

    Outputs:
        shift_data_<BMRB_ID>.csv: File containing ASV data.
        final_data_<BMRB_ID>.csv: File containing ASV data with secondary structure.
    """

    def scrape_bmrb_ids(search_url, n):
        """Scrape the first N BMRB IDs from the search page."""
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            bmrb_ids = []
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "summary/index.php?bmrbId=" in href:
                    match = re.search(r"bmrbId=(\d+)", href)
                    if match:
                        bmrb_ids.append(match.group(1))

            bmrb_ids = list(set(bmrb_ids))  # Remove duplicates
            bmrb_ids = sorted(bmrb_ids, key=int)[:n]  # Get the first N IDs
            print(f"Found BMRB IDs: {bmrb_ids}")
            return bmrb_ids

        except Exception as e:
            print(f"Error scraping BMRB IDs: {e}")
            return []

    def scrape_ASV(url_directories, output_file):
        """Scrape ASV data and save to a CSV."""
        try:
            response = requests.get(url_directories)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            rows = []
            current_residue = None

            for line in soup.get_text().splitlines():
                line = line.strip()

                if line and "Overall:" in line:
                    parts = line.split("Overall:")
                    current_residue = parts[0].strip()

                elif "Ave C Shift Values>>" in line:
                    shift_data = line.split(">>")[1].strip()
                    values = {key.strip(): val.strip() for key, val in (item.split("::") for item in shift_data.split("\t") if "::" in item)}
                    c_value = values.get("C", "None")
                    ca_value = values.get("CA", "None")
                    cb_value = values.get("CB", "None")

                    if current_residue:
                        rows.append([current_residue, c_value, ca_value, cb_value])

            df = pd.DataFrame(rows, columns=["Residue", "C", "CA", "CB"])
            df.to_csv(output_file, index=False)
            print(f"ASV data saved to {output_file}")
            return df

        except Exception as e:
            print(f"Error processing ASV data: {e}")
            return pd.DataFrame()

    def scrape_secondary_structure(pdb_id):
        """Scrape secondary structure data for a given PDB ID."""
        try:
            pdb_url = f"https://www.ebi.ac.uk/pdbe/entry-files/pdb{pdb_id.lower()}.ent"
            response = requests.get(pdb_url)
            response.raise_for_status()

            secondary_structure = []
            for line in response.text.splitlines():
                if line.startswith("HELIX") or line.startswith("SHEET"):
                    secondary_structure.append(line.strip())

            return secondary_structure
        except Exception as e:
            print(f"Error fetching secondary structure for {pdb_id}: {e}")
            return []

    def scrape_pdb_values(url_data_library):
        """Scrape PDB values from the data library page."""
        try:
            response = requests.get(url_data_library)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            pdb_values = []
            for row in soup.find_all("tr"):
                if "PDB" in row.get_text():
                    pdb_cell = row.find_all("td")[-1]
                    if pdb_cell:
                        raw_text = pdb_cell.get_text(" ", strip=True)
                        pdb_values = re.findall(r"\b[A-Z0-9]{4}\b", raw_text)

            pdb_values = sorted(set(pdb_values))
            pdb_values = [value for value in pdb_values if value != "RCSB"]
            return pdb_values

        except Exception as e:
            print(f"Error scraping PDB values: {e}")
            return []

    def update_data_with_structure(pdb_values, asv_df, bmrb_id):
        """Update the data table with secondary structure information."""
        try:
            random_pdb = random.choice(pdb_values)
            print(f"Selected PDB ID: {random_pdb}")

            secondary_data = scrape_secondary_structure(random_pdb)

            matched_data = []
            for line in secondary_data:
                if line.startswith("HELIX"):
                    helix_start = int(line[21:25].strip())
                    helix_end = int(line[33:37].strip())
                    matched_data.append({"Type": "HELIX", "Start": helix_start, "End": helix_end})
                elif line.startswith("SHEET"):
                    sheet_start = int(line[22:26].strip())
                    sheet_end = int(line[33:37].strip())
                    matched_data.append({"Type": "SHEET", "Start": sheet_start, "End": sheet_end})

            structure_df = pd.DataFrame(matched_data)

            def match_residue(row):
                residue_number = int(re.findall(r"\d+", row["Residue"])[0])
                for _, struct_row in structure_df.iterrows():
                    if struct_row["Start"] <= residue_number <= struct_row["End"]:
                        return struct_row["Type"]
                return "None"

            asv_df["Secondary_Structure"] = asv_df.apply(match_residue, axis=1)
            final_output_file = f"final_data_{bmrb_id}.csv"
            asv_df.to_csv(final_output_file, index=False)
            print(f"Updated data with secondary structure saved to {final_output_file}")

        except Exception as e:
            print(f"Error updating data with structure: {e}")

    # Main processing logic
    bmrb_ids = scrape_bmrb_ids(search_url, n)

    for bmrb_id in bmrb_ids:
        url_directories = f"https://bmrb.io/ftp/pub/bmrb/entry_directories/bmr{bmrb_id}/validation/AVS_full.txt"
        url_data_library = f"https://bmrb.io/data_library/summary/index.php?bmrbId={bmrb_id}"

        asv_file = f"shift_data_{bmrb_id}.csv"
        asv_df = scrape_ASV(url_directories, asv_file)

        pdb_values = scrape_pdb_values(url_data_library)

        if not asv_df.empty and pdb_values:
            update_data_with_structure(pdb_values, asv_df, bmrb_id)


# Example usage
process_bmrb_data("https://bmrb.io/search/query_grid/?data_types%5B%5D=carbon_shifts&polymers%5B%5D=polypeptide%28L%29&polymer_join_type=OR", 10)
