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

age_sleep_disorder_perc = age_sleep_disorder.div(age_sleep_disorder.sum(axis=1), axis=0) * 100


plt.figure()
age_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Distribution of sleep disorders by age ranges')
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

#occupation percentage
occupation_sleep_disorder_perc = occupation_sleep_disorder.div(occupation_sleep_disorder.sum(axis=1), axis=0) * 100

plt.figure()
occupation_sleep_disorder_perc.plot(kind='bar', stacked=True, color=colors)
plt.title('Percentage distribution of Sleep Disorders by Occupation Group')
plt.xlabel('Occupation Group')
plt.ylabel('Count')
plt.legend(title='Sleep Disorder')

df_encoded = pd.get_dummies(df, columns=['Sleep Disorder'], drop_first=False)
df_encoded['Sleep Disorder'] = df['Sleep Disorder']

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

#QUALITY OF SLEEP
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

plt.figure(figsize=(10, 6))
quality_of_sleep_age.plot(kind='line', marker='o', color='blue')
plt.title('Average quality of sleep by age')
plt.xlabel('Age Range')
plt.ylabel('Average Quality of Sleep')



#one hot encoding
#df_encoded = pd.get_dummies(df, columns=['Sleep Disorder'], drop_first=False)
#df_encoded['Sleep Disorder'] = df['Sleep Disorder']


#PHYSICAL ACTIVITY LEVEL
#STRESS LEVEL
#BMI CATEGORY