import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# 1. LOAD DATA
# =========================================================

activity = pd.read_csv("mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")
sleep = pd.read_csv("mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")


# =========================================================
# 2. BASIC DATA CHECK
# =========================================================

print("Activity shape:", activity.shape)
print("Sleep shape:", sleep.shape)

print("\nActivity missing values:")
print(activity.isnull().sum())

print("\nSleep missing values:")
print(sleep.isnull().sum())


# =========================================================
# 3. DUPLICATE CHECK & CLEANING
# =========================================================

print("\nActivity duplicates:", activity.duplicated().sum())
print("Sleep duplicates:", sleep.duplicated().sum())

activity = activity.drop_duplicates()
sleep = sleep.drop_duplicates()

print("\nSleep duplicates after cleaning:", sleep.duplicated().sum())


# =========================================================
# 4. UNIQUE USERS
# =========================================================

print("\nUnique activity users:", activity["Id"].nunique())
print("Unique sleep users:", sleep["Id"].nunique())

common_users = set(activity["Id"]) & set(sleep["Id"])

print("Common users:", len(common_users))


# =========================================================
# 5. DATE CONVERSION
# =========================================================

print("\nBefore conversion:")
print(activity["ActivityDate"].dtype)
print(sleep["SleepDay"].dtype)

activity["ActivityDate"] = pd.to_datetime(
    activity["ActivityDate"],
    format="%m/%d/%Y"
)

sleep["SleepDay"] = pd.to_datetime(
    sleep["SleepDay"],
    format="%m/%d/%Y %I:%M:%S %p"
)

print("\nAfter conversion:")
print(activity["ActivityDate"].dtype)
print(sleep["SleepDay"].dtype)


# =========================================================
# 6. DATE RANGE
# =========================================================

print("\nActivity date range:")
print(
    activity["ActivityDate"].min(),
    "to",
    activity["ActivityDate"].max()
)

print("\nSleep date range:")
print(
    sleep["SleepDay"].min(),
    "to",
    sleep["SleepDay"].max()
)


# =========================================================
# 7. MISSING VALUES AFTER CLEANING
# =========================================================

print("\nActivity missing values:")
print(activity.isnull().sum())

print("\nSleep missing values:")
print(sleep.isnull().sum())


# =========================================================
# 8. BASIC ACTIVITY ANALYSIS
# =========================================================

print("\nAverage steps:",
      activity["TotalSteps"].mean())

print("Average calories:",
      activity["Calories"].mean())

print("Average very active minutes:",
      activity["VeryActiveMinutes"].mean())

print("Average fairly active minutes:",
      activity["FairlyActiveMinutes"].mean())

print("Average lightly active minutes:",
      activity["LightlyActiveMinutes"].mean())

print("Average sedentary minutes:",
      activity["SedentaryMinutes"].mean())


# =========================================================
# 9. BASIC SLEEP ANALYSIS
# =========================================================

print("\nAverage sleep minutes:",
      sleep["TotalMinutesAsleep"].mean())

print("Average time in bed:",
      sleep["TotalTimeInBed"].mean())


# =========================================================
# 10. ACTIVITY DAYS PER USER
# =========================================================

print("\nActivity days per user:")
print(
    activity.groupby("Id")["ActivityDate"]
    .count()
    .describe()
)


# =========================================================
# 11. SLEEP DAYS PER USER
# =========================================================

print("\nSleep days per user:")
print(
    sleep.groupby("Id")["SleepDay"]
    .count()
    .describe()
)


# =========================================================
# 12. CHECK ID + DATE
# =========================================================

print("\nActivity sample:")
print(activity[["Id", "ActivityDate"]].head())

print("\nSleep sample:")
print(sleep[["Id", "SleepDay"]].head())


# =========================================================
# 13. MERGE ACTIVITY + SLEEP
# =========================================================

merged = pd.merge(
    activity,
    sleep,
    left_on=["Id", "ActivityDate"],
    right_on=["Id", "SleepDay"],
    how="inner"
)

print("\nMerged shape:")
print(merged.shape)

print("\nMerged data:")
print(merged.head())


# =========================================================
# 14. REMOVE DUPLICATE DATE COLUMN
# =========================================================

merged = merged.drop(columns=["SleepDay"])

print("\nFinal merged shape:")
print(merged.shape)

print(merged.head())


# =========================================================
# 15. STEPS VS SLEEP CORRELATION
# =========================================================

print("\nSteps vs Sleep correlation:")

print(
    merged[
        ["TotalSteps", "TotalMinutesAsleep"]
    ].corr()
)


# =========================================================
# 16. ACTIVITY LEVEL
# =========================================================

median_steps = merged["TotalSteps"].median()

merged["ActivityLevel"] = merged["TotalSteps"].apply(
    lambda x: "Active"
    if x >= median_steps
    else "Less Active"
)

print("\nAverage sleep by activity level:")

print(
    merged.groupby("ActivityLevel")["TotalMinutesAsleep"]
    .mean()
)


# =========================================================
# 17. DAY OF WEEK ANALYSIS
# =========================================================

merged["DayOfWeek"] = (
    merged["ActivityDate"]
    .dt.day_name()
)

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

print("\nAverage steps by day of week:")

print(
    merged.groupby("DayOfWeek")["TotalSteps"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage sleep by day of week:")

print(
    merged.groupby("DayOfWeek")["TotalMinutesAsleep"]
    .mean()
    .sort_values(ascending=False)
)


# =========================================================
# 18. SLEEP LEVEL
# =========================================================

sleep_by_user = (
    sleep.groupby("Id")["TotalMinutesAsleep"]
    .mean()
)

print("\nSleep statistics by user:")
print(sleep_by_user.describe())

sleep_level = sleep_by_user.apply(
    lambda x: "7+ hours"
    if x >= 420
    else "Below 7 hours"
)

print("\nSleep level:")
print(sleep_level.value_counts())


# =========================================================
# 19. SLEEP EFFICIENCY
# =========================================================

merged["SleepEfficiency"] = (
    merged["TotalMinutesAsleep"]
    / merged["TotalTimeInBed"]
) * 100

print(
    "\nAverage sleep efficiency:",
    merged["SleepEfficiency"].mean()
)


# =========================================================
# 20. CORRELATIONS
# =========================================================

print("\nSteps vs Calories correlation:")

print(
    merged["TotalSteps"]
    .corr(merged["Calories"])
)


print("\nSteps vs Sedentary Minutes correlation:")

print(
    merged["TotalSteps"]
    .corr(merged["SedentaryMinutes"])
)


# =========================================================
# 21. STEP STATISTICS
# =========================================================

step_stats = merged["TotalSteps"].describe()

print("\nStep statistics:")
print(step_stats)


# =========================================================
# 22. VISUALIZATION
# =========================================================

# ---- 1. Distribution of Daily Steps ----

plt.figure(figsize=(8, 5))

sns.histplot(
    merged["TotalSteps"],
    bins=20,
    kde=True
)

plt.title("Distribution of Daily Steps")
plt.xlabel("Total Steps")
plt.ylabel("Number of Days")

plt.tight_layout()
plt.show()


# ---- 2. Steps vs Calories ----

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=merged,
    x="TotalSteps",
    y="Calories"
)

plt.title("Daily Steps vs Calories Burned")
plt.xlabel("Total Steps")
plt.ylabel("Calories")

plt.tight_layout()
plt.show()


# ---- 3. Steps vs Sedentary Minutes ----

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=merged,
    x="TotalSteps",
    y="SedentaryMinutes"
)

plt.title("Daily Steps vs Sedentary Minutes")
plt.xlabel("Total Steps")
plt.ylabel("Sedentary Minutes")

plt.tight_layout()
plt.show()


# ---- 4. Steps vs Sleep ----

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=merged,
    x="TotalSteps",
    y="TotalMinutesAsleep"
)

plt.title("Daily Steps vs Sleep Duration")
plt.xlabel("Total Steps")
plt.ylabel("Minutes Asleep")

plt.tight_layout()
plt.show()


# ---- 5. Average Steps by Day ----

daily_steps = (
    merged.groupby("DayOfWeek")["TotalSteps"]
    .mean()
    .reindex(day_order)
)

plt.figure(figsize=(9, 5))

daily_steps.plot(kind="bar")

plt.title("Average Daily Steps by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Steps")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ---- 6. Average Sleep by Day ----

daily_sleep = (
    merged.groupby("DayOfWeek")["TotalMinutesAsleep"]
    .mean()
    .reindex(day_order)
)

plt.figure(figsize=(9, 5))

daily_sleep.plot(kind="bar")

plt.title("Average Sleep Duration by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Minutes Asleep")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# =========================================================
# 23. EXPORT FINAL DATASET
# =========================================================

merged.to_csv(
    "bellabeat_final_analysis.csv",
    index=False
)

print("\nFinal dataset exported successfully!")
print("Final shape:", merged.shape)