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
df.isnull().any()
df.isna()

df = df.drop(columns='Person ID')


#TARGET
disorder_count=df['Sleep Disorder'].value_counts()

plt.figure()
plt.pie(disorder_count, labels=disorder_count.index, colors = ['yellowgreen', 'darkred', 'skyblue'],
        autopct='%1.1f%%', shadow=False, startangle=70)
plt.title('Distribution of Sleep Disorder', fontsize=14, fontweight='bold')

'''
plt.figure()
df['Sleep Disorder'].hist(bins=10)
plt.title('Distribution of Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Count')
'''

custom_palette = ['#8ee553', '#e21916', '#4fd1de']

plt.figure()
sns.countplot(x='Sleep Disorder', data=df, palette=custom_palette)
plt.title('Distribution of Sleep Disorders')
plt.xlabel('Sleep Disorder')
plt.ylabel('Count')
plt.show()

df_encoded = pd.get_dummies(df, columns=['Sleep Disorder'], drop_first=False)
df_encoded['Sleep Disorder'] = df['Sleep Disorder']

#GENDER
gender_count=df_encoded['Gender'].value_counts()

plt.figure()
plt.pie(gender_count, labels=gender_count.index, colors = ['dodgerblue', 'orchid'],
        autopct='%1.1f%%', shadow=False, startangle=90)
plt.title('Gender Distribution', fontsize=14, fontweight='bold')


gender_sleep_disorder = df_encoded.groupby(['Gender', 'Sleep Disorder']).size().unstack(fill_value=0)

colors = ['#4fd1de', '#8ee553', '#e21916']

plt.figure()
gender_sleep_disorder.plot(kind='bar', stacked=True, color=colors)
plt.title('Distribution of sleep disorders by gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')


#AGE
plt.figure()
df_encoded['Age'].hist(bins=50)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Count')

plt.figure()
sns.boxplot(x='Sleep Disorder', y='Age', data=df_encoded, palette=custom_palette)
plt.title('Boxplot')
plt.xlabel('Sleep Disorder')
plt.ylabel('Age')

bins = [25, 30, 35, 40, 45, 50, 55, 60]
labels = ['25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60']

df_encoded['Age Range'] = pd.cut(df_encoded['Age'], bins=bins, labels=labels, right=False)

age_sleep_disorder = df_encoded.groupby(['Age Range', 'Sleep Disorder']).size().unstack(fill_value=0)

age_sleep_disorder_perc = age_sleep_disorder.div(age_sleep_disorder.sum(axis=1), axis=0) * 100


plt.figure()
age_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Distribution of sleep disorders by age ranges')
plt.xlabel('Age Range')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')


#OCCUPATION
occupation_count = df_encoded['Occupation'].value_counts()

plt.figure()
sns.countplot(x='Occupation', data=df_encoded, palette='viridis')
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
    

df_encoded['Occupation Group'] = df_encoded['Occupation'].apply(categorize_occupation)

occupation_sleep_disorder = df_encoded.groupby(['Occupation Group', 'Sleep Disorder']).size().unstack(fill_value=0)

#occupation percentage
occupation_sleep_disorder_perc = occupation_sleep_disorder.div(occupation_sleep_disorder.sum(axis=1), axis=0) * 100

plt.figure()
occupation_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Percentage distribution of Sleep Disorders by Occupation Group')
plt.xlabel('Occupation Group')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')



#SLEEP DURATION
plt.figure()
df_encoded['Sleep Duration'].hist(bins=20)
plt.title('Distribution of sleep duration')
plt.xlabel('Sleep Duration [hours]')
plt.ylabel('Count')


mean_sleep_duration = df_encoded.groupby('Sleep Disorder')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration.plot(kind='bar', color=colors)
plt.title('Average sleep duration for each sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Average sleep duration [hours]')

plt.figure()
sns.violinplot(x='Sleep Disorder', y='Sleep Duration', data=df_encoded, palette=custom_palette)
plt.title('Sleep duration for each sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Sleep Duration')

#SLEEP DURATION IN GENDER
mean_sleep_duration_by_gender = df_encoded.groupby('Gender')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration_by_gender.plot(kind='bar', color=['dodgerblue', 'orchid'])
plt.title('Average Sleep Duration by Gender')
plt.xlabel('Gender')
plt.ylabel('Average sleep duration [hours]')

mean_sleep_duration_by_occup = df_encoded.groupby('Occupation Group')['Sleep Duration'].mean()

plt.figure()
mean_sleep_duration_by_occup.plot(kind='bar', color=['#357dbd', '#15a28f', '#1c9a50', '#e9c825', '#a21a0e'])
plt.title('Sleep duration by occupation')
plt.xlabel('Occupation Group')
plt.ylabel('Average sleep duration [hours]')

#QUALITY OF SLEEP
plt.figure()
df_encoded['Quality of Sleep'].hist(bins=20)
plt.title('Distribution of Quality of Sleep')
plt.xlabel('Quality of Sleep')
plt.ylabel('Count')

quality_of_sleep = df_encoded.groupby('Sleep Disorder')['Quality of Sleep'].mean()

plt.figure()
sns.barplot(x='Sleep Disorder', y='Quality of Sleep', data=df_encoded, palette=custom_palette)
plt.title('Average Quality of Sleep by Sleep Disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Average Quality of Sleep')

quality_of_sleep_age = df_encoded.groupby('Age Range')['Quality of Sleep'].mean()

plt.figure(figsize=(10, 6))
quality_of_sleep_age.plot(kind='line', marker='o', color='blue')
plt.title('Average quality of sleep by age')
plt.xlabel('Age Range')
plt.ylabel('Average Quality of Sleep')

#PHYSICAL ACTIVITY LEVEL
plt.figure()
df_encoded['Physical Activity Level'].hist(bins=30)
plt.title('Distribution of physical acitivity')
plt.xlabel('Physical Activity Level [minutes/day]')
plt.ylabel('Count')

activity_gender_age = df_encoded.groupby(['Age Range', 'Gender'])['Physical Activity Level'].mean().reset_index()

plt.figure()
sns.barplot(x='Age Range', y='Physical Activity Level', hue='Gender',
            data=activity_gender_age, palette='viridis')
plt.title('Average daily physical activity by age range and gender')
plt.xlabel('Age Range')
plt.ylabel('Physical Activity Level [minutes/day]')
plt.legend(title='Gender')

activity_by_occup = df_encoded.groupby('Occupation Group')['Physical Activity Level'].mean().reset_index()

plt.figure()
sns.barplot(x='Occupation Group', y='Physical Activity Level', data=activity_by_occup, palette='pastel')
plt.title('Average daily physical activity by occupation')
plt.xlabel('Occupation Group')
plt.ylabel('Physical Activity Level [minutes/day]')

df_encoded['Sleep Disorder_Insomnia'] = df_encoded['Sleep Disorder_Insomnia'].astype(int)
df_encoded['Sleep Disorder_None'] = df_encoded['Sleep Disorder_None'].astype(int)
df_encoded['Sleep Disorder_Sleep Apnea'] = df_encoded['Sleep Disorder_Sleep Apnea'].astype(int)

corr_activity_ins = df_encoded[['Physical Activity Level', 'Sleep Disorder_Insomnia']].corr().loc['Physical Activity Level', 'Sleep Disorder_Insomnia']
corr_activity_none = df_encoded[['Physical Activity Level', 'Sleep Disorder_None']].corr().loc['Physical Activity Level', 'Sleep Disorder_None']
corr_activity_sa = df_encoded[['Physical Activity Level', 'Sleep Disorder_Sleep Apnea']].corr().loc['Physical Activity Level', 'Sleep Disorder_Sleep Apnea']

plt.figure(figsize=(10, 6))
sns.regplot(x='Physical Activity Level', y='Sleep Disorder_Insomnia', data=df_encoded, logistic=True, scatter_kws={'s':10}, line_kws={'color':'red'})
plt.title('Correlation between Physical Activity Level and Insomnia')
plt.xlabel('Physical Activity Level (minutes/day)')
plt.ylabel('Insomnia (0/1)')
plt.grid(True)

insomnia_data = df_encoded.groupby('Sleep Disorder')['Physical Activity Level'].mean().reset_index()

palette = ['#4fd1de', '#8ee553', '#e21916']

plt.figure()
sns.barplot(x='Sleep Disorder', y='Physical Activity Level', data=insomnia_data, palette=palette)
plt.title('Average daily physical activity by sleep disorder')
plt.xlabel('Sleep Disorder')
plt.ylabel('Physical Activity Level [minutes/day]')

#STRESS LEVEL
plt.figure()
df_encoded['Stress Level'].hist(bins=50)
plt.title('Distribution of stress level')
plt.xlabel('Stress Level')
plt.ylabel('Count')


plt.figure()
sns.barplot(x='Sleep Disorder', y='Stress Level', hue='Gender', data=df_encoded, palette='viridis')
plt.title('Stress Level by Sleep Disorder and Gender')
plt.xlabel('Sleep Disorder')
plt.ylabel('Stress Level')
plt.legend(title='Gender')

mean_stress_by_age_occup = df_encoded.groupby(['Age Range', 'Occupation Group'])['Stress Level'].mean().reset_index()


plt.figure()
sns.lineplot(x='Age Range', y='Stress Level', hue='Occupation Group', data=mean_stress_by_age_occup, marker='o', palette='viridis', linewidth=2.5)
plt.title('Average stress level by Age Range')
plt.xlabel('Age Range')
plt.ylabel('Average stress level')
plt.legend(title='Occupation Group')

#BMI CATEGORY

df_encoded['BMI Category'].value_counts()

df_encoded['BMI Category'] = df['BMI Category'].replace({
    'Normal Weight': 'Normal'
    })

df_encoded['BMI Category'].value_counts()

plt.figure()
df_encoded['BMI Category'].hist(bins=50)

plt.figure()
sns.barplot(x='Sleep Disorder', y='Age', hue='BMI Category', data=df_encoded, palette='plasma')
plt.title('BMI by sleep disorder and age')
plt.xlabel('Sleep Disorder')
plt.ylabel('Age')
plt.legend(title='BMI Category')

df_bmi_encoded = pd.get_dummies(df_encoded['BMI Category'])

df_encoded = pd.concat([df_encoded, df_bmi_encoded], axis=1)

df_encoded['Normal'] = df_encoded['Normal'].astype(int)
df_encoded['Obese'] = df_encoded['Obese'].astype(int)
df_encoded['Overweight'] = df_encoded['Overweight'].astype(int)


bmi_columns = [col for col in df_encoded.columns if col in ['Normal', 'Obese', 'Overweight']]
sleep_disorder_columns = [col for col in df_encoded.columns if 'Sleep Disorder_' in col]

for bmi_column in bmi_columns:
    for sleep_disorder_column in sleep_disorder_columns:
        corr = df_encoded[bmi_column].corr(df_encoded[sleep_disorder_column])
        print(f'Correlation between {bmi_column} and {sleep_disorder_column}: {corr:.2f}')
        
plt.figure()
sns.regplot(x='Normal', y='Sleep Disorder_None', data=df_encoded, logistic=True, scatter_kws={'s': 40}, line_kws={'color': 'red'}, ci=None)
plt.title('Correlation between BMI Category - Normal and None Disorder')
plt.xlabel('Presence of BMI Normal (0/1)')
plt.ylabel('Presence of None (0/1)')
plt.grid(True)

plt.figure()
sns.regplot(x='Overweight', y='Sleep Disorder_Insomnia', data=df_encoded, logistic=True, scatter_kws={'s': 40}, line_kws={'color': 'red'}, ci=None)
plt.title('Correlation between BMI Category - Overweight and Insomnia Disorder')
plt.xlabel('Presence of BMI Overweight (0/1)')
plt.ylabel('Presence of Insomnia (0/1)')
plt.grid(True)

plt.figure()
sns.regplot(x='Overweight', y='Sleep Disorder_Sleep Apnea', data=df_encoded, logistic=True, scatter_kws={'s': 40}, line_kws={'color': 'red'}, ci=None)
plt.title('Correlation between BMI Category - Overweight and Insomnia Disorder')
plt.xlabel('Presence of BMI Overweight (0/1)')
plt.ylabel('Presence of Insomnia (0/1)')
plt.grid(True)

#BLOOD PRESSURE
df_encoded[['systolic', 'diastolic']] = df_encoded['Blood Pressure'].str.split('/', expand=True)

df_encoded['systolic'] = pd.to_numeric(df_encoded['systolic'])
df_encoded['diastolic'] = pd.to_numeric(df_encoded['diastolic'])


bp_index = df_encoded.columns.get_loc('Blood Pressure')

new_list = (
    df_encoded.columns[:bp_index+1].tolist() +
    ['systolic', 'diastolic'] +
    df_encoded.columns[bp_index+1:].tolist()    
    )

df_encoded = df_encoded[new_list]


df_encoded.info()
print(df_encoded.dtypes)