import calendar
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def return_cmap(data):
    # Function to create a colormap
    v = data["Count"].values
    colors = plt.cm.RdBu_r((v - v.min()) / (v.max() - v.min()))
    return colors


if __name__=="__main__":
    weekdays = [calendar.day_name[i] for i in range(7)]

    mail_df = pd.read_csv("myEmails.csv")
    mail_df["Date"] = pd.to_datetime(mail_df["Date"])
    mail_df = mail_df.set_index("Date")

    # E-Mails per Hour
    per_hour = pd.DataFrame(mail_df["Subject"].resample("h").count())
    per_hour_day = (
        per_hour.groupby([per_hour.index.hour]).sum()
        / per_hour.groupby([per_hour.index.hour]).count()
    )
    per_hour_day.reset_index(inplace=True)
    per_hour_day.columns = ["Hour", "Count"]

    # E-Mails per day
    per_day = pd.DataFrame(mail_df["Subject"].resample("d").count())
    per_day_week = (
        per_day.groupby([per_day.index.weekday]).sum()
        / per_day.groupby([per_day.index.weekday]).count()
    )
    per_day_week.reset_index(inplace=True)
    per_day_week.columns = ["Weekday", "Count"]
    per_day_week["Weekday"] = weekdays

    plt.figure(figsize=(14, 12))
    plt.subplot(2, 1, 1)
    cmap = return_cmap(per_hour_day)
    sns.barplot(x="Hour", y="Count", data=per_hour_day)
    plt.title("Emails per hour")

    plt.subplot(2, 1, 2)
    cmap = return_cmap(per_day_week)
    sns.barplot(x="Weekday", y="Count", data=per_day_week)
    plt.title("Emails per weekday")

    plt.show()

    print(
        "Average number of emails per day: {:.2f}".format(
            per_hour_day.sum()["Count"]
        )
    )
