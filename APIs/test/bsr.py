import numpy as np, tabula, pandas as pd, operator as op, sys, json
from flask import jsonify

def json_bankstatements(json_list):
    json_output = []
    for i in json_list:
        all_data = json.loads(i)
        all_data_values = all_data.values()
        all_statements = []
        for i in all_data_values: all_statements.append(i)
        json_output.append(all_statements)
    return json_output

def columns(cols, trans_list):
    trans_ind = []
    for i in range(len(cols)):
        for j in range(len(trans_list)):
            if cols[i] in trans_list[j]: data = cols[i]; trans_ind.append(i)
    return trans_ind

def tables(df,df_list):
	num_row = 0; pdf_data = []; pdf_data.append(list(df[num_row])); pdf_columns = list(df[num_row])
	for ls in range(len(df_list)-num_row): page_data = df[ls+num_row].values.tolist(); pdf_data = pdf_data + page_data
	data_pdf = pd.DataFrame(pdf_data); data_pdf = data_pdf.replace(np.nan,''); repete = data_pdf.shape[1]-len(pdf_columns)
	for _ in range(repete): pdf_columns.append('columns')
	return data_pdf

def unknown_columns(tab_cols,col_list):
	table_columns = []
	for elem in range(len(tab_cols)):
		if tab_cols[elem] in col_list: col_name = tab_cols[elem]; table_columns.append(col_name)
		else: table_columns.append('Unknown_column')
	return table_columns

def bank_statement_read(file_path, bank_name):
    
    if not sys.warnoptions: import warnings; warnings.simplefilter('ignore')
    pd.set_option('display.max_rows',None); pd.set_option('display.max_columns',None)
    
    try:
        df = tabula.read_pdf(file_path,pages='all',multiple_tables = True)
        df_list = df
        
        col_list = ['Description','Narration','Remarks','Particulars','DESCRIPTION','Description','Description','PARTICULARS','Transaction Details','Narration','NARRATION','PERTICULERS','Details of transaction','ransaction Remarks','Transaction\rParticulars','Transaction Description','ransaction Remarks','Account Description','NARATION','Narration Chq/Ref No','Deposits','Amount (Rs.)','Credit','CREDIT','Deposit Amt.','DEPOSIT','Deposit','Deposit Amount\r(INR )','Amount','Deposit Amt','Type','Deposit Balance','WithDrawal','Value','Credit (Rs.)','Withdrawal Amt. Deposit Amt.','Deposit Amount\r(INR )','Credit(Rs)','Withdrawals Deposits','Cr Amount','Withdrawal (Dr)/','Withdrawal Amt.','Withdrawal','Withdrawal','DEBIT','Withdrawals','Debit','Withdrawal (Dr)','Withdrawal Amt. Deposit Amt.','Withdrawal (Dr)/','Withdrawal Amount\r(INR )','Debit (Rs.)','Debit(Rs)','WITHDRAWALS','Withdrawal INR','Withdrawal Amt','Amount','Withdrawal Amount','Withdrawals Deposits','Dr Amount','Balance','Closing Balance','BALANCE','Running Balance','BALANCE','Balance (INR )','Amount','MODE**','Running','Balance(Rs)','Total Amount\rDr/Cr','Date','date','Transaction','Txn','Transaction Date','Debit/Credit','Transaction date','Txn Date','Tran Date','Balance (?)','Branch','Cheque No','Chq./Ref.','Entry Date','Cheque','TRANSACTION\rDATE','Trans Date','Tran Date','DATE','Post Date','Value\rDate','Date (Value\rDate)','Tran Date','Txn dt','Txn Dt','Value Date','Chq./Ref.No.','Value Dt','Chq\rNo.','Transaction Description','Total Amount\rDr/Cr','Debit (Rs.)','Credit (Rs.)','Balance (Rs.)','Dr Amount','Cr Amount','Instruments','Total Amou']
        
        date_list=['Date','date','Transaction','Txn','Transaction Date','Transaction date','Txn Date','Tran Date','Date','TRANSACTION\rDATE','Trans Date','Tran Date','DATE','Post Date','Value\rDate','Date (Value\rDate)','Txn dt','Txn Dt','Value Date']
        
        narration_list = ['Description','Narration','Remarks','Particulars','DESCRIPTION','Description','Description','PARTICULARS','Transaction Details','Narration','NARRATION','PERTICULERS','Details of transaction','ransaction Remarks','Transaction\rParticulars','Transaction Description','ransaction Remarks','Account Description','NARATION','Narration Chq/Ref No']
        
        credit_list = ['Deposits','Amount (Rs.)','Credit','CREDIT','Deposit Amt.','DEPOSIT','Deposit','Deposit Amount\r(INR )','Amount','Credit (Rs.)','Withdrawal Amt. Deposit Amt.','Deposit Amount\r(INR )','Credit(Rs)','Withdrawals Deposits','Cr Amount','Withdrawal (Dr)/','DEPOSITS','WITHDRAWALS']
        
        debit_list = ['Withdrawal Amt.','Withdrawal','Withdrawal','DEBIT','Withdrawals','Debit','Withdrawal (Dr)','Withdrawal Amt. Deposit Amt.','Withdrawal (Dr)/','Withdrawal Amount\r(INR )','Debit (Rs.)','Debit(Rs)','WITHDRAWALS','Withdrawal INR','Withdrawal Amt','Amount','Withdrawal Amount', 'Withdrawals Deposits','WithDrawal','Dr Amount']
        
        balance_list = ['Balance','Closing Balance','BALANCE','Running Balance','BALANCE','Balance (INR )','Amount','Running','Balance(Rs)','Total Amount\rDr/Cr']
        
        test_data = df_list[0]
        col_len = test_data.shape[1]
        tab_cols = test_data.columns; table_columns = []
        row_index = []
        table_columns = unknown_columns(tab_cols,col_list)
        uc_count = op.countOf(table_columns,'Unknown_column')

        if uc_count >= 3 or len(table_columns)<=3:
            for row_ind in range(col_len-1):
                test_list = list(test_data[tab_cols[row_ind]])
                for i in range(len(col_list)):
                    col_el = col_list[i]
                    if col_el in test_list: row_inde = test_list.index(col_el); row_index.append(row_inde)
            
            if len(row_index) == 0:
                lst_no = 0 if len(df_list) <= 4 else 4; data1 = df_list[1]; data2 = df_list[2]; data3 = df_list[lst_no]
                data1_columns = []; data2_columns = []; data3_columns = []; 
                
                page_data1 = data1.values.tolist(); page_data2 = data2.values.tolist(); page_data3 = data3.values.tolist(); 
                data1_cols = data1.columns; data2_cols = data2.columns; data3_cols = data3.columns; 
                
                data1_columns = unknown_columns(data1_cols,col_list); data1_count = op.countOf(data1_columns,'Unknown_column')
                data2_columns = unknown_columns(data2_cols,col_list); data2_count = op.countOf(data1_columns,'Unknown_column')
                data3_columns = unknown_columns(data3_cols,col_list); data3_count = op.countOf(data1_columns,'Unknown_column')
                
                data_uc_count = [data1_count,data2_count,data3_count]; min_uc_index = data_uc_count.index(min(data_uc_count))
                dict_cols = {0:data1_columns,1:data2_columns,2:data3_columns}; dict_data = {0:data1,1:data2,2:data3}
                data_tab_cols = dict_cols[min_uc_index]; data_first = dict_data[min_uc_index]; page_data0 = data_first.values.tolist()
                pdf_data = []
                pdf_data = pdf_data + page_data0 + page_data1 + page_data2 + page_data3
                
                for ls in range(len(df_list)): page_data = df[ls].values.tolist(); pdf_data = pdf_data + page_data
                data1_pdf = pd.DataFrame(pdf_data); repete = data1_pdf.shape[1]-len(data_tab_cols)
                
                for _ in range(repete): data_tab_cols.append('column_added')
                pdf_data = pd.DataFrame(pdf_data,columns = data_tab_cols); data_pdf = pdf_data.replace(np.nan,''); com_table = data_pdf; new_com_table = data_pdf
            
            elif min(row_index) >= 2:
                test_data1 = test_data.values.tolist(); row_value = min(row_index); data_col_list = test_data1[row_value] + test_data1[row_value+1]; columns_list=[]; row_columns=[]
                for elem in range(len(data_col_list)): list_txt = list(str(data_col_list[elem]).split()); columns_list = columns_list + list_txt
                
                for elem in range(len(columns_list)):
                    if columns_list[elem] in col_list: col_name = columns_list[elem]; row_columns.append(col_name)
                data1 = df_list[1]; data1 = data1.values.tolist()
                
                for lst_len in range(len(df_list)): page_data = df_list[lst_len]; page_data = page_data.values.tolist(); data1 = data1 + page_data
                pdf_data1 = pd.DataFrame(data1); repete = pdf_data1.shape[1]-len(row_columns)
                
                for _ in range(repete): row_columns.append('column_added')
                pdf_data = pd.DataFrame(data1,columns = row_columns); pdf_data = pdf_data.replace(np.nan,''); com_table = pdf_data; new_com_table = pdf_data
            
            else: data_pdf = tables(df,df_list); com_table = data_pdf.rename(columns = data_pdf.iloc[0]).drop(data_pdf.index[0]);new_com_table=data_pdf.rename(columns=data_pdf.iloc[0]).drop(data_pdf.index[0])
        
        else: data_pdf = tables(df,df_list); com_table = data_pdf.rename(columns=data_pdf.iloc[0]).drop(data_pdf.index[0]); new_com_table = data_pdf.rename(columns=data_pdf.iloc[0]).drop(data_pdf.index[0])
            
        cols = list(com_table.columns); cols1 = list(new_com_table.columns); trans_list = [date_list,narration_list,credit_list,debit_list,balance_list]; trans_ind = columns(cols,trans_list); 
        Transaction_date = list(com_table[cols[trans_ind[0]]]); Narration = list(com_table[cols[trans_ind[1]]]); Deposits = list(com_table[cols[trans_ind[2]]]); Debit = list(com_table[cols[trans_ind[3]]]); Balance = list(com_table[cols[trans_ind[4]]]); 
        trans_data = pd.DataFrame(Transaction_date,columns = ['Transaction Date']); nar_data = pd.DataFrame(Narration,columns = ['Narration']); cred_data = pd.DataFrame(Deposits,columns = ['Credit']); debt_data = pd.DataFrame(Debit,columns = ['Debit']); bal_data = pd.DataFrame(Balance,columns = ['Balance'])
        data = trans_data.join(nar_data); data = data.join(cred_data); data = data.join(debt_data); data = data.join(bal_data); data = data.replace(np.nan,'')
        
        axis_list=['axis-bank','Axis Bank  India','Axis Bank  India','AXIS (UTI) Bank','Axis Bank India','Axis Bank, India','Axis Ban','Axis Bank','Axis Bank Ltd','Axis Bank Ltd.','Axis Bank ','Axis','axis','AXIS']
            
        if bank_name in axis_list:
            for ele in range(len(Narration)-1):
                if Transaction_date[ele] == '' and Balance[ele] == '': Narration[ele+1] = str(Narration[ele]) + str(Narration[ele+1])
        else:   
            for ele in range(len(Narration)):
                if Transaction_date[ele] == '': Narration[ele-1] = str(Narration[ele-1]) + str(Narration[ele])
        
        Transaction_date = pd.DataFrame(Transaction_date,columns = ['Transaction Date']); Narration = pd.DataFrame(Narration,columns = ['Narration']); Deposits = pd.DataFrame(Deposits,columns = ['Credit']); Debit = pd.DataFrame(Debit,columns = ['Debit']); Balance = pd.DataFrame(Balance,columns = ['Balance']); 
        data = Transaction_date.join(Narration); data = data.join(Deposits); data = data.join(Debit); data = data.join(Balance); txn_date = list(data['Transaction Date']); cr_list = list(data['Credit']); dr_list = list(data['Debit']); bls_list = list(data['Balance']); row_index = []
        
        for row_num in range(len(data['Narration'])):
            if txn_date[row_num] == '': a = row_num; row_index.append(a)
            elif cr_list[row_num] == '' and dr_list[row_num] == '' and bls_list == '': b = row_num; row_index.append(b)
        unique_row_index=[]
        
        for x in range(len(row_index)):
            if row_index[x] not in unique_row_index: row_ind = row_index[x]; unique_row_index.append(row_ind)
        data = data.drop(unique_row_index,axis=0); salary1 = data[data['Narration'].str.contains('SALARY')]; salary2 = data[data['Narration'].str.contains('Salary')]; salary3 = data[data['Narration'].str.contains('salary')]; sal_ac = data[data['Narration'].str.contains('SAL')]; sal_fl = data[data['Narration'].str.contains('Sal')]; NEFT = data[data['Narration'].str.contains('NEFT')]; IMPS = data[data['Narration'].str.contains('IMPS')]; sal = sal_ac.append(sal_fl); salary = salary1.append(salary2); salary = salary.append(salary3); salary = salary.append(sal); 
        salary = salary.drop_duplicates(subset='Narration'); 
        UPI = data[data['Narration'].str.contains('UPI')]; NACH = data[data['Narration'].str.contains('NACH')]; ACH = data[data['Narration'].str.contains('ACH')]; NACH = NACH.append(ACH); 
        main_tab = salary.append(NACH); main_tab = main_tab.append(NEFT); main_tab = main_tab.append(IMPS); main_tab = main_tab.append(UPI); main_tab = main_tab.reset_index(); main_tab = main_tab.drop(['index'],axis=1); 
        ecs = ['ECSRTN','ECSRTNCHGS','NACH_AD,RTN_CHRG','ACH DEBIT RETURN CHARGES','EMI RTN CHARGES','NACH RTN CHG','Chrg:Ecs Return','Chrg:Ecs Mandate','ECS DR RTN','NACH RETURN CHARGES','ECS Return','Bounce Charges','ACH RTN','Debit Return Charges','NACH Return','RTN Charges','ECS/ACH RETURN','ACH D','ACH RETURN','ACH DEBIT RETURN'];fantasy_gaming=['Rummy','rummy','Junglee','junglee','Mpl','mpl','Dream11','dream11','Adda52','adda52','Ace2three','ace2three','Poker','poker','Rummy Circle','Pokerbaazi','pokerbaazi','Ace2Three','My11Circle']; 
        ecs_rtn = data[data['Narration'].str.contains('ECSRTN')]; ecs_col = list(ecs_rtn.columns); ecs_rtn_data = ecs_rtn.values.tolist()
        
        for es in range(len(ecs)): ecs_name = ecs[es]; ecs1 = data[data['Narration'].str.contains(ecs_name)]; ecs1_data = ecs1.values.tolist(); ecs_list = ecs_rtn_data + ecs1_data
        ecs_tab = pd.DataFrame(ecs_list,columns = ecs_col); gaming = data[data['Narration'].str.contains('ummy')]; gm_col = list(gaming.columns); gm_rtn_data = gaming.values.tolist()
        
        for es in range(len(fantasy_gaming)): gm_name = fantasy_gaming[es]; gm1 = data[data['Narration'].str.contains(gm_name)]; gm1_data = gm1.values.tolist(); gm_list = gm_rtn_data + gm1_data
        gm_tab = pd.DataFrame(gm_list,columns = gm_col)
        data_frame = data.to_json(); 
        bankData = data.T; data_json = bankData.to_json(); upi_json = UPI.T.to_json(); sal_json = salary.T.to_json(); neft_json = NEFT.T.to_json(); imps_json = IMPS.T.to_json(); nach_json = NACH.T.to_json()
        json_list = [data_json, sal_json, upi_json, nach_json, neft_json, imps_json]; 
        json_out = json_bankstatements(json_list)

        bsr_data = {
            "statements" : json_out[0],
            "salary" : json_out[1],
            "upi" : json_out[2],
            "nach" : json_out[3],
            "neft" : json_out[4],
            "imps" : json_out[5]
        }

        return bsr_data
    
    except:
        resp = jsonify({'status':'failed', 'message' : 'Allowed file types are png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
    