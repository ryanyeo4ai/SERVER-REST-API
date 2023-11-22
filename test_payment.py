import pandas as pd
from db_connect import *


def extract_transaction_from_email(email):
    full_pay_df = pd.read_csv('test_balance.CSV')
    print(full_pay_df)

    # mass_pay_df = full_pay_df[full_pay_df['Type'] == 'Mass Pay Payment']
    # print(mass_pay_df)

    # my_transaction_df = mass_pay_df[['Date', 'To Email Address', 'Net']]
    # print(my_transaction_df)

    # print()
    user_transaction_df = full_pay_df[full_pay_df['To Email Address'] == email]
    # print(user_transaction_df)

    return user_transaction_df


if __name__ == "__main__":
    email = 'lossefanya+test2@gmail.com'
    df = extract_transaction_from_email(email)
    print(df)
    transaction_reward = float(df['Net'])
    completed_reward = (-1.0) * transaction_reward
    str_completed_reward = str(completed_reward)

    print(
        f"type, completed_reward : {type(completed_reward)}, {completed_reward}")
    print(
        f"type, str_completed_reward : {type(str_completed_reward)}, {str_completed_reward}")

    update_reward_to_DB(email, completed_reward)
