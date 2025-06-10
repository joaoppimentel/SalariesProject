def highest_avarage(df, year, column):
    
    if year == 'All':
        column_average = df.groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column}',
            value= f'{salary}$ | {column_name}'
        )  
    elif (year-1) in df['work_year'].values:
        column_average_current_year = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        column_average_last_year = df.loc[df['work_year'] == year-1].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column_current_year = column_average_current_year.iloc[column_average_current_year['average_salary'].idxmax()]
        highest_column_last_year = column_average_last_year.iloc[column_average_last_year['average_salary'].idxmax()]
        salary_current_year = round(highest_column_current_year['average_salary'], 2)
        salary_last_year = round(highest_column_last_year['average_salary'], 2)
        delta = round(salary_current_year - salary_last_year, 2)
        column_current_year = highest_column_current_year[column]
        column_last_year = highest_column_last_year[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column}',
            value=f'{salary_current_year}$ | {column_current_year}',
            delta=f'{delta}$ | {column_last_year}'
        )
    else:
        column_average = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column}',
            value= f'{salary}$ | {column_name}'
        )