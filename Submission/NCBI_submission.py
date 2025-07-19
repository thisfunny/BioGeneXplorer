from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from File_process.NCBI_file_process import *
import os


class NCBISubmission:
    def __init__(self, timeout=10, retries=1, gene_name=None):
        for attempt in range(retries):
            try:
                self.driver = webdriver.Chrome() # Todo: Headless need to be added
                self.url = "https://account.ncbi.nlm.nih.gov/?back_url=https%3A%2F%2Fwww.ncbi.nlm.nih.gov%2F"
                self.timeout = timeout
                self.process = NCBIFileProcess(f"D:/Metagenomics/{gene_name}") # Todo: change address
                # self.features, self.files = self.process.feature_check()
                self.process.seq_file_combine()
                self.process.creat_empty_table()
                self.process.add_modify_table()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")

    def get_url(self):
        self.driver.get(self.url)

    def click_element(self, method, address, retries=3, massage=None):
        for attempt in range(retries):
            try:
                click_button = WebDriverWait(self.driver, self.timeout).until(
                    ec.element_to_be_clickable((method, address)))
                return click_button.click()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e} massage: {massage}")

    def alert(self):
        try:
            alert = WebDriverWait(self.driver, self.timeout).until(ec.alert_is_present())
            return alert.accept()
        except Exception as e:
            print(f"Error: {e}, alert was not found")

    def locate_element(self, address):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                ec.presence_of_element_located((By.ID, address)))
        except Exception as e:
            print(f"Error: {e}")

    def add_author(self, author_list):
        for index, author in enumerate(author_list):
            first_name = self.locate_element(f"author_first_000{index + 1}")
            first_name.send_keys(author.split()[0])

            if len(author.split()) == 3:
                middle_name = self.locate_element(f"author_middle_000{index + 1}")
                middle_name.send_keys(author.split()[1])

                last_name = self.locate_element(f"author_last_000{index + 1}")
                last_name.send_keys(author.split()[2])
            else:
                last_name = self.locate_element(f"author_last_000{index + 1}")
                last_name.send_keys(author.split()[1])

            self.click_element(By.ID, "add_author")

    def select_molecule_type(self, selected_type):
        comb = self.locate_element("mol_type")
        Select(comb).select_by_value(selected_type)

    def add_organism(self, organism):
        self.locate_element("organism").send_keys(organism)

    @staticmethod
    def file_dir(directory):
        return os.path.abspath(directory)

    def add_seq_file(self):
        self.locate_element("dnaseq_file").send_keys(self.file_dir("D:/combined_seq.txt")) # Todo: change address

    def add_modifier_file(self):
        self.locate_element("smod_grid_file_1").send_keys(self.file_dir("D:/modifier_table.txt")) # Todo: change address

    def login(self, username, password):
        self.locate_element("username-input").send_keys(username)
        self.locate_element("password").send_keys(password)
        self.click_element(By.ID, "signin-button")

    def creat_situ_set(self):
        situ_set = set()
        for situ in self.process.situ_list:
            for key, value in situ.items():
                situ_set.add(value)

        return situ_set

    def enter_add_feature(self):
        label_list = ["label[for='itype_form_radio']", "label[for='feat_selection_CDS_radio']",
                      "label[for='cds_by_interval_radio']"]
        for label in label_list:
            self.click_element(By.CSS_SELECTOR, label)

        self.click_element(By.ID, "id_add")

    def enter_feature_params(self, protein_name, gene_name):
        self.click_element(By.CSS_SELECTOR, "label[for='feat_0_ilessgene_radio_y']")
        self.locate_element("feat_0_prot_name").send_keys(protein_name)
        self.locate_element("feat_0_gene_name").send_keys(gene_name)

    def enter_query(self, situ):
        self.click_element(By.CSS_SELECTOR, "label[for=feat_0_apply_seq_radio_specific]")
        for record in self.process.situ_list:
            for query_id, feature in record.items():
                if situ in feature:
                    comb = self.locate_element("feat_0_allseqs_select")
                    Select(comb).select_by_visible_text(query_id)
                    self.click_element(By.ID, "id_addToFeat")

    def add_feature(self, protein_name, gene_name):
        situ_set = self.creat_situ_set()

        for situ in situ_set:
            self.enter_add_feature()
            self.enter_feature_params(protein_name, gene_name)
            if situ == "Plus Complete":
                self.enter_query("Plus Complete")
            elif situ == "Minus Complete":
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_default_strand_radio_n")
                self.enter_query("Minus Complete")
            elif situ == "Plus 3-partial":
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_3prime]")
                self.enter_query("Plus 3-partial")
            elif situ == "Minus 3-partial":
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_default_strand_radio_n")
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_3prime]")
                self.enter_query("Minus 3-partial")
            elif "Plus 5-partial" in situ:
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_5prime]")
                self.click_element(By.CSS_SELECTOR, f"label[for=feat_0_rframe_radio_{situ.split()[3]}")
                self.enter_query(f"Plus 5-partial ORF {situ.split()[3]}")
            elif "Minus 5-partial" in situ:
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_default_strand_radio_n")
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_5prime]")
                self.click_element(By.CSS_SELECTOR, f"label[for=feat_0_rframe_radio_{situ.split()[3]}")
                self.enter_query(f"Minus 5-partial ORF {situ.split()[3]}")
            elif "Plus 5&3-partial" in situ:
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_5prime]")
                self.click_element(By.CSS_SELECTOR, f"label[for=feat_0_rframe_radio_{situ.split()[3]}")
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_3prime]")
                self.enter_query(f"Plus 5&3-partial ORF {situ.split()[3]}")
            elif "Minus 5&3-partial" in situ:
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_default_strand_radio_n")
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_5prime]")
                self.click_element(By.CSS_SELECTOR, f"label[for=feat_0_rframe_radio_{situ.split()[3]}")
                self.click_element(By.CSS_SELECTOR, "label[for=feat_0_3prime]")
                self.enter_query(f"Minus 5&3-partial ORF {situ.split()[3]}")

            self.click_element(By.ID, "id_feat_accept")

    def continue_button(self, count=1):
        for i in range(count):
            self.click_element(By.NAME, "cmd")

    def close(self):
        self.driver.quit()
