import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import pickle 

# Load the trained model
load_model = pickle.load(open('RFmodel.sav', 'rb'))

# Function for fraud detection
def fraud_detection(input_data):
    try:
        # Convert input data to float
        input_data = [float(value) for value in input_data]

        input_data_as_numpy_array = np.asarray(input_data)
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        prediction = load_model.predict(input_data_reshaped)

        if prediction[0] == 0:
            return "The transaction is not fraudulent"
        else:
            return "The transaction is fraudulent"
    except ValueError:
        return "Invalid input. Please provide information"
# Function to save transaction details to SQLite database
def save_to_database(data):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (TransactionAmount REAL, NewBalance REAL, PaymentCurrency TEXT, ReceivedCurrency TEXT,
                 SenderBankLocation TEXT, ReceiverBankLocation TEXT, PaymentType TEXT, LaunderingType TEXT, OldBalance REAL)''')
    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def main():
    st.title("Detecting Fraudulent Transactions")

    # Input form for user
    st.sidebar.header("Enter Transaction Details")
    Transaction_amount = st.sidebar.text_input("Transaction Amount")
    NewBalance = st.sidebar.text_input("New Balance")
    Payment_currency = st.sidebar.text_input("Payment Currency")
    Received_currency = st.sidebar.text_input("Received Currency")
    Sender_bank_location = st.sidebar.text_input("Sender Bank Location")
    Receiver_bank_location = st.sidebar.text_input("Receiver Bank Location")
    Payment_type = st.sidebar.text_input("Payment Type")
    Laundering_type = st.sidebar.text_input("Laundering Type")
    Old_Balance = st.sidebar.text_input("Old Balance")

    # Button to detect fraud
    if st.sidebar.button('Detect Fraud'):
        detection = fraud_detection([Transaction_amount, NewBalance, Payment_currency, Received_currency, Sender_bank_location, Receiver_bank_location,
                                     Payment_type, Laundering_type, Old_Balance])
        st.sidebar.success(detection)

        # Save transaction details to database
        data = (Transaction_amount, NewBalance, Payment_currency, Received_currency, Sender_bank_location, Receiver_bank_location,
                Payment_type, Laundering_type, Old_Balance)
        save_to_database(data)

    # Display header for app
    st.header("Welcome to Fraud Detection App")

    # Display some information about the app
    st.markdown("This app detects fraudulent transactions based on user input. Fill in the transaction details on the left sidebar and click 'Detect Fraud' to see the result.")

    # Add an image to make the app more visually appealing
    st.image("cbz.png", use_column_width=True)

    # Add some additional information or instructions
    st.write("Please provide the necessary transaction details to detect fraud. Ensure all fields are filled correctly and with numeric values.")

if __name__ == '__main__':
    main()
