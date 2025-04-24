from model.BL.MainProcess import MainProcess

if __name__ == '__main__':
    gene_sample_path = r'C:\Users\mrnaj\OneDrive\Desktop\genes sample'
    genome_sample_path = r'C:\Users\mrnaj\OneDrive\Desktop\whole_genome'

    main_process = MainProcess(gene_sample_path, genome_sample_path, create_drop=False)
    main_process.process()
