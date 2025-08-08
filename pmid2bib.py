from Bio import Entrez
from Bio import Medline
import time

# Your email (NCBI requires it for identification)
Entrez.email = "hoelzer.martin@gmail.com"

# Your list of PMIDs
## From the Introduction, already added to Overleaf
pmid_list = [
    "14961025", "16185861", "18321793", "20486139", "20890839", "22068540", "23560931", "26542840",
    "27184599", "28398311", "28820135", "29788404", "31399121", "31882191", "31992387", "32015508",
    "32191675", "32474280", "32669681", "32860762", "33147627", "33316067", "33649511", "33828291",
    "33957064", "34108654", "34750572", "34774123", "35311562", "35365786", "35395576", "35630482",
    "35818472", "35930904", "36075919", "36076085", "36097170", "36227259", "36385137", "36423141",
    "36681102", "36683701", "36811098", "36811648", "37099616", "37129842", "37227251", "37508427",
    "37636268", "37749210", "37870287", "37977161", "37977162", "38020187", "38348304", "38407068",
    "38601602", "38716230", "38746185", "38840103", "39123217", "39160186", "39293510", "39299261",
    "39303692", "39317773", "39357172", "39742706", "39747833", "39878472", "40053686", "40183123",
    "40356662", "40516408", "40688383", "7542800"
]

def fetch_bibtex(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
        records = Medline.parse(handle)
        record = next(records)

        # Use FAU (full author name) field: "Last, First Middle"
        authors = record.get("FAU", [])
        formatted_authors = []
        for author in authors:
            parts = author.split(", ")
            if len(parts) == 2:
                last, first = parts[0].strip(), parts[1].strip()
                formatted_authors.append(f"{last}, {first}")
            else:
                # fallback: treat whole name as last name
                formatted_authors.append(author.strip())

        authors_bibtex = " and ".join(formatted_authors)

        bibtex_entry = f"@article{{{pmid},\n"
        bibtex_entry += f"  title={{ {record.get('TI', '').strip()} }},\n"
        bibtex_entry += f"  author={{ {authors_bibtex} }},\n"
        bibtex_entry += f"  journal={{ {record.get('JT', '')} }},\n"
        bibtex_entry += f"  year={{ {record.get('DP', '')[:4]} }},\n"
        bibtex_entry += f"  volume={{ {record.get('VI', '')} }},\n"
        bibtex_entry += f"  pages={{ {record.get('PG', '')} }},\n"
        bibtex_entry += f"  doi={{ {record.get('LID', '').split(' ')[0]} }},\n"
        bibtex_entry += f"  pmid={{ {pmid} }}\n"
        bibtex_entry += f"}}\n"
        return bibtex_entry

    except Exception as e:
        return f"% Failed to fetch PMID {pmid}: {e}\n"


def main():
    with open("pubmed_references.bib", "w", encoding="utf-8") as bibfile:
        for pmid in pmid_list:
            bibtex = fetch_bibtex(pmid)
            bibfile.write(bibtex + "\n")
            time.sleep(0.4)  # avoid hitting NCBI too quickly

    print("BibTeX entries saved to pubmed_references.bib")

if __name__ == "__main__":
    main()
