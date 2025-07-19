import time

from model.DB.db_model import DB
from model.entity.StatisticalReport import StatisticalReport

class StatisticalResultProcess:
    def __init__(self):
        self.db = DB()

    def analyze_genes(self):
        table_names = self.db.search_all_result_table_names()
        print(table_names)

        for table_name in table_names:
            total_blasts = self.db.search_row_counts(table_name)
            total_blasts = total_blasts[0]
            print("total_blasts", total_blasts)
            total_count = self.db.search_row_counts_distinct_name(table_name)
            total_count = total_count[0]
            print("total_count", total_count)

            Total_Count_of_Gene_Occurrence_Across_All_Isolates = self.db.search_Total_Count_of_Gene_Occurrence_Across_All_Isolates(table_name)
            print("Total_Count_of_Gene_Occurrence_Across_All_Isolates", Total_Count_of_Gene_Occurrence_Across_All_Isolates)
            Number_of_Isolates_Containing_Duplicate_Genes = Total_Count_of_Gene_Occurrence_Across_All_Isolates - self.db.search_Number_of_Isolates_Containing_Duplicate_Genes(table_name)
            print("Number_of_Isolates_Containing_Duplicate_Genes", Number_of_Isolates_Containing_Duplicate_Genes)
            cutoff_count = (total_blasts - Total_Count_of_Gene_Occurrence_Across_All_Isolates)
            if total_blasts == 0:
                continue
            else:
                cutoff_percentage = (cutoff_count / total_blasts) * 100 if total_count else 0
                Percentage_of_Gene_Occurrence_Across_All_Isolates = (Number_of_Isolates_Containing_Duplicate_Genes / total_count) * 100 if total_count else 0

            Number_of_Alleles = self.db.search_duplicate_gene_count(table_name)
            Number_of_Repeated_Alleles = (Total_Count_of_Gene_Occurrence_Across_All_Isolates - Number_of_Alleles)
            if Total_Count_of_Gene_Occurrence_Across_All_Isolates == 0:
                continue
            else:
                Percentage_of_Repeated_Alleles = (Number_of_Repeated_Alleles / Total_Count_of_Gene_Occurrence_Across_All_Isolates) * 100 if total_count else 0
                Percentage_of_Alleles = (Number_of_Alleles / Total_Count_of_Gene_Occurrence_Across_All_Isolates) * 100 if total_count else 0

            # Insert or update analysis results in gene_analysis table
            statistical_report = StatisticalReport(table_name, cutoff_count, cutoff_percentage, Number_of_Repeated_Alleles, Percentage_of_Repeated_Alleles, Total_Count_of_Gene_Occurrence_Across_All_Isolates,
            Percentage_of_Gene_Occurrence_Across_All_Isolates, Number_of_Alleles, Percentage_of_Alleles, Number_of_Isolates_Containing_Duplicate_Genes)

            self.db.insert_statistical_result_table(statistical_report)

        print("Analysis complete.")
