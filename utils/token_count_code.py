import tiktoken


def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    token_count = len(encoding.encode(text))
    return token_count


text = """create table transaction (id bigint PK, txn_id varchar(40), client_ref_num varchar(50), destination varchar, access_date date, start_time datetime(6), end_time datetime(6), token_expires_on datetime(6), statement_start_month varchar(10), statement_end_month varchar(10), txn_completed_cburl varchar(500), return_url varchar(500), txn_token varchar(300), acceptance_policy varchar(100), report_url varchar(500), client_id int, client_request_id bigint, institution_id bigint, txn_status_id int, access_date_ist date, bank_auto_detected tinyint(1), relaxation_days smallint, report_subtype enum('type1','type2','type3','type4','aa_type','type5','type6','type7','type8','type9','type10','type11'), report_type enum('json','xlsx','xml','pdf'), scanned_statements tinyint(1), tamper_detection enum('NONE','PDF','PDF_2','BOTH','BOTH_2','BOTH_3'), employer_details varchar(5000), max_pages_in_pdf int, req_institution_id bigint, category_version varchar(5), email_access_token varchar(300), income_tax_doc varchar(100), is_new_nb_enabled tinyint(1), stmt_cron_run tinyint(1), txn_callback tinyint(1), is_deleted tinyint(1), v2_institution_id varchar(100), req_v2_institution_list varchar(50), multi_account_support_required tinyint(1), multi_stmt_inst_id varchar(100), bs_testing_required tinyint(1), compressed_selection_enabled smallint, multi_selection_enabled smallint, complete_stmt_parsing_required tinyint(1), parsing_mode smallint)"""
model = "t5-small"  # Replace with your model, e.g., "gpt-3.5-turbo", "gpt-4"
tokens = count_tokens(text, model)
print(f"Number of tokens: {tokens}")