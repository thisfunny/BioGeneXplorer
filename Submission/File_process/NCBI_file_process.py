import os
import re


class NCBIFileProcess:
    def __init__(self, directory):
        self.directory = directory.replace("\\", "/")
        self.situ_list, self.cleaned_files = self.feature_check()

    def __repr__(self):
        return self.situ_list.__repr__()

    def seq_file_combine(self):
        """ Combines all the sequence files to a single file """
        with open("combined_seq.txt", "w") as combined_file:
            for seq in self.cleaned_files:
                with open(os.path.join(self.directory, seq), "r") as seq_file:
                    combined_file.write(seq_file.read() + "\n")

    def seq_modify(self):
        """ Returns a list dicts which include Query ID and isolate name """
        modifier_list = []
        for idx, seq in enumerate(self.cleaned_files):
            with open(os.path.join(self.directory, seq), "r") as file:
                query_id = file.readline()[5:].split(" ")[0]
                isolate_name = self.cleaned_files[idx].split(".")[0].replace("HP", "PS")
                modifier_list.append({query_id: isolate_name})
        return modifier_list

    @staticmethod
    def creat_empty_table():
        """ Creates an empty modifier table """
        if "modifier_table.txt" in os.listdir("D:/"):
            os.remove("D:/modifier_table.txt")
        table_title = ["Sequence_ID", "Country", "Isolation_source", "Isolate", "Strain"]
        with open("modifier_table.txt", "w") as modifier_table:
            modifier_table.write("\t".join(table_title))

    def add_modify_table(self):
        """ Adds features from modifier list to the modifier table """
        for records in self.seq_modify():
            for key, value in records.items():
                with open("D:/modifier_table.txt", "a") as modifier_table:
                    items = [key, "Iran", "Gastric Biopsy", value, value]
                    modifier_table.write("\n" + "\t".join(items))

    @staticmethod
    def orf_check(sequence):
        """ Checks the ORF if the Sequence is 5' partial """
        stop_codons = {"TAA", "TAG", "TGA"}

        for i in range(3):
            orf = re.findall(r".{3}", sequence[i:])

            if orf[-1] in stop_codons:
                orf.pop(orf.index(orf[-1]))
            if not any(codon in stop_codons for codon in orf):
                return f"ORF {i + 1}"

        return False

    def seq_check(self, strand, sequence):
        """ Checks sequence if it is complete or partial """
        stop_codon = {"TAA", "TAG", "TGA"}

        start = sequence[:3]
        stop = sequence[-3:]
        orf_result = self.orf_check(sequence)

        if start == "ATG" and stop in stop_codon:
            return f"{strand} Complete"
        elif start == "ATG" and stop not in stop_codon:
            return f"{strand} 3-partial"
        elif start != "ATG" and stop in stop_codon:
            return f"{strand} 5-partial {orf_result}"
        else:
            if orf_result:
                return f"{strand} 5&3-partial {orf_result}"
            else:
                return False

    @staticmethod
    def make_compliment(sequence):
        """ Generates the reverse complement of a DNA sequence """
        return sequence.translate(str.maketrans("ATCG", "TAGC"))

    @staticmethod
    def situ_control(situation_list):
        """ Indicates sequences with low quality """
        for idx, rec in enumerate(situation_list):
            for key, value in rec.items():
                if "False" in value:
                    situation_list.remove(rec)
                    return idx

    def feature_check(self):
        """ Returns a list of all Queries ID and their features for add features part in NCBI"""
        files = os.listdir(self.directory)

        situ_list = []

        for seq in files:
            with open(os.path.join(self.directory, seq), "r") as seq_file:
                query_id = seq_file.readline().strip()[5:].split(" ")[0]
                sequence = seq_file.read().replace("\n", "").strip()

                plus_situation = self.seq_check("Plus", sequence)
                if plus_situation:
                    situation = plus_situation
                else:
                    minus_sequence = self.make_compliment(sequence[::-1])
                    situation = self.seq_check("Minus", minus_sequence)

            situ_list.append({query_id: situation})

        del_idx = self.situ_control(situ_list)
        files.remove(files[del_idx])
        return situ_list, files


# Example
process = NCBIFileProcess(r"D:\Metagenomics\ABC_2")
process.seq_file_combine()
process.creat_empty_table()
process.add_modify_table()
print(process)
