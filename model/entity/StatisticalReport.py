import json

class StatisticalReport:
    def __init__(self, gene_name, Total_Count_of_Gene_Occurrence_Across_All_Isolates, Percentage_of_Gene_Occurrence_Across_All_Isolates, cutoff_count, cutoff_percentage,
                 Number_of_Repeated_Alleles, Percentage_of_Repeated_Alleles, Number_of_Alleles, Percentage_of_Alleles,
                 Number_of_Isolates_Containing_Duplicate_Genes):
        self.gene_name = gene_name
        self.Total_Count_of_Gene_Occurrence_Across_All_Isolates = Total_Count_of_Gene_Occurrence_Across_All_Isolates
        self.Percentage_of_Gene_Occurrence_Across_All_Isolates = Percentage_of_Gene_Occurrence_Across_All_Isolates
        self.cutoff_count = cutoff_count
        self.cutoff_percentage = cutoff_percentage
        self.Number_of_Repeated_Alleles = Number_of_Repeated_Alleles
        self.Percentage_of_Repeated_Alleles = Percentage_of_Repeated_Alleles
        self.Number_of_Alleles = Number_of_Alleles
        self.Percentage_of_Alleles = Percentage_of_Alleles
        self.Number_of_Isolates_Containing_Duplicate_Genes = Number_of_Isolates_Containing_Duplicate_Genes

    def __repr__(self):
        return json.dumps(self.__dict__)
