from Submission.NCBI_submission import *
import time

driver = NCBISubmission(gene_name="ABC_2")
driver.get_url()

driver.click_element(By.CLASS_NAME, "orcid")

driver.login("0000000317298256",
             "@Pargolparyas1400")
driver.click_element(By.ID, "deny-button")

driver.click_element(By.CLASS_NAME, "gray-light")
driver.click_element(By.CLASS_NAME, "toolbox-submit-link")
driver.click_element(By.ID, "id_sub_new")
driver.click_element(By.ID, "create-new-submission-anyway")

driver.click_element(By.CSS_SELECTOR, "label[for='id_submission_type-organism_or_material_0']")
driver.click_element(By.CSS_SELECTOR, "label[for='id_submission_type-prok_seqs_contain_3']")
driver.click_element(By.ID, "link_to_websub_genbank")

driver.click_element(By.ID, "id_sub_new")
driver.alert()
driver.continue_button(1)

author_list = ["Parastoo Saniee", "Ali Roshandel"]
driver.add_author(author_list)
driver.click_element(By.ID, "id_sub_continue")

driver.click_element(By.CSS_SELECTOR, "label[for='seqtech_original_box_illumina']")
driver.click_element(By.CSS_SELECTOR, "label[for='seqtech_assembled_radio']")
driver.locate_element("asmb_prog_0001").send_keys("FASTQC")
driver.locate_element("asmb_vers_0001").send_keys("v9.11")
driver.click_element(By.NAME, "cmd")

driver.locate_element("release_date").send_keys("20-Feb-2026")
driver.select_molecule_type("1D")
driver.add_seq_file()
driver.continue_button(1)

driver.add_organism("Helicobacter pylori")
driver.continue_button(2)

driver.click_element(By.CSS_SELECTOR, "label[for='set_type_radio_pop']")
driver.continue_button(2)

driver.click_element(By.CSS_SELECTOR, "label[for='bact_radio_cult']")
driver.click_element(By.CSS_SELECTOR, "label[for='smod_grid_file_radio']")
driver.add_modifier_file()
driver.continue_button(2)

driver.add_feature("Protein", "ABC_2")
driver.click_element(By.ID, "id_sub_continue")

time.sleep(10000000)
