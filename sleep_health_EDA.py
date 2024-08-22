import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df  = pd.read_csv(r'C:\Users\Wiktoria\Desktop\Python Basics\Project5_Pandas\sleep_health_dataset.csv', keep_default_na=False)

df.shape
df.head()
df.info()
pd.set_option('display.max_columns', None)
df.describe()
df.isna().any()

df = df.drop(columns='Person ID')


#SLEEP DISORDER
disorder_count=df['Sleep Disorder'].value_counts()

plt.figure()
plt.pie(disorder_count, labels=disorder_count.index, colors = ['yellowgreen', 'darkred', 'skyblue'],
        autopct='%1.1f%%', shadow=False, startangle=70)
plt.title('Distribution of Sleep Disorder', fontsize=14, fontweight='bold')

custom_palette = ['#8ee553', '#e21916', '#4fd1de']

plt.figure()
sns.countplot(x='Sleep Disorder', data=df, palette=custom_palette)
plt.title('Distribution of Sleep Disorders')
plt.xlabel('Sleep Disorder')
plt.ylabel('Count')
plt.show()


#GENDER
gender_count=df['Gender'].value_counts()

plt.figure()
plt.pie(gender_count, labels=gender_count.index, colors = ['dodgerblue', 'orchid'],
        autopct='%1.1f%%', shadow=False, startangle=90)
plt.title('Gender Distribution', fontsize=14, fontweight='bold')


gender_sleep_disorder = df.groupby(['Gender', 'Sleep Disorder']).size().unstack(fill_value=0)

colors = ['#4fd1de', '#8ee553', '#e21916']

plt.figure()
gender_sleep_disorder.plot(kind='bar', stacked=True, color=colors)
plt.title('Distribution of sleep disorders by gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')


#AGE
plt.figure()
df['Age'].hist(bins=50)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Count')

plt.figure()
sns.boxplot(x='Sleep Disorder', y='Age', data=df, palette=custom_palette)
plt.title('Boxplot')
plt.xlabel('Sleep Disorder')
plt.ylabel('Age')

bins = [25, 30, 35, 40, 45, 50, 55, 60]
labels = ['25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60']

df['Age Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

age_sleep_disorder = df.groupby(['Age Range', 'Sleep Disorder']).size().unstack(fill_value=0)

age_sleep_disorder_perc = age_sleep_disorder.apply(lambda x: x / x.sum(), axis=1) * 100


plt.figure()
age_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Percentage distribution of sleep disorders by age ranges')
plt.xlabel('Age Range')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')


#OCCUPATION
occupation_count = df['Occupation'].value_counts()

plt.figure()
sns.countplot(x='Occupation', data=df, palette='viridis')
plt.title('Distribution of occupations')
plt.xlabel('Occupation')
plt.ylabel('Count')

def categorize_occupation(occupation):
    if occupation in ['Nurse', 'Doctor']:
        return 'Medicine'
    elif occupation in ['Engineer', 'Software Engineer', 'Scientist']:
        return 'Technology and Engineering'
    elif occupation in ['Lawyer']:
        return 'Law'
    elif occupation in ['Accountant', 'Salesperson', 'Sales Representative', 'Manager']:
        return 'Business and Finance'
    else:
        return 'Education'
    

df['Occupation Group'] = df['Occupation'].apply(categorize_occupation)

occupation_sleep_disorder = df.groupby(['Occupation Group', 'Sleep Disorder']).size().unstack(fill_value=0)

occupation_sleep_disorder_perc = occupation_sleep_disorder.apply(lambda x: x/x.sum(), axis=1) * 100

plt.figure()
occupation_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Percentage distribution of Sleep Disorders by Occupation Group')
plt.xlabel('Occupation Group')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')


#SLEEP DURATION
plt.figure()
df['Sleep Duration'].hist(bins=20)
plt.title('Distribution of sleep duration')
plt.xlabel('Sleep Duration [hours]')
plt.ylabel('Count')

mean_sleep_duration = df.groupby('Sleep Disorder')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration.plot(kind='bar', color=colors)
plt.title('Average sleep duration for each sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Average sleep duration [hours]')

plt.figure()
sns.violinplot(x='Sleep Disorder', y='Sleep Duration', data=df, palette=custom_palette)
plt.title('Sleep duration for each sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Sleep Duration')

#SLEEP DURATION IN GENDER
mean_sleep_duration_by_gender = df.groupby('Gender')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration_by_gender.plot(kind='bar', color=['dodgerblue', 'orchid'])
plt.title('Average Sleep Duration by Gender')
plt.xlabel('Gender')
plt.ylabel('Average sleep duration [hours]')

mean_sleep_duration_by_occup = df.groupby('Occupation Group')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration_by_occup.plot(kind='bar', color=['#357dbd', '#15a28f', '#1c9a50', '#e9c825', '#a21a0e'])
plt.title('Sleep duration by occupation')
plt.xlabel('Occupation Group')
plt.ylabel('Average sleep duration [hours]')

#QUALITY OF SLEEP - TARGET
plt.figure()
df['Quality of Sleep'].hist(bins=20)
plt.title('Distribution of Quality of Sleep')
plt.xlabel('Quality of Sleep')
plt.ylabel('Count')

quality_of_sleep = df.groupby('Sleep Disorder')['Quality of Sleep'].mean()

plt.figure()
sns.barplot(x='Sleep Disorder', y='Quality of Sleep', data=df, palette=custom_palette)
plt.title('Average Quality of Sleep by Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Average Quality of Sleep')

quality_of_sleep_age = df.groupby('Age Range')['Quality of Sleep'].mean()

plt.figure()
quality_of_sleep_age.plot(kind='line', marker='o', color='blue')
plt.title('Average quality of sleep by age')
plt.xlabel('Age Range')
plt.ylabel('Average Quality of Sleep')

#PHYSICAL ACTIVITY LEVEL
plt.figure()
df['Physical Activity Level'].hist(bins=30)
plt.title('Distribution of physical acitivity')
plt.xlabel('Physical Activity Level [minutes/day]')
plt.ylabel('Count')

activity_gender_age = df.groupby(['Age Range', 'Gender'])['Physical Activity Level'].mean().reset_index()

plt.figure()
sns.barplot(x='Age Range', y='Physical Activity Level', hue='Gender',
            data=activity_gender_age, palette='viridis')
plt.title('Average daily physical activity by age range and gender')
plt.xlabel('Age Range')
plt.ylabel('Physical Activity Level [minutes/day]')
plt.legend(title='Gender')

activity_by_occup = df.groupby('Occupation Group')['Physical Activity Level'].mean().reset_index()

plt.figure()
sns.barplot(x='Occupation Group', y='Physical Activity Level', data=activity_by_occup, palette='pastel')
plt.title('Average daily physical activity by occupation')
plt.xlabel('Occupation Group')
plt.ylabel('Physical Activity Level [minutes/day]')

sleep_quality_activity_corr = df['Quality of Sleep'].corr(df['Physical Activity Level'])

plt.figure()
sns.lineplot(x='Physical Activity Level', y='Quality of Sleep', hue='Gender', data=df)
plt.title('Correlation between Physical Activity Level and Quality of Sleep by Gender')
plt.xlabel('Physical Activity Level [minutes/day]')
plt.ylabel('Quality of Sleep')

insomnia_data = df.groupby('Sleep Disorder')['Physical Activity Level'].mean().reset_index()

palette = ['#4fd1de', '#8ee553', '#e21916']

plt.figure()
sns.barplot(x='Sleep Disorder', y='Physical Activity Level', data=insomnia_data, palette=palette)
plt.title('Average daily physical activity by sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Physical Activity Level [minutes/day]')


#STRESS LEVEL
plt.figure()
df['Stress Level'].hist(bins=50)
plt.title('Distribution of stress level')
plt.xlabel('Stress Level')
plt.ylabel('Count')


plt.figure()
sns.barplot(x='Sleep Disorder', y='Stress Level', hue='Gender', data=df, palette='viridis')
plt.title('Stress Level by Sleep Disorder and Gender')
plt.xlabel('Sleep Disorder')
plt.ylabel('Stress Level')
plt.legend(title='Gender')

mean_stress_by_age_occup = df.groupby(['Age Range', 'Occupation Group'])['Stress Level'].mean().reset_index()


plt.figure()
sns.lineplot(x='Age Range', y='Stress Level', hue='Occupation Group', data=mean_stress_by_age_occup, marker='o', palette='viridis', linewidth=2.5)
plt.title('Average stress level by Age Range')
plt.xlabel('Age Range')
plt.ylabel('Average stress level')
plt.legend(title='Occupation Group')

plt.figure()
sns.lineplot(x='Stress Level', y='Quality of Sleep', hue='Gender', data=df, palette='viridis')
plt.title('Correlation between stress level and quality of sleep by gender')
plt.xlabel('Stress Level')
plt.ylabel('Quality of Sleep')

#BMI CATEGORY
df['BMI Category'].value_counts()

df['BMI Category'] = df['BMI Category'].replace({
    'Normal Weight': 'Normal'
    })

df['BMI Category'].value_counts()

plt.figure()
df['BMI Category'].hist(bins=50)
plt.title('Distribution of BMI Category')
plt.xlabel('BMI Category')
plt.ylabel('Count')

plt.figure()
sns.barplot(x='Sleep Disorder', y='Age', hue='BMI Category', data=df, palette='plasma')
plt.title('BMI by sleep disorder and age')
plt.xlabel('Sleep Disorder')
plt.ylabel('Age')
plt.legend(title='BMI Category')

df_bmi_encoded = pd.get_dummies(df['BMI Category'])

df = pd.concat([df, df_bmi_encoded], axis=1)

df['Normal'] = df['Normal'].astype(int)
df['Obese'] = df['Obese'].astype(int)
df['Overweight'] = df['Overweight'].astype(int)


bmi_columns = [col for col in df.columns if col in ['Normal', 'Obese', 'Overweight']]

for bmi_column in bmi_columns:
        corr = df[bmi_column].corr(df['Quality of Sleep'])
        print(f'Correlation between {bmi_column} and Quality of Sleep: {corr:.2f}')
        
plt.figure()
sns.barplot(x='BMI Category', y='Quality of Sleep', hue='Gender', data=df, palette='viridis')
plt.title('Quality of Sleep by BMI category by gender')
plt.xlabel('BMI Category')
plt.ylabel('Quality of Sleep')
plt.legend(title='Gender')

#BLOOD PRESSURE
df[['Systolic', 'Diastolic']] = df['Blood Pressure'].str.split('/', expand=True)

df['Systolic'] = pd.to_numeric(df['Systolic'])
df['Diastolic'] = pd.to_numeric(df['Diastolic'])

bp_index = df.columns.get_loc('Blood Pressure')

new_list = (
    df.columns[:bp_index+1].tolist() +
    ['Systolic', 'Diastolic'] +
    df.columns[bp_index+1:].tolist()    
    )

df = df[new_list]

df = df.loc[:, ~df.columns.duplicated()]

bp_columns = [col for col in df.columns if col in ['Systolic', 'Diastolic']]

for bp_col in bp_columns:
    corr = df[bp_col].corr(df['Quality of Sleep'])
    print(f'Correlation between {bp_col} and Quality of Sleep: {corr:.2f}')
    
plt.figure()
df_melted = df.melt(id_vars='Sleep Disorder', value_vars=['Systolic', 'Diastolic'], 
                     var_name='Pressure Type', value_name='Pressure')

plt.figure()
sns.boxplot(x='Sleep Disorder', y='Pressure', hue='Pressure Type', data=df_melted)
plt.title('Systolic and Diastolic Blood Prressure by Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Pressure')

plt.figure()
sns.barplot(x='Age Range', y='Systolic', hue='Gender', data=df, palette='plasma')
plt.title('Systolic blood pressure by age and gender')
plt.xlabel('Age Range')
plt.ylabel('Systolic Blood Pressure')

plt.figure()
sns.barplot(x='Age Range', y='Diastolic', hue='Gender', data=df, palette='plasma')
plt.title('Diastolic blood pressure by age and gender')
plt.xlabel('Age Range')
plt.ylabel('Diastolic Blood Pressure')

bp_category = [
    (df['Systolic']<120) & (df['Diastolic']<80),
    (df['Systolic'].between(120,129)) & (df['Diastolic']<=85),
    (df['Systolic'].between(130,139)) & (df['Diastolic']<=89),
    (df['Systolic']>=140) | (df['Diastolic']>=90 )
    ]

bp_labels = ['Optimal', 'Normal','High Normal','Hypertension']

df['Blood Pressure Category'] = np.select(bp_category, bp_labels, default='Undefined')

undef_sum = (df['Blood Pressure Category'] == 'Undefined').sum()
undef_row = df.loc[df['Blood Pressure Category'] == 'Undefined']


df_bp_by_occup = df.groupby(['Occupation Group', 'Blood Pressure Category']).size().unstack().apply(lambda x: x/x.sum(), axis=1)

df_bp_by_occup = df_bp_by_occup.reset_index()

df_bp_perc_melted = df_bp_by_occup.melt(id_vars='Occupation Group', var_name='Blood Pressure Category', value_name='Percentage')

bp_palette = {
    'Optimal':'#21bf17',
    'Normal': '#14afcd',
    'High Normal': '#e1c109',
    'Hypertension':'#d60e1a'
    }

plt.figure()
sns.barplot(data=df_bp_perc_melted, x='Occupation Group', y='Percentage', hue='Blood Pressure Category', palette=bp_palette)
plt.title('Percentage distribution of blood pressure in different occupation groups')
plt.xlabel('Occupation Group')
plt.ylabel('Percentage')
plt.legend(title='Blood Pressure Category')

#HEART RATE
df['Heart Rate'].hist(bins=30)

corr_hr_quality_sleep = df['Heart Rate'].corr(df['Quality of Sleep'])

plt.figure()
sns.regplot(data=df, x='Heart Rate', y='Quality of Sleep')
plt.title('Correlation between heart rate and quality of sleep')
plt.xlabel('Heart Rate')
plt.ylabel('Quality of Sleep')

plt.figure()
sns.barplot(data=df, x='Age Range', y='Heart Rate', hue='Gender', palette=['dodgerblue', 'orchid'])
plt.title('Heart rate by age and gender')
plt.xlabel('Age Range')
plt.ylabel('Heart Rate')
plt.legend(title='Gender')

plt.figure()
sns.violinplot(data=df, x='Sleep Disorder', y='Heart Rate')
plt.title('Sleep Disorder by heart rate')
plt.xlabel('Sleep Disorder')
plt.ylabel('Heart Rate')

sns.set(style='whitegrid')
plt.figure()
sns.scatterplot(x='Heart Rate', y='Quality of Sleep', hue='Occupation Group', style='Occupation Group', s=100, data=df)
plt.title('Quality of sleep by heart rate in different occupation groups')
plt.xlabel('Heart Rate')
plt.ylabel('Quality of Sleep')

sns.set(style='whitegrid')
plt.figure()
sns.lmplot(data=df, x='Heart Rate', y='Quality of Sleep', hue='Occupation Group', markers=["o", "s", "D", "+", "H"], palette='deep')
plt.title('Linear regression of sleep quality on resting heart rate in different occupation groups')
plt.xlabel('Heart Rate')
plt.ylabel('Quality of Sleep')

plt.figure()
sns.lineplot(data=df, x='Heart Rate', y='Sleep Duration', marker='o', linestyle='-')
plt.title('Sleep Duration by Heart Rate')
plt.xlabel('Heart Rate')
plt.ylabel('Sleep Duration')

#DAILY STEPS
df['Daily Steps'].hist(bins=30)
plt.title('Distribution of Daily Steps')
plt.xlabel('Daily Steps per day')
plt.ylabel('Sleep Duration')

corr_steps_quality_sleep = df['Daily Steps'].corr(df['Quality of Sleep'])

corr_steps_activity = df['Daily Steps'].corr(df['Physical Activity Level'])

plt.figure()
sns.scatterplot(data=df, x='Physical Activity Level', y='Daily Steps', hue='Gender', size='Heart Rate', sizes=(20,200))
plt.title('Daily steps by physical activity level by gender')
plt.xlabel('Physical Activity Level [minutes/day]')
plt.ylabel('Daily Steps per day')

plt.figure()
sns.violinplot(data=df, x='Sleep Disorder', y='Daily Steps')
plt.title('Daily steps by sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Daily Steps')


plt.figure(figsize=(14, 7))
sns.boxplot(x='Gender', y='Daily Steps', hue='BMI Category', data=df, palette='Set2')
plt.title('Daily Steps by Gender and Age Range')
plt.xlabel('Gender')
plt.ylabel('Daily Steps')


df_with_num_col = df.drop(columns=['Gender', 'Occupation', 'BMI Category',
                                'Blood Pressure', 'Sleep Disorder', 'Age Range',
                                'Occupation Group', 'Blood Pressure Category'])

corr_matrix = df_with_num_col.corr()

plt.figure()
sns.heatmap(corr_matrix, annot=True, square=True)
plt.title('Corr')

